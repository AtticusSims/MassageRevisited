"""
Compare Qwen2.5-VL vs Qwen3-VL on the same spreads.
Runs both OCR (raw + structured) on 3 representative spreads,
plus image description on 2 spreads. Saves JSON comparison.

Usage:
  python source/compare_qwen_versions.py
"""

import json
import sys
import os
import base64
import time
import requests

OLLAMA_BASE = "http://localhost:11434"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERED = os.path.join(BASE, "rendered")
OUTPUT = os.path.join(BASE, "output", "vlm_extractions")


def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def ollama_chat(model: str, image_path: str, prompt: str) -> str:
    img_b64 = image_to_base64(image_path)
    payload = {
        "model": model,
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
    except Exception as e:
        return f"ERROR: {e}"


# ── Prompts ──

OCR_RAW_PROMPT = (
    "You are an expert OCR system. Extract ALL text visible in this image, "
    "preserving the exact wording, spelling, punctuation, and capitalization. "
    "Include all text: titles, body text, captions, page numbers, credits, "
    "quotation marks, attribution lines, and any text used as design elements "
    "(e.g., large display words). "
    "Organize the extracted text by its position on the page "
    "(top to bottom, left to right). "
    "For text that spans across a gutter/spine, reconstruct the complete words. "
    "Mark any text you're uncertain about with [?]. "
    "Do NOT describe the images or layout — only extract text."
)

OCR_STRUCTURED_PROMPT = (
    "You are an expert OCR and document analysis system. "
    "Extract ALL text from this image and categorize it into these sections:\n\n"
    "DISPLAY_TEXT: Any text used as a large typographic design element "
    "(giant words, section titles that dominate the page)\n"
    "BODY_TEXT: Main prose/paragraph text by the authors\n"
    "QUOTATIONS: Any quoted text with attribution (include the author name)\n"
    "CAPTIONS: Image captions, photo credits, small contextual text\n"
    "PAGE_NUMBERS: Any visible page numbers\n\n"
    "For each section, transcribe the text EXACTLY as it appears — "
    "preserve spelling, punctuation, capitalization, and any unusual "
    "typographic effects (like repeated letters). "
    "If a section has no content, write NONE. "
    "Reconstruct words split across a gutter/spine. "
    "Mark uncertain readings with [?]."
)

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


MODELS = ["qwen2.5vl:7b", "qwen3-vl"]

# Test spreads: cover (text over image), dense body text, typography-as-design, branded egg, hand close-up
OCR_TEST_SPREADS = ["spread_001", "spread_009", "spread_010"]
VISUAL_TEST_SPREADS = ["spread_005", "spread_007"]


def run_comparison():
    results = {}

    for spread_id in OCR_TEST_SPREADS + VISUAL_TEST_SPREADS:
        img = os.path.join(RENDERED, f"{spread_id}.png")
        if not os.path.exists(img):
            print(f"  SKIP {spread_id} (not found)")
            continue

        results[spread_id] = {}

        for model in MODELS:
            print(f"\n{'='*60}")
            print(f"  {spread_id} / {model}")
            print(f"{'='*60}")

            entry = {}

            if spread_id in OCR_TEST_SPREADS:
                # Raw OCR
                print(f"  [OCR raw]...", end="", flush=True)
                t0 = time.time()
                entry["ocr_raw"] = ollama_chat(model, img, OCR_RAW_PROMPT)
                entry["ocr_raw_time"] = round(time.time() - t0, 1)
                print(f" {entry['ocr_raw_time']}s, {len(entry['ocr_raw'])}ch")

                # Structured OCR
                print(f"  [OCR structured]...", end="", flush=True)
                t0 = time.time()
                entry["ocr_structured"] = ollama_chat(model, img, OCR_STRUCTURED_PROMPT)
                entry["ocr_structured_time"] = round(time.time() - t0, 1)
                print(f" {entry['ocr_structured_time']}s, {len(entry['ocr_structured'])}ch")

            if spread_id in VISUAL_TEST_SPREADS:
                # Image description
                print(f"  [Image describe]...", end="", flush=True)
                t0 = time.time()
                entry["image_describe"] = ollama_chat(model, img, IMAGE_DESCRIBE_PROMPT)
                entry["image_describe_time"] = round(time.time() - t0, 1)
                print(f" {entry['image_describe_time']}s, {len(entry['image_describe'])}ch")

                # Layout
                print(f"  [Layout]...", end="", flush=True)
                t0 = time.time()
                entry["layout"] = ollama_chat(model, img, LAYOUT_PROMPT)
                entry["layout_time"] = round(time.time() - t0, 1)
                print(f" {entry['layout_time']}s, {len(entry['layout'])}ch")

            results[spread_id][model] = entry

    # Save
    out_path = os.path.join(OUTPUT, "qwen_version_comparison.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved comparison to {out_path}")

    # Print summary
    print(f"\n{'='*70}")
    print(f"  TIMING SUMMARY")
    print(f"{'='*70}")
    for spread_id in results:
        for model in results[spread_id]:
            e = results[spread_id][model]
            times = []
            for k in ["ocr_raw_time", "ocr_structured_time", "image_describe_time", "layout_time"]:
                if k in e:
                    times.append(f"{k.replace('_time','')}: {e[k]}s")
            print(f"  {spread_id} / {model}: {', '.join(times)}")


if __name__ == "__main__":
    run_comparison()
