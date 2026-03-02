"""
Batch generate Qwen3-VL OCR extractions for all spreads.
Saves per-spread JSON files matching the format from Session 4.

Usage:
  python source/batch_ocr_qwen3.py                    # All spreads 001-085
  python source/batch_ocr_qwen3.py --start 11         # From spread 011
  python source/batch_ocr_qwen3.py --start 11 --end 40  # Range
  python source/batch_ocr_qwen3.py --force             # Overwrite existing
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

# ── Prompts (from vlm_tools.py) ──

RAW_OCR_PROMPT = (
    "You are an expert OCR system. Extract ALL text visible in this image, "
    "preserving the exact wording, spelling, punctuation, and capitalization. "
    "Include all text: titles, body text, captions, page numbers, credits, "
    "quotation marks, attribution lines, and any text used as design elements "
    "(e.g., large display words). Organize the extracted text by its position "
    "on the page (top to bottom, left to right). For text that spans across "
    "a gutter/spine, reconstruct the complete words. Mark any text you're "
    "uncertain about with [?]. Do NOT describe the images or layout — only "
    "extract text."
)

STRUCTURED_OCR_PROMPT = (
    "You are an expert OCR and document analysis system. Extract ALL text "
    "from this image and categorize it into these sections:\n\n"
    "DISPLAY_TEXT: Any text used as a large typographic design element\n"
    "BODY_TEXT: Main prose/paragraph text by the authors\n"
    "QUOTATIONS: Any quoted text with attribution\n"
    "CAPTIONS: Image captions, photo credits, small contextual text\n"
    "PAGE_NUMBERS: Any visible page numbers\n\n"
    "For each section, transcribe the text EXACTLY as it appears. "
    "If a section has no content, write NONE. "
    "Preserve original spelling, punctuation, and capitalization. "
    "For text spanning the gutter/spine, reconstruct complete words."
)


def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def ollama_chat(image_path, prompt):
    """Send image + prompt to Qwen3-VL via Ollama."""
    img_b64 = image_to_base64(image_path)
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt, "images": [img_b64]}],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 4096},
    }
    try:
        resp = requests.post(f"{OLLAMA_BASE}/api/chat", json=payload, timeout=300)
        resp.raise_for_status()
        return resp.json().get("message", {}).get("content", "")
    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect to Ollama"
    except Exception as e:
        return f"ERROR: {e}"


def generate_ocr(spread_id, force=False):
    """Generate raw + structured OCR for a single spread."""
    out_path = os.path.join(OUTPUT_DIR, f"{spread_id}_ocr_qwen3.json")
    img_path = os.path.join(RENDERED_DIR, f"{spread_id}.png")

    if not os.path.exists(img_path):
        print(f"  SKIP {spread_id}: image not found")
        return None

    if os.path.exists(out_path) and not force:
        print(f"  SKIP {spread_id}: already exists")
        return None

    print(f"\n  {spread_id}:")

    # Raw OCR
    print(f"    [1/2] Raw OCR...", end="", flush=True)
    t0 = time.time()
    raw = ollama_chat(img_path, RAW_OCR_PROMPT)
    raw_time = round(time.time() - t0, 1)
    print(f" {raw_time}s, {len(raw)} chars")

    # Retry on empty
    if len(raw.strip()) == 0:
        print(f"    [1/2] RETRY...", end="", flush=True)
        t0 = time.time()
        raw = ollama_chat(img_path, RAW_OCR_PROMPT)
        raw_time = round(time.time() - t0, 1)
        print(f" {raw_time}s, {len(raw)} chars")

    # Structured OCR
    print(f"    [2/2] Structured OCR...", end="", flush=True)
    t0 = time.time()
    structured = ollama_chat(img_path, STRUCTURED_OCR_PROMPT)
    structured_time = round(time.time() - t0, 1)
    print(f" {structured_time}s, {len(structured)} chars")

    # Retry on empty
    if len(structured.strip()) == 0:
        print(f"    [2/2] RETRY...", end="", flush=True)
        t0 = time.time()
        structured = ollama_chat(img_path, STRUCTURED_OCR_PROMPT)
        structured_time = round(time.time() - t0, 1)
        print(f" {structured_time}s, {len(structured)} chars")

    result = {
        "spread_id": spread_id,
        "model": OLLAMA_MODEL,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ocr_raw": raw,
        "ocr_structured": structured,
        "ocr_raw_time": raw_time,
        "ocr_structured_time": structured_time,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


def main():
    parser = argparse.ArgumentParser(description="Batch Qwen3-VL OCR")
    parser.add_argument("--start", type=int, default=1, help="Start spread number")
    parser.add_argument("--end", type=int, default=85, help="End spread number")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()

    print(f"Batch OCR: spreads {args.start:03d}-{args.end:03d}")
    print(f"Model: {OLLAMA_MODEL}")

    generated = 0
    skipped = 0
    errors = 0
    t_start = time.time()

    for i in range(args.start, args.end + 1):
        spread_id = f"spread_{i:03d}"
        result = generate_ocr(spread_id, force=args.force)
        if result is None:
            skipped += 1
        elif result.get("ocr_raw", "").startswith("ERROR"):
            errors += 1
        else:
            generated += 1

    elapsed = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"  OCR batch complete")
    print(f"  Generated: {generated}, Skipped: {skipped}, Errors: {errors}")
    print(f"  Total time: {elapsed/60:.1f} minutes")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
