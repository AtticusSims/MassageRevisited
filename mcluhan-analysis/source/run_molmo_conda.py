"""
Run Molmo2-8B inside the 'molmo' conda env (transformers 4.57.1).
Standalone script — no dependency on vlm_tools.py.

Usage (from project root):
  conda run -n molmo python source/run_molmo_conda.py describe rendered/spread_007.png
  conda run -n molmo python source/run_molmo_conda.py layout rendered/spread_009.png
  conda run -n molmo python source/run_molmo_conda.py batch rendered 5 8
"""

import json
import sys
import os
import time
import argparse
from pathlib import Path

# Config
MOLMO_MODEL_ID = "allenai/Molmo2-8B"

# Global model/processor
_model = None
_processor = None


def load_model():
    global _model, _processor
    if _model is not None:
        return

    import torch
    from transformers import AutoProcessor, AutoModelForImageTextToText

    print(f"Loading {MOLMO_MODEL_ID}...")
    t0 = time.time()

    _processor = AutoProcessor.from_pretrained(
        MOLMO_MODEL_ID,
        trust_remote_code=True,
    )
    _model = AutoModelForImageTextToText.from_pretrained(
        MOLMO_MODEL_ID,
        trust_remote_code=True,
        dtype=torch.bfloat16,
        device_map="auto",
    )
    print(f"Loaded in {time.time()-t0:.1f}s")


def run_molmo(image_path: str, prompt: str, max_tokens: int = 2048) -> str:
    import torch
    from PIL import Image

    load_model()
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

    inputs = _processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
    )
    inputs = {k: v.to(_model.device) for k, v in inputs.items()}

    with torch.inference_mode():
        output = _model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.2,
            do_sample=True,
        )

    tokens = output[0, inputs["input_ids"].size(1):]
    return _processor.tokenizer.decode(tokens, skip_special_tokens=True)


DESCRIBE_PROMPT = """Describe every photograph, illustration, graphic symbol, or visual element \
in this book spread image (NOT the text — only the visual/pictorial elements). \
For each image or visual element:
1. What does it depict? Be very specific — identify people, objects, scenes, events.
2. Where is it positioned on the page (left page, right page, full bleed, spanning both pages, inset)?
3. What is the visual style (black and white photograph, illustration, graphic symbol)?
4. Describe the composition: framing, angle, contrast, key visual qualities.
5. Approximately how much of the page does it occupy?

If there are NO photographs or illustrations (only text/typography), say so and describe \
the typography AS a visual element: its scale, weight, color, position, and how the letterforms \
work as visual design."""

LAYOUT_PROMPT = """Analyze the visual layout and design of this book spread. Describe:
1. SPATIAL ARRANGEMENT: Where does text sit? Where do images sit? How is the space divided?
2. TYPOGRAPHY: What kinds of text are visible? Large display text? Small body text? \
Serif or sans-serif? Bold or light? Normal or reversed (white on black)?
3. CONTRAST & TONE: Predominantly dark or light? High contrast or low?
4. WHITE SPACE: How much empty space? Sparse, moderate, dense, or packed?
5. LEFT-RIGHT RELATIONSHIP: Mirror, contrast, continuation, one dominates, unified?
6. OVERALL FEEL: Visual mood or energy — calm, aggressive, chaotic, minimal, overwhelming?"""


def main():
    parser = argparse.ArgumentParser(description="Run Molmo2-8B on spread images")
    parser.add_argument("command", choices=["describe", "layout", "both", "batch"],
                       help="What to run")
    parser.add_argument("path", help="Image path or directory for batch")
    parser.add_argument("start", nargs="?", type=int, default=1, help="Start spread (batch)")
    parser.add_argument("end", nargs="?", type=int, default=10, help="End spread (batch)")
    parser.add_argument("--output", "-o", default=None, help="Output JSON file")
    args = parser.parse_args()

    if args.command == "batch":
        results = []
        for i in range(args.start, args.end + 1):
            img = os.path.join(args.path, f"spread_{i:03d}.png")
            if not os.path.exists(img):
                print(f"  Skipping spread_{i:03d} (not found)")
                continue

            print(f"\n{'='*50}")
            print(f"  spread_{i:03d}")
            print(f"{'='*50}")

            entry = {"spread_id": f"spread_{i:03d}"}

            t0 = time.time()
            entry["image_description"] = run_molmo(img, DESCRIBE_PROMPT)
            entry["image_time"] = round(time.time() - t0, 1)
            print(f"  describe: {entry['image_time']}s, {len(entry['image_description'])}ch")

            t0 = time.time()
            entry["layout_description"] = run_molmo(img, LAYOUT_PROMPT)
            entry["layout_time"] = round(time.time() - t0, 1)
            print(f"  layout:   {entry['layout_time']}s, {len(entry['layout_description'])}ch")

            results.append(entry)

        out = args.output or os.path.join(args.path, "..", "output", "vlm_extractions", "molmo_batch.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nSaved {len(results)} results to {out}")

    else:
        img = args.path
        result = {}

        if args.command in ("describe", "both"):
            t0 = time.time()
            result["image_description"] = run_molmo(img, DESCRIBE_PROMPT)
            print(f"\n=== Image Description ({time.time()-t0:.1f}s) ===")
            print(result["image_description"])

        if args.command in ("layout", "both"):
            t0 = time.time()
            result["layout_description"] = run_molmo(img, LAYOUT_PROMPT)
            print(f"\n=== Layout Analysis ({time.time()-t0:.1f}s) ===")
            print(result["layout_description"])

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
