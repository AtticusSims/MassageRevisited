#!/usr/bin/env python3
"""
generate_images.py — Image generation pipeline for "The Model is the Massage"

Uses Google Nano Banana 2 (gemini-3.1-flash-image-preview) to generate images
for each spread based on the design_spec's image_direction field.

Approaches:
  - generated:       AI-generate from crafted B&W prompt
  - graphic_symbol:  AI-generate abstract/symbolic imagery
  - combination:     AI-generate composite/layered imagery
  - found:           Search Unsplash for copyright-free images (placeholder prompt logged)
  - typography_only: Skip (text IS the visual)
  - none:            Skip

All generated images are post-processed to grayscale via Pillow.
Output: docs/images/spread_NNN_opt_N.jpg + output/image_metadata.json

Usage:
  python source/generate_images.py                    # Generate all
  python source/generate_images.py --spread 7         # Single spread
  python source/generate_images.py --range 6 25       # Range of spreads
  python source/generate_images.py --approach generated  # Only generated approach
  python source/generate_images.py --dry-run           # Show prompts without calling API
  python source/generate_images.py --options 2         # Generate 2 options per spread
"""

import argparse
import io
import json
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

# Force unbuffered output so we can monitor progress
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Request timeout (seconds) — kill hanging API calls
REQUEST_TIMEOUT = 120

# ── Paths ──
BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
IMAGES_DIR = BASE_DIR / "docs" / "images"
METADATA_PATH = OUTPUT_DIR / "image_metadata.json"

# ── Gemini Setup ──

# Model for image generation (Nano Banana 2)
IMAGE_MODEL = "gemini-3.1-flash-image-preview"
# Fallback model (Nano Banana 1)
IMAGE_MODEL_FALLBACK = "gemini-2.5-flash-image"

# Rate limiting
CALLS_PER_MINUTE = 20  # conservative limit
CALL_INTERVAL = 60.0 / CALLS_PER_MINUTE  # seconds between calls


def _load_api_key():
    """Load Gemini API key from environment or .env file."""
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
    """Get configured Gemini client."""
    from google import genai
    return genai.Client(api_key=_load_api_key())


def load_authoring_output():
    """Load the authoring output JSON."""
    path = OUTPUT_DIR / "authoring_output.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_metadata():
    """Load existing image metadata or create empty."""
    if METADATA_PATH.exists():
        return json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    return {}


def save_metadata(metadata):
    """Save image metadata."""
    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ── Prompt Engineering ──

def craft_prompt(spread_id: str, image_direction: dict, design_spec: dict) -> str:
    """Craft a B&W image generation prompt from design spec data."""
    approach = image_direction.get("approach", "generated")
    subject = image_direction.get("subject", "")
    mood = image_direction.get("mood", "")
    bw_treatment = image_direction.get("bw_treatment", "")
    scale = image_direction.get("scale", "")

    # Get layout context
    layout = design_spec.get("layout", {})
    layout_type = layout.get("type", "")
    tone = design_spec.get("tone", {})
    tone_value = tone.get("overall", "") if isinstance(tone, dict) else str(tone)

    # Build the prompt
    parts = []

    # Core subject
    parts.append(f"Create a black and white photograph/image: {subject}")

    # Mood and atmosphere
    if mood:
        parts.append(f"Mood and atmosphere: {mood}")

    # B&W treatment specifics
    if bw_treatment:
        parts.append(f"Black and white treatment: {bw_treatment}")
    else:
        parts.append(
            "High-contrast black and white. Dramatic tonal range from deep blacks "
            "to bright whites. Monochrome, no color whatsoever."
        )

    # Scale/composition
    if scale:
        parts.append(f"Composition scale: {scale}")

    # Layout context for aspect ratio
    if layout_type in ("full_bleed_image", "full_bleed_typography"):
        parts.append("Landscape orientation, edge-to-edge composition suitable for a full double-page book spread.")
    elif layout_type in ("split_asymmetric", "split_symmetric"):
        parts.append("Portrait orientation, suitable for one page of a book spread.")
    elif layout_type == "image_dominant":
        parts.append("Landscape orientation, the image should dominate with minimal text space.")

    # Tone
    if tone_value == "dark":
        parts.append("Dark overall tone — predominantly deep shadows with selective highlights.")
    elif tone_value == "light":
        parts.append("Light overall tone — predominantly bright with selective dark accents.")

    # Style constraints
    parts.append(
        "Style: editorial, documentary, art photography quality. "
        "This is for a serious intellectual book in the tradition of McLuhan and Fiore's "
        "'The Medium is the Massage' (1967). The aesthetic should be bold, graphic, "
        "and conceptually rigorous. Absolutely no color — pure monochrome."
    )

    # Approach-specific additions
    if approach == "graphic_symbol":
        parts.append(
            "This should be a bold graphic symbol or icon, not a photograph. "
            "Think high-contrast graphic design: clean lines, geometric forms, "
            "stark silhouettes. Like a woodcut or linocut print."
        )
    elif approach == "combination":
        parts.append(
            "This is a composite/layered image. Multiple visual elements should "
            "be clearly present, creating a visual argument through juxtaposition."
        )

    return "\n\n".join(parts)


def craft_found_search_query(image_direction: dict) -> str:
    """Extract search keywords from a 'found' image direction for Unsplash."""
    subject = image_direction.get("subject", "")
    mood = image_direction.get("mood", "")

    # Extract key nouns/concepts from subject (first 2 sentences)
    sentences = subject.split(". ")[:2]
    query = ". ".join(sentences)

    # Add mood keywords
    if mood:
        mood_words = mood.split(",")[:2]
        query += " " + " ".join(w.strip() for w in mood_words)

    return query[:200]  # Unsplash query limit


# ── Image Generation ──

def generate_image(
    client,
    prompt: str,
    spread_id: str,
    option_idx: int,
    model: str = IMAGE_MODEL,
    aspect_ratio: str = "16:9",
) -> Path | None:
    """Generate a single image via Nano Banana 2 API and save as grayscale JPEG."""
    from google.genai import types

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{spread_id}_opt_{option_idx}.jpg"
    out_path = IMAGES_DIR / filename

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

        # Extract image from response
        image_saved = False
        if not response.parts:
            print(f"    WARNING: Empty response for {spread_id} opt {option_idx}")
            return None
        for part in response.parts:
            if part.inline_data is not None:
                # Get the genai Image object
                genai_image = part.as_image()
                # Extract raw bytes and open with PIL
                raw_bytes = genai_image.image_bytes
                pil_image = Image.open(io.BytesIO(raw_bytes))
                # Convert to grayscale
                gray = pil_image.convert("L")
                # Enhance contrast slightly
                enhancer = ImageEnhance.Contrast(gray)
                gray = enhancer.enhance(1.15)
                # Save as JPEG
                gray.save(str(out_path), "JPEG", quality=88)
                image_saved = True
                break

        if not image_saved:
            print(f"    WARNING: No image in response for {spread_id} opt {option_idx}")
            # Check if there's text explaining why
            for part in response.parts:
                if hasattr(part, "text") and part.text:
                    print(f"    Response text: {part.text[:200]}")
            return None

        return out_path

    except Exception as e:
        error_str = str(e)
        # Try fallback model on certain errors
        retryable = ["503", "429", "500", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "timeout", "Timeout", "timed out"]
        if model == IMAGE_MODEL and any(code in error_str for code in retryable):
            print(f"    [{model}] Error: {error_str[:80]} — trying fallback...")
            time.sleep(5)
            return generate_image(
                client, prompt, spread_id, option_idx,
                model=IMAGE_MODEL_FALLBACK, aspect_ratio=aspect_ratio,
            )
        elif model == IMAGE_MODEL_FALLBACK and any(code in error_str for code in retryable):
            print(f"    [{model}] Also failed: {error_str[:80]} — skipping")
            return None
        print(f"    ERROR generating {spread_id} opt {option_idx}: {error_str[:120]}")
        return None


def generate_for_spread(
    client,
    spread: dict,
    num_options: int = 2,
    dry_run: bool = False,
    metadata: dict = None,
) -> dict:
    """Generate images for a single spread. Returns metadata entry."""
    spread_id = spread["spread_id"]
    if not spread["design_specs"]:
        return None

    ds = spread["design_specs"][0]
    idir = ds.get("image_direction", {})
    approach = idir.get("approach", "")

    # Skip approaches that don't need images
    if approach in ("typography_only", "none", ""):
        return {
            "approach": approach,
            "selected": None,
            "options": [],
            "skipped": True,
            "reason": f"Approach is '{approach}' — no image needed",
        }

    # Check if already generated
    if metadata and spread_id in metadata:
        existing = metadata[spread_id]
        if not existing.get("skipped") and len(existing.get("options", [])) >= num_options:
            print(f"  {spread_id}: Already has {len(existing['options'])} options, skipping")
            return existing

    # Determine aspect ratio from layout
    layout_type = ds.get("layout", {}).get("type", "")
    if layout_type in ("full_bleed_image", "full_bleed_typography", "image_dominant", "dense_collage"):
        aspect_ratio = "16:9"  # landscape for full spreads
    elif layout_type in ("split_asymmetric", "split_symmetric", "text_dominant"):
        aspect_ratio = "3:4"  # portrait for single-page images
    else:
        aspect_ratio = "16:9"  # default landscape

    # Craft prompt
    prompt = craft_prompt(spread_id, idir, ds)

    if approach == "found":
        # For 'found' images, log the search query and generate AI alternatives
        search_query = craft_found_search_query(idir)
        if dry_run:
            print(f"  {spread_id} [found]: Would search Unsplash for: {search_query[:80]}...")
            print(f"    Also generating AI alternatives with prompt: {prompt[:80]}...")
            return {
                "approach": approach,
                "selected": None,
                "options": [],
                "search_query": search_query,
                "prompt": prompt[:500],
                "dry_run": True,
            }
        # Generate AI alternatives even for 'found' approach
        print(f"  {spread_id} [found+gen]: Generating {num_options} AI alternatives...")
    else:
        if dry_run:
            print(f"  {spread_id} [{approach}]: {prompt[:100]}...")
            return {
                "approach": approach,
                "selected": None,
                "options": [],
                "prompt": prompt[:500],
                "dry_run": True,
            }
        print(f"  {spread_id} [{approach}]: Generating {num_options} images...")

    # Generate images
    options = []
    for i in range(num_options):
        # Rate limiting
        if i > 0:
            time.sleep(CALL_INTERVAL)

        result_path = generate_image(
            client, prompt, spread_id, i,
            aspect_ratio=aspect_ratio,
        )

        if result_path:
            size_kb = result_path.stat().st_size / 1024
            options.append({
                "file": result_path.name,
                "source": "generated",
                "model": IMAGE_MODEL,
                "prompt": prompt[:500],
                "license": "synthetic",
                "size_kb": round(size_kb, 1),
            })
            print(f"    opt_{i}: {result_path.name} ({size_kb:.1f} KB)")
        else:
            print(f"    opt_{i}: FAILED")

    entry = {
        "approach": approach,
        "selected": 0 if options else None,
        "options": options,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    if approach == "found":
        entry["search_query"] = craft_found_search_query(idir)

    return entry


# ── Main Pipeline ──

def main():
    parser = argparse.ArgumentParser(description="Generate images for The Model is the Massage")
    parser.add_argument("--spread", type=int, help="Generate for a single spread number")
    parser.add_argument("--range", type=int, nargs=2, metavar=("START", "END"),
                        help="Generate for a range of spreads")
    parser.add_argument("--approach", type=str,
                        choices=["generated", "graphic_symbol", "combination", "found", "all"],
                        default="all", help="Only process spreads with this approach")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompts without calling API")
    parser.add_argument("--options", type=int, default=2,
                        help="Number of image options per spread (default: 2)")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate even if images already exist")
    args = parser.parse_args()

    # Load data
    print("Loading authoring output...")
    data = load_authoring_output()
    spreads = data["spreads"]
    print(f"  {len(spreads)} spreads loaded")

    # Load existing metadata
    metadata = load_metadata()
    if args.force:
        metadata = {}

    # Filter spreads
    if args.spread:
        spreads = [s for s in spreads if s["spread_id"] == f"spread_{args.spread:03d}"]
    elif args.range:
        start, end = args.range
        target_ids = {f"spread_{i:03d}" for i in range(start, end + 1)}
        spreads = [s for s in spreads if s["spread_id"] in target_ids]

    if args.approach and args.approach != "all":
        filtered = []
        for s in spreads:
            if s["design_specs"]:
                idir = s["design_specs"][0].get("image_direction", {})
                if idir.get("approach") == args.approach:
                    filtered.append(s)
        spreads = filtered

    # Filter to only spreads needing images
    actionable = []
    for s in spreads:
        if not s["design_specs"]:
            continue
        idir = s["design_specs"][0].get("image_direction", {})
        approach = idir.get("approach", "")
        if approach not in ("typography_only", "none", ""):
            actionable.append(s)

    print(f"\n  {len(actionable)} spreads to process")
    if not actionable:
        print("  Nothing to do!")
        return 0

    # Show approach breakdown
    approach_counts = {}
    for s in actionable:
        a = s["design_specs"][0].get("image_direction", {}).get("approach", "?")
        approach_counts[a] = approach_counts.get(a, 0) + 1
    for a, c in sorted(approach_counts.items()):
        print(f"    {a}: {c}")

    # Initialize client
    client = None
    if not args.dry_run:
        print("\nConnecting to Gemini API...")
        client = get_client()
        print(f"  Model: {IMAGE_MODEL}")

    # Process spreads
    print(f"\n{'='*50}")
    print(f"  GENERATING IMAGES ({args.options} options each)")
    print(f"{'='*50}\n")

    total_generated = 0
    total_failed = 0
    total_skipped = 0

    for i, spread in enumerate(actionable):
        sid = spread["spread_id"]

        # Rate limiting between spreads
        if i > 0 and not args.dry_run:
            time.sleep(CALL_INTERVAL)

        entry = generate_for_spread(
            client, spread,
            num_options=args.options,
            dry_run=args.dry_run,
            metadata=metadata if not args.force else None,
        )

        if entry:
            if entry.get("skipped"):
                total_skipped += 1
            elif entry.get("dry_run"):
                pass  # dry run
            else:
                generated = len(entry.get("options", []))
                total_generated += generated
                if generated < args.options:
                    total_failed += (args.options - generated)

            metadata[sid] = entry

            # Save metadata incrementally (after each spread) to avoid data loss on crash
            if not args.dry_run:
                save_metadata(metadata)

    # Final metadata save + copy to docs
    if not args.dry_run:
        save_metadata(metadata)
        print(f"\nMetadata saved to: {METADATA_PATH}")

        # Also copy to docs/data/ for web serving
        docs_meta_path = BASE_DIR / "docs" / "data" / "image_metadata.json"
        docs_meta_path.parent.mkdir(parents=True, exist_ok=True)
        docs_meta_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Copied to: {docs_meta_path}")

    # Summary
    print(f"\n{'='*50}")
    print(f"  SUMMARY")
    print(f"{'='*50}")
    print(f"  Processed: {len(actionable)} spreads")
    print(f"  Generated: {total_generated} images")
    print(f"  Failed:    {total_failed}")
    print(f"  Skipped:   {total_skipped}")

    if IMAGES_DIR.exists():
        images = list(IMAGES_DIR.glob("*.jpg"))
        total_size = sum(f.stat().st_size for f in images)
        print(f"  Total images on disk: {len(images)} ({total_size/1024/1024:.1f} MB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
