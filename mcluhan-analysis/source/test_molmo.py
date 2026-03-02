"""
Test Molmo2-8B on sample spreads from the McLuhan analysis.
Runs image description and layout analysis on 3 representative spreads.
"""

import sys
import os
import json
import time

# Add source dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vlm_tools import run_molmo, describe_images, describe_layout, _load_molmo

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERED = os.path.join(BASE, "rendered")
OUTPUT = os.path.join(BASE, "output", "vlm_extractions")

# Test spreads: image_dominant, typography_as_design, text_with_specific_image
TEST_SPREADS = ["spread_005", "spread_007", "spread_008"]


def test_spread(spread_id: str) -> dict:
    """Run Molmo describe_images and describe_layout on one spread."""
    img_path = os.path.join(RENDERED, f"{spread_id}.png")
    if not os.path.exists(img_path):
        return {"error": f"Image not found: {img_path}"}

    print(f"\n{'='*60}")
    print(f"  Testing Molmo on {spread_id}")
    print(f"{'='*60}")

    result = {"spread_id": spread_id}

    # Image description
    print(f"  [1/2] describe_images...")
    t0 = time.time()
    result["image_description"] = describe_images(img_path)
    result["image_description_time"] = round(time.time() - t0, 1)
    print(f"        Done ({result['image_description_time']}s, {len(result['image_description'])} chars)")

    # Layout analysis
    print(f"  [2/2] describe_layout...")
    t0 = time.time()
    result["layout_description"] = describe_layout(img_path)
    result["layout_description_time"] = round(time.time() - t0, 1)
    print(f"        Done ({result['layout_description_time']}s, {len(result['layout_description'])} chars)")

    return result


def main():
    print("=" * 60)
    print("  Molmo2-8B Test Suite")
    print("=" * 60)

    # Pre-load model once
    print("\nLoading Molmo2-8B (first load will take ~60s)...")
    t0 = time.time()
    _load_molmo()
    load_time = time.time() - t0
    print(f"Model loaded in {load_time:.1f}s")

    results = []
    for spread_id in TEST_SPREADS:
        result = test_spread(spread_id)
        results.append(result)

        # Print results immediately
        print(f"\n--- {spread_id} Image Description ---")
        print(result.get("image_description", "N/A")[:500])
        print(f"\n--- {spread_id} Layout ---")
        print(result.get("layout_description", "N/A")[:500])

    # Save results
    out_path = os.path.join(OUTPUT, "molmo_test_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")

    # Summary
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Model load time: {load_time:.1f}s")
    for r in results:
        img_t = r.get("image_description_time", 0)
        lay_t = r.get("layout_description_time", 0)
        img_len = len(r.get("image_description", ""))
        lay_len = len(r.get("layout_description", ""))
        print(f"  {r['spread_id']}: img={img_t}s ({img_len}ch) lay={lay_t}s ({lay_len}ch)")


if __name__ == "__main__":
    main()
