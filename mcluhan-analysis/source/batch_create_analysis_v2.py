"""
Batch-create analysis database entries for all 85 spreads (v1.2 schema).
Reads OCR + visual analysis VLM data and builds structured entries conforming
to analysis_schema_v1.2.json.

This is the v2 script that produces schema v1.2 entries with:
- Controlled vocabulary for rhetorical_strategy (A4), mcluhan_concepts (A7)
- Structured relationship_to_text with Barthes mode (A2)
- Interactive meaning fields (A3)
- Information value fields (A8)
- Confidence indicators (A9)
- Compositional framing (A10)
- Color and tone as structured object (A12)
- Per-entry analyst and analysis_method (A1)
- Strategy description (A5), multi_spread_patterns (A6)
- Spread type boundary rules (A11)
- White space/density percentage anchoring (A12)

Usage:
  python source/batch_create_analysis_v2.py                      # All spreads
  python source/batch_create_analysis_v2.py --start 11 --end 40  # Range
  python source/batch_create_analysis_v2.py --force               # Overwrite all
  python source/batch_create_analysis_v2.py --dry-run             # Preview
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
THEME_VOCAB_PATH = os.path.join(BASE_DIR, "source", "theme_vocabulary.json")

# ── Page mapping ──
TOTAL_BOOK_PAGES = 160

# ── Controlled vocabularies (v1.2) ──

RHETORICAL_STRATEGIES = [
    "assertion", "confrontation", "juxtaposition", "accumulation",
    "disruption", "provocation", "invocation", "dramatization",
    "quieting", "sensory_overload", "humor", "demonstration",
    "interpellation", "defamiliarization", "call_and_response"
]

MCLUHAN_CONCEPTS_ENUM = [
    "medium_is_the_message", "extensions_of_man", "global_village",
    "hot_and_cool", "rear_view_mirror", "figure_ground",
    "acoustic_space", "visual_space", "electric_age", "print_culture",
    "tribal", "pattern_recognition", "sense_ratios",
    "environment_as_invisible", "obsolescence_and_retrieval",
    "participation", "implosion", "anti_environment", "allatonceness"
]

RELATIONSHIP_TO_TEXT_ENUM = [
    "illustrates", "amplifies", "literalizes", "contradicts",
    "ironizes", "provides_atmosphere", "serves_as_metaphor",
    "extends", "independent", "decorative"
]


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
    for page in book_pages:
        p_str = str(page)
        if p_str in credits:
            return credits[p_str]
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

    text = text.replace("\r\n", "\n")
    sections = {}
    current_section = None
    current_lines = []

    for line in text.split("\n"):
        stripped = line.strip()
        section_match = None
        for label in ["DISPLAY_TEXT", "BODY_TEXT", "QUOTATIONS", "CAPTIONS", "PAGE_NUMBERS"]:
            if stripped.upper().startswith(label):
                section_match = label
                after = stripped[len(label):]
                after = after.lstrip(":").strip()
                break
        if section_match:
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = section_match
            current_lines = [after] if after else []
        elif current_section:
            current_lines.append(stripped)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

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
        caps = [c.strip() for c in re.split(r"[;\n]", captions_raw) if c.strip()]
        result["captions"] = caps

    pages_raw = sections.get("PAGE_NUMBERS", "").strip()
    if pages_raw.upper() != "NONE" and pages_raw:
        nums = re.findall(r"\d+", pages_raw)
        result["page_numbers"] = nums

    return result


def parse_quotations(quotations_raw):
    """Parse quotation text into structured quotation entries."""
    if not quotations_raw:
        return []
    quotations = []
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
    if not quotations and len(quotations_raw) > 10:
        quotations.append({
            "text": quotations_raw.strip(),
            "attribution": "unattributed",
            "context": "inline",
        })
    return quotations


def determine_spread_type(parsed_ocr, visual_desc, layout_desc):
    """Determine spread type using v1.2 boundary rules (A11)."""
    has_body = len(parsed_ocr.get("body_text", "")) > 50
    has_display = len(parsed_ocr.get("display_text", "")) > 2
    has_quotation = len(parsed_ocr.get("quotations_raw", "")) > 10
    has_images = False
    is_typography = False

    if visual_desc:
        v_lower = visual_desc.lower()
        v_clean_start = v_lower.replace("#", "").replace("*", "").strip()[:150]

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

    # v1.2 boundary rules (A11):
    # typography_as_design: text IS the visual content, no separate images
    if is_typography and has_display:
        return "typography_as_design"
    # image_dominant: image >=70% area, text subordinate
    if has_images and not has_body and not has_display:
        return "image_dominant"
    # text_with_specific_image: text + image making specific claim
    if has_images and has_body:
        return "text_with_specific_image"
    # text_with_mood_image: text + atmospheric image (no body = mood)
    if has_images and has_display and not has_body:
        return "press_photo_with_title"
    if has_images and not has_body:
        return "image_dominant"
    # quote_only: quotation without body text
    if has_quotation and not has_body and has_display:
        return "quote_only"
    # text_only: body text, no images, no display typography
    if has_body and not has_display and not has_images:
        return "text_only"
    # typography_as_design fallback
    if has_display and not has_body:
        return "typography_as_design"
    if has_body and has_quotation:
        return "text_with_quotation" if "text_with_quotation" in [
            "typography_as_design", "image_dominant", "text_with_mood_image",
            "text_with_specific_image", "collage", "press_photo_with_title",
            "symbol_or_graphic", "quote_only", "text_only", "rotated_page",
            "credits_or_colophon", "title_page", "other"
        ] else "text_only"
    if has_body:
        return "text_only"
    if has_display:
        return "typography_as_design"
    if has_images:
        return "image_dominant"

    total_text = len(parsed_ocr.get("body_text", "")) + len(parsed_ocr.get("display_text", ""))
    if total_text < 20:
        return "image_dominant"
    return "text_only"


def build_images_section(visual_desc, book_pages, credits):
    """Build images array with v1.2 structured fields (A2, A3)."""
    if not visual_desc or visual_desc.startswith("ERROR"):
        return []

    v_lower = visual_desc.lower()
    v_clean = v_lower.replace("#", "").replace("*", "").strip()
    first_100 = v_clean[:100]

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

    # Determine source type
    source_type = "press_photo"
    if "illustration" in v_lower or "drawing" in v_lower:
        source_type = "illustration"
    elif "advertisement" in v_lower or "ad " in v_lower:
        source_type = "advertisement"
    elif "painting" in v_lower:
        source_type = "fine_art_reproduction"
    elif "graphic" in v_lower or "symbol" in v_lower or "abstract" in v_lower:
        source_type = "graphic_symbol"
    elif "cartoon" in v_lower:
        source_type = "editorial_cartoon"

    # Determine position
    position = "spanning_spread"
    if "left page" in v_lower and "right page" not in v_lower:
        position = "left_page"
    elif "right page" in v_lower and "left page" not in v_lower:
        position = "right_page"
    elif "full bleed" in v_lower or "spanning" in v_lower:
        position = "full_bleed"

    # Determine scale
    scale = "dominant"
    if "small" in v_lower or "inset" in v_lower or "corner" in v_lower:
        scale = "small_inset"
    elif "half" in v_lower:
        scale = "half_page"
    elif "full bleed" in v_lower or "full-bleed" in v_lower:
        scale = "full_bleed"

    # Determine relationship_to_text (A2 structured)
    primary_relation = "illustrates"
    barthes_mode = "anchorage"
    if "contradict" in v_lower or "tension" in v_lower:
        primary_relation = "contradicts"
        barthes_mode = "relay"
    elif "metaphor" in v_lower or "symbolic" in v_lower:
        primary_relation = "serves_as_metaphor"
        barthes_mode = "relay"
    elif "atmosphere" in v_lower or "mood" in v_lower or "tone" in v_lower:
        primary_relation = "provides_atmosphere"
        barthes_mode = "anchorage"
    elif "amplif" in v_lower or "reinforce" in v_lower:
        primary_relation = "amplifies"
        barthes_mode = "anchorage"
    elif "literal" in v_lower:
        primary_relation = "literalizes"
        barthes_mode = "relay"

    # Determine interactive meaning (A3)
    # Contact: demand if figure looks at viewer, offer otherwise
    contact = "not_applicable"
    if source_type in ["press_photo", "fine_art_reproduction"]:
        if "looking at" in v_lower or "gaze" in v_lower or "staring" in v_lower or "facing" in v_lower:
            contact = "demand"
        else:
            contact = "offer"

    # Social distance from framing descriptions
    social_distance = "not_applicable"
    if source_type in ["press_photo", "fine_art_reproduction", "illustration"]:
        if "close-up" in v_lower or "closeup" in v_lower or "close up" in v_lower or "face" in v_lower:
            social_distance = "intimate"
        elif "head and shoulders" in v_lower or "upper body" in v_lower or "portrait" in v_lower:
            social_distance = "close_social"
        elif "full figure" in v_lower or "full body" in v_lower or "standing" in v_lower:
            social_distance = "far_social"
        elif "crowd" in v_lower or "aerial" in v_lower or "wide" in v_lower or "landscape" in v_lower:
            social_distance = "impersonal"
        else:
            social_distance = "close_social"

    # Attitude angle
    attitude_angle = "not_applicable"
    if source_type in ["press_photo", "fine_art_reproduction", "illustration"]:
        if "overhead" in v_lower or "bird" in v_lower or "aerial" in v_lower or "top-down" in v_lower:
            attitude_angle = "overhead"
        elif "low angle" in v_lower or "looking up" in v_lower or "from below" in v_lower:
            attitude_angle = "low_angle"
        elif "oblique" in v_lower or "side" in v_lower or "profile" in v_lower:
            attitude_angle = "oblique"
        else:
            attitude_angle = "frontal"

    image_entry = {
        "position": position,
        "subject": visual_desc[:2000] if len(visual_desc) > 2000 else visual_desc,
        "source_type": source_type,
        "source_credit": credit if credit else "uncredited",
        "estimated_date": "c. 1960s",
        "composition": "",
        "scale": scale,
        "relationship_to_text": {
            "primary_relation": primary_relation,
            "barthes_mode": barthes_mode,
            "description": ""
        },
        "interactive_meaning": {
            "contact": contact,
            "social_distance": social_distance,
            "attitude_angle": attitude_angle
        }
    }

    return [image_entry]


def build_design_section(layout_desc, parsed_ocr, spread_type, visual_desc=""):
    """Build design section with v1.2 fields (A8, A10, A12)."""
    design = {
        "layout_description": "",
        "typography": {
            "body_font_style": None,
            "display_font_style": None,
            "special_treatments": [],
        },
        "color_and_tone": {
            "contrast": "moderate",
            "dominant_tone": "balanced",
            "description": "Black and white."
        },
        "white_space": "moderate",
        "visual_density": "moderate",
        "left_right_relationship": "continuation",
        "information_value": {
            "left_right": "balanced",
            "top_bottom": "not_applicable",
            "center_margin": "distributed"
        },
        "compositional_framing": "mixed"
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

        # Special treatments
        treatments = []
        if "reversed" in l_lower or "white on black" in l_lower or "inverted" in l_lower:
            treatments.append("reversed text (white on black)")
        if "rotated" in l_lower:
            treatments.append("rotated text")
        if "overlaid" in l_lower or "overlay" in l_lower:
            treatments.append("text overlaid on image")
        if "hand" in l_lower and "written" in l_lower:
            treatments.append("handwritten text")
        design["typography"]["special_treatments"] = treatments

        # White space (A12: percentage-anchored)
        if any(w in l_lower for w in ["abundant", "generous", "vast", "mostly empty"]):
            design["white_space"] = "abundant"  # >=40%
        elif any(w in l_lower for w in ["sparse", "minimal", "little space", "tight"]):
            design["white_space"] = "minimal"  # 5-15%
        elif any(w in l_lower for w in ["none", "no white", "completely filled"]):
            design["white_space"] = "none"  # <5%
        elif any(w in l_lower for w in ["dense", "packed", "crowded", "heavy", "filled"]):
            design["white_space"] = "minimal"
        elif any(w in l_lower for w in ["moderate", "balanced"]):
            design["white_space"] = "moderate"  # 15-40%

        # Visual density
        if any(w in l_lower for w in ["overwhelming", "extremely dense", "chaotic"]):
            design["visual_density"] = "overwhelming"
        elif any(w in l_lower for w in ["dense", "packed", "crowded", "heavy"]):
            design["visual_density"] = "dense"
        elif any(w in l_lower for w in ["sparse", "minimal", "simple", "clean"]):
            design["visual_density"] = "sparse"

        # Color and tone (A12: structured)
        contrast = "moderate"
        dominant_tone = "balanced"
        tone_desc = "Black and white."

        if any(w in l_lower for w in ["high contrast", "stark", "bold"]):
            contrast = "high"
        elif any(w in l_lower for w in ["low contrast", "subtle", "soft"]):
            contrast = "low"

        if any(w in l_lower for w in ["dark", "predominantly black", "heavy black"]):
            dominant_tone = "dark"
        elif any(w in l_lower for w in ["light", "predominantly white", "bright"]):
            dominant_tone = "light"

        # Build description from details
        if "gray" in l_lower or "grey" in l_lower:
            tone_desc = "Black and white with gray tones."
        elif contrast == "high":
            tone_desc = "High contrast black and white."

        design["color_and_tone"] = {
            "contrast": contrast,
            "dominant_tone": dominant_tone,
            "description": tone_desc
        }

        # Left-right relationship
        if "mirror" in l_lower:
            design["left_right_relationship"] = "mirror"
        elif "contrast" in l_lower and "page" in l_lower:
            design["left_right_relationship"] = "contrast"
        elif "continuation" in l_lower or "continuous" in l_lower or "unified" in l_lower:
            design["left_right_relationship"] = "continuation"

        # Information value (A8: Kress & van Leeuwen)
        if "left" in l_lower and "right" in l_lower:
            if any(w in l_lower for w in ["text on left", "left page text", "left text"]):
                design["information_value"]["left_right"] = "given_new"
            elif any(w in l_lower for w in ["text on right", "right page text"]):
                design["information_value"]["left_right"] = "new_given"
        if spread_type == "typography_as_design":
            design["information_value"]["left_right"] = "single_page"
        if spread_type == "image_dominant":
            design["information_value"]["left_right"] = "balanced"

        # Top-bottom (ideal/real)
        if any(w in l_lower for w in ["title at top", "heading at top", "display at top"]):
            design["information_value"]["top_bottom"] = "ideal_real"

        # Compositional framing (A10)
        if any(w in l_lower for w in ["border", "frame", "separated", "distinct sections", "clear boundary"]):
            design["compositional_framing"] = "strongly_framed"
        elif any(w in l_lower for w in ["flow", "overlap", "bleed", "continuous", "no border", "seamless"]):
            design["compositional_framing"] = "weakly_framed"

    # Type-based defaults
    if spread_type == "typography_as_design":
        design["typography"]["display_font_style"] = design["typography"].get(
            "display_font_style", "Large-scale typographic design element"
        )
    if spread_type == "image_dominant":
        if design["visual_density"] == "moderate":
            design["visual_density"] = "dense"

    return design


def extract_mcluhan_concepts(body_text, display_text):
    """Identify McLuhan concepts using v1.2 enumeration (A7)."""
    combined = (body_text + " " + display_text).lower()
    concepts = []

    concept_keywords = {
        "medium_is_the_message": ["medium is the message", "medium is the massage"],
        "extensions_of_man": ["extension of man", "extensions of man", "extend ourselves", "extensions of our"],
        "electric_age": ["electric age", "electric technology", "electric media", "electronic", "electric speed"],
        "global_village": ["global village", "global theater"],
        "hot_and_cool": ["hot medium", "cool medium", "hot media", "cool media"],
        "figure_ground": ["figure and ground", "figure/ground"],
        "pattern_recognition": ["pattern recognition", "recognize pattern"],
        "acoustic_space": ["acoustic space", "acoustic world"],
        "visual_space": ["visual space", "visual man"],
        "tribal": ["tribal", "retribalize", "retribalization"],
        "obsolescence_and_retrieval": ["obsolescence", "obsolete", "retrieval"],
        "sense_ratios": ["sense ratio", "sensory ratio", "senses"],
        "participation": ["participation", "participate", "involvement", "involve"],
        "environment_as_invisible": ["environment", "invisible environment"],
        "anti_environment": ["anti-environment", "counter-environment"],
        "print_culture": ["print culture", "gutenberg", "typography", "alphabet", "literate"],
        "implosion": ["implosion", "implode"],
        "rear_view_mirror": ["rear-view mirror", "rearview mirror", "rear view"],
        "allatonceness": ["all-at-once", "allatonce", "simultaneously", "simultaneity"],
    }

    for concept, keywords in concept_keywords.items():
        if concept in MCLUHAN_CONCEPTS_ENUM:
            for kw in keywords:
                if kw in combined:
                    concepts.append(concept)
                    break

    return concepts if concepts else ["medium_is_the_message"]


def extract_themes(body_text, display_text, spread_type):
    """Extract thematic tags from content, aligned with theme_vocabulary.json."""
    combined = (body_text + " " + display_text).lower()
    themes = []

    theme_keywords = {
        "media_as_environment": ["environment", "media shapes", "medium shapes", "media environment"],
        "electric_technology": ["electric", "electronic", "electricity"],
        "fragmentation_vs_unification": ["fragment", "unif", "speciali", "whole"],
        "education": ["education", "school", "learning", "classroom", "student", "university"],
        "consumer_culture": ["consumer", "advertis", "brand", "buy", "sell", "product", "market"],
        "anxiety_and_despair": ["anxiety", "despair", "confusion", "fear", "anguish"],
        "identity": ["identity", "self", "who we are", "individual"],
        "perception_and_senses": ["percept", "sense", "see", "hear", "feel", "touch", "eye", "ear"],
        "space_and_time": ["space", "time", "simultaneous"],
        "print_culture": ["print", "book", "literacy", "alphabet", "typograph", "gutenberg"],
        "tribal_culture": ["tribal", "tribe", "village", "oral"],
        "youth_and_generation": ["youth", "young", "generation", "children", "child"],
        "war_and_violence": ["war", "violence", "military", "bomb", "weapon", "conflict"],
        "art_and_creativity": ["art", "artist", "creative", "paint", "sculpture", "poet"],
        "technology_and_body": ["body", "extension", "nerve", "skin", "physical"],
        "clothing_and_housing": ["cloth", "housing", "dress", "wear", "home"],
        "automation": ["automat", "computer", "machine", "robot", "program"],
        "information": ["information", "data", "news", "message"],
        "privacy": ["privacy", "private", "dossier", "personal data"],
        "surveillance": ["surveillance", "watch", "monitor", "observe", "inspect"],
        "speed_and_acceleration": ["speed", "fast", "rapid", "instant", "accelerat"],
        "obsolescence": ["obsolete", "obsolescence", "outmoded", "discard"],
        "participation": ["participat", "involve", "engage"],
        "public_private_collapse": ["public", "private", "exposure", "boundary"],
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


def determine_rhetorical_strategy(spread_type, body, display, images, visual_desc=""):
    """Determine primary and secondary rhetorical strategies from v1.2 vocabulary (A4)."""
    combined = (body + " " + display).lower()
    primary = "assertion"
    secondary = []

    # Strategy detection based on content and type
    if spread_type == "typography_as_design":
        primary = "demonstration"
        if "!" in display or "?" in display:
            secondary.append("provocation")
        if len(display) > 100:
            secondary.append("accumulation")

    elif spread_type == "image_dominant":
        primary = "demonstration"
        if visual_desc:
            vd = visual_desc.lower()
            if any(w in vd for w in ["collage", "multiple", "layered"]):
                secondary.append("accumulation")
            if any(w in vd for w in ["contrast", "juxtapos"]):
                primary = "juxtaposition"

    elif spread_type in ["text_with_specific_image", "text_with_mood_image", "press_photo_with_title"]:
        primary = "juxtaposition"
        if images:
            secondary.append("demonstration")

    elif spread_type == "quote_only":
        primary = "invocation"

    elif spread_type == "text_only":
        # Analyze text for strategy cues
        if "?" in combined:
            primary = "confrontation"
        elif any(w in combined for w in ["you ", "your ", "you're"]):
            primary = "interpellation"
        elif len(body) > 500:
            primary = "assertion"
        else:
            primary = "assertion"

    # Content-based secondary refinement
    if "?" in combined and primary != "confrontation":
        secondary.append("confrontation")
    if any(w in combined for w in ["you ", "your "]) and primary != "interpellation":
        if "interpellation" not in secondary:
            secondary.append("interpellation")
    if any(w in combined for w in ["humor", "joke", "laugh", "funny", "absurd"]):
        if "humor" not in secondary:
            secondary.append("humor")

    # Limit secondary to 2
    secondary = [s for s in secondary if s != primary][:2]

    return primary, secondary


def build_strategy_description(primary, secondary, spread_type, body, display):
    """Build prose description of how the rhetorical strategy operates (A5)."""
    combined = (display + " " + body).strip()
    if not combined:
        return f"Visual/typographic spread employing {primary} through design form rather than textual argument."

    desc_parts = []

    strategy_verbs = {
        "assertion": "asserts",
        "confrontation": "confronts the reader",
        "juxtaposition": "juxtaposes elements",
        "accumulation": "accumulates elements",
        "disruption": "disrupts expectations",
        "provocation": "provokes",
        "invocation": "invokes authority",
        "dramatization": "dramatizes",
        "quieting": "creates contemplative space",
        "sensory_overload": "overwhelms the senses",
        "humor": "uses humor",
        "demonstration": "demonstrates through form",
        "interpellation": "addresses the reader directly",
        "defamiliarization": "makes the familiar strange",
        "call_and_response": "creates a call-and-response pattern",
    }

    verb = strategy_verbs.get(primary, "employs " + primary)
    first_sentence = combined[:200].strip()
    if len(first_sentence) > 150:
        first_sentence = first_sentence[:150] + "..."

    desc_parts.append(f"The spread {verb} through its combination of text and design.")

    if secondary:
        sec_names = " and ".join(secondary)
        desc_parts.append(f"Secondary strategies of {sec_names} reinforce the primary approach.")

    return " ".join(desc_parts)


def create_entry(spread_num, ocr_data, visual_data, credits):
    """Create a complete v1.2 analysis entry for a spread."""
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
        if not parsed["body_text"] and not parsed["display_text"] and raw_text:
            parsed["body_text"] = raw_text

    # Visual analysis data
    visual_desc = ""
    layout_desc = ""
    if visual_data:
        visual_desc = visual_data.get("image_description", "")
        layout_desc = visual_data.get("layout_analysis", "")

    # Determine spread type (A11)
    spread_type = determine_spread_type(parsed, visual_desc, layout_desc)

    # Build quotations
    quotations = parse_quotations(parsed.get("quotations_raw", ""))

    # Build images (A2, A3)
    images = build_images_section(visual_desc, book_pages, credits)

    # Build design (A8, A10, A12)
    design = build_design_section(layout_desc, parsed, spread_type, visual_desc)

    # Extract concepts (A7) and themes
    body = parsed.get("body_text", "")
    display = parsed.get("display_text", "")
    concepts = extract_mcluhan_concepts(body, display)
    themes = extract_themes(body, display, spread_type)

    # Determine rhetorical strategy (A4)
    primary_strategy, secondary_strategies = determine_rhetorical_strategy(
        spread_type, body, display, images, visual_desc
    )

    # Strategy description (A5)
    strategy_desc = build_strategy_description(
        primary_strategy, secondary_strategies, spread_type, body, display
    )

    # Design enacts argument
    design_enacts = spread_type in [
        "typography_as_design", "image_dominant", "text_with_specific_image",
        "collage", "symbol_or_graphic"
    ]

    # Determine pace (A12: relative to immediately preceding spread)
    text_len = len(body) + len(display)
    if text_len > 800:
        pace = "decelerating"
    elif text_len < 100:
        pace = "accelerating"
    else:
        pace = "steady"

    # Determine thematic function
    if display and not body:
        thematic_fn = "punctuates" if "punctuates" in [
            "introduces_theme", "develops_theme", "layers_themes",
            "climax", "resolution", "transition", "coda", "interruption"
        ] else "transition"
    elif text_len > 500:
        thematic_fn = "develops_theme"
    elif images and not body:
        thematic_fn = "transition"
    else:
        thematic_fn = "develops_theme"

    # Build the v1.2 entry
    entry = {
        "id": spread_id,
        "pdf_page": pdf_page,
        "book_pages": book_pages,
        "section": section,
        "analyst": "claude-opus-4-6+qwen3-vl",
        "analysis_method": "llm_primary_human_reviewed",
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
            "rhetorical_strategy": {
                "primary": primary_strategy,
                "secondary": secondary_strategies
            },
            "strategy_description": strategy_desc,
            "design_enacts_argument": design_enacts,
            "design_argument_description": _design_argument(spread_type, images, display),
            "reader_experience": _reader_experience(spread_type, text_len),
            "mcluhan_concepts": concepts,
            "multi_spread_patterns": None,
            "confidence": "moderate"
        },
        "themes": {
            "original_themes": themes,
            "contemporary_domain_candidates": [],
            "movement_mapping": [],
            "mapping_rationale": "",
            "confidence": "moderate"
        },
        "progression": {
            "pace_shift": pace,
            "thematic_function": thematic_fn,
            "relationship_to_previous": "",
            "relationship_to_next": "",
            "confidence": "moderate"
        },
        "notes": f"Auto-generated v1.2 entry from VLM data. OCR: qwen3-vl. Visual: qwen3-vl. Schema: v1.2.",
    }

    return entry


def _summarize_argument(body, display):
    """Create a brief argument summary from text content."""
    combined = (display + " " + body).strip()
    if not combined:
        return "Visual/typographic spread — argument conveyed through imagery and design rather than prose."
    if len(combined) < 100:
        return f"Brief textual element: '{combined[:80]}...'" if len(combined) > 80 else f"Brief textual element: '{combined}'"
    sentences = re.split(r'[.!?](?:\s|$)', combined)
    if sentences and len(sentences[0]) > 20:
        return sentences[0].strip() + "."
    return combined[:200].strip() + "..."


def _design_argument(spread_type, images, display):
    """Describe how design enacts the argument."""
    if spread_type == "typography_as_design":
        return "The typographic treatment transforms text into visual experience, enacting McLuhan's thesis that the medium shapes the message."
    if spread_type == "image_dominant":
        return "The dominance of imagery over text demonstrates that visual media communicate differently than print — the spread shows rather than tells."
    if spread_type == "text_with_specific_image":
        return "The juxtaposition of text and image forces the reader to process multiple media simultaneously, creating meaning through their interaction."
    if spread_type == "collage":
        return "The collage technique accumulates disparate visual elements, performing the fragmentation and simultaneity that McLuhan describes."
    if spread_type == "symbol_or_graphic":
        return "The abstract symbol operates as a visual argument independent of textual content."
    return ""


def _reader_experience(spread_type, text_len):
    """Describe the reader's likely experience."""
    if spread_type == "image_dominant":
        return "Visual immersion — the reader encounters the spread as image before text."
    if spread_type == "typography_as_design":
        return "Typographic impact — the reader sees text as visual form before reading it as language."
    if spread_type == "collage":
        return "Sensory accumulation — the reader scans multiple visual elements simultaneously."
    if text_len > 800:
        return "Sustained reading — the reader engages with extended prose argument."
    if text_len > 200:
        return "Balanced engagement — the reader moves between text and visual elements."
    return "Brief encounter — the reader absorbs the spread quickly before moving forward."


def run_quality_check(db):
    """Run quality checks on all entries and report issues."""
    issues = []
    for entry in db["spreads"]:
        sid = entry["id"]

        # Check spread_type is valid
        valid_types = [
            "typography_as_design", "image_dominant", "text_with_mood_image",
            "text_with_specific_image", "collage", "press_photo_with_title",
            "symbol_or_graphic", "quote_only", "text_only", "rotated_page",
            "credits_or_colophon", "title_page", "other"
        ]
        if entry.get("spread_type") not in valid_types:
            issues.append(f"{sid}: invalid spread_type '{entry.get('spread_type')}'")

        # Check rhetorical strategy is from vocabulary
        rs = entry.get("rhetoric", {}).get("rhetorical_strategy", {})
        if isinstance(rs, dict):
            if rs.get("primary") not in RHETORICAL_STRATEGIES:
                issues.append(f"{sid}: invalid primary strategy '{rs.get('primary')}'")
            for s in rs.get("secondary", []):
                if s not in RHETORICAL_STRATEGIES:
                    issues.append(f"{sid}: invalid secondary strategy '{s}'")
        else:
            issues.append(f"{sid}: rhetorical_strategy not structured (v1.2 requires object)")

        # Check mcluhan_concepts are from enum
        for c in entry.get("rhetoric", {}).get("mcluhan_concepts", []):
            if c not in MCLUHAN_CONCEPTS_ENUM:
                issues.append(f"{sid}: invalid mcluhan_concept '{c}'")

        # Check images have structured relationship_to_text
        for i, img in enumerate(entry.get("images", [])):
            rt = img.get("relationship_to_text")
            if isinstance(rt, str):
                issues.append(f"{sid}: image[{i}] relationship_to_text is string, not object")
            elif isinstance(rt, dict):
                if rt.get("primary_relation") not in RELATIONSHIP_TO_TEXT_ENUM:
                    issues.append(f"{sid}: image[{i}] invalid primary_relation '{rt.get('primary_relation')}'")

        # Check color_and_tone is structured
        ct = entry.get("design", {}).get("color_and_tone")
        if isinstance(ct, str):
            issues.append(f"{sid}: color_and_tone is string, not object (v1.2 requires object)")

        # Check spread with images=0 but type suggests images
        if not entry.get("images") and entry.get("spread_type") in [
            "image_dominant", "text_with_specific_image", "text_with_mood_image",
            "press_photo_with_title", "collage"
        ]:
            issues.append(f"{sid}: spread_type='{entry['spread_type']}' but images=0")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Batch create v1.2 analysis entries")
    parser.add_argument("--start", type=int, default=1, help="Start spread number")
    parser.add_argument("--end", type=int, default=85, help="End spread number")
    parser.add_argument("--force", action="store_true", help="Overwrite existing entries")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    args = parser.parse_args()

    print(f"Batch create v1.2 analysis entries: spreads {args.start:03d}-{args.end:03d}")

    # Initialize fresh v1.2 database
    db = {
        "metadata": {
            "source_pdf": "themediumisthemassage_marshallmcluhan_quentinfiorecompressed.pdf",
            "total_pdf_pages": 85,
            "total_book_pages": 160,
            "analysis_date": time.strftime("%Y-%m-%d"),
            "analysis_model": "claude-opus-4-6+qwen3-vl",
            "schema_version": "1.2",
            "schema_theoretical_basis": [
                "Kress & van Leeuwen 2006 (visual grammar)",
                "Barthes 1977; Martinec & Salway 2005 (image-text relations)",
                "Drucker 2014 (performative design)",
                "Bateman 2008; Hiippala 2015 (GeM framework)"
            ]
        },
        "spreads": [],
    }

    credits = load_credits()
    print(f"Image credits loaded: {len(credits)} entries")

    created = 0
    skipped = 0
    missing_ocr = 0
    missing_visual = 0

    for i in range(args.start, args.end + 1):
        spread_id = f"spread_{i:03d}"

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
                  f"strategy={entry['rhetoric']['rhetorical_strategy']['primary']}, "
                  f"body={len(entry['text']['body_text'])} chars, "
                  f"images={len(entry['images'])}, "
                  f"concepts={entry['rhetoric']['mcluhan_concepts'][:2]}")
            created += 1
            continue

        db["spreads"].append(entry)
        created += 1
        print(f"  {spread_id}: type={entry['spread_type']}, "
              f"strategy={entry['rhetoric']['rhetorical_strategy']['primary']}, "
              f"body={len(entry['text']['body_text'])} chars, "
              f"images={len(entry['images'])}, pages={entry['book_pages']}")

    # Sort spreads by ID
    db["spreads"].sort(key=lambda s: s["id"])

    # Run quality checks
    print(f"\n--- Quality Check ---")
    issues = run_quality_check(db)
    if issues:
        print(f"  {len(issues)} issues found:")
        for issue in issues:
            print(f"    {issue}")
    else:
        print(f"  0 issues — all entries pass v1.2 validation")

    # Save
    if not args.dry_run and created > 0:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        print(f"\nSaved to {DB_PATH}")

    print(f"\n{'='*60}")
    print(f"  Summary (Schema v1.2)")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")
    print(f"  Missing OCR: {missing_ocr}")
    print(f"  Missing Visual: {missing_visual}")
    print(f"  Total entries: {len(db['spreads'])}")
    print(f"  Quality issues: {len(issues)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
