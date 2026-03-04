#!/usr/bin/env python3
"""
regenerate_images_v2.py — Improved image generation for problem spreads.

Addresses issues found in first-pass generation:
1. "Photograph of a book" problem — images render with page edges/binding
2. AI text garbling — misspelled labels
3. Concept misinterpretation — wrong visual concepts
4. Over-cluttered AI slop — too busy, too many elements

Key prompt improvements:
- Remove ALL book/page/print references
- Use natural language creative director style
- Add explicit anti-book constraints
- Specify flat digital output format
- Use cultural shorthand for style
- Simplify complex multi-element compositions
"""

import io
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageEnhance

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
IMAGES_DIR = BASE_DIR / "docs" / "images"
V2_DIR = IMAGES_DIR / "v2"

IMAGE_MODEL = "gemini-3.1-flash-image-preview"
IMAGE_MODEL_FALLBACK = "gemini-2.5-flash-image"
REQUEST_TIMEOUT = 120
CALL_INTERVAL = 4.0  # seconds between API calls


def _load_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    env_path = SOURCE_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip("'\"")
    raise EnvironmentError("GEMINI_API_KEY not found")


def get_client():
    from google import genai
    return genai.Client(api_key=_load_api_key())


# ══════════════════════════════════════════════════════
# IMPROVED PROMPTS — one per spread
# ══════════════════════════════════════════════════════

IMPROVED_PROMPTS = {
    "spread_018": {
        "prompt": (
            "A minimal, flat architectural section diagram rendered in clean black ink on white. "
            "Six horizontal strata stacked vertically like geological layers in a textbook cross-section. "
            "From bottom to top, labeled in a clean sans-serif typeface: EARTH, GEOSPHERE, INFRASTRUCTURE, NETWORK, INTERFACE, USER. "
            "Each layer is a simple flat rectangle — the bottom layer is solid black, each successive layer slightly lighter, "
            "the top layer is white with a thin black outline. "
            "The style is purely diagrammatic: no 3D effects, no shadows, no perspective, no decoration. "
            "Think of a clean technical illustration from an Edward Tufte book or a minimal infographic in a scientific journal. "
            "The entire image should be flat and edge-to-edge with NO page borders, NO paper texture, and NO book edges visible."
        ),
        "aspect_ratio": "3:4",
        "issue": "Original looked like a photograph of a physical book with 3D cartoon blocks",
    },

    "spread_022": {
        "prompt": (
            "A stark black and white diptych composition, split vertically down the center. "
            "Left half: an overhead view of an open hardcover book lying flat, its pages spread wide, "
            "photographed from directly above against a pure black background. The text on the pages is visible as texture but not readable. "
            "Right half: a minimalist dark interface showing lines of text appearing one word at a time, "
            "with a blinking cursor at the end. The interface is stripped of all branding — just light text on a dark field. "
            "The contrast is between the static, complete object (the book) and the dynamic, incomplete process (the generation). "
            "Shot as a clean flat-lay composition. No table surface visible. No device bezels. No reflections. "
            "Pure black background behind both halves. High contrast monochrome. "
            "Do NOT include any text that could be read as real words — all text should be abstract marks suggesting letterforms. "
            "The image must fill the entire frame edge to edge with NO page borders and NO paper texture."
        ),
        "aspect_ratio": "3:4",
        "issue": "Original looked like photo of physical book on a table, with garbled chat text",
    },

    "spread_066": {
        "prompt": (
            "A bold graphic design composition: the copyright symbol (a capital C inside a circle) rendered in solid black, "
            "centered on a pure white background. The symbol is large, filling most of the frame. "
            "The right side and bottom of the symbol are disintegrating — breaking apart into angular fragments, pixels, "
            "and particles that scatter outward and dissolve into noise. The left side of the symbol remains crisp and geometric. "
            "The dissolution should progress from clean to chaotic, left to right, as if the symbol is being eroded by entropy. "
            "Rendered in a high-contrast screen-print or risograph aesthetic — solid blacks, stark whites, visible halftone dots "
            "in the transition zones. Think of Wolfgang Weingart's deconstructed typography or April Greiman's digital experiments. "
            "The image must be completely flat and fill the entire frame. "
            "NO page edges, NO book binding shadows, NO paper texture visible at the borders."
        ),
        "aspect_ratio": "3:4",
        "issue": "Original concept was good but rendered as photograph of a book page",
    },

    "spread_074": {
        "prompt": (
            "A documentary-style black and white photograph of a large crowd gathered in a public square, "
            "shot from a slightly elevated vantage point — perhaps a second-floor window. "
            "The crowd is dense, hundreds of people filling the frame. Some hold signs (the signs should have "
            "abstract marks suggesting text, NOT readable words). There is a haze of smoke or tear gas "
            "drifting across the upper portion of the scene. Wet pavement reflects the crowd. "
            "The composition and grain should evoke 1960s press photography — think Don McCullin or Philip Jones Griffiths. "
            "Shot on Kodak Tri-X 400 film, with authentic film grain, deep blacks, and bright highlights in the wet surfaces. "
            "Shallow depth of field so the nearest figures are sharp and the far crowd softens into abstraction. "
            "The image must fill the entire frame with NO borders, NO page edges, and NO book binding visible."
        ),
        "aspect_ratio": "3:4",
        "issue": "Original looked like a photograph of a book page with garbled protest sign text",
    },

    "spread_075": {
        "prompt": (
            "A detailed pen-and-ink illustration in the style of Sir John Tenniel's engravings for Alice in Wonderland. "
            "The scene depicts a chaotic battle: dozens of small figures tumble over each other in a dense melee. "
            "Instead of soldiers, the combatants are anonymous figures — some wearing suits, some in hoodies — "
            "wielding shields shaped like verification checkmarks, throwing speech bubbles as projectiles, "
            "and charging behind banner-like flags. A few robot-like figures (simple, geometric, not detailed) "
            "are mixed into the crowd. The overall composition should be a single dense, swirling mass of conflict "
            "rendered entirely in fine cross-hatching and parallel line shading, exactly like a Victorian woodcut engraving. "
            "Pure black ink on white paper. No digital effects. No actual readable text on any element — "
            "all labels and signs should be abstract squiggles suggesting text. "
            "The image fills the entire frame. No borders. No page edges."
        ),
        "aspect_ratio": "3:4",
        "issue": "Original was too cluttered with readable AI-garbled text labels; felt more like a poster than an engraving",
    },

    "spread_080": {
        "prompt": (
            "A dramatic black and white photograph of a lone surfer riding inside the barrel of an enormous wave. "
            "The wave is captured at the moment of maximum curl, with the surfer crouched low and focused. "
            "Within the texture of the water — in the foam, the spray, the glass-smooth face of the wave — "
            "there are subtle visual echoes of data patterns: faint grid lines in the water's surface, "
            "node-and-edge patterns in the foam, flowing curves that suggest both hydrodynamics and neural network diagrams. "
            "These data elements should be VERY subtle — visible only on close inspection, integrated into the water's natural texture, "
            "not overlaid as a separate graphic layer. The primary read should be: powerful surf photograph. "
            "The secondary read, on closer look: the water is also information. "
            "Shot in the style of Clark Little or Aaron Chang — crisp, high-contrast, with deep blacks in the barrel "
            "and brilliant whites in the spray. The surfer should be small relative to the wave, emphasizing the scale. "
            "Landscape orientation, filling the entire frame edge to edge. No borders."
        ),
        "aspect_ratio": "16:9",
        "issue": "Original had digital overlay too obvious/pasted-on; portrait when should be landscape",
    },

    "spread_081": {
        "prompt": (
            "A clean, flat, black and white illustration divided into two halves. "
            "Left half: a grid of 12 human head-and-shoulders portraits arranged in 4 rows of 3, "
            "each drawn in simple line art with minimal detail. Each figure has a small number above their head (1 through 12). "
            "The figures are nearly identical but with tiny variations — slightly different hairlines, "
            "jaw shapes, or ear positions — like outputs from a generative model with slightly different random seeds. "
            "The style is clinical and diagrammatic, like figures in a psychology textbook. "
            "Right half: a large circle containing an abstract network visualization — "
            "glowing nodes connected by thin lines against a solid black background, suggesting a computational system. "
            "Below the circle, in clean sans-serif type: a single short question. "
            "The entire image is flat digital illustration. "
            "NO perspective, NO paper texture, NO page edges, NO book binding shadows. "
            "Do not render this as if it is photographed from a physical book."
        ),
        "aspect_ratio": "16:9",
        "issue": "Original clearly rendered as photograph of an open book with visible binding",
    },

    "spread_082": {
        "prompt": (
            "A panoramic black and white line drawing showing a sequence of human figures standing in a row, "
            "like a police lineup or a series of paper dolls. There are approximately 20 figures total, "
            "stretching from left to right across the full width. "
            "On the far left, the figures are clearly human — standing straight, wearing suits, each with a number tag. "
            "Moving rightward, each successive figure is subtly different from its neighbor: posture shifts slightly, "
            "clothing details blur, proportions stretch or compress. By the center, the figures are in mid-transformation — "
            "outlines becoming fluid, a sleeve dissolving into abstract marks, a face losing definition. "
            "On the far right, the figures have become abstract shapes that merely suggest human form — "
            "like a morphological gradient from representation to abstraction. "
            "The drawing style is clean pen-and-ink throughout, with the line work itself becoming progressively looser "
            "and more gestural from left to right. Think of a scientific morphological series. "
            "The tone should feel generative and transformative — metamorphosis, not horror. "
            "Flat composition on white background. No page edges. No book elements."
        ),
        "aspect_ratio": "16:9",
        "issue": "Original completely misinterpreted the concept as human-to-animal transformation",
    },
}


def generate_image(client, prompt, spread_id, option_idx, model=IMAGE_MODEL, aspect_ratio="16:9"):
    """Generate a single image and save as grayscale JPEG."""
    from google.genai import types

    V2_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{spread_id}_v2_opt_{option_idx}.jpg"
    out_path = V2_DIR / filename

    try:
        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size="1K",
            ),
            http_options=types.HttpOptions(timeout=REQUEST_TIMEOUT * 1000),
        )

        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=config,
        )

        if not response.parts:
            print(f"    WARNING: Empty response for {spread_id} opt {option_idx}")
            return None

        for part in response.parts:
            if part.inline_data is not None:
                genai_image = part.as_image()
                raw_bytes = genai_image.image_bytes
                pil_image = Image.open(io.BytesIO(raw_bytes))
                gray = pil_image.convert("L")
                enhancer = ImageEnhance.Contrast(gray)
                gray = enhancer.enhance(1.15)
                gray.save(str(out_path), "JPEG", quality=88)
                print(f"    opt_{option_idx}: {filename} ({out_path.stat().st_size/1024:.1f} KB)")
                return out_path

        print(f"    WARNING: No image in response for {spread_id} opt {option_idx}")
        for part in response.parts:
            if hasattr(part, "text") and part.text:
                print(f"    Response text: {part.text[:200]}")
        return None

    except Exception as e:
        error_str = str(e)
        retryable = ["503", "429", "500", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "timeout", "Timeout", "timed out"]
        if model == IMAGE_MODEL and any(code in error_str for code in retryable):
            print(f"    [{model}] Error: {error_str[:80]} — trying fallback...")
            time.sleep(5)
            return generate_image(client, prompt, spread_id, option_idx,
                                  model=IMAGE_MODEL_FALLBACK, aspect_ratio=aspect_ratio)
        print(f"    ERROR: {error_str[:120]}")
        return None


def main():
    print("=" * 60)
    print("  REGENERATION v2 — Improved prompts for problem spreads")
    print("=" * 60)

    V2_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\nTarget spreads: {len(IMPROVED_PROMPTS)}")
    for sid, data in IMPROVED_PROMPTS.items():
        print(f"  {sid}: {data['issue']}")

    print("\nConnecting to Gemini API...")
    client = get_client()
    print(f"  Model: {IMAGE_MODEL}")

    results = {}
    num_options = 2

    for sid, data in IMPROVED_PROMPTS.items():
        prompt = data["prompt"]
        aspect = data.get("aspect_ratio", "16:9")

        print(f"\n{'-'*50}")
        print(f"  {sid} [{aspect}]")
        print(f"  Issue: {data['issue']}")
        print(f"  Prompt: {prompt[:100]}...")

        options = []
        for i in range(num_options):
            if i > 0:
                time.sleep(CALL_INTERVAL)

            result = generate_image(client, prompt, sid, i, aspect_ratio=aspect)
            if result:
                options.append({
                    "file": result.name,
                    "size_kb": round(result.stat().st_size / 1024, 1),
                    "model": IMAGE_MODEL,
                })

        results[sid] = {
            "prompt": prompt,
            "aspect_ratio": aspect,
            "issue": data["issue"],
            "options": options,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        # Rate limiting between spreads
        time.sleep(CALL_INTERVAL)

    # Save v2 metadata
    meta_path = V2_DIR / "v2_metadata.json"
    meta_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nMetadata saved to: {meta_path}")

    # Summary
    total = sum(len(r["options"]) for r in results.values())
    print(f"\n{'='*60}")
    print(f"  SUMMARY: Generated {total} images for {len(results)} spreads")
    print(f"{'='*60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
