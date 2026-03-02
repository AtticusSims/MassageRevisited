"""
Generate Qwen3-VL image descriptions and layout analysis for all spreads.
Saves per-spread JSON files to output/vlm_extractions/.

Usage:
  python source/generate_visual_analysis.py              # All spreads 001-010
  python source/generate_visual_analysis.py --start 5    # From spread 005
  python source/generate_visual_analysis.py --force       # Overwrite existing
"""

import json
import os
import sys
import base64
import time
import argparse
import requests

OLLAMA_BASE = "http://localhost:11434"
OLLAMA_MODEL = "qwen3-vl"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERED_DIR = os.path.join(BASE_DIR, "rendered")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "vlm_extractions")

# ── Prompts (from compare_qwen_versions.py, tested with Qwen3-VL) ──

IMAGE_DESCRIBE_PROMPT = (
    "Describe every photograph, illustration, graphic symbol, or visual element "
    "in this book spread image (NOT the text — only the visual/pictorial elements). "
    "For each image or visual element:\n"
    "1. What does it depict? Be very specific — identify people, objects, scenes, events.\n"
    "2. Where is it positioned on the page (left page, right page, full bleed, spanning both pages, inset)?\n"
    "3. What is the visual style (black and white photograph, illustration, graphic symbol)?\n"
    "4. Describe the composition: framing, angle, contrast, key visual qualities.\n"
    "5. Approximately how much of the page does it occupy?\n\n"
    "If there are NO photographs or illustrations (only text/typography), say so and describe "
    "the typography AS a visual element: its scale, weight, color, position, and how the letterforms "
    "work as visual design."
)

LAYOUT_PROMPT = (
    "Analyze the visual layout and design of this book spread. Describe:\n"
    "1. SPATIAL ARRANGEMENT: Where does text sit? Where do images sit? How is the space divided?\n"
    "2. TYPOGRAPHY: What kinds of text are visible? Large display text? Small body text? "
    "Serif or sans-serif? Bold or light? Normal or reversed (white on black)?\n"
    "3. CONTRAST & TONE: Predominantly dark or light? High contrast or low?\n"
    "4. WHITE SPACE: How much empty space? Sparse, moderate, dense, or packed?\n"
    "5. LEFT-RIGHT RELATIONSHIP: Mirror, contrast, continuation, one dominates, unified?\n"
    "6. OVERALL FEEL: Visual mood or energy — calm, aggressive, chaotic, minimal, overwhelming?"
)


def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def ollama_chat(image_path: str, prompt: str) -> str:
    """Send image + prompt to Qwen3-VL via Ollama."""
    img_b64 = image_to_base64(image_path)
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [img_b64],
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 4096,
        }
    }
    try:
        resp = requests.post(
            f"{OLLAMA_BASE}/api/chat",
            json=payload,
            timeout=300
        )
        resp.raise_for_status()
        result = resp.json()
        return result.get("message", {}).get("content", "")
    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect to Ollama. Is it running?"
    except Exception as e:
        return f"ERROR: {e}"


def generate_visual(spread_id: str, force: bool = False) -> dict:
    """Generate image description + layout analysis for a single spread."""
    out_path = os.path.join(OUTPUT_DIR, f"{spread_id}_visual_qwen3.json")
    img_path = os.path.join(RENDERED_DIR, f"{spread_id}.png")

    if not os.path.exists(img_path):
        print(f"  SKIP {spread_id}: image not found at {img_path}")
        return None

    if os.path.exists(out_path) and not force:
        print(f"  SKIP {spread_id}: already exists (use --force to overwrite)")
        return None

    print(f"\n{'='*60}")
    print(f"  Generating visual analysis: {spread_id}")
    print(f"{'='*60}")

    # Image description
    print(f"  [1/2] Image description...", end="", flush=True)
    t0 = time.time()
    img_desc = ollama_chat(img_path, IMAGE_DESCRIBE_PROMPT)
    img_time = round(time.time() - t0, 1)
    print(f" {img_time}s, {len(img_desc)} chars")

    # Retry on empty
    if len(img_desc.strip()) == 0:
        print(f"  [1/2] RETRY (empty response)...", end="", flush=True)
        t0 = time.time()
        img_desc = ollama_chat(img_path, IMAGE_DESCRIBE_PROMPT)
        img_time = round(time.time() - t0, 1)
        print(f" {img_time}s, {len(img_desc)} chars")

    # Layout analysis
    print(f"  [2/2] Layout analysis...", end="", flush=True)
    t0 = time.time()
    layout = ollama_chat(img_path, LAYOUT_PROMPT)
    layout_time = round(time.time() - t0, 1)
    print(f" {layout_time}s, {len(layout)} chars")

    # Retry on empty
    if len(layout.strip()) == 0:
        print(f"  [2/2] RETRY (empty response)...", end="", flush=True)
        t0 = time.time()
        layout = ollama_chat(img_path, LAYOUT_PROMPT)
        layout_time = round(time.time() - t0, 1)
        print(f" {layout_time}s, {len(layout)} chars")

    result = {
        "spread_id": spread_id,
        "model": OLLAMA_MODEL,
        "image_description": img_desc,
        "image_description_time": img_time,
        "layout_analysis": layout,
        "layout_analysis_time": layout_time,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {out_path}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Generate Qwen3-VL visual analysis")
    parser.add_argument("--start", type=int, default=1, help="Start spread number")
    parser.add_argument("--end", type=int, default=10, help="End spread number")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    print(f"Generating visual analysis for spreads {args.start:03d}-{args.end:03d}")
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Output: {OUTPUT_DIR}")

    results = []
    for i in range(args.start, args.end + 1):
        spread_id = f"spread_{i:03d}"
        result = generate_visual(spread_id, force=args.force)
        if result:
            results.append(result)

    print(f"\n{'='*60}")
    print(f"  Complete: {len(results)} visual analyses generated")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
