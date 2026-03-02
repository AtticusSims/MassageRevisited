"""
Batch-create analysis database entries for all spreads (011-085).
Reads OCR + visual analysis VLM data and builds structured entries.

Usage:
  python source/batch_create_analysis.py                    # All missing spreads
  python source/batch_create_analysis.py --start 11 --end 40  # Range
  python source/batch_create_analysis.py --force             # Overwrite existing entries
  python source/batch_create_analysis.py --dry-run           # Preview without saving
"""

import json
import os
import re
import sys
import argparse
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VLM_DIR = os.path.join(BASE_DIR, "output", "vlm_extractions")
DB_PATH = os.path.join(BASE_DIR, "output", "analysis_database.json")
CREDITS_PATH = os.path.join(BASE_DIR, "source", "image_credits_lookup.json")
RENDERED_DIR = os.path.join(BASE_DIR, "rendered")

# ── Page mapping ──
# Spreads 1-4: front matter (no book page numbers)
# Spread 5: book page [1]
# Spreads 6-85: book pages [(n-5)*2, (n-5)*2+1]
TOTAL_BOOK_PAGES = 160


def get_book_pages(pdf_page):
    """Map PDF page number to book page numbers."""
    if pdf_page <= 4:
        return []
    if pdf_page == 5:
        return [1]
    left = (pdf_page - 5) * 2
    right = left + 1
    if left > TOTAL_BOOK_PAGES:
        return []
    if right > TOTAL_BOOK_PAGES:
        return [left]
    return [left, right]


def get_section(pdf_page, book_pages):
    """Determine which section of the book this spread belongs to."""
    if pdf_page <= 4:
        return "front_matter"
    if not book_pages:
        return "back_matter"
    max_page = max(book_pages)
    if max_page <= 1:
        return "front_matter"
    if max_page >= 158:
        return "back_matter"
    return "body"


def load_credits():
    """Load image credits lookup."""
    try:
        data = json.load(open(CREDITS_PATH, "r", encoding="utf-8"))
        return data.get("credits", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def find_credit(book_pages, credits):
    """Find image credit for given book pages."""
    if not book_pages:
        return None

    # Try exact page matches and ranges
    for page in book_pages:
        p_str = str(page)
        if p_str in credits:
            return credits[p_str]

    # Try ranges like "15-16", "19-20"
    for key, val in credits.items():
        if "-" in key:
            parts = key.split("-")
            try:
                lo, hi = int(parts[0]), int(parts[1])
                for page in book_pages:
                    if lo <= page <= hi:
                        return val
            except ValueError:
                continue

    return None


def parse_structured_ocr(text):
    """Parse structured OCR output into component sections."""
    result = {
        "display_text": "",
        "body_text": "",
        "quotations_raw": "",
        "captions": [],
        "page_numbers": [],
    }

    if not text or text.startswith("ERROR"):
        return result

    # Normalize line endings
    text = text.replace("\r\n", "\n")

    # Extract sections using the DISPLAY_TEXT, BODY_TEXT, etc. markers
    sections = {}
    current_section = None
    current_lines = []

    for line in text.split("\n"):
        stripped = line.strip()

        # Check for section headers
        section_match = None
        for label in ["DISPLAY_TEXT", "BODY_TEXT", "QUOTATIONS", "CAPTIONS", "PAGE_NUMBERS"]:
            if stripped.upper().startswith(label):
                section_match = label
                # Get text after the label and colon
                after = stripped[len(label):]
                after = after.lstrip(":").strip()
                break

        if section_match:
            # Save previous section
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = section_match
            current_lines = [after] if after else []
        elif current_section:
            current_lines.append(stripped)

    # Save last section
    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    # Map to result
    display = sections.get("DISPLAY_TEXT", "").strip()
    if display.upper() == "NONE" or not display:
        display = ""
    result["display_text"] = display

    body = sections.get("BODY_TEXT", "").strip()
    if body.upper() == "NONE" or not body:
        body = ""
    result["body_text"] = body

    quotations = sections.get("QUOTATIONS", "").strip()
    if quotations.upper() == "NONE" or not quotations:
        quotations = ""
    result["quotations_raw"] = quotations

    captions_raw = sections.get("CAPTIONS", "").strip()
    if captions_raw.upper() != "NONE" and captions_raw:
        # Split on line breaks or semicolons
        caps = [c.strip() for c in re.split(r"[;\n]", captions_raw) if c.strip()]
        result["captions"] = caps

    pages_raw = sections.get("PAGE_NUMBERS", "").strip()
    if pages_raw.upper() != "NONE" and pages_raw:
        # Extract numbers
        nums = re.findall(r"\d+", pages_raw)
        result["page_numbers"] = nums

    return result


def parse_quotations(quotations_raw):
    """Parse quotation text into structured quotation entries."""
    if not quotations_raw:
        return []

    quotations = []
    # Try to find quoted text with attribution
    # Patterns: "quote" — Author, "quote" - Author, "quote" (Author)
    patterns = [
        r'"([^"]+)"\s*[—–-]\s*(.+?)(?:\n|$)',
        r'"([^"]+)"\s*\(([^)]+)\)',
        r'["""]([^"""]+)["""]\s*[—–-]\s*(.+?)(?:\n|$)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, quotations_raw)
        for quote_text, attribution in matches:
            quotations.append({
                "text": quote_text.strip(),
                "attribution": attribution.strip(),
                "context": "inline",
            })

    # If no structured quotations found but text exists, treat as a single block
    if not quotations and len(quotations_raw) > 10:
        quotations.append({
            "text": quotations_raw.strip(),
            "attribution": "unattributed",
            "context": "inline",
        })

    return quotations


def determine_spread_type(parsed_ocr, visual_desc, layout_desc):
    """Determine spread type from content analysis."""
    has_body = len(parsed_ocr.get("body_text", "")) > 50
    has_display = len(parsed_ocr.get("display_text", "")) > 2
    has_quotation = len(parsed_ocr.get("quotations_raw", "")) > 10
    has_images = False
    is_typography = False

    if visual_desc:
        v_lower = visual_desc.lower()
        v_clean_start = v_lower.replace("#", "").replace("*", "").strip()[:150]

        # First check if the description starts by saying there are NO images
        starts_with_no = any(phrase in v_clean_start for phrase in [
            "no images", "no photographs", "no illustrations",
            "there are no photographs", "there are no images",
            "there are no visual", "no visual elements",
            "typography only", "text-only", "text only",
            "no pictorial",
        ])

        if starts_with_no:
            has_images = False
            is_typography = True
        else:
            has_images = any(w in v_lower for w in [
                "photograph", "photo", "illustration", "image", "picture",
                "graphic", "figure", "portrait", "scene", "painting",
            ])
            is_typography = (
                any(w in v_lower for w in ["typographic", "letterforms"])
                and not has_images
            )

    # Determine type
    if is_typography and has_display:
        return "typography_as_design"
    if has_images and has_body:
        return "text_with_specific_image"
    if has_images and not has_body:
        return "image_dominant"
    if has_display and not has_body:
        return "typography_as_design"
    if has_body and has_quotation:
        return "text_with_quotation"
    if has_body:
        return "text_only"
    if has_display:
        return "typography_as_design"
    if has_images:
        return "image_dominant"

    # Default — check total text length
    total_text = len(parsed_ocr.get("body_text", "")) + len(parsed_ocr.get("display_text", ""))
    if total_text < 20:
        return "image_dominant"
    return "text_only"


def build_images_section(visual_desc, book_pages, credits):
    """Build the images array from visual description."""
    if not visual_desc or visual_desc.startswith("ERROR"):
        return []

    # Check for "no images" type responses — but only if the WHOLE description
    # is about there being no visual elements (not just "no photographs on the left page")
    v_lower = visual_desc.lower()
    # Strip markdown formatting for cleaner check
    v_clean = v_lower.replace("#", "").replace("*", "").strip()
    first_100 = v_clean[:100]
    # Only consider it "no images" if the very beginning says so
    # (the VLM sometimes says "no photographs on left page" but describes images on right)
    no_image_starts = [
        "no images", "no photographs", "no illustrations",
        "typography only", "text-only", "text only",
        "there are no photographs", "there are no images",
        "no visual elements", "no pictorial",
    ]
    is_no_images = any(first_100.startswith(phrase) or
                       first_100.startswith("this spread contains " + phrase) or
                       first_100.startswith("this page contains " + phrase)
                       for phrase in no_image_starts)
    if is_no_images:
        return []

    credit = find_credit(book_pages, credits)

    # Create a single image entry from the visual description
    # (the VLM describes all images together; splitting would require more parsing)
    image_entry = {
        "position": "spanning_spread",
        "subject": visual_desc[:2000] if len(visual_desc) > 2000 else visual_desc,
        "source_type": "photograph",
        "source_credit": credit if credit else "uncredited",
        "estimated_date": "c. 1960s",
        "composition": "",
        "scale": "full_spread",
        "relationship_to_text": "",
    }

    # Try to determine position from description
    if "left page" in v_lower and "right page" not in v_lower:
        image_entry["position"] = "left_page"
    elif "right page" in v_lower and "left page" not in v_lower:
        image_entry["position"] = "right_page"
    elif "full bleed" in v_lower or "spanning" in v_lower:
        image_entry["position"] = "full_bleed"

    # Try to determine source type
    if "illustration" in v_lower or "drawing" in v_lower:
        image_entry["source_type"] = "illustration"
    elif "advertisement" in v_lower or "ad " in v_lower:
        image_entry["source_type"] = "advertisement"
    elif "painting" in v_lower:
        image_entry["source_type"] = "painting"
    elif "graphic" in v_lower or "symbol" in v_lower:
        image_entry["source_type"] = "graphic"

    return [image_entry]


def build_design_section(layout_desc, parsed_ocr, spread_type):
    """Build the design section from layout analysis."""
    design = {
        "layout_description": "",
        "typography": {
            "body_font_style": None,
            "display_font_style": None,
            "special_treatments": [],
        },
        "color_and_tone": "Black and white.",
        "white_space": "moderate",
        "visual_density": "moderate",
        "left_right_relationship": "continuation",
    }

    if layout_desc and not layout_desc.startswith("ERROR"):
        design["layout_description"] = layout_desc[:2000] if len(layout_desc) > 2000 else layout_desc

        l_lower = layout_desc.lower()

        # Typography detection
        if "serif" in l_lower and "sans" not in l_lower:
            design["typography"]["body_font_style"] = "Serif text"
        elif "sans-serif" in l_lower or "sans serif" in l_lower:
            design["typography"]["body_font_style"] = "Sans-serif text"

        if parsed_ocr.get("display_text"):
            design["typography"]["display_font_style"] = "Large display typography"

        # White space
        if any(w in l_lower for w in ["sparse", "minimal", "empty", "breathing"]):
            design["white_space"] = "sparse"
        elif any(w in l_lower for w in ["dense", "packed", "crowded", "heavy"]):
            design["white_space"] = "dense"
        elif any(w in l_lower for w in ["moderate", "balanced"]):
            design["white_space"] = "moderate"

        # Density
        if "dense" in l_lower or "packed" in l_lower:
            design["visual_density"] = "dense"
        elif "sparse" in l_lower or "minimal" in l_lower:
            design["visual_density"] = "sparse"

        # Left-right relationship
        if "mirror" in l_lower:
            design["left_right_relationship"] = "mirror"
        elif "contrast" in l_lower:
            design["left_right_relationship"] = "contrast"
        elif "continuation" in l_lower or "continuous" in l_lower:
            design["left_right_relationship"] = "continuation"
        elif "unified" in l_lower:
            design["left_right_relationship"] = "unified"

    # Type-based defaults
    if spread_type == "typography_as_design":
        design["typography"]["display_font_style"] = design["typography"].get(
            "display_font_style", "Large-scale typographic design element"
        )
    if spread_type == "image_dominant":
        design["visual_density"] = design.get("visual_density", "dense")

    return design


def extract_mcluhan_concepts(body_text, display_text):
    """Identify McLuhan concepts mentioned in the text."""
    combined = (body_text + " " + display_text).lower()
    concepts = []

    concept_keywords = {
        "medium_is_the_message": ["medium is the message", "medium is the massage"],
        "extensions_of_man": ["extension of man", "extensions of man", "extend ourselves"],
        "electric_age": ["electric age", "electric technology", "electric media", "electronic"],
        "global_village": ["global village", "global theater"],
        "hot_and_cool_media": ["hot medium", "cool medium", "hot media", "cool media"],
        "figure_ground": ["figure and ground", "figure/ground"],
        "pattern_recognition": ["pattern recognition", "pattern"],
        "acoustic_space": ["acoustic space", "acoustic"],
        "visual_space": ["visual space", "visual man"],
        "tribal": ["tribal", "retribalize", "retribalization"],
        "obsolescence": ["obsolescence", "obsolete"],
        "sensory_ratio": ["sense ratio", "sensory", "senses"],
        "participation": ["participation", "participate", "involvement"],
        "environment": ["environment", "environments"],
        "anti_environment": ["anti-environment", "counter-environment"],
    }

    for concept, keywords in concept_keywords.items():
        for kw in keywords:
            if kw in combined:
                concepts.append(concept)
                break

    return concepts if concepts else ["media_ecology"]


def extract_themes(body_text, display_text, spread_type):
    """Extract thematic tags from content."""
    combined = (body_text + " " + display_text).lower()
    themes = []

    theme_keywords = {
        "media_as_environment": ["environment", "media shapes", "medium shapes"],
        "electric_technology": ["electric", "electronic", "electricity"],
        "fragmentation_vs_unification": ["fragment", "unif", "speciali"],
        "education": ["education", "school", "learning", "classroom", "student"],
        "consumer_culture": ["consumer", "advertis", "brand", "buy", "sell", "product"],
        "anxiety": ["anxiety", "despair", "confusion", "fear"],
        "identity": ["identity", "self", "who we are", "individual"],
        "perception": ["percept", "sense", "see", "hear", "feel", "touch"],
        "space_and_time": ["space", "time", "simultaneous"],
        "print_culture": ["print", "book", "literacy", "alphabet", "typograph"],
        "tribal_culture": ["tribal", "tribe", "village"],
        "youth_and_generation": ["youth", "young", "generation", "children"],
        "war_and_violence": ["war", "violence", "military", "bomb", "weapon"],
        "art_and_creativity": ["art", "artist", "creative", "paint", "sculpture"],
        "technology_and_body": ["body", "extension", "nerve", "skin"],
        "clothing_and_housing": ["cloth", "housing", "dress", "wear"],
        "automation": ["automat", "computer", "machine", "robot"],
        "information": ["information", "data", "news"],
    }

    for theme, keywords in theme_keywords.items():
        for kw in keywords:
            if kw in combined:
                themes.append(theme)
                break

    if not themes:
        if spread_type == "image_dominant":
            themes = ["visual_rhetoric"]
        elif spread_type == "typography_as_design":
            themes = ["typographic_expression"]
        else:
            themes = ["media_ecology"]

    return themes


def create_entry(spread_num, ocr_data, visual_data, credits):
    """Create a complete analysis entry for a spread."""
    spread_id = f"spread_{spread_num:03d}"
    pdf_page = spread_num
    book_pages = get_book_pages(pdf_page)
    section = get_section(pdf_page, book_pages)

    # Parse OCR data
    raw_text = ""
    parsed = {
        "display_text": "",
        "body_text": "",
        "quotations_raw": "",
        "captions": [],
        "page_numbers": [],
    }

    if ocr_data:
        raw_text = ocr_data.get("ocr_raw", "")
        structured_text = ocr_data.get("ocr_structured", "")
        parsed = parse_structured_ocr(structured_text)

        # If structured parsing failed, use raw text as body
        if not parsed["body_text"] and not parsed["display_text"] and raw_text:
            parsed["body_text"] = raw_text

    # Visual analysis data
    visual_desc = ""
    layout_desc = ""
    if visual_data:
        visual_desc = visual_data.get("image_description", "")
        layout_desc = visual_data.get("layout_analysis", "")

    # Determine spread type
    spread_type = determine_spread_type(parsed, visual_desc, layout_desc)

    # Build quotations
    quotations = parse_quotations(parsed.get("quotations_raw", ""))

    # Build images
    images = build_images_section(visual_desc, book_pages, credits)

    # Build design
    design = build_design_section(layout_desc, parsed, spread_type)

    # Extract concepts and themes
    body = parsed.get("body_text", "")
    display = parsed.get("display_text", "")
    concepts = extract_mcluhan_concepts(body, display)
    themes = extract_themes(body, display, spread_type)

    # Determine pace
    text_len = len(body) + len(display)
    if text_len > 800:
        pace = "decelerating"
    elif text_len < 100:
        pace = "accelerating"
    else:
        pace = "steady"

    # Determine thematic function
    if display and not body:
        thematic_fn = "punctuates"
    elif text_len > 500:
        thematic_fn = "develops_theme"
    elif images and not body:
        thematic_fn = "illustrates"
    else:
        thematic_fn = "develops_theme"

    # Build the entry
    entry = {
        "id": spread_id,
        "pdf_page": pdf_page,
        "book_pages": book_pages,
        "section": section,
        "spread_type": spread_type,
        "orientation": "landscape_spread",
        "text": {
            "body_text": parsed.get("body_text", ""),
            "display_text": parsed.get("display_text", ""),
            "captions": parsed.get("captions", []),
            "page_numbers_visible": parsed.get("page_numbers", []),
        },
        "quotations": quotations,
        "images": images,
        "design": design,
        "rhetoric": {
            "argument": _summarize_argument(body, display),
            "rhetorical_strategy": _determine_strategy(spread_type, body, display, images),
            "design_enacts_argument": spread_type in [
                "typography_as_design", "image_dominant", "text_with_specific_image"
            ],
            "design_argument_description": _design_argument(spread_type, images, display),
            "reader_experience": _reader_experience(spread_type, text_len),
            "mcluhan_concepts": concepts,
        },
        "themes": {
            "original_themes": themes,
            "contemporary_domain_candidates": [],
            "movement_mapping": [],
            "mapping_rationale": "",
        },
        "progression": {
            "pace_shift": pace,
            "thematic_function": thematic_fn,
            "relationship_to_previous": "",
            "relationship_to_next": "",
        },
        "notes": f"Auto-generated from VLM data. OCR model: qwen3-vl. Visual model: qwen3-vl.",
    }

    return entry


def _summarize_argument(body, display):
    """Create a brief argument summary from text content."""
    combined = (display + " " + body).strip()
    if not combined:
        return "Visual/typographic spread — argument conveyed through imagery and design rather than prose."
    if len(combined) < 100:
        return f"Brief textual element: '{combined[:80]}...'" if len(combined) > 80 else f"Brief textual element: '{combined}'"
    # Use first sentence or first 200 chars
    sentences = re.split(r'[.!?](?:\s|$)', combined)
    if sentences and len(sentences[0]) > 20:
        return sentences[0].strip() + "."
    return combined[:200].strip() + "..."


def _determine_strategy(spread_type, body, display, images):
    """Determine the rhetorical strategy based on content type."""
    strategies = {
        "typography_as_design": "Typographic design as rhetorical act — the visual form of the text IS the argument.",
        "image_dominant": "Visual rhetoric — the image(s) carry the argument without reliance on prose.",
        "text_with_specific_image": "Juxtaposition of text and image — the relationship between word and picture creates meaning neither carries alone.",
        "text_with_quotation": "Authority appeal through quotation — external voice reinforces or complicates the argument.",
        "text_only": "Discursive prose — the argument unfolds through sustained written exposition.",
    }
    return strategies.get(spread_type, "Mixed media — multiple rhetorical registers operate simultaneously.")


def _design_argument(spread_type, images, display):
    """Describe how design enacts the argument."""
    if spread_type == "typography_as_design":
        return "The typographic treatment transforms text into visual experience, enacting McLuhan's thesis that the medium shapes the message."
    if spread_type == "image_dominant":
        return "The dominance of imagery over text demonstrates that visual media communicate differently than print — the spread shows rather than tells."
    if spread_type == "text_with_specific_image":
        return "The juxtaposition of text and image forces the reader to process multiple media simultaneously, creating meaning through their interaction."
    return ""


def _reader_experience(spread_type, text_len):
    """Describe the reader's likely experience."""
    if spread_type == "image_dominant":
        return "Visual immersion — the reader encounters the spread as image before text."
    if spread_type == "typography_as_design":
        return "Typographic impact — the reader sees text as visual form before reading it as language."
    if text_len > 800:
        return "Sustained reading — the reader engages with extended prose argument."
    if text_len > 200:
        return "Balanced engagement — the reader moves between text and visual elements."
    return "Brief encounter — the reader absorbs the spread quickly before moving forward."


def main():
    parser = argparse.ArgumentParser(description="Batch create analysis entries")
    parser.add_argument("--start", type=int, default=11, help="Start spread number")
    parser.add_argument("--end", type=int, default=85, help="End spread number")
    parser.add_argument("--force", action="store_true", help="Overwrite existing entries")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    args = parser.parse_args()

    print(f"Batch create analysis entries: spreads {args.start:03d}-{args.end:03d}")

    # Load existing database
    if os.path.exists(DB_PATH):
        db = json.load(open(DB_PATH, "r", encoding="utf-8"))
    else:
        db = {
            "metadata": {
                "source_pdf": "themediumisthemassage_marshallmcluhan_quentinfiorecompressed.pdf",
                "total_pdf_pages": 85,
                "total_book_pages": 160,
                "analysis_date": time.strftime("%Y-%m-%d"),
                "analysis_model": "claude-opus-4-6-claude-code",
                "schema_version": "1.1",
            },
            "spreads": [],
        }

    existing_ids = {s["id"] for s in db["spreads"]}
    credits = load_credits()

    print(f"Existing entries: {len(existing_ids)}")
    print(f"Image credits loaded: {len(credits)} entries")

    created = 0
    skipped = 0
    missing_ocr = 0
    missing_visual = 0

    for i in range(args.start, args.end + 1):
        spread_id = f"spread_{i:03d}"

        if spread_id in existing_ids and not args.force:
            skipped += 1
            continue

        # Load OCR data
        ocr_path = os.path.join(VLM_DIR, f"{spread_id}_ocr_qwen3.json")
        ocr_data = None
        if os.path.exists(ocr_path):
            try:
                ocr_data = json.load(open(ocr_path, "r", encoding="utf-8"))
            except json.JSONDecodeError:
                print(f"  WARN: Invalid JSON in {ocr_path}")
        else:
            missing_ocr += 1

        # Load visual analysis data
        visual_path = os.path.join(VLM_DIR, f"{spread_id}_visual_qwen3.json")
        visual_data = None
        if os.path.exists(visual_path):
            try:
                visual_data = json.load(open(visual_path, "r", encoding="utf-8"))
            except json.JSONDecodeError:
                print(f"  WARN: Invalid JSON in {visual_path}")
        else:
            missing_visual += 1

        # Check if image exists
        img_path = os.path.join(RENDERED_DIR, f"{spread_id}.png")
        if not os.path.exists(img_path):
            print(f"  SKIP {spread_id}: no rendered image")
            skipped += 1
            continue

        # Create entry
        entry = create_entry(i, ocr_data, visual_data, credits)

        if args.dry_run:
            print(f"  DRY-RUN {spread_id}: type={entry['spread_type']}, "
                  f"body={len(entry['text']['body_text'])} chars, "
                  f"images={len(entry['images'])}, "
                  f"themes={entry['themes']['original_themes'][:3]}")
            created += 1
            continue

        # Add or replace entry
        if spread_id in existing_ids:
            for j, s in enumerate(db["spreads"]):
                if s["id"] == spread_id:
                    db["spreads"][j] = entry
                    break
        else:
            db["spreads"].append(entry)
            existing_ids.add(spread_id)

        created += 1
        print(f"  {spread_id}: type={entry['spread_type']}, "
              f"body={len(entry['text']['body_text'])} chars, "
              f"images={len(entry['images'])}, pages={entry['book_pages']}")

    # Sort spreads by ID
    db["spreads"].sort(key=lambda s: s["id"])

    # Update metadata
    db["metadata"]["analysis_date"] = time.strftime("%Y-%m-%d")

    # Save
    if not args.dry_run and created > 0:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        print(f"\nSaved to {DB_PATH}")

    print(f"\n{'='*60}")
    print(f"  Summary")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")
    print(f"  Missing OCR: {missing_ocr}")
    print(f"  Missing Visual: {missing_visual}")
    print(f"  Total entries: {len(db['spreads'])}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
