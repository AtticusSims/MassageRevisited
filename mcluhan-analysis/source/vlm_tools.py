"""
VLM Tools for McLuhan Analysis Pipeline
========================================
Two-model approach:
  - Qwen2.5-VL-7B (via Ollama) for OCR / text extraction
  - Molmo2-8B (via Transformers) for image description and layout analysis

Usage:
  python vlm_tools.py ocr <image_path>           # Run OCR only
  python vlm_tools.py describe <image_path>       # Run Molmo description only
  python vlm_tools.py analyze <image_path>        # Run both, save combined JSON
  python vlm_tools.py batch <image_dir> [start] [end]  # Batch process spreads
"""

import json
import sys
import os
import base64
import time
import argparse
import requests
from pathlib import Path

# ── Ollama config ──
OLLAMA_BASE = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5vl:7b"

# ── Molmo config ──
MOLMO_MODEL_ID = "allenai/Molmo2-8B"

# ── Output dir ──
VLM_OUTPUT_DIR = None  # Set at runtime


def image_to_base64(image_path: str) -> str:
    """Convert image file to base64 string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ═══════════════════════════════════════════════════════════════
# Qwen2.5-VL OCR via Ollama
# ═══════════════════════════════════════════════════════════════

def _ollama_chat(image_path: str, prompt: str) -> str:
    """
    Send an image + prompt to Ollama using the /api/chat endpoint.
    This endpoint works much better for vision models than /api/generate.
    """
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
        return "ERROR: Cannot connect to Ollama. Is it running? Start with: ollama serve"
    except Exception as e:
        return f"ERROR: {e}"


def run_ocr(image_path: str, prompt: str = None) -> str:
    """
    Extract all text from an image using Qwen2.5-VL via Ollama.
    Returns the raw text extraction.
    """
    if prompt is None:
        prompt = (
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

    return _ollama_chat(image_path, prompt)


def run_structured_ocr(image_path: str) -> str:
    """
    Extract text with structural markup — distinguishing body text,
    display text, quotations, captions, and page numbers.
    """
    prompt = (
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
    return _ollama_chat(image_path, prompt)


# ═══════════════════════════════════════════════════════════════
# Molmo2-8B Image Description via Transformers
# ═══════════════════════════════════════════════════════════════

# Global model/processor (loaded once, reused)
_molmo_model = None
_molmo_processor = None


def _load_molmo():
    """Load Molmo2-8B model and processor (once)."""
    global _molmo_model, _molmo_processor

    if _molmo_model is not None:
        return

    import torch
    from transformers import AutoProcessor, AutoModelForImageTextToText

    print(f"Loading {MOLMO_MODEL_ID}... (this may take a few minutes on first run)")
    start = time.time()

    _molmo_processor = AutoProcessor.from_pretrained(
        MOLMO_MODEL_ID,
        trust_remote_code=True,
    )

    _molmo_model = AutoModelForImageTextToText.from_pretrained(
        MOLMO_MODEL_ID,
        trust_remote_code=True,
        dtype=torch.bfloat16,
        device_map="auto",
    )

    elapsed = time.time() - start
    print(f"Molmo2-8B loaded in {elapsed:.1f}s")


def run_molmo(image_path: str, prompt: str) -> str:
    """
    Run Molmo2-8B inference on an image with a given prompt.
    Returns the generated text.
    """
    import torch
    from PIL import Image

    _load_molmo()

    img = Image.open(image_path).convert("RGB")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": img},
                {"type": "text", "text": prompt},
            ]
        }
    ]

    inputs = _molmo_processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
    )
    inputs = {k: v.to(_molmo_model.device) for k, v in inputs.items()}

    with torch.inference_mode():
        generated_ids = _molmo_model.generate(
            **inputs,
            max_new_tokens=2048,
            temperature=0.2,
            do_sample=True,
        )

    generated_tokens = generated_ids[0, inputs["input_ids"].size(1):]
    return _molmo_processor.tokenizer.decode(generated_tokens, skip_special_tokens=True)


def describe_images(image_path: str) -> str:
    """
    Describe all photographs, illustrations, and graphic elements
    in the spread image using Molmo2-8B.
    """
    prompt = (
        "Describe every photograph, illustration, graphic symbol, or visual element "
        "in this book spread image (NOT the text — only the visual/pictorial elements). "
        "For each image or visual element:\n"
        "1. What does it depict? Be very specific — identify people, objects, scenes, events.\n"
        "2. Where is it positioned on the page (left page, right page, full bleed, spanning both pages, inset, etc.)?\n"
        "3. What is the visual style (black and white photograph, illustration, graphic symbol, etc.)?\n"
        "4. Describe the composition: framing, angle, contrast, key visual qualities.\n"
        "5. Approximately how much of the page does it occupy?\n\n"
        "If there are NO photographs or illustrations (only text/typography), say 'NO IMAGES — typography only'."
    )
    return run_molmo(image_path, prompt)


def describe_layout(image_path: str) -> str:
    """
    Describe the overall spatial layout and design of the spread
    using Molmo2-8B.
    """
    prompt = (
        "Analyze the visual layout and design of this book spread. Describe:\n"
        "1. SPATIAL ARRANGEMENT: Where does text sit? Where do images sit? "
        "How is the space divided between left and right pages?\n"
        "2. TYPOGRAPHY: What kinds of text are visible? Large display text? "
        "Small body text? What are the approximate relative sizes? "
        "Is text serif or sans-serif? Bold or light? Normal or reversed (white on black)?\n"
        "3. CONTRAST & TONE: Is the spread predominantly dark or light? "
        "High contrast or low? What is the ratio of black to white?\n"
        "4. WHITE SPACE: How much empty/breathing space exists? "
        "Is the spread sparse, moderate, dense, or packed?\n"
        "5. LEFT-RIGHT RELATIONSHIP: How do the two pages relate — "
        "mirror, contrast, continuation, one dominates the other, unified?\n"
        "6. OVERALL FEEL: What is the visual mood or energy of this spread? "
        "Calm, aggressive, chaotic, minimal, overwhelming?"
    )
    return run_molmo(image_path, prompt)


# ═══════════════════════════════════════════════════════════════
# Combined Analysis Pipeline
# ═══════════════════════════════════════════════════════════════

def analyze_spread(image_path: str, output_dir: str = None) -> dict:
    """
    Run full VLM analysis on a spread image:
    1. Structured OCR via Qwen2.5-VL
    2. Image description via Molmo2-8B
    3. Layout analysis via Molmo2-8B

    Returns dict with all results. Saves to JSON file if output_dir provided.
    """
    spread_name = Path(image_path).stem  # e.g., "spread_001"

    print(f"\n{'='*60}")
    print(f"  Analyzing: {spread_name}")
    print(f"{'='*60}")

    # Step 1: OCR
    print(f"  [1/3] Running OCR (Qwen2.5-VL)...")
    t0 = time.time()
    ocr_raw = run_ocr(image_path)
    ocr_structured = run_structured_ocr(image_path)
    ocr_time = time.time() - t0
    print(f"        Done ({ocr_time:.1f}s)")

    # Step 2: Image description
    print(f"  [2/3] Describing images (Molmo2-8B)...")
    t0 = time.time()
    img_desc = describe_images(image_path)
    img_time = time.time() - t0
    print(f"        Done ({img_time:.1f}s)")

    # Step 3: Layout analysis
    print(f"  [3/3] Analyzing layout (Molmo2-8B)...")
    t0 = time.time()
    layout_desc = describe_layout(image_path)
    layout_time = time.time() - t0
    print(f"        Done ({layout_time:.1f}s)")

    result = {
        "spread_id": spread_name,
        "image_path": str(image_path),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ocr": {
            "raw_extraction": ocr_raw,
            "structured_extraction": ocr_structured,
        },
        "image_description": img_desc,
        "layout_analysis": layout_desc,
        "processing_time": {
            "ocr_seconds": round(ocr_time, 1),
            "image_description_seconds": round(img_time, 1),
            "layout_analysis_seconds": round(layout_time, 1),
            "total_seconds": round(ocr_time + img_time + layout_time, 1),
        }
    }

    # Save to file
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, f"{spread_name}_vlm.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {out_path}")

    return result


def batch_analyze(image_dir: str, output_dir: str, start: int = 1, end: int = 10):
    """Process a range of spreads."""
    results = []
    for i in range(start, end + 1):
        img_path = os.path.join(image_dir, f"spread_{i:03d}.png")
        if not os.path.exists(img_path):
            print(f"  SKIP: {img_path} not found")
            continue
        result = analyze_spread(img_path, output_dir)
        results.append(result)

    print(f"\n{'='*60}")
    print(f"  Batch complete: {len(results)} spreads analyzed")
    print(f"{'='*60}")
    return results


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VLM tools for McLuhan analysis")
    parser.add_argument("command", choices=["ocr", "ocr-structured", "describe", "layout", "analyze", "batch"])
    parser.add_argument("path", help="Image path or directory for batch")
    parser.add_argument("--start", type=int, default=1, help="Start spread number (batch mode)")
    parser.add_argument("--end", type=int, default=10, help="End spread number (batch mode)")
    parser.add_argument("--output", "-o", default=None, help="Output directory")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_output = os.path.join(base_dir, "output", "vlm_extractions")

    if args.command == "ocr":
        print(run_ocr(args.path))
    elif args.command == "ocr-structured":
        print(run_structured_ocr(args.path))
    elif args.command == "describe":
        print(describe_images(args.path))
    elif args.command == "layout":
        print(describe_layout(args.path))
    elif args.command == "analyze":
        out = args.output or default_output
        analyze_spread(args.path, out)
    elif args.command == "batch":
        out = args.output or default_output
        batch_analyze(args.path, out, args.start, args.end)
