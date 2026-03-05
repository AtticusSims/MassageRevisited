#!/usr/bin/env python3
"""
Generate a comprehensive review document from authoring selections.
Outputs Markdown and PDF.
"""

import json
import os
import sys
from datetime import datetime

# Paths
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELECTIONS_PATH = os.path.join(BASE, "authoring_selections_2026-03-05_APS_Draft1.json")
AUTHORING_OUTPUT_PATH = os.path.join(BASE, "output", "authoring_output.json")
AUTHORING_OUTPUT_PATH_ALT = os.path.join(BASE, "docs", "data", "authoring_output.json")
CONTENT_PLAN_PATH = os.path.join(BASE, "output", "content_plan.json")
OUTPUT_MD = os.path.join(BASE, "output", "Draft1_Review_Report.md")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_rating_label(rating):
    labels = {1: "★ Weak", 2: "★★ Decent", 3: "★★★ Strong"}
    return labels.get(rating, f"★×{rating}")


def option_id_to_label(oid):
    return {"a": "Option A", "b": "Option B", "c": "Option C"}.get(oid, oid)


def format_text_block(opt, include_label=True):
    """Format a text option into readable markdown."""
    lines = []
    label = option_id_to_label(opt.get("option_id", "?"))
    if include_label:
        lines.append(f"**{label}**" + (f" — *{opt.get('label', '')}*" if opt.get("label") else ""))

    if opt.get("display_text"):
        lines.append(f"")
        lines.append(f"**Display:** {opt['display_text']}")

    if opt.get("body_text"):
        body = opt["body_text"]
        # Indent body text in a blockquote for readability
        body_lines = body.split("\n")
        lines.append("")
        lines.append("**Body:**")
        for bl in body_lines:
            lines.append(f"> {bl}")

    if opt.get("caption_text"):
        lines.append("")
        lines.append(f"**Caption:** *{opt['caption_text']}*")

    if opt.get("quotations_used"):
        quotes = opt["quotations_used"]
        if quotes:
            lines.append("")
            lines.append("**Quotes used:** " + "; ".join(
                [f"{q.get('thinker', '?')}: \"{q.get('text', '')[:80]}...\"" if len(q.get('text', '')) > 80
                 else f"{q.get('thinker', '?')}: \"{q.get('text', '')}\""
                 for q in quotes]
            ))

    return "\n".join(lines)


def main():
    print("Loading data...")
    selections = load_json(SELECTIONS_PATH)
    # Try both possible locations for authoring output
    if os.path.exists(AUTHORING_OUTPUT_PATH):
        authoring = load_json(AUTHORING_OUTPUT_PATH)
    else:
        authoring = load_json(AUTHORING_OUTPUT_PATH_ALT)
    content_plan = load_json(CONTENT_PLAN_PATH)

    # Build lookup: spread_id -> text_options list
    text_lookup = {}
    design_lookup = {}
    theme_lookup = {}
    for spread in authoring["spreads"]:
        sid = spread["spread_id"]
        text_lookup[sid] = spread.get("text_options", [])
        design_lookup[sid] = spread.get("design_specs", [])
        theme_lookup[sid] = spread.get("theme", "")

    # Build lookup from content_plan for movement info
    movement_lookup = {}
    plan_theme_lookup = {}
    for page in content_plan["pages"]:
        sid = page["spread_id"]
        movement_lookup[sid] = page.get("movement", "")
        cp = page.get("contemporary_plan", {})
        plan_theme_lookup[sid] = cp.get("theme", "")

    sel = selections["selections"]
    sorted_spreads = sorted(sel.keys(), key=lambda x: int(x.split("_")[1]))

    # Statistics
    total_reviewed = len(sorted_spreads)
    ratings_all = []
    spreads_needing_revision = []
    spreads_needing_new_images = []
    spreads_needing_rethink = []

    for sid in sorted_spreads:
        review = sel[sid]
        notes = review.get("reviewer_notes")
        if notes:
            lower_notes = notes.lower()
            if any(w in lower_notes for w in ["combine", "revise", "revision", "merge", "rethink", "redo", "rewrite", "reconsidered", "improving", "integrate"]):
                spreads_needing_revision.append(sid)
            if any(w in lower_notes for w in ["new image", "replace image", "found image", "terrible image", "redo image", "need image", "not happy with", "garbage", "rethink image"]):
                spreads_needing_new_images.append(sid)
            if any(w in lower_notes for w in ["rethink", "reconsider", "redo", "reconsidered", "redone"]):
                spreads_needing_rethink.append(sid)
        qr = review.get("quality_ratings", {})
        if qr:
            for k, v in qr.items():
                ratings_all.append(v)

    avg_rating = sum(ratings_all) / len(ratings_all) if ratings_all else 0

    # Build the document
    lines = []
    lines.append("# The Model is the Massage — Draft 1 Review Report")
    lines.append("")
    lines.append(f"**Reviewer:** APS  ")
    lines.append(f"**Date:** {datetime.now().strftime('%B %d, %Y')}  ")
    lines.append(f"**Source:** `authoring_selections_2026-03-05_APS_Draft1.json`  ")
    lines.append(f"**Spreads reviewed:** {total_reviewed} of 85")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"- **Total spreads reviewed:** {total_reviewed}")
    lines.append(f"- **Average quality rating:** {avg_rating:.1f} / 3.0")
    lines.append(f"- **Spreads rated 3 (strong):** {sum(1 for r in ratings_all if r == 3)} ratings across all options")
    lines.append(f"- **Spreads rated 2 (decent):** {sum(1 for r in ratings_all if r == 2)} ratings across all options")
    lines.append(f"- **Spreads rated 1 (weak):** {sum(1 for r in ratings_all if r == 1)} ratings across all options")
    lines.append(f"- **Spreads needing text revision:** {len(spreads_needing_revision)}")
    lines.append(f"- **Spreads needing new images:** {len(spreads_needing_new_images)}")
    lines.append(f"- **Spreads needing fundamental rethink:** {len(spreads_needing_rethink)}")
    lines.append("")

    # Quick reference tables
    lines.append("### Spreads Requiring Text Revision")
    lines.append("")
    if spreads_needing_revision:
        lines.append("| Spread | Selected | Action |")
        lines.append("|--------|----------|--------|")
        for sid in spreads_needing_revision:
            review = sel[sid]
            selected = review.get("selected_text", "—")
            notes = review.get("reviewer_notes", "")
            # Extract key action
            action = ""
            ln = notes.lower()
            if "combine" in ln:
                action = "Combine options"
            elif "rethink" in ln or "reconsider" in ln or "redone" in ln:
                action = "Rethink spread"
            elif "revise" in ln or "revision" in ln:
                action = "Revise text"
            elif "integrate" in ln or "merge" in ln:
                action = "Merge elements"
            elif "redo" in ln or "rewrite" in ln:
                action = "Rewrite"
            lines.append(f"| {sid} | {selected or '—'} | {action} |")
    else:
        lines.append("*None identified.*")
    lines.append("")

    lines.append("### Spreads Requiring New Images")
    lines.append("")
    if spreads_needing_new_images:
        lines.append("| Spread | Note |")
        lines.append("|--------|------|")
        for sid in spreads_needing_new_images:
            notes = sel[sid].get("reviewer_notes", "")
            # Extract image-related note
            img_note = ""
            for sentence in notes.replace("\n", " ").split("."):
                sl = sentence.lower().strip()
                if any(w in sl for w in ["image", "photo", "graphic", "depict"]):
                    img_note = sentence.strip()[:100]
                    break
            lines.append(f"| {sid} | {img_note}{'...' if len(img_note) >= 100 else ''} |")
    else:
        lines.append("*None identified.*")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Spread-by-Spread Review")
    lines.append("")

    # Current movement tracker
    current_movement = ""

    for sid in sorted_spreads:
        review = sel[sid]
        spread_num = int(sid.split("_")[1])

        # Movement header
        movement = movement_lookup.get(sid, "")
        if movement and movement != current_movement:
            current_movement = movement
            movement_labels = {
                "prologue": "Prologue (Spreads 001–010)",
                "movement_1_environment": "Movement 1 — The Environment (Spreads 011–035)",
                "movement_2_acceleration": "Movement 2 — Acceleration (Spreads 036–060)",
                "hinge": "The Hinge (Spreads 061–065)",
                "movement_3_dreamscape": "Movement 3 — The Dreamscape (Spreads 066–085)",
            }
            lines.append(f"## {movement_labels.get(movement, movement)}")
            lines.append("")
            lines.append("---")
            lines.append("")

        # Spread header
        theme = plan_theme_lookup.get(sid, theme_lookup.get(sid, ""))
        lines.append(f"### {sid.replace('_', ' ').title()}")
        if theme:
            lines.append(f"**Theme:** {theme}")
        lines.append("")

        # Selected text and image
        selected_text = review.get("selected_text")
        selected_image = review.get("selected_image")
        selected_design = review.get("selected_design")

        sel_parts = []
        if selected_text:
            sel_parts.append(f"Text: **{selected_text.upper()}**")
        else:
            sel_parts.append("Text: **none selected**")
        if selected_image is not None:
            sel_parts.append(f"Image: **Option {selected_image}**")
        if selected_design is not None:
            sel_parts.append(f"Design: **{selected_design}**")
        lines.append("**Selection:** " + " · ".join(sel_parts))
        lines.append("")

        # Quality ratings
        qr = review.get("quality_ratings")
        if qr:
            rating_strs = []
            for opt_id in sorted(qr.keys()):
                rating = qr[opt_id]
                rating_strs.append(f"{opt_id.upper()}: {get_rating_label(rating)}")
            lines.append("**Quality Ratings:** " + " | ".join(rating_strs))
            lines.append("")

        # Text options rated 2+
        text_options = text_lookup.get(sid, [])
        rated_options = []
        if qr:
            for opt in text_options:
                oid = opt.get("option_id", "")
                r = qr.get(oid, 0)
                if r >= 2:
                    rated_options.append((opt, r))
        else:
            # If no ratings, include the selected option
            for opt in text_options:
                if opt.get("option_id") == selected_text:
                    rated_options.append((opt, None))

        if rated_options:
            lines.append("#### Text Options Rated ★★ or Higher")
            lines.append("")
            for opt, rating in rated_options:
                oid = opt.get("option_id", "?")
                rating_str = f" ({get_rating_label(rating)})" if rating else ""
                selected_marker = " ✅ SELECTED" if oid == selected_text else ""
                lines.append(f"##### {option_id_to_label(oid)}{rating_str}{selected_marker}")
                lines.append("")
                lines.append(format_text_block(opt, include_label=False))
                lines.append("")
        elif selected_text:
            # Show the selected option even without ratings
            for opt in text_options:
                if opt.get("option_id") == selected_text:
                    lines.append("#### Selected Text")
                    lines.append("")
                    lines.append(f"##### {option_id_to_label(selected_text)} ✅ SELECTED")
                    lines.append("")
                    lines.append(format_text_block(opt, include_label=False))
                    lines.append("")
                    break

        # Reviewer notes
        notes = review.get("reviewer_notes")
        if notes:
            lines.append("#### Reviewer Notes")
            lines.append("")
            for note_line in notes.split("\n"):
                lines.append(f"> {note_line}")
            lines.append("")

            # Actionable suggestions section
            lower_notes = notes.lower()
            has_actionable = any(w in lower_notes for w in [
                "combine", "revise", "merge", "integrate", "rethink",
                "redo", "replace", "should", "need", "fix", "improve",
                "perhaps", "rewrite", "reconsidered", "different"
            ])

            if has_actionable:
                lines.append("#### Suggested Actions")
                lines.append("")
                actions = analyze_notes_for_actions(notes, review, text_options, sid)
                for action in actions:
                    lines.append(f"- {action}")
                lines.append("")

        lines.append("---")
        lines.append("")

    # Write markdown
    md_content = "\n".join(lines)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Markdown written to: {OUTPUT_MD}")
    print(f"Total lines: {len(lines)}")
    return OUTPUT_MD


def analyze_notes_for_actions(notes, review, text_options, sid):
    """Parse reviewer notes and generate actionable suggestions."""
    actions = []
    lower = notes.lower()
    selected = review.get("selected_text", "")

    # Combination suggestions
    if "combine" in lower or "merge" in lower or "integrate" in lower:
        # Find which options to combine
        opts_mentioned = set()
        for opt_id in ["a", "b", "c"]:
            if f"option {opt_id}" in lower or f"of {opt_id}" in lower or f"from {opt_id}" in lower or f"text in {opt_id}" in lower or f"text of {opt_id}" in lower:
                opts_mentioned.add(opt_id.upper())
        # Also check for standalone A, B, C references
        import re
        for m in re.finditer(r'\b([ABC])\b', notes):
            opts_mentioned.add(m.group(1))

        if len(opts_mentioned) >= 2:
            actions.append(f"🔀 **Combine** elements from Options {', '.join(sorted(opts_mentioned))}")
        else:
            actions.append(f"🔀 **Combine** the best elements from multiple options")

    # Text revision
    if any(w in lower for w in ["revise", "revision", "improve", "improving", "punchier", "edit"]):
        actions.append(f"✏️ **Revise** selected text ({selected.upper() if selected else 'TBD'})")

    # Specific text to keep/extract
    quoted_fragments = []
    for line in notes.split("\n"):
        if '"' in line or "'" in line:
            # Find quoted text fragments the reviewer highlighted
            import re
            for m in re.finditer(r'"([^"]{10,})"', line):
                frag = m.group(1)
                if len(frag) < 300:
                    quoted_fragments.append(frag)
            for m in re.finditer(r"'([^']{10,})'", line):
                frag = m.group(1)
                if len(frag) < 300:
                    quoted_fragments.append(frag)

    if quoted_fragments:
        actions.append(f"💎 **Preserve** {len(quoted_fragments)} highlighted phrase(s) from reviewer")

    # Image changes
    if any(w in lower for w in ["new image", "replace image", "found image", "need image"]):
        actions.append("🖼️ **Replace image** — find or commission new artwork")
    if "mirror" in lower or "wrong side" in lower:
        actions.append("🖼️ **Mirror/flip image** — subject on wrong side of spread")
    if "terrible" in lower or "garbage" in lower:
        actions.append("🖼️ **Urgent image replacement** needed")

    # Rethink
    if any(w in lower for w in ["rethink", "reconsider", "redone", "reconsidered"]):
        actions.append("🔄 **Rethink** this spread's approach or concept")

    # Match original
    if any(w in lower for w in ["match original", "match the original", "original design", "model the original", "mirror the graphic", "match layout", "conform with"]):
        actions.append("📐 **Align** more closely with original McLuhan/Fiore spread design")

    # Factual corrections
    if any(w in lower for w in ["wrong", "not a word", "dates are wrong", "incorrect", "facts"]):
        actions.append("⚠️ **Factual correction** needed")

    # Sequence considerations
    if any(w in lower for w in ["sequence", "progression", "pair", "interconnected", "previous spread"]):
        actions.append("🔗 **Sequence consideration** — review in context of adjacent spreads")

    # Remove specific references
    if any(w in lower for w in ["remove", "should not reference", "don't like the reference"]):
        actions.append("✂️ **Remove** specific references or phrases as noted")

    # Quote changes
    if "quote" in lower and any(w in lower for w in ["replace", "remove", "no need", "don't like"]):
        actions.append("📝 **Revise quotation** selection or placement")

    if not actions:
        actions.append("📋 Review notes above for specific guidance")

    return actions


if __name__ == "__main__":
    main()
