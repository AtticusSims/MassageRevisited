"""
generate_gemini_analysis.py — Phase 3: Independent Full Analysis Pass

Uses Gemini to produce complete, independent analysis of all 85 spreads
from "The Medium is the Massage," following the full methodology document.

Gemini receives:
  - System instruction: methodology + schema + samples + framework + theorist profiles
  - Per-spread: the rendered PNG image + existing OCR text + analysis prompt

Output: output/gemini_extractions/spread_NNN_analysis.json

Usage:
  python source/generate_gemini_analysis.py              # All 85 spreads
  python source/generate_gemini_analysis.py --start 50   # From spread 050
  python source/generate_gemini_analysis.py --spread 50  # Single spread
  python source/generate_gemini_analysis.py --force       # Overwrite cached
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
    load_full_analysis_context,
    load_database,
    get_spread_text,
    RENDERED_DIR,
)

# ── Prompts ──

SYSTEM_PREAMBLE = """You are an expert analyst of multimodal texts, specializing in visual rhetoric,
media theory, and book design analysis.

You are analyzing spreads (two-page openings) from "The Medium is the Massage" by Marshall
McLuhan and Quentin Fiore (1967). This is a landmark work of graphic design where visual
layout, typography, and image placement ARE the argument — not merely illustration.

Below you will find:
1. The complete ANALYSIS METHODOLOGY — follow it precisely for ALL analysis fields.
2. The ANALYSIS SCHEMA (v1.2) — your output must conform to this schema exactly.
3. GOLD-STANDARD SAMPLE ENTRIES — study these for the expected quality bar, depth, and
   format of analysis.
4. The INTELLECTUAL FRAMEWORK — use this for mapping spreads to theoretical movements,
   convergences, and thinkers.
5. THEORIST REFERENCE PROFILES — use these for accurate thematic and theoretical mapping.

CRITICAL INSTRUCTIONS:
- Produce a COMPLETE analysis covering ALL schema fields.
- For images[]: Describe what you ACTUALLY SEE in the image. Be precise about body
  parts, objects, people, scenes. Do not rely on the text fields provided — look at
  the image yourself.
- For design{}: Analyze layout, typography, color/tone as visual design elements.
- For rhetoric{}: Identify the argument being made, the rhetorical strategy, how
  design enacts the argument, and relevant McLuhan concepts.
- For themes{}: Map to intellectual themes using the framework document. Identify
  both original 1967 themes and contemporary domain relevance.
- For progression{}: Consider pace, thematic function, and relationship to the
  book's overall sequence.
- Use precise terminology from the methodology document.
- Be specific, not vague. Quality over breadth.
"""

SPREAD_PROMPT_TEMPLATE = """Analyze spread_{num:03d} (PDF page {num}) from "The Medium is the Massage."

Here is the transcribed text from this spread (use this for text fields, but
LOOK AT THE IMAGE for visual analysis — do not assume the text tells you what's
in the images):

BODY TEXT:
{body_text}

DISPLAY TEXT:
{display_text}

QUOTATIONS:
{quotations}

CAPTIONS:
{captions}

Using the methodology document, schema, and gold-standard examples provided,
produce a COMPLETE analysis entry for this spread covering ALL fields:

1. "images": Array of image entries — describe what you SEE (not what was previously
   recorded). Be precise about subjects, composition, interactive meaning.

2. "design": Full design analysis — layout, typography, color/tone, white space,
   visual density, left-right relationship, information value, compositional framing.

3. "rhetoric": {{
     "argument": The specific argument this spread advances,
     "rhetorical_strategy": Classification from methodology,
     "design_enacts_argument": Whether/how visual design performs the argument,
     "design_argument_description": HOW design embodies the argument,
     "mcluhan_concepts": Array of relevant McLuhan concepts,
     "mcluhan_concept_connections": How the concepts connect to this spread
   }}

4. "themes": {{
     "original_themes": Array of themes from the 1967 context,
     "contemporary_domains": Array of modern domains this maps to,
     "framework_movement": Which movement from the intellectual framework,
     "key_thinkers": Array of relevant thinkers from the framework
   }}

5. "progression": {{
     "pace": "pause" / "development" / "intensification" / "resolution" / "transition",
     "thematic_function": How this spread functions in the book's argument sequence,
     "sequence_notes": Relationship to surrounding spreads
   }}

6. "spread_description": 2-3 sentence overall description.

7. "confidence": {{
     "images": 0.0-1.0,
     "design": 0.0-1.0,
     "rhetoric": 0.0-1.0,
     "themes": 0.0-1.0,
     "progression": 0.0-1.0
   }}

Output ONLY valid JSON. No markdown wrapping."""


def process_spread(spread_num: int, system_context: str, db: dict, force: bool = False) -> dict | None:
    """Process a single spread through Gemini full analysis."""
    # Check cache
    if not force:
        cached = get_cached_result(spread_num, "analysis")
        if cached:
            print(f"  [cached] spread_{spread_num:03d} -- skipping")
            return cached

    # Check image exists
    img_path = get_spread_image_path(spread_num)
    if not Path(img_path).exists():
        print(f"  [skip] spread_{spread_num:03d} -- image not found")
        return None

    # Get text from database
    text = get_spread_text(db, spread_num)

    # Build prompt with text fields
    quotation_text = "\n".join(
        f"  - \"{q.get('text', '')}\" -- {q.get('attribution', 'unattributed')}"
        for q in text.get("quotations", [])
    ) or "(none)"

    caption_text = "\n".join(
        f"  - {c}" for c in text.get("captions", [])
    ) or "(none)"

    prompt = SPREAD_PROMPT_TEMPLATE.format(
        num=spread_num,
        body_text=text.get("body_text", "(none)") or "(none)",
        display_text=text.get("display_text", "(none)") or "(none)",
        quotations=quotation_text,
        captions=caption_text,
    )

    # Call Gemini
    print(f"  [analysis] spread_{spread_num:03d}...", end="", flush=True)
    t0 = time.time()

    try:
        result = gemini_json(
            image_path=img_path,
            prompt=prompt,
            system_prompt=SYSTEM_PREAMBLE + "\n\n" + system_context,
            temperature=0.3,  # Slightly higher for analytical creativity
            max_output_tokens=16384,
        )
        elapsed = time.time() - t0
        model_used = result.pop("_model_used", "unknown")
        print(f" done ({elapsed:.1f}s) [{model_used}]")

        # Wrap with metadata
        output = {
            "spread_id": f"spread_{spread_num:03d}",
            "model": model_used,
            "phase": "independent_analysis",
            "timestamp": datetime.now().isoformat(),
            "generation_time_s": round(elapsed, 1),
            **result,
        }

        # Save
        path = save_result(spread_num, "analysis", output)
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
    parser = argparse.ArgumentParser(description="Generate Gemini independent full analysis")
    parser.add_argument("--start", type=int, default=1, help="Start from spread N")
    parser.add_argument("--end", type=int, default=85, help="End at spread N")
    parser.add_argument("--spread", type=int, help="Process a single spread")
    parser.add_argument("--force", action="store_true", help="Overwrite cached results")
    args = parser.parse_args()

    print("=" * 60)
    print("  Gemini -- Independent Full Analysis Pass")
    print("=" * 60)

    # Load context docs once
    print("\nLoading context documents...")
    system_context = load_full_analysis_context()
    print(f"  Context size: {len(system_context):,} chars (~{len(system_context)//4:,} tokens)")

    # Load database for text fields
    print("Loading analysis database...")
    db = load_database()
    print(f"  Spreads in database: {len(db.get('spreads', []))}")

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
        result = process_spread(num, system_context, db, args.force)
        if result:
            if get_cached_result(num, "analysis") and not args.force:
                cached += 1
            else:
                success += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"  Complete: {success} generated, {cached} cached, {failed} failed")
    print(f"  Output: output/gemini_extractions/spread_NNN_analysis.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
