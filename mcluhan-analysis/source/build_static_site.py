"""
Build static site for GitHub Pages deployment.
Generates docs/ directory at repo root with all data, images, and static HTML.

Usage:
  python source/build_static_site.py              # Build everything
  python source/build_static_site.py --no-images  # Skip image compression (faster)
  python source/build_static_site.py --clean      # Remove docs/ first
"""

import json
import os
import sys
import shutil
import argparse
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DATA_DIR = os.path.join(DOCS_DIR, "data")
IMAGES_DIR = os.path.join(DOCS_DIR, "images")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
VLM_DIR = os.path.join(OUTPUT_DIR, "vlm_extractions")
RENDERED_DIR = os.path.join(BASE_DIR, "rendered")
DB_PATH = os.path.join(OUTPUT_DIR, "analysis_database.json")
PLAN_PATH = os.path.join(OUTPUT_DIR, "content_plan.json")

VIEWER_DIR = os.path.join(BASE_DIR, "viewer")
STATIC_HTML = os.path.join(VIEWER_DIR, "static_viewer.html")
STATIC_CSS = os.path.join(VIEWER_DIR, "static_style.css")

# Total pages in the PDF
TOTAL_PAGES = 85
JPEG_QUALITY = 85


def load_json(path):
    """Load a JSON file, return None if not found."""
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    """Save data as pretty-printed JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_index(db):
    """Build index.json with nav items and metadata."""
    entries = db.get("spreads", [])
    analyzed_ids = {e["id"] for e in entries}

    spreads = []
    for page_num in range(1, TOTAL_PAGES + 1):
        spread_id = f"spread_{page_num:03d}"
        entry = next((e for e in entries if e["id"] == spread_id), None)
        spreads.append({
            "id": spread_id,
            "pdf_page": page_num,
            "book_pages": entry.get("book_pages", []) if entry else [],
            "analyzed": spread_id in analyzed_ids,
        })

    metadata = db.get("metadata", {})
    return {
        "total_pages": TOTAL_PAGES,
        "total_analyzed": len(entries),
        "schema_version": metadata.get("schema_version", "1.1"),
        "spreads": spreads,
    }


def build_spread_data(spread_id, db, plan_pages=None):
    """Build merged per-spread JSON (analysis + OCR + visual + content plan)."""
    entries = db.get("spreads", [])
    entry = next((e for e in entries if e["id"] == spread_id), None)

    # Load Qwen3 OCR
    ocr_path = os.path.join(VLM_DIR, f"{spread_id}_ocr_qwen3.json")
    ocr_data = load_json(ocr_path)

    # Load Qwen3 visual analysis
    visual_path = os.path.join(VLM_DIR, f"{spread_id}_visual_qwen3.json")
    visual_data = load_json(visual_path)

    result = {
        "id": spread_id,
    }

    if entry:
        result["analysis"] = entry

    if ocr_data:
        result["ocr"] = {
            "ocr_raw": ocr_data.get("ocr_raw", ""),
            "ocr_raw_time": ocr_data.get("ocr_raw_time"),
            "ocr_structured": ocr_data.get("ocr_structured", ""),
            "ocr_structured_time": ocr_data.get("ocr_structured_time"),
            "model": ocr_data.get("model", "qwen3-vl"),
        }

    if visual_data:
        result["visual"] = {
            "image_description": visual_data.get("image_description", ""),
            "image_description_time": visual_data.get("image_description_time"),
            "layout_analysis": visual_data.get("layout_analysis", ""),
            "layout_analysis_time": visual_data.get("layout_analysis_time"),
            "model": visual_data.get("model", "qwen3-vl"),
        }

    # Merge content plan data if available
    if plan_pages:
        plan_entry = next((p for p in plan_pages if p.get("spread_id") == spread_id), None)
        if plan_entry:
            result["content_plan"] = plan_entry

    return result


def compress_images():
    """Compress rendered PNGs to JPEG for web delivery."""
    try:
        from PIL import Image
    except ImportError:
        print("  ERROR: Pillow not installed. Run: pip install Pillow")
        return False

    os.makedirs(IMAGES_DIR, exist_ok=True)
    count = 0
    total_original = 0
    total_compressed = 0

    for page_num in range(1, TOTAL_PAGES + 1):
        spread_id = f"spread_{page_num:03d}"
        png_path = os.path.join(RENDERED_DIR, f"{spread_id}.png")
        jpg_path = os.path.join(IMAGES_DIR, f"{spread_id}.jpg")

        if not os.path.exists(png_path):
            continue

        # Skip if JPEG already exists and is newer than PNG
        if os.path.exists(jpg_path) and os.path.getmtime(jpg_path) > os.path.getmtime(png_path):
            count += 1
            continue

        img = Image.open(png_path)
        # Convert RGBA to RGB if needed (JPEG doesn't support alpha)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        original_size = os.path.getsize(png_path)
        img.save(jpg_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
        compressed_size = os.path.getsize(jpg_path)

        total_original += original_size
        total_compressed += compressed_size
        count += 1
        print(f"  {spread_id}: {original_size/1024:.0f}KB -> {compressed_size/1024:.0f}KB "
              f"({compressed_size/original_size*100:.0f}%)")

    if total_original > 0:
        print(f"\n  Images: {count} files, "
              f"{total_original/1024/1024:.1f}MB -> {total_compressed/1024/1024:.1f}MB "
              f"({total_compressed/total_original*100:.0f}%)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Build static site for GitHub Pages")
    parser.add_argument("--no-images", action="store_true", help="Skip image compression")
    parser.add_argument("--clean", action="store_true", help="Remove docs/ before building")
    args = parser.parse_args()

    print(f"{'='*60}")
    print(f"  Building static site")
    print(f"  Output: {DOCS_DIR}")
    print(f"{'='*60}")

    # Clean if requested
    if args.clean and os.path.exists(DOCS_DIR):
        print(f"\n  Cleaning {DOCS_DIR}...")
        shutil.rmtree(DOCS_DIR)

    # Create directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Load analysis database
    print(f"\n[1/5] Loading analysis database...")
    db = load_json(DB_PATH)
    if not db:
        print(f"  ERROR: {DB_PATH} not found")
        sys.exit(1)
    entries = db.get("spreads", [])
    print(f"  Found {len(entries)} analyzed spreads")

    # Load content plan
    print(f"\n[2/5] Loading content plan...")
    content_plan = load_json(PLAN_PATH)
    plan_pages = []
    plan_meta = None
    if content_plan:
        plan_pages = content_plan.get("pages", [])
        plan_meta = content_plan.get("meta", None)
        print(f"  Found {len(plan_pages)} page plans")
        # Save meta.json for the overview view
        if plan_meta:
            meta_out = {
                "version": content_plan.get("version", "1.0"),
                "generated": content_plan.get("generated", ""),
                "schema_version": content_plan.get("schema_version", ""),
                "meta": plan_meta,
            }
            save_json(os.path.join(DATA_DIR, "meta.json"), meta_out)
            print(f"  Saved data/meta.json")
    else:
        print(f"  WARNING: {PLAN_PATH} not found, building without content plan data")

    # Build index.json
    print(f"\n[3/5] Building index and per-spread data files...")
    index_data = build_index(db)
    # Add content plan status to index
    index_data["has_content_plan"] = len(plan_pages) > 0
    index_data["content_plan_version"] = content_plan.get("version", "") if content_plan else ""
    save_json(os.path.join(DATA_DIR, "index.json"), index_data)
    print(f"  Saved data/index.json ({len(index_data['spreads'])} spreads)")

    # Build per-spread data files
    spread_count = 0
    for page_num in range(1, TOTAL_PAGES + 1):
        spread_id = f"spread_{page_num:03d}"
        # Only build data files for spreads that have SOME data
        has_analysis = any(e["id"] == spread_id for e in entries)
        has_ocr = os.path.exists(os.path.join(VLM_DIR, f"{spread_id}_ocr_qwen3.json"))
        has_visual = os.path.exists(os.path.join(VLM_DIR, f"{spread_id}_visual_qwen3.json"))
        has_plan = any(p.get("spread_id") == spread_id for p in plan_pages)

        if has_analysis or has_ocr or has_visual or has_plan:
            spread_data = build_spread_data(spread_id, db, plan_pages)
            save_json(os.path.join(DATA_DIR, f"{spread_id}.json"), spread_data)
            spread_count += 1

    print(f"  Generated {spread_count} spread data files")

    # Compress images
    if not args.no_images:
        print(f"\n[4/5] Compressing images (JPEG quality {JPEG_QUALITY})...")
        compress_images()
    else:
        print(f"\n[4/5] Skipping image compression (--no-images)")

    # Copy HTML and CSS
    print(f"\n[5/5] Copying viewer files...")
    shutil.copy2(STATIC_HTML, os.path.join(DOCS_DIR, "index.html"))
    shutil.copy2(STATIC_CSS, os.path.join(DOCS_DIR, "style.css"))
    print(f"  Copied index.html and style.css")

    # Summary
    print(f"\n{'='*60}")
    print(f"  Build complete!")
    print(f"  Output: {DOCS_DIR}")
    print(f"  Files:")

    def count_files(d):
        return sum(1 for _ in Path(d).rglob("*") if _.is_file())

    def dir_size(d):
        return sum(f.stat().st_size for f in Path(d).rglob("*") if f.is_file())

    total_files = count_files(DOCS_DIR)
    total_size = dir_size(DOCS_DIR)
    print(f"    {total_files} files, {total_size/1024/1024:.1f}MB total")
    print(f"    data/: {count_files(DATA_DIR)} JSON files")
    print(f"    images/: {count_files(IMAGES_DIR)} JPEG images")
    print(f"{'='*60}")
    print(f"\n  To test locally, open docs/index.html in a browser")
    print(f"  (Note: requires a local server for fetch() to work)")
    print(f"  Quick test: python -m http.server 8000 --directory docs")


if __name__ == "__main__":
    main()
