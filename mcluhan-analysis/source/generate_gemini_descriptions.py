"""
generate_gemini_descriptions.py — Phase 2: Visual Description Pass

Uses Gemini 3.1 Pro to produce detailed visual descriptions of all 85 spreads
from "The Medium is the Massage," following the methodology document.

Gemini receives:
  - System instruction: methodology + schema + gold-standard sample entries
  - Per-spread: the rendered PNG image + a description prompt

Output: output/gemini_extractions/spread_NNN_visual.json

Usage:
  python source/generate_gemini_descriptions.py              # All 85 spreads
  python source/generate_gemini_descriptions.py --start 50   # From spread 050
  python source/generate_gemini_descriptions.py --spread 50  # Single spread
  python source/generate_gemini_descriptions.py --force       # Overwrite cached
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gemini_tools import (
    gemini_json,
    get_spread_image_path,
    get_cached_result,
    save_result,
    load_visual_description_context,
    RENDERED_DIR,
)

# ── Prompts ──

SYSTEM_PREAMBLE = """You are an expert visual analyst specializing in multimodal book design,
visual rhetoric, and art/photography identification.

You are analyzing spreads (two-page openings) from "The Medium is the Massage" by Marshall
McLuhan and Quentin Fiore (1967). This is a landmark work of graphic design where visual
layout, typography, and image placement ARE the argument — not merely illustration.

Below you will find:
1. The complete ANALYSIS METHODOLOGY — follow it precisely for image identification,
   design analysis, and visual description. Pay special attention to the "Images" and
   "Design" sections.
2. The ANALYSIS SCHEMA (v1.2) — your output must conform to the images[] and design{}
   sections of this schema.
3. GOLD-STANDARD SAMPLE ENTRIES — study these for the expected quality bar, depth, and
   format of analysis.

CRITICAL INSTRUCTIONS:
- Be PRECISE about what you see. If it's a foot, say foot (not hand). If it's an ear,
  say ear. Identify body parts, objects, people, and scenes accurately.
- Note photographic technique: halftone printing, high-contrast B&W, motion blur, etc.
- Describe spatial relationships: what's on the left page vs right page, what spans
  the gutter, what's full-bleed vs inset.
- Estimate era/context of photographs where possible.
- For text-only spreads, describe the typography AS a visual design element.
- Use the Kress & van Leeuwen framework for interactive meaning (contact, social
  distance, attitude angle) as described in the methodology.
"""

SPREAD_PROMPT_TEMPLATE = """Analyze this spread image (spread_{num:03d}, PDF page {num}) from "The Medium is the Massage."

Produce a detailed visual analysis as a JSON object with these sections:

1. "images": An array of image entries, one per distinct visual element (photograph,
   illustration, graphic symbol). For each:
   - "position": Where on the spread (left_page, right_page, full_bleed, spanning_gutter,
     inset_left, inset_right)
   - "subject": PRECISE description of what the image depicts. Be specific about body parts,
     objects, people, scenes. Avoid vague descriptions.
   - "source_type": Classification (press_photo, art_photograph, fine_art_reproduction,
     editorial_cartoon, illustration, advertisement, technical_diagram, graphic_symbol,
     historical_document, film_still, unknown)
   - "composition": Framing, angle, contrast, key visual qualities
   - "scale": How much page area (full_bleed, dominant, half_page, quarter_page, small_inset, icon)
   - "estimated_date": Approximate era if determinable
   - "interactive_meaning": {{
       "contact": "demand" (gaze at viewer) / "offer" (no gaze) / "not_applicable",
       "social_distance": "intimate" / "close_social" / "far_social" / "impersonal" / "not_applicable",
       "attitude_angle": "frontal" / "oblique" / "overhead" / "low_angle" / "not_applicable"
     }}

2. "design": {{
   "layout_description": Prose description of spatial arrangement,
   "typography": {{
     "body_font_style": Font classification if text visible,
     "display_font_style": Display/headline typography if present,
     "special_treatments": Array of unusual typographic choices
   }},
   "color_and_tone": {{
     "contrast": "high" / "moderate" / "low",
     "dominant_tone": "dark" / "light" / "balanced",
     "description": Brief description
   }},
   "white_space": "abundant" / "moderate" / "minimal" / "none",
   "visual_density": "sparse" / "moderate" / "dense" / "overwhelming",
   "left_right_relationship": Description of how left and right pages relate,
   "information_value": {{
     "left_right": "given_new" / "new_given" / "balanced" / "single_page" / "not_applicable",
     "top_bottom": "ideal_real" / "real_ideal" / "balanced" / "not_applicable",
     "center_margin": "centered" / "marginal" / "distributed" / "not_applicable"
   }},
   "compositional_framing": "strongly_framed" / "weakly_framed" / "mixed"
   }}

3. "spread_description": A 2-3 sentence overall description of what a reader would see
   and experience encountering this spread.

Output ONLY valid JSON. No markdown wrapping."""


def process_spread(spread_num: int, system_context: str, force: bool = False) -> dict | None:
    """Process a single spread through Gemini visual description."""
    # Check cache
    if not force:
        cached = get_cached_result(spread_num, "visual")
        if cached:
            print(f"  [cached] spread_{spread_num:03d} — skipping")
            return cached

    # Check image exists
    img_path = get_spread_image_path(spread_num)
    if not Path(img_path).exists():
        print(f"  [skip] spread_{spread_num:03d} — image not found")
        return None

    # Build prompt
    prompt = SPREAD_PROMPT_TEMPLATE.format(num=spread_num)

    # Call Gemini
    print(f"  [visual] spread_{spread_num:03d}...", end="", flush=True)
    t0 = time.time()

    try:
        result = gemini_json(
            image_path=img_path,
            prompt=prompt,
            system_prompt=SYSTEM_PREAMBLE + "\n\n" + system_context,
            temperature=0.2,
        )
        elapsed = time.time() - t0
        model_used = result.pop("_model_used", "unknown")
        print(f" done ({elapsed:.1f}s) [{model_used}]")

        # Wrap with metadata
        output = {
            "spread_id": f"spread_{spread_num:03d}",
            "model": model_used,
            "timestamp": datetime.now().isoformat(),
            "generation_time_s": round(elapsed, 1),
            **result,
        }

        # Save
        path = save_result(spread_num, "visual", output)
        print(f"         saved: {Path(path).name}")
        return output

    except json.JSONDecodeError as e:
        elapsed = time.time() - t0
        print(f" JSON parse error ({elapsed:.1f}s): {e}")
        return None
    except Exception as e:
        elapsed = time.time() - t0
        print(f" error ({elapsed:.1f}s): {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate Gemini visual descriptions")
    parser.add_argument("--start", type=int, default=1, help="Start from spread N")
    parser.add_argument("--end", type=int, default=85, help="End at spread N")
    parser.add_argument("--spread", type=int, help="Process a single spread")
    parser.add_argument("--force", action="store_true", help="Overwrite cached results")
    args = parser.parse_args()

    print("=" * 60)
    print("  Gemini 3.1 Pro — Visual Description Pass")
    print("=" * 60)

    # Load context docs once
    print("\nLoading context documents...")
    system_context = load_visual_description_context()
    print(f"  Context size: {len(system_context):,} chars (~{len(system_context)//4:,} tokens)")

    # Determine spread range
    if args.spread:
        spreads = [args.spread]
    else:
        spreads = list(range(args.start, args.end + 1))

    print(f"\nProcessing {len(spreads)} spreads...")
    print("-" * 60)

    success = 0
    cached = 0
    failed = 0

    for num in spreads:
        result = process_spread(num, system_context, args.force)
        if result:
            if get_cached_result(num, "visual") and not args.force:
                cached += 1
            else:
                success += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"  Complete: {success} generated, {cached} cached, {failed} failed")
    print(f"  Output: output/gemini_extractions/spread_NNN_visual.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
