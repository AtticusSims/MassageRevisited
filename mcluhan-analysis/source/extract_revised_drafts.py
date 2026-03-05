#!/usr/bin/env python3
"""Extract revised drafts from review markdown files into JSON for the authoring UI."""

import os
import re
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE, "output")
DOCS_DATA = os.path.join(BASE, "docs", "data")

SECTION_FILES = [
    os.path.join(OUTPUT_DIR, "review_section_1.md"),
    os.path.join(OUTPUT_DIR, "review_section_2.md"),
    os.path.join(OUTPUT_DIR, "review_section_3.md"),
]

def extract_revised_drafts(md_text: str) -> dict:
    """Parse markdown text and extract revised drafts per spread."""
    drafts = {}

    # Split into spread sections
    # Match ### Spread NNN
    spread_pattern = re.compile(r'^### Spread (\d{3})', re.MULTILINE)
    matches = list(spread_pattern.finditer(md_text))

    for i, match in enumerate(matches):
        spread_num = match.group(1)
        spread_id = f"spread_{spread_num}"

        # Get the section text (from this heading to the next heading or end)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        section = md_text[start:end]

        # Look for revised draft marker
        # Two variants: "**Revised Draft:**" and "**✎ Revised Draft:**"
        draft_match = re.search(
            r'\*\*(?:✎\s*)?Revised Draft:\*\*\s*\n',
            section
        )

        if not draft_match:
            continue

        # Extract text from after the marker to the next section boundary
        draft_start = draft_match.end()
        remaining = section[draft_start:]

        # End markers: **Also noted:**, **Notes:**, --- (horizontal rule), ## heading
        end_match = re.search(
            r'^(?:\*\*(?:Also noted|Notes):?\*\*|---\s*$|## )',
            remaining,
            re.MULTILINE
        )

        if end_match:
            draft_text = remaining[:end_match.start()]
        else:
            draft_text = remaining

        # Clean up: strip trailing whitespace/newlines
        draft_text = draft_text.strip()

        if draft_text:
            drafts[spread_id] = {"text": draft_text}

    return drafts


def main():
    all_drafts = {}

    for filepath in SECTION_FILES:
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found, skipping")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            md_text = f.read()

        section_drafts = extract_revised_drafts(md_text)
        print(f"  {os.path.basename(filepath)}: {len(section_drafts)} revised drafts")
        all_drafts.update(section_drafts)

    # Sort by spread ID
    all_drafts = dict(sorted(all_drafts.items()))

    # Write to docs/data for the web UI
    os.makedirs(DOCS_DATA, exist_ok=True)
    output_path = os.path.join(DOCS_DATA, "revised_drafts.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_drafts, f, indent=2, ensure_ascii=False)

    print(f"\nTotal: {len(all_drafts)} revised drafts extracted")
    print(f"Output: {output_path}")

    # List which spreads have drafts
    print("\nSpreads with revised drafts:")
    for sid in all_drafts:
        preview = all_drafts[sid]["text"][:60].replace("\n", " ")
        print(f"  {sid}: {preview}...")


if __name__ == "__main__":
    main()
