#!/usr/bin/env python3
"""
Assemble authoring output from all source files into a single
authoring_output.json covering all 85 spreads (001-085).

Spreads 001-005 get placeholder entries (front matter).
Spreads 006-085 are loaded from individual batch files.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "output"

# All batch files in order
BATCH_FILES = [
    ("spreads_006_010_text_options.json", 6, 10),
    ("spreads_011_017_text_options.json", 11, 17),
    ("spreads_018_025_text_options.json", 18, 25),
    ("spreads_026_033_text_options.json", 26, 33),
    ("spreads_034_041_text_options.json", 34, 41),
    ("spreads_042_049_text_options.json", 42, 49),
    ("spreads_050_057_text_options.json", 50, 57),
    ("spreads_058_065_text_options.json", 58, 65),
    ("spreads_066_073_text_options.json", 66, 73),
    ("spreads_074_081_text_options.json", 74, 81),
    ("spreads_082_085_text_options.json", 82, 85),
]

FRONT_MATTER_THEMES = {
    1: "Cover — The Model is the Massage",
    2: "Inside front cover / half-title",
    3: "Credits and colophon",
    4: "Inventory of effects — opening litany",
    5: "Inventory of effects — continuation",
}


def load_batch(filename):
    """Load spreads from a batch file (handles both wrapper and bare array formats)."""
    path = BASE / filename
    if not path.exists():
        print(f"  WARNING: {filename} not found, skipping")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Handle wrapper format (has "spreads" key)
    if isinstance(data, dict) and "spreads" in data:
        return data["spreads"]
    # Bare array
    if isinstance(data, list):
        return data
    print(f"  WARNING: Unexpected format in {filename}")
    return []


def create_placeholder(num):
    """Create a placeholder entry for front-matter spreads."""
    return {
        "spread_id": f"spread_{num:03d}",
        "movement": "prologue",
        "theme": FRONT_MATTER_THEMES.get(num, f"Front matter {num}"),
        "text_options": [
            {
                "option_id": "a",
                "label": "Placeholder — front matter",
                "display_text": FRONT_MATTER_THEMES.get(num, ""),
                "body_text": None,
                "caption_text": None,
                "quotations_used": [],
                "voice_register": "declarative",
                "rhetorical_strategy": "assertion",
                "rationale": "Placeholder for front matter. To be designed separately.",
                "word_count": len(FRONT_MATTER_THEMES.get(num, "").split()),
            }
        ],
        "design_specs": [],
        "selected_text": None,
        "selected_design": None,
        "reviewer_notes": None,
        "dependency_flags": [],
    }


def get_movement(sid_num):
    """Determine movement from spread number."""
    if sid_num <= 10:
        return "prologue"
    if sid_num <= 35:
        return "movement_1_environment"
    if sid_num <= 60:
        return "movement_2_acceleration"
    if sid_num <= 65:
        return "hinge"
    return "movement_3_dreamscape"


def normalize_spread(s):
    """Ensure each spread has all required fields with defaults."""
    assert "spread_id" in s, "Missing spread_id"
    assert "text_options" in s, f"Missing text_options in {s['spread_id']}"

    # Ensure movement is set
    if "movement" not in s:
        sid_num = int(s["spread_id"].split("_")[1])
        s["movement"] = get_movement(sid_num)

    # Ensure design_specs exists
    if "design_specs" not in s:
        s["design_specs"] = []

    # Default nullable fields
    s.setdefault("theme", "")
    s.setdefault("selected_text", None)
    s.setdefault("selected_design", None)
    s.setdefault("reviewer_notes", None)
    s.setdefault("dependency_flags", [])

    # Normalize text options
    for opt in s["text_options"]:
        opt.setdefault("caption_text", None)
        opt.setdefault("quotations_used", [])
        opt.setdefault("voice_register", "declarative")
        opt.setdefault("rhetorical_strategy", "assertion")
        opt.setdefault("word_count", 0)
        # Calculate word_count if 0
        if opt["word_count"] == 0:
            words = 0
            for field in ["display_text", "body_text", "caption_text"]:
                if opt.get(field):
                    words += len(opt[field].split())
            opt["word_count"] = words

    # Normalize design specs
    for spec in s["design_specs"]:
        spec.setdefault("density", "moderate")
        spec.setdefault("tone", "balanced")
        spec.setdefault("svg_wireframe", "")

    return s


def main():
    all_spreads = []

    # Front matter placeholders (001-005)
    print("Creating front matter placeholders (001-005)...")
    for i in range(1, 6):
        all_spreads.append(create_placeholder(i))
    print(f"  Created {len(all_spreads)} placeholders")

    # Load all batch files
    for filename, start, end in BATCH_FILES:
        print(f"Loading {filename} (spreads {start:03d}-{end:03d})...")
        batch = load_batch(filename)
        if batch:
            print(f"  Got {len(batch)} spreads: {[s['spread_id'] for s in batch]}")
            all_spreads.extend(batch)
        else:
            print(f"  EMPTY — creating placeholders for {start:03d}-{end:03d}")
            for i in range(start, end + 1):
                all_spreads.append({
                    "spread_id": f"spread_{i:03d}",
                    "movement": get_movement(i),
                    "theme": f"(pending generation — spread {i:03d})",
                    "text_options": [{
                        "option_id": "a",
                        "label": "Pending generation",
                        "display_text": f"Spread {i:03d}",
                        "body_text": None,
                        "caption_text": None,
                        "quotations_used": [],
                        "voice_register": "declarative",
                        "rhetorical_strategy": "assertion",
                        "rationale": "Awaiting text generation.",
                        "word_count": 2,
                    }],
                    "design_specs": [],
                    "selected_text": None,
                    "selected_design": None,
                    "reviewer_notes": None,
                    "dependency_flags": [],
                })

    print(f"\nTotal raw spreads: {len(all_spreads)}")

    # Normalize all
    all_spreads = [normalize_spread(s) for s in all_spreads]

    # Deduplicate and sort by spread_id
    seen = {}
    for s in all_spreads:
        sid = s["spread_id"]
        if sid in seen:
            # Keep the one with more text options (i.e., the real one over placeholder)
            if len(s["text_options"]) > len(seen[sid]["text_options"]):
                seen[sid] = s
        else:
            seen[sid] = s
    all_spreads = sorted(seen.values(), key=lambda s: s["spread_id"])

    # Validate completeness
    expected = {f"spread_{i:03d}" for i in range(1, 86)}
    actual = {s["spread_id"] for s in all_spreads}
    missing = expected - actual
    extra = actual - expected
    if missing:
        print(f"WARNING: Missing spreads: {sorted(missing)}")
    if extra:
        print(f"WARNING: Extra spreads: {sorted(extra)}")

    # Count stats by movement
    movement_counts = {}
    for s in all_spreads:
        m = s["movement"]
        if m not in movement_counts:
            movement_counts[m] = 0
        movement_counts[m] += 1

    # Build output
    output = {
        "version": "2.0",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "claude-opus-4-6",
        "spread_range": "spread_001-spread_085",
        "spreads": all_spreads,
    }

    # Stats
    total_options = sum(len(s["text_options"]) for s in all_spreads)
    total_specs = sum(len(s["design_specs"]) for s in all_spreads)
    total_words = sum(
        opt["word_count"] for s in all_spreads for opt in s["text_options"]
    )

    print(f"\n{'='*40}")
    print(f"   ASSEMBLY STATS")
    print(f"{'='*40}")
    print(f"Spreads:        {len(all_spreads)}")
    print(f"Text options:   {total_options}")
    print(f"Design specs:   {total_specs}")
    print(f"Total words:    {total_words:,}")
    print(f"\nBy movement:")
    for m, c in sorted(movement_counts.items()):
        print(f"  {m}: {c} spreads")

    # Write main output
    outpath = BASE / "authoring_output.json"
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    size_kb = outpath.stat().st_size / 1024
    print(f"\nWritten to: {outpath}")
    print(f"File size: {size_kb:.1f} KB")

    # Also copy to docs/data/ for web serving
    docs_path = BASE.parent / "docs" / "data" / "authoring_output.json"
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    with open(docs_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Copied to: {docs_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
