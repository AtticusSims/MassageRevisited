#!/usr/bin/env python
"""
generate_framework_data.py

Parses ContextDocs/framework_v3.md and outputs docs/data/framework.json.

The framework document is organized by movement, then by thinker, with
blockquotes containing direct quotations and attributions. This script
extracts thinkers, their quotes, bios, concepts, key works, and the
six convergences into structured JSON for the review interface.

Usage:
    python generate_framework_data.py

Paths (relative to this script's location in source/):
    Input:  ../../ContextDocs/framework_v3.md
    Output: ../docs/data/framework.json
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
FRAMEWORK_MD = SCRIPT_DIR / ".." / "ContextDocs" / "framework_v3.md"
OUTPUT_JSON = SCRIPT_DIR / ".." / "docs" / "data" / "framework.json"


# ---------------------------------------------------------------------------
# Movement definitions
# ---------------------------------------------------------------------------

# Map section heading text (lowered) to canonical movement IDs.
# The parser matches headings containing these substrings.
MOVEMENT_HEADING_MAP = {
    "prologue": {
        "id": "prologue",
        "title": "You -- the spiral from self outward",
        "match": "prologue",
    },
    "movement 1": {
        "id": "movement_1_environment",
        "title": "The Environment -- Computation as invisible medium",
        "match": "movement 1",
    },
    "movement 2": {
        "id": "movement_2_acceleration",
        "title": "The Acceleration -- The singularity as lived condition",
        "match": "movement 2",
    },
    "movement 3": {
        "id": "movement_3_dreamscape",
        "title": "The Dreamscape -- Past the event horizon",
        "match": "movement 3",
    },
}

# Titles and descriptions are populated from the actual document text
# during parsing, but we seed them with canonical IDs here.
MOVEMENT_SEED = {
    "prologue": {
        "title": "You -- the spiral from self outward",
        "description": "",
    },
    "movement_1_environment": {
        "title": "The Environment -- Computation as invisible medium",
        "description": "",
    },
    "movement_2_acceleration": {
        "title": "The Acceleration -- The singularity as lived condition",
        "description": "",
    },
    "movement_3_dreamscape": {
        "title": "The Dreamscape -- Past the event horizon",
        "description": "",
    },
}


# ---------------------------------------------------------------------------
# Thinker registry: maps heading names to canonical keys and full names.
# Some thinkers appear only inline (McLuhan, Crawford, Haraway in Prologue)
# or under combined headings (Crawford and Noble).
# ---------------------------------------------------------------------------

THINKER_REGISTRY = {
    # Movement 1
    "Benjamin Bratton": {
        "key": "Bratton",
        "full_name": "Benjamin Bratton",
        "field": "Philosophy of Technology, Speculative Design",
    },
    "Friedrich Kittler": {
        "key": "Kittler",
        "full_name": "Friedrich Kittler",
        "field": "Media Theory, German Studies",
    },
    "N. Katherine Hayles": {
        "key": "Hayles",
        "full_name": "N. Katherine Hayles",
        "field": "Literature, Science and Technology Studies",
    },
    "Hito Steyerl": {
        "key": "Steyerl",
        "full_name": "Hito Steyerl",
        "field": "Filmmaking, Visual Culture, Media Art",
    },
    "Yuk Hui": {
        "key": "Hui",
        "full_name": "Yuk Hui",
        "field": "Philosophy of Technology, Digital Objects",
    },
    "Donna Haraway": {
        "key": "Haraway",
        "full_name": "Donna Haraway",
        "field": "Science and Technology Studies, Feminist Theory",
    },
    "Kate Crawford": {
        "key": "Crawford",
        "full_name": "Kate Crawford",
        "field": "AI Ethics, Media Studies",
    },
    "Safiya Noble": {
        "key": "Noble",
        "full_name": "Safiya Umoja Noble",
        "field": "Information Studies, Critical Race Studies",
    },
    # Combined section -- both Crawford and Noble
    "Kate Crawford and Safiya Noble": {
        "key": "_combined_crawford_noble",
        "full_name": None,  # handled specially
    },
    # Movement 2
    "Ray Kurzweil": {
        "key": "Kurzweil",
        "full_name": "Ray Kurzweil",
        "field": "Futurism, Artificial Intelligence, Invention",
    },
    "John Vervaeke": {
        "key": "Vervaeke",
        "full_name": "John Vervaeke",
        "field": "Psychology, Cognitive Science, Philosophy",
    },
    "Jaron Lanier": {
        "key": "Lanier",
        "full_name": "Jaron Lanier",
        "field": "Computer Science, Virtual Reality, Music",
    },
    # Movement 3
    "Terence McKenna": {
        "key": "McKenna",
        "full_name": "Terence McKenna",
        "field": "Ethnobotany, Psychedelic Philosophy, Cultural Criticism",
    },
    "Erik Davis": {
        "key": "Davis",
        "full_name": "Erik Davis",
        "field": "Cultural Criticism, Techno-mysticism, Journalism",
    },
    "William Gibson": {
        "key": "Gibson",
        "full_name": "William Gibson",
        "field": "Science Fiction, Cyberpunk Literature",
    },
    "Neal Stephenson": {
        "key": "Stephenson",
        "full_name": "Neal Stephenson",
        "field": "Science Fiction, Speculative Literature",
    },
    "Joscha Bach": {
        "key": "Bach",
        "full_name": "Joscha Bach",
        "field": "Artificial Intelligence, Cognitive Science, Consciousness",
    },
    "Donald Hoffman": {
        "key": "Hoffman",
        "full_name": "Donald Hoffman",
        "field": "Cognitive Science, Perception, Consciousness",
    },
    "Karl Friston": {
        "key": "Friston",
        "full_name": "Karl Friston",
        "field": "Neuroscience, Computational Neuroscience, Free Energy Principle",
    },
    "Michael Levin": {
        "key": "Levin",
        "full_name": "Michael Levin",
        "field": "Developmental Biology, Bioelectricity, Cognitive Science",
    },
    "Stephen Wolfram": {
        "key": "Wolfram",
        "full_name": "Stephen Wolfram",
        "field": "Mathematics, Computer Science, Complex Systems",
    },
    "@janus": {
        "key": "janus",
        "full_name": "@janus (repligate)",
        "field": "AI Research, Alignment, Ontological Exploration",
    },
    # Prologue-only / inline thinkers
    "Marshall McLuhan": {
        "key": "McLuhan",
        "full_name": "Marshall McLuhan",
        "field": "Media Theory, Communication Studies",
    },
}


# ---------------------------------------------------------------------------
# Utility: strip markdown bold/italic markers
# ---------------------------------------------------------------------------

def strip_bold_italic(text: str) -> str:
    """Remove markdown ** and * wrappers from text."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    return text


def clean_quote_text(text: str) -> str:
    """Clean up a quote's text: strip outer quotes, whitespace, bold."""
    text = text.strip()
    # Remove leading/trailing curly or straight quotes
    text = re.sub(r'^[\u201c\u201d"\u2018\u2019\']+', '', text)
    text = re.sub(r'[\u201c\u201d"\u2018\u2019\']+$', '', text)
    text = text.strip()
    return text


def normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespace chars into single spaces."""
    return re.sub(r'\s+', ' ', text).strip()


# ---------------------------------------------------------------------------
# Heading-to-movement-ID resolver
# ---------------------------------------------------------------------------

def resolve_movement_id(heading_text: str) -> str | None:
    """Given a ## heading line, return the canonical movement ID or None."""
    lower = heading_text.lower()
    for key, info in MOVEMENT_HEADING_MAP.items():
        if info["match"] in lower:
            return info["id"]
    return None


# ---------------------------------------------------------------------------
# Heading-to-thinker resolver
# ---------------------------------------------------------------------------

def resolve_thinker_from_heading(heading_text: str) -> dict | None:
    """
    Given a ### heading line (after stripping ###), try to match a thinker.
    Returns the THINKER_REGISTRY entry or None.

    Headings look like:
        "Benjamin Bratton: the accidental megastructure"
        "Kate Crawford and Safiya Noble: the material and the political"
        "@janus (repligate) and machine spirituality"
        "Neal Stephenson's *The Diamond Age*: the Primer as AI meaning-maker"
    """
    # Strip markdown formatting
    clean = strip_bold_italic(heading_text).strip()

    # Try each registered name
    for name, info in THINKER_REGISTRY.items():
        if name.lower() in clean.lower():
            return info

    # Special case: heading contains "janus" or "repligate"
    if "janus" in clean.lower() or "repligate" in clean.lower():
        return THINKER_REGISTRY["@janus"]

    return None


# ---------------------------------------------------------------------------
# Quote block parser
# ---------------------------------------------------------------------------

def parse_blockquotes(lines: list[str]) -> list[dict]:
    """
    Parse blockquote lines into quote objects.

    Blockquotes are lines starting with "> ".  Consecutive blockquote lines
    form a single block.  Within a block:

    - Lines starting with > -- or > --- are attribution lines.
    - The remaining text (possibly bold) is the quote itself.
    - A quote is "featured" if wrapped in **...**  inside the blockquote.

    Returns list of dicts: {text, source, featured}
    """
    quotes = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith(">"):
            i += 1
            continue

        # Gather contiguous blockquote lines
        block_lines = []
        while i < len(lines) and lines[i].startswith(">"):
            # Strip the leading "> " or ">"
            content = re.sub(r'^>\s?', '', lines[i])
            block_lines.append(content)
            i += 1

        # Now parse this block into quote text + attribution
        quote_text_parts = []
        attribution = None
        is_featured = False

        for bline in block_lines:
            stripped = bline.strip()
            # Check for attribution line: starts with em-dash or triple-dash
            if re.match(r'^[\u2014\u2013\-]{1,3}\s', stripped):
                # This is an attribution line
                attr_text = re.sub(r'^[\u2014\u2013\-]{1,3}\s*', '', stripped)
                attribution = strip_bold_italic(attr_text).strip()
            else:
                # This is quote text
                # Check if bold (featured)
                if '**' in stripped:
                    is_featured = True
                quote_text_parts.append(stripped)

        if quote_text_parts:
            raw_text = ' '.join(quote_text_parts)
            # Strip bold markers
            raw_text = strip_bold_italic(raw_text)
            # Clean curly/straight quotes at boundaries
            raw_text = clean_quote_text(raw_text)
            raw_text = normalize_whitespace(raw_text)

            if len(raw_text) > 10:  # skip trivially short fragments
                quotes.append({
                    "text": raw_text,
                    "source": attribution or "",
                    "featured": is_featured,
                })

    return quotes


# ---------------------------------------------------------------------------
# Extract concepts from bold concept headings
# ---------------------------------------------------------------------------

def extract_concepts(lines: list[str]) -> list[str]:
    """
    Find bold concept headings like:
        **The Stack as accidental megastructure:**
        **Hemispherical Stacks -- the geopolitics of computation:**
        **The bootstrap hypothesis**

    Returns list of concept strings (cleaned).
    """
    concepts = []
    for line in lines:
        # Match lines that are primarily a bold heading (with optional colon)
        # Pattern: **text:** or **text** at start of line (possibly indented)
        m = re.match(r'^\s*\*\*(.+?)\*\*\s*:?\s*$', line)
        if m:
            concept = m.group(1).strip()
            # Skip "Key works:" which is a different pattern
            if concept.lower().startswith("key works"):
                continue
            concepts.append(concept)
            continue

        # Also match bold concept headings that appear as paragraph starters
        # e.g., "**The Earth layer -- materiality and extraction:**"
        m = re.match(r'^\*\*(.+?):?\*\*\s*$', line)
        if m:
            concept = m.group(1).strip().rstrip(':')
            if concept.lower().startswith("key works"):
                continue
            concepts.append(concept)

    return concepts


# ---------------------------------------------------------------------------
# Extract key works
# ---------------------------------------------------------------------------

def extract_key_works(lines: list[str]) -> list[str]:
    """
    Find the **Key works:** line and parse the works list.
    Works are separated by periods followed by spaces.
    """
    for line in lines:
        if line.strip().startswith("**Key works:**"):
            raw = line.strip().replace("**Key works:**", "").strip()
            raw = strip_bold_italic(raw)
            # Split on ". " but be careful about abbreviations
            # Better: split on period-space where next char is uppercase or italic
            works = re.split(r'\.\s+(?=[A-Z*"\u201c])', raw)
            works = [w.strip().rstrip('.').strip() for w in works if w.strip()]
            return works
    return []


# ---------------------------------------------------------------------------
# Extract bio paragraph
# ---------------------------------------------------------------------------

def extract_bio(lines: list[str]) -> str:
    """
    The bio is the first substantial paragraph after a ### heading.
    We skip blank lines and stop at the first blockquote, bold concept
    heading, or another heading.
    """
    bio_parts = []
    found_content = False

    for line in lines:
        stripped = line.strip()

        # Skip blank lines before content starts
        if not found_content and not stripped:
            continue

        # Stop at blockquotes
        if stripped.startswith(">"):
            break

        # Stop at bold concept headings
        if re.match(r'^\*\*[^*]+\*\*\s*:?\s*$', stripped):
            break

        # Stop at sub-headings
        if stripped.startswith("#"):
            break

        # Stop at horizontal rules
        if stripped == "---" or stripped == "***":
            break

        if stripped:
            found_content = True
            bio_parts.append(stripped)
        elif found_content:
            # Hit a blank line after content -> end of first paragraph
            break

    bio = ' '.join(bio_parts)
    bio = strip_bold_italic(bio)
    bio = normalize_whitespace(bio)
    return bio


# ---------------------------------------------------------------------------
# Extract inline quotes from prose paragraphs
# ---------------------------------------------------------------------------

def extract_inline_quotes(text: str) -> list[dict]:
    """
    Find inline quotes in prose text.  These appear as:
        "quoted text" (Source, Year)
    or:
        "quoted text" -- attribution

    We look for substantial quoted strings (>20 chars) with nearby
    attributions.
    """
    quotes = []
    # Match curly or straight quoted text
    pattern = r'[\u201c"]([^"\u201d]{20,}?)[\u201d"]'
    for m in re.finditer(pattern, text):
        quote_text = m.group(1).strip()
        # Look for attribution immediately after the closing quote
        after = text[m.end():m.end() + 200]

        # Try to find parenthetical source
        source_match = re.match(r'\s*\(([^)]+)\)', after)
        source = ""
        if source_match:
            source = source_match.group(1).strip()
        else:
            # Try em-dash attribution
            source_match = re.match(r'\s*[\u2014\u2013\-]{1,3}\s*(.+?)(?:\.|$)', after)
            if source_match:
                source = source_match.group(1).strip()

        if quote_text and len(quote_text) > 20:
            quotes.append({
                "text": clean_quote_text(quote_text),
                "source": source,
                "featured": False,
            })

    return quotes


# ---------------------------------------------------------------------------
# Parse the Prologue section for inline thinker references
# ---------------------------------------------------------------------------

def parse_prologue_inline(lines: list[str], thinkers: dict):
    """
    The Prologue mentions McLuhan, Crawford, Haraway, and Bratton inline
    rather than in their own ### sections.  Extract quotes attributed to
    McLuhan in blockquotes, and inline quotes for others.
    """
    movement = "prologue"

    # McLuhan blockquotes in the prologue
    mcluhan_quotes = parse_blockquotes(lines)
    for q in mcluhan_quotes:
        q["movement"] = movement
        source_lower = q.get("source", "").lower()
        # Determine which thinker the quote belongs to based on source
        if "mcluhan" in source_lower or "culkin" in source_lower or "massage" in source_lower:
            _ensure_thinker(thinkers, "McLuhan")
            thinkers["McLuhan"]["quotes"].append(q)
            if movement not in thinkers["McLuhan"]["movements"]:
                thinkers["McLuhan"]["movements"].append(movement)

    # Inline quotes from the Prologue paragraph mentioning Crawford, Haraway, Bratton
    full_text = '\n'.join(lines)

    # Crawford: "AI is neither artificial nor intelligent"
    if "AI is neither artificial nor intelligent" in full_text:
        _ensure_thinker(thinkers, "Crawford")
        thinkers["Crawford"]["quotes"].append({
            "text": "AI is neither artificial nor intelligent.",
            "source": "Atlas of AI (Yale University Press, 2021)",
            "featured": False,
            "movement": movement,
        })
        if movement not in thinkers["Crawford"]["movements"]:
            thinkers["Crawford"]["movements"].append(movement)

    # Haraway: "we are inside of what we make..."
    haraway_match = re.search(
        r'[\u201c"]we are inside of what we make.*?[\u201d"]',
        full_text, re.IGNORECASE
    )
    if haraway_match:
        _ensure_thinker(thinkers, "Haraway")
        thinkers["Haraway"]["quotes"].append({
            "text": "We are inside of what we make, and it's inside of us.",
            "source": "A Cyborg Manifesto, Simians, Cyborgs and Women (Routledge, 1991)",
            "featured": False,
            "movement": movement,
        })
        if movement not in thinkers["Haraway"]["movements"]:
            thinkers["Haraway"]["movements"].append(movement)

    # Bratton: "We are inside The Stack and it is inside of us"
    bratton_match = re.search(
        r'[\u201c"]We are inside The Stack.*?[\u201d"]',
        full_text
    )
    if bratton_match:
        _ensure_thinker(thinkers, "Bratton")
        thinkers["Bratton"]["quotes"].append({
            "text": "We are inside The Stack and it is inside of us.",
            "source": "The Stack (MIT Press, 2015)",
            "featured": False,
            "movement": movement,
        })
        if movement not in thinkers["Bratton"]["movements"]:
            thinkers["Bratton"]["movements"].append(movement)


def _ensure_thinker(thinkers: dict, key: str):
    """Ensure a thinker entry exists in the dict."""
    if key not in thinkers:
        reg = None
        for name, info in THINKER_REGISTRY.items():
            if info["key"] == key:
                reg = info
                break
        thinkers[key] = {
            "full_name": reg["full_name"] if reg else key,
            "field": reg.get("field", "") if reg else "",
            "bio": "",
            "key_works": [],
            "quotes": [],
            "concepts": [],
            "movements": [],
        }


# ---------------------------------------------------------------------------
# Parse the Convergences section
# ---------------------------------------------------------------------------

def parse_convergences(lines: list[str]) -> dict:
    """
    Parse the ## Convergences section.  Each convergence starts with:
        **N. Title.**  description...

    Returns dict keyed by slug.
    """
    convergences = {}

    # Combine all lines into text for easier paragraph splitting
    text = '\n'.join(lines)

    # Find numbered convergence blocks: **1. Title.** or **1. Title.**
    pattern = r'\*\*(\d+)\.\s+(.+?)\.\*\*\s*(.+?)(?=\*\*\d+\.|$)'
    matches = re.findall(pattern, text, re.DOTALL)

    if not matches:
        # Try alternate pattern: **N. Title.** without bold on period
        pattern = r'\*\*(\d+)\.\s+(.+?)\*\*\.?\s*(.+?)(?=\*\*\d+\.|$)'
        matches = re.findall(pattern, text, re.DOTALL)

    convergence_names = {
        "1": "reality_as_interface",
        "2": "intelligence_substrate_independent",
        "3": "failure_of_propositions",
        "4": "recursive_acceleration",
        "5": "return_of_the_numinous",
        "6": "accidental_megastructure",
    }

    convergence_titles = {
        "1": "Reality as Interface",
        "2": "Intelligence as Substrate-Independent",
        "3": "The Failure of Propositions",
        "4": "Recursive Acceleration",
        "5": "The Return of the Numinous",
        "6": "The Accidental Megastructure",
    }

    for num, title, body in matches:
        slug = convergence_names.get(num, f"convergence_{num}")
        display_title = convergence_titles.get(num, title.strip().rstrip('.'))

        # Clean the body text
        thesis = normalize_whitespace(strip_bold_italic(body.strip()))

        # Extract thinker names mentioned in the body
        mentioned_thinkers = _extract_mentioned_thinkers(body)

        convergences[slug] = {
            "name": display_title,
            "thesis": thesis,
            "thinkers": mentioned_thinkers,
        }

    return convergences


def _extract_mentioned_thinkers(text: str) -> list[str]:
    """Extract thinker last names mentioned in a block of text."""
    # All known last names / keys
    names_to_check = [
        "Hoffman", "Bach", "Kittler", "Gibson", "Bratton", "Levin",
        "Friston", "Wolfram", "Vervaeke", "Kurzweil", "McKenna",
        "Davis", "Crawford", "Noble", "Hayles", "Steyerl", "Hui",
        "Haraway", "Lanier", "Stephenson", "McLuhan", "janus",
    ]
    found = []
    for name in names_to_check:
        if name.lower() == "janus":
            if "@janus" in text or "Janus" in text or "janus" in text:
                found.append("janus")
        elif name in text:
            found.append(name)
    return found


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

def parse_framework(filepath: Path) -> dict:
    """
    Parse the entire framework_v3.md file and return the structured data.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    # Strip trailing newlines but keep content
    all_lines = [line.rstrip('\n') for line in all_lines]

    # -----------------------------------------------------------------------
    # Phase 1: Split into sections by ## headings
    # -----------------------------------------------------------------------

    sections = []  # list of (heading_text, line_index, lines_in_section)
    current_heading = None
    current_start = 0

    for i, line in enumerate(all_lines):
        if line.startswith("## ") and not line.startswith("### "):
            if current_heading is not None:
                sections.append((current_heading, current_start, all_lines[current_start:i]))
            current_heading = line[3:].strip()
            current_start = i + 1

    # Last section
    if current_heading is not None:
        sections.append((current_heading, current_start, all_lines[current_start:]))

    # -----------------------------------------------------------------------
    # Phase 2: Identify movement sections and special sections
    # -----------------------------------------------------------------------

    thinkers = {}  # key -> thinker data
    movements = dict(MOVEMENT_SEED)  # id -> {title, description}
    convergences = {}

    for heading, start_idx, section_lines in sections:
        heading_lower = heading.lower()

        # Skip preamble sections (Version, etc.)
        if "version" in heading_lower and "revised" in heading_lower:
            continue

        # Check for Convergences section
        if "convergence" in heading_lower:
            convergences = parse_convergences(section_lines)
            continue

        # Check for Thinker Map section (table, skip)
        if "thinker map" in heading_lower:
            continue

        # Check for Conclusion section (skip)
        if "conclusion" in heading_lower:
            continue

        # Resolve movement ID
        movement_id = resolve_movement_id(heading)
        if movement_id is None:
            continue

        # Update movement title from the actual heading
        # e.g., "Prologue: You -- the spiral from self outward"
        if ":" in heading:
            after_colon = heading.split(":", 1)[1].strip()
            title_from_heading = heading.split(":")[0].strip() + " -- " + after_colon
        else:
            title_from_heading = heading

        # Keep the seed title but update description from first paragraph
        first_para = extract_bio(section_lines)
        if first_para and len(first_para) > 20:
            movements[movement_id]["description"] = first_para

        # ---------------------------------------------------------------
        # Phase 3: Split this movement section into ### thinker sub-sections
        # ---------------------------------------------------------------

        # Special handling for Prologue (inline thinkers, no ### headings expected
        # except possibly for some)
        if movement_id == "prologue":
            parse_prologue_inline(section_lines, thinkers)
            # Ensure McLuhan is in movements
            _ensure_thinker(thinkers, "McLuhan")
            if "prologue" not in thinkers["McLuhan"]["movements"]:
                thinkers["McLuhan"]["movements"].append("prologue")
            continue

        # Find ### sub-sections
        sub_sections = []
        current_sub_heading = None
        current_sub_start = 0

        for j, sline in enumerate(section_lines):
            if sline.startswith("### "):
                if current_sub_heading is not None:
                    sub_sections.append((
                        current_sub_heading,
                        section_lines[current_sub_start:j]
                    ))
                current_sub_heading = sline[4:].strip()
                current_sub_start = j + 1

        # Last sub-section
        if current_sub_heading is not None:
            sub_sections.append((
                current_sub_heading,
                section_lines[current_sub_start:]
            ))

        # Also handle lines BEFORE the first ### (movement intro text)
        if sub_sections:
            first_sub_idx = None
            for j, sline in enumerate(section_lines):
                if sline.startswith("### "):
                    first_sub_idx = j
                    break
            if first_sub_idx and first_sub_idx > 0:
                intro_lines = section_lines[:first_sub_idx]
                intro_text = '\n'.join(intro_lines)
                # Extract any blockquotes from intro
                intro_quotes = parse_blockquotes(intro_lines)
                # These belong to the movement intro, not a specific thinker

        # ---------------------------------------------------------------
        # Phase 4: Parse each thinker sub-section
        # ---------------------------------------------------------------

        for sub_heading, sub_lines in sub_sections:
            # Skip non-thinker sub-sections
            sub_lower = sub_heading.lower()
            if "organizing principle" in sub_lower:
                # This is the movement's organizing section, not a thinker
                # But may contain Bratton references -- extract those
                org_quotes = parse_blockquotes(sub_lines)
                for q in org_quotes:
                    q["movement"] = movement_id
                continue

            if "cross-cutting" in sub_lower or "vervaeke hinge" in sub_lower:
                # Commentary sections, not individual thinkers
                # Still extract any quotes
                continue

            if "recursive loop" in sub_lower:
                # "The recursive loop closing: AI self-improvement in 2024-2026"
                # Not a thinker section, but empirical evidence section
                continue

            # Resolve thinker
            thinker_info = resolve_thinker_from_heading(sub_heading)
            if thinker_info is None:
                # Unknown sub-section, skip
                continue

            # Handle combined Crawford/Noble section
            if thinker_info["key"] == "_combined_crawford_noble":
                _parse_combined_crawford_noble(
                    sub_lines, movement_id, thinkers
                )
                continue

            thinker_key = thinker_info["key"]
            _ensure_thinker(thinkers, thinker_key)
            thinker = thinkers[thinker_key]

            # Update field from registry if not set
            if not thinker["field"] and thinker_info.get("field"):
                thinker["field"] = thinker_info["field"]

            # Extract bio (first paragraph)
            bio = extract_bio(sub_lines)
            if bio and (not thinker["bio"] or len(bio) > len(thinker["bio"])):
                thinker["bio"] = bio

            # Extract blockquote pairs
            quotes = parse_blockquotes(sub_lines)
            for q in quotes:
                q["movement"] = movement_id
            thinker["quotes"].extend(quotes)

            # Extract concepts
            concepts = extract_concepts(sub_lines)
            for c in concepts:
                if c not in thinker["concepts"]:
                    thinker["concepts"].append(c)

            # Extract key works
            works = extract_key_works(sub_lines)
            if works and not thinker["key_works"]:
                thinker["key_works"] = works

            # Track movement membership
            if movement_id not in thinker["movements"]:
                thinker["movements"].append(movement_id)

    # -----------------------------------------------------------------------
    # Phase 5: Post-processing
    # -----------------------------------------------------------------------

    # Add movement membership for thinkers mentioned in convergences
    # (they may already have it from their sections, but ensure completeness)

    # Deduplicate quotes (same text appearing twice)
    for key, t in thinkers.items():
        seen_texts = set()
        unique_quotes = []
        for q in t["quotes"]:
            normalized = normalize_whitespace(q["text"].lower()[:80])
            if normalized not in seen_texts:
                seen_texts.add(normalized)
                unique_quotes.append(q)
        t["quotes"] = unique_quotes

    # Add movement title overrides from actual headings
    _update_movement_titles(movements, sections)

    # -----------------------------------------------------------------------
    # Phase 6: Assemble output
    # -----------------------------------------------------------------------

    output = {
        "version": "1.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_file": "ContextDocs/framework_v3.md",
        "thinkers": thinkers,
        "convergences": convergences,
        "movements": movements,
    }

    return output


def _parse_combined_crawford_noble(
    lines: list[str], movement_id: str, thinkers: dict
):
    """
    Handle the combined 'Kate Crawford and Safiya Noble' section.
    Split quotes between Crawford and Noble based on attribution.
    """
    quotes = parse_blockquotes(lines)
    bio = extract_bio(lines)

    for q in quotes:
        q["movement"] = movement_id
        source = q.get("source", "").lower()

        if "noble" in source or "algorithms of oppression" in source:
            _ensure_thinker(thinkers, "Noble")
            thinkers["Noble"]["quotes"].append(q)
            if movement_id not in thinkers["Noble"]["movements"]:
                thinkers["Noble"]["movements"].append(movement_id)
        elif "crawford" in source or "atlas" in source:
            _ensure_thinker(thinkers, "Crawford")
            thinkers["Crawford"]["quotes"].append(q)
            if movement_id not in thinkers["Crawford"]["movements"]:
                thinkers["Crawford"]["movements"].append(movement_id)
        else:
            # Check quote text for attribution clues
            text_lower = q["text"].lower()
            if "algorithmic oppression" in text_lower or "human rights" in text_lower:
                _ensure_thinker(thinkers, "Noble")
                thinkers["Noble"]["quotes"].append(q)
                if movement_id not in thinkers["Noble"]["movements"]:
                    thinkers["Noble"]["movements"].append(movement_id)
            else:
                _ensure_thinker(thinkers, "Crawford")
                thinkers["Crawford"]["quotes"].append(q)
                if movement_id not in thinkers["Crawford"]["movements"]:
                    thinkers["Crawford"]["movements"].append(movement_id)

    # Bio goes to both (shortened)
    if bio:
        _ensure_thinker(thinkers, "Crawford")
        _ensure_thinker(thinkers, "Noble")
        if not thinkers["Crawford"]["bio"]:
            thinkers["Crawford"]["bio"] = bio
        if not thinkers["Noble"]["bio"]:
            thinkers["Noble"]["bio"] = bio


def _update_movement_titles(movements: dict, sections: list):
    """
    Update movement titles and descriptions from the actual ## headings
    and first paragraphs.
    """
    for heading, start_idx, section_lines in sections:
        movement_id = resolve_movement_id(heading)
        if movement_id and movement_id in movements:
            # Parse the title from the heading
            # e.g., "Prologue: You -- the spiral from self outward"
            # e.g., "Movement 1: The Environment -- Computation as invisible medium"
            clean_heading = strip_bold_italic(heading).strip()

            # Extract after the colon for subtitle
            if ": " in clean_heading:
                parts = clean_heading.split(": ", 1)
                prefix = parts[0].strip()
                subtitle = parts[1].strip()
                # Replace em-dashes with double-dashes for consistency
                subtitle = subtitle.replace('\u2014', '--').replace('\u2013', '--')
                movements[movement_id]["title"] = f"{subtitle}"
            else:
                movements[movement_id]["title"] = clean_heading


# ---------------------------------------------------------------------------
# Statistics printer
# ---------------------------------------------------------------------------

def print_stats(data: dict):
    """Print summary statistics about the parsed data."""
    thinkers = data["thinkers"]
    convergences = data["convergences"]
    movements = data["movements"]

    total_quotes = sum(len(t["quotes"]) for t in thinkers.values())
    featured_quotes = sum(
        sum(1 for q in t["quotes"] if q.get("featured"))
        for t in thinkers.values()
    )
    total_concepts = sum(len(t["concepts"]) for t in thinkers.values())

    print(f"Thinkers:      {len(thinkers)}")
    print(f"Movements:     {len(movements)}")
    print(f"Convergences:  {len(convergences)}")
    print(f"Total quotes:  {total_quotes}")
    print(f"  Featured:    {featured_quotes}")
    print(f"Total concepts:{total_concepts}")
    print()

    for key in sorted(thinkers.keys()):
        t = thinkers[key]
        n_quotes = len(t["quotes"])
        n_featured = sum(1 for q in t["quotes"] if q.get("featured"))
        mvmts = ', '.join(t["movements"]) if t["movements"] else "(none)"
        print(f"  {key:20s}  {n_quotes:2d} quotes ({n_featured} featured)  [{mvmts}]")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    # Resolve paths
    framework_path = FRAMEWORK_MD.resolve()
    output_path = OUTPUT_JSON.resolve()

    if not framework_path.exists():
        print(f"ERROR: Framework file not found: {framework_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading: {framework_path}")

    # Parse
    data = parse_framework(framework_path)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=True)

    print(f"Written: {output_path}")
    print()

    # Print statistics
    print_stats(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
