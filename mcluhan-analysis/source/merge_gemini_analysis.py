"""
merge_gemini_analysis.py — Phase 4: Compare & Merge Gemini Analysis

Compares Gemini's independent analysis with existing Claude analysis and
produces a comparison report and/or merged database.

Modes:
  --report       Generate comparison report only
  --auto         Apply automatic merge rules (prefer Gemini for vision fields)
  --full         Apply ALL Gemini fields (completely replace existing)
  --images-only  Merge only images[] and design{} from visual descriptions

Usage:
  python source/merge_gemini_analysis.py --report
  python source/merge_gemini_analysis.py --auto
  python source/merge_gemini_analysis.py --images-only
  python source/merge_gemini_analysis.py --full
  python source/merge_gemini_analysis.py --spread 50 --auto
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gemini_tools import (
    get_cached_result,
    load_database,
    BASE_DIR,
    OUTPUT_DIR,
)


# ── Merge Rules ──

# Fields where Gemini (with vision) should be preferred
VISION_PREFER_FIELDS = {
    "images",           # Gemini can actually see the images
    "design",           # Layout, typography, color — vision-grounded
}

# Fields where comparison is needed (no automatic preference)
COMPARE_FIELDS = {
    "rhetoric",         # Both have valid approaches
    "themes",           # Framework-dependent
}

# Fields to always keep from existing (require full-book sequential context)
KEEP_EXISTING_FIELDS = {
    "text",             # Already corrected via OCR passes
    "quotations",       # Already corrected
    "progression",      # Requires full-book sequential context
    "id", "pdf_page", "book_pages", "section", "spread_type",
    "orientation", "analyst", "analysis_method", "notes",
}


def load_gemini_visual(spread_num: int) -> dict | None:
    """Load Gemini visual description for a spread."""
    return get_cached_result(spread_num, "visual")


def load_gemini_analysis(spread_num: int) -> dict | None:
    """Load Gemini independent analysis for a spread."""
    return get_cached_result(spread_num, "analysis")


def find_spread_in_db(db: dict, spread_num: int) -> dict | None:
    """Find a spread entry in the database."""
    sid = f"spread_{spread_num:03d}"
    for s in db["spreads"]:
        if s["id"] == sid:
            return s
    return None


def compare_images(existing_imgs: list, gemini_imgs: list) -> list:
    """Compare image entries between existing and Gemini analysis."""
    diffs = []

    # Compare count
    if len(existing_imgs) != len(gemini_imgs):
        diffs.append(f"Image count: existing={len(existing_imgs)}, gemini={len(gemini_imgs)}")

    # Compare subjects
    for i, (e, g) in enumerate(zip(existing_imgs, gemini_imgs)):
        e_subj = e.get("subject", "")
        g_subj = g.get("subject", "")
        if e_subj != g_subj:
            diffs.append(f"Image[{i}] subject differs:\n    EXISTING: {e_subj[:100]}\n    GEMINI:   {g_subj[:100]}")

    return diffs


def compare_design(existing_design: dict, gemini_design: dict) -> list:
    """Compare design entries."""
    diffs = []
    for key in ["layout_description", "white_space", "visual_density",
                 "left_right_relationship", "compositional_framing"]:
        e_val = existing_design.get(key, "")
        g_val = gemini_design.get(key, "")
        if str(e_val) != str(g_val):
            diffs.append(f"design.{key}:\n    EXISTING: {str(e_val)[:80]}\n    GEMINI:   {str(g_val)[:80]}")
    return diffs


def compare_rhetoric(existing_rhet: dict, gemini_rhet: dict) -> list:
    """Compare rhetoric entries."""
    diffs = []
    for key in ["argument", "rhetorical_strategy", "design_enacts_argument"]:
        e_val = existing_rhet.get(key, "")
        g_val = gemini_rhet.get(key, "")
        if str(e_val) != str(g_val):
            diffs.append(f"rhetoric.{key}:\n    EXISTING: {str(e_val)[:100]}\n    GEMINI:   {str(g_val)[:100]}")
    return diffs


def generate_report(db: dict, spread_nums: list) -> str:
    """Generate a comparison report between existing and Gemini analysis."""
    lines = [
        "# Gemini vs Existing Analysis Comparison Report",
        f"Generated: {datetime.now().isoformat()}",
        f"Spreads analyzed: {len(spread_nums)}",
        "",
        "---",
        "",
    ]

    total_image_diffs = 0
    total_design_diffs = 0
    total_rhetoric_diffs = 0
    spreads_with_gemini_visual = 0
    spreads_with_gemini_analysis = 0

    for num in spread_nums:
        existing = find_spread_in_db(db, num)
        g_visual = load_gemini_visual(num)
        g_analysis = load_gemini_analysis(num)

        if not existing:
            continue

        has_visual = g_visual is not None
        has_analysis = g_analysis is not None

        if has_visual:
            spreads_with_gemini_visual += 1
        if has_analysis:
            spreads_with_gemini_analysis += 1

        # Pick the best Gemini source for comparison
        gemini = g_analysis or g_visual
        if not gemini:
            continue

        spread_diffs = []

        # Compare images
        if "images" in gemini:
            img_diffs = compare_images(
                existing.get("images", []),
                gemini.get("images", [])
            )
            if img_diffs:
                spread_diffs.extend(img_diffs)
                total_image_diffs += len(img_diffs)

        # Compare design
        if "design" in gemini:
            des_diffs = compare_design(
                existing.get("design", {}),
                gemini.get("design", {})
            )
            if des_diffs:
                spread_diffs.extend(des_diffs)
                total_design_diffs += len(des_diffs)

        # Compare rhetoric (only if full analysis available)
        if has_analysis and "rhetoric" in gemini:
            rhet_diffs = compare_rhetoric(
                existing.get("rhetoric", {}),
                gemini.get("rhetoric", {})
            )
            if rhet_diffs:
                spread_diffs.extend(rhet_diffs)
                total_rhetoric_diffs += len(rhet_diffs)

        if spread_diffs:
            lines.append(f"## spread_{num:03d}")
            gemini_model = gemini.get("model", "unknown")
            lines.append(f"*Gemini model: {gemini_model}*")
            lines.append("")
            for diff in spread_diffs:
                lines.append(f"- {diff}")
            lines.append("")

    # Summary
    lines.insert(5, f"")
    lines.insert(6, f"## Summary")
    lines.insert(7, f"- Spreads with Gemini visual descriptions: {spreads_with_gemini_visual}")
    lines.insert(8, f"- Spreads with Gemini full analysis: {spreads_with_gemini_analysis}")
    lines.insert(9, f"- Total image differences: {total_image_diffs}")
    lines.insert(10, f"- Total design differences: {total_design_diffs}")
    lines.insert(11, f"- Total rhetoric differences: {total_rhetoric_diffs}")
    lines.insert(12, f"")

    return "\n".join(lines)


def merge_visual_only(existing: dict, g_visual: dict) -> dict:
    """Merge only images[] and design{} from Gemini visual description."""
    merged = dict(existing)  # shallow copy

    if "images" in g_visual:
        merged["images"] = g_visual["images"]

    if "design" in g_visual:
        merged["design"] = g_visual["design"]

    if "spread_description" in g_visual:
        # Add Gemini's spread description to notes
        existing_notes = merged.get("notes", "")
        gemini_desc = g_visual["spread_description"]
        merged["notes"] = (
            f"{existing_notes}\n\n[Gemini visual description] {gemini_desc}".strip()
        )

    # Track merge metadata
    merged["analysis_method"] = (
        f"{existing.get('analysis_method', 'claude_analysis')}"
        f" + gemini_visual({g_visual.get('model', 'unknown')})"
    )

    return merged


def merge_auto(existing: dict, g_visual: dict | None, g_analysis: dict | None) -> dict:
    """Auto-merge following the rules in the plan.

    Merge rules:
    - images[]: Prefer Gemini (has vision)
    - design{}: Prefer Gemini (vision-grounded)
    - rhetoric{}: Compare & pick best (prefer higher confidence)
    - themes{}: Compare (use framework)
    - progression{}: Keep existing (needs full-book context)
    - text{}/quotations: Keep existing (already corrected)
    """
    merged = dict(existing)  # shallow copy

    # Use analysis if available, fall back to visual
    gemini = g_analysis or g_visual

    if not gemini:
        return merged

    # VISION FIELDS: Always prefer Gemini
    if "images" in gemini:
        merged["images"] = gemini["images"]

    if "design" in gemini:
        merged["design"] = gemini["design"]

    # RHETORIC: Compare confidence, prefer higher
    if g_analysis and "rhetoric" in g_analysis:
        existing_conf = existing.get("rhetoric", {}).get("confidence", 0.5)
        gemini_conf = g_analysis.get("confidence", {}).get("rhetoric", 0.5)

        if gemini_conf >= existing_conf:
            # Prefer Gemini rhetoric
            merged["rhetoric"] = g_analysis["rhetoric"]
        # else keep existing

    # THEMES: Compare confidence, prefer higher
    if g_analysis and "themes" in g_analysis:
        existing_conf = existing.get("themes", {}).get("confidence", 0.5)
        gemini_conf = g_analysis.get("confidence", {}).get("themes", 0.5)

        if gemini_conf >= existing_conf:
            merged["themes"] = g_analysis["themes"]

    # PROGRESSION: Always keep existing
    # (requires full-book sequential context)

    # Add spread description if available
    desc = gemini.get("spread_description", "")
    if desc:
        existing_notes = merged.get("notes", "")
        merged["notes"] = f"{existing_notes}\n\n[Gemini] {desc}".strip()

    # Track merge metadata
    sources = []
    sources.append(existing.get("analysis_method", "claude_analysis"))
    if g_visual:
        sources.append(f"gemini_visual({g_visual.get('model', 'unknown')})")
    if g_analysis:
        sources.append(f"gemini_analysis({g_analysis.get('model', 'unknown')})")
    merged["analysis_method"] = " + ".join(sources)

    return merged


def merge_full(existing: dict, g_analysis: dict) -> dict:
    """Full merge — replace all mergeable fields with Gemini's version."""
    merged = dict(existing)

    for field in ["images", "design", "rhetoric", "themes"]:
        if field in g_analysis:
            merged[field] = g_analysis[field]

    if "progression" in g_analysis:
        # Even in full mode, we merge progression carefully
        merged["progression"] = g_analysis["progression"]

    desc = g_analysis.get("spread_description", "")
    if desc:
        existing_notes = merged.get("notes", "")
        merged["notes"] = f"{existing_notes}\n\n[Gemini full] {desc}".strip()

    merged["analysis_method"] = (
        f"{existing.get('analysis_method', 'claude_analysis')}"
        f" + gemini_full({g_analysis.get('model', 'unknown')})"
    )

    return merged


def main():
    parser = argparse.ArgumentParser(description="Compare and merge Gemini analysis")
    parser.add_argument("--report", action="store_true", help="Generate comparison report only")
    parser.add_argument("--auto", action="store_true", help="Auto-merge (prefer Gemini for vision)")
    parser.add_argument("--images-only", action="store_true", help="Merge only images+design from visual pass")
    parser.add_argument("--full", action="store_true", help="Full Gemini replacement")
    parser.add_argument("--spread", type=int, help="Process a single spread")
    parser.add_argument("--start", type=int, default=1, help="Start from spread N")
    parser.add_argument("--end", type=int, default=85, help="End at spread N")
    args = parser.parse_args()

    if not any([args.report, args.auto, args.images_only, args.full]):
        parser.error("Specify one of: --report, --auto, --images-only, --full")

    print("=" * 60)
    print("  Gemini Analysis — Compare & Merge")
    print("=" * 60)

    # Load database
    print("\nLoading analysis database...")
    db = load_database()
    print(f"  Spreads: {len(db.get('spreads', []))}")

    # Determine spread range
    if args.spread:
        spread_nums = [args.spread]
    else:
        spread_nums = list(range(args.start, args.end + 1))

    # Count available Gemini data
    visual_count = sum(1 for n in spread_nums if load_gemini_visual(n))
    analysis_count = sum(1 for n in spread_nums if load_gemini_analysis(n))
    print(f"  Gemini visual descriptions: {visual_count}")
    print(f"  Gemini full analyses: {analysis_count}")

    # ── Report Mode ──
    if args.report:
        print("\nGenerating comparison report...")
        report = generate_report(db, spread_nums)
        report_path = BASE_DIR / "output" / "gemini_comparison_report.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"  Report saved: {report_path}")
        print(f"  Report size: {len(report):,} chars")
        return

    # ── Merge Modes ──
    mode = "auto" if args.auto else ("images_only" if args.images_only else "full")
    print(f"\nMerge mode: {mode}")

    # Backup database
    backup_name = f"analysis_database_backup_merge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    backup_path = BASE_DIR / "output" / backup_name
    shutil.copy2(BASE_DIR / "output" / "analysis_database.json", backup_path)
    print(f"  Backup: {backup_path.name}")

    merged_count = 0
    skipped_count = 0

    for num in spread_nums:
        existing = find_spread_in_db(db, num)
        if not existing:
            skipped_count += 1
            continue

        g_visual = load_gemini_visual(num)
        g_analysis = load_gemini_analysis(num)

        if mode == "images_only":
            if g_visual:
                merged = merge_visual_only(existing, g_visual)
                # Update in-place
                idx = db["spreads"].index(existing)
                db["spreads"][idx] = merged
                merged_count += 1
                print(f"  [merged] spread_{num:03d} (images+design from visual)")
            else:
                skipped_count += 1

        elif mode == "auto":
            if g_visual or g_analysis:
                merged = merge_auto(existing, g_visual, g_analysis)
                idx = db["spreads"].index(existing)
                db["spreads"][idx] = merged
                merged_count += 1
                print(f"  [merged] spread_{num:03d} (auto)")
            else:
                skipped_count += 1

        elif mode == "full":
            if g_analysis:
                merged = merge_full(existing, g_analysis)
                idx = db["spreads"].index(existing)
                db["spreads"][idx] = merged
                merged_count += 1
                print(f"  [merged] spread_{num:03d} (full)")
            else:
                skipped_count += 1

    # Save merged database
    if merged_count > 0:
        db_path = BASE_DIR / "output" / "analysis_database.json"
        db_path.write_text(json.dumps(db, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n  Database saved: {db_path}")

    print("\n" + "=" * 60)
    print(f"  Complete: {merged_count} merged, {skipped_count} skipped")
    print(f"  Backup: {backup_name}")
    print("=" * 60)


if __name__ == "__main__":
    main()
