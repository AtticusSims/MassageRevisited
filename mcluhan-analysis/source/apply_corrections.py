"""
apply_corrections.py — Phase B Quality Corrections

Fixes five categories of issues identified in review:
1. body_font_style: Set to "sans-serif" for all spreads (the book uses sans-serif throughout)
2. special_treatments: Per-spread corrections based on visual inspection of all 85 images
3. OCR/text corrections: Fix transcription errors and missing text
4. Cross-spread text continuations: Update relationship fields where text flows across spreads
5. Minor cleanup: Fix [No text detected] placeholders for image-only spreads

Run: python source/apply_corrections.py
"""

import json
import os
import shutil
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'output', 'analysis_database.json')

# =============================================================================
# 1. SPECIAL TREATMENTS — Per-spread corrections from visual inspection
# =============================================================================
# Each spread gets an accurate list of actual typographic special treatments.
# The previous data incorrectly applied "reversed text (white on black)" to 69/85 spreads.

SPECIAL_TREATMENTS = {
    "spread_001": ["text overlaid on image"],
    "spread_002": [],
    "spread_003": [],
    "spread_004": ["text overlaid on image"],
    "spread_005": [],
    "spread_006": ["rotated text (90 degrees counterclockwise)", "reversed text (white on black)"],
    "spread_007": ["text overlaid on image"],
    "spread_008": ["reversed text (white on black)", "oversized display typography"],
    "spread_009": [],
    "spread_010": [],
    "spread_011": ["oversized display typography"],
    "spread_012": ["oversized display typography"],
    "spread_013": ["oversized display typography"],
    "spread_014": ["rotated text (90 degrees counterclockwise)", "oversized display typography"],
    "spread_015": ["oversized display typography"],
    "spread_016": ["oversized display typography"],
    "spread_017": ["reversed text (white on black)", "oversized display typography"],
    "spread_018": ["oversized display typography"],
    "spread_019": [],
    "spread_020": [],
    "spread_021": ["text overlaid on image"],
    "spread_022": [],
    "spread_023": ["text overlaid on image"],
    "spread_024": [],
    "spread_025": ["oversized display typography"],
    "spread_026": ["hand-drawn lettering"],
    "spread_027": ["letter-spaced text"],
    "spread_028": ["reversed text (white on black)", "text overlaid on image"],
    "spread_029": ["reversed text (white on black)", "repeated text pattern"],
    "spread_030": ["reversed text (white on black)"],
    "spread_031": ["reversed text (white on black)"],
    "spread_032": ["inverted text (upside-down and mirrored)"],
    "spread_033": ["reversed text (white on black)", "inverted text (upside-down)"],
    "spread_034": [],
    "spread_035": [],
    "spread_036": ["letter-spaced text"],
    "spread_037": ["text overlaid on image"],
    "spread_038": ["text overlaid on image"],
    "spread_039": [],
    "spread_040": [],
    "spread_041": [],
    "spread_042": ["reversed text (white on black)", "text overlaid on image"],
    "spread_043": ["reversed text (white on black)", "oversized display typography"],
    "spread_044": ["oversized display typography"],
    "spread_045": ["text overlaid on image"],
    "spread_046": ["oversized display typography"],
    "spread_047": [],
    "spread_048": ["oversized display typography"],
    "spread_049": [],
    "spread_050": [],
    "spread_051": [],
    "spread_052": [],
    "spread_053": [],
    "spread_054": [],
    "spread_055": [],
    "spread_056": ["oversized display typography"],
    "spread_057": ["text overlaid on image"],
    "spread_058": [],
    "spread_059": [],
    "spread_060": ["oversized display typography"],
    "spread_061": [],
    "spread_062": [],
    "spread_063": ["oversized display typography", "handwritten text"],
    "spread_064": ["reversed text (white on black)", "oversized display typography"],
    "spread_065": [],
    "spread_066": ["oversized display typography"],
    "spread_067": [],
    "spread_068": [],
    "spread_069": [],
    "spread_070": [],
    "spread_071": ["oversized display typography"],
    "spread_072": [],
    "spread_073": ["cascading text sizes"],
    "spread_074": ["oversized display typography"],
    "spread_075": [],
    "spread_076": ["text overlaid on image"],
    "spread_077": ["reversed text (white on black)", "text overlaid on image"],
    "spread_078": [],
    "spread_079": ["reversed text (white on black)", "negative reproduction"],
    "spread_080": ["reversed text (white on black)", "text overlaid on image"],
    "spread_081": ["oversized display typography"],
    "spread_082": [],
    "spread_083": [],
    "spread_084": [],
    "spread_085": ["reversed text (white on black)", "text overlaid on image"],
}

# =============================================================================
# 2. TEXT CORRECTIONS — Fix OCR errors and missing text
# =============================================================================
# Only spreads with identified errors. Keys match spread IDs.
# Each entry can contain: body_text, display_text (replacement values)

TEXT_CORRECTIONS = {
    "spread_019": {
        # Was "[No text detected in the image.]" — this is a pure photograph spread (toes/fingers)
        "body_text": "",
    },
    "spread_021": {
        # Hubcap text was OCR'd as "SOUTH PL" — actually reads "PLYMOUTH"
        "display_text": "PLYMOUTH",
    },
    "spread_034": {
        # Was "[No text detected in the image.]" — this is a pure photograph spread (prison bars)
        "body_text": "",
    },
    "spread_054": {
        # Was "[No text detected in the image.]" — this is a pure photograph spread (kiss)
        "body_text": "",
    },
}

# =============================================================================
# 3. CROSS-SPREAD TEXT CONTINUATIONS — Relationship updates
# =============================================================================
# Updates to relationship_to_previous and relationship_to_next where text
# flows across spread boundaries but wasn't properly documented.

RELATIONSHIP_UPDATES = {
    # Title sequence: 005 → 006 → 007
    "spread_005": {
        "relationship_to_next": "Initiates the three-spread title sequence. 'Good Morning!' opens the book's interior before the title page on 006.",
    },
    "spread_006": {
        "relationship_to_previous": "Continues from 005's greeting into the formal title page. The title 'The Medium is the Massage' displayed here leads into 007's question.",
        "relationship_to_next": "TEXT CONTINUES: The title 'The Medium is the Massage' set up on this spread leads directly to 007's '...the massage?' — the ellipsis and question mark transform the title into a question.",
    },
    "spread_007": {
        "relationship_to_previous": "TEXT CONTINUES from 006: '...the massage?' completes/questions the title established on the previous spread. The leading ellipsis explicitly marks textual continuation.",
        "relationship_to_next": "TEXT CONTINUES: '...the massage?' is answered by 008's 'and how!' — a call-and-response pair across the page turn.",
    },
    "spread_008": {
        "relationship_to_previous": "TEXT CONTINUES from 007: 'and how!' answers the question '...the massage?' — completing a call-and-response sequence. The dramatic scale shift (from small question to enormous answer) performs the argument about media's overwhelming impact.",
    },
    # Extensions sequence: 020 → 021
    "spread_020": {
        "relationship_to_next": "TEXT CONTINUES: 'The wheel' begins a phrase completed on 021 ('...is an extension of the foot'). The page turn enacts the extension concept.",
    },
    "spread_021": {
        "relationship_to_previous": "TEXT CONTINUES from 020: '...is an extension of the foot' completes 'The wheel' from the previous spread. The ellipsis at the start explicitly marks continuation.",
    },
    # Extensions sequence: 022 → 023
    "spread_022": {
        "relationship_to_next": "TEXT CONTINUES: 'the book' begins a phrase completed on 023 ('is an extension of the eye...'). Same cross-spread extension pattern.",
    },
    "spread_023": {
        "relationship_to_previous": "TEXT CONTINUES from 022: 'is an extension of the eye...' completes 'the book' from the previous spread. Continues the systematic extensions sequence.",
    },
    # Printing ditto: 029 → 030
    "spread_029": {
        "relationship_to_next": "TEXT/PATTERN CONTINUES: The 'Printing, a ditto device' repetition pattern on the right page continues directly onto 030's left page, the ditto device literally demonstrated by the cross-spread repetition.",
    },
    "spread_030": {
        "relationship_to_previous": "TEXT/PATTERN CONTINUES from 029: The 'Printing, a ditto device' repetition pattern flows across the page turn from 029's right page to 030's left page, enacting print's duplicating function.",
    },
    # Information collision: 043 → 044
    "spread_043": {
        "relationship_to_next": "TEXT CONTINUES: 'When information is brushed against information...' (ending with ellipsis) is completed on 044 with 'the results are startling and effective.' The page turn itself becomes the collision.",
    },
    "spread_044": {
        "relationship_to_previous": "TEXT CONTINUES from 043: 'the results are startling and effective' (beginning with lowercase 'the') completes the sentence begun on 043 ('When information is brushed against information...'). The lowercase opening explicitly marks continuation.",
    },
    # Environment split: 046 → 047 → 048
    "spread_046": {
        "relationship_to_next": "TEXT CONTINUES: The truncated word 'enviro' is deliberately split, with 'nment' appearing on 048 (after the intervening 047). The physical separation across three spreads performs the concept of environmental invisibility.",
    },
    "spread_047": {
        "relationship_to_previous": "Intervenes between the split word 'enviro-nment' (046/048). The statement 'Environments are invisible' occupies the space between the split halves, itself becoming an invisible environment between word-fragments.",
        "relationship_to_next": "The statement about environmental invisibility is literally positioned inside the split word 'environment' (046/048), performing its own thesis.",
    },
    "spread_048": {
        "relationship_to_previous": "TEXT CONTINUES from 046: 'nment' completes 'enviro-' from 046, with 047's 'Environments are invisible' intervening. The three-spread sequence performs environmental invisibility through typographic splitting.",
    },
    # Socrates/memory: 061 → 062
    "spread_061": {
        "relationship_to_next": "TEXT CONTINUES: The body text ends mid-sentence with 'The mimetic form, a technique' which is completed on 062 ('that exploited rhythm, meter, and music, achieved the desired psychological response in the listener.'). This is a direct textual continuation across the page turn.",
    },
    "spread_062": {
        "relationship_to_previous": "TEXT CONTINUES from 061: 'that exploited rhythm, meter, and music, achieved the desired psychological response in the listener.' completes the sentence begun on 061 ('The mimetic form, a technique'). The found advertisement on the right page (memory course) provides ironic commentary on the Socratic warning about memory loss.",
    },
    # Art sequence: 071 → 072 → 073
    "spread_071": {
        "relationship_to_next": "TEXT CONTINUES: The giant letter 'A' with small 'rt' begins 'Art' — completed across three spreads as 'Art is anything you can get away with.' The monumental scale of the 'A' forces the reader to physically confront art-as-environment.",
    },
    "spread_072": {
        "relationship_to_previous": "TEXT CONTINUES from 071: 'is anything' continues the sentence begun with the giant 'Art' on 071.",
        "relationship_to_next": "TEXT CONTINUES: The fragment 'is anything' leads to 073's 'you can get away with' — completing the three-spread aphorism.",
    },
    "spread_073": {
        "relationship_to_previous": "TEXT CONTINUES from 071-072: 'you can get away with' completes the three-spread sentence 'Art is anything you can get away with.' The cascading text sizes perform the idea of art expanding beyond containment.",
    },
    # Fire imagery: 076 → 077
    "spread_076": {
        "relationship_to_next": "IMAGE CONTINUES: The fire photograph on the right page continues into 077's full-bleed fire image. The Joyce quote ('The west shall shake the east awake...') appears on both spreads, bridging the visual continuation.",
    },
    "spread_077": {
        "relationship_to_previous": "IMAGE CONTINUES from 076: The fire imagery spans both spreads. The Joyce quote repeats from 076, now accompanied by Laotze and McLuhan's East-West synthesis.",
    },
    # Identity sequence: 081 → 082
    "spread_081": {
        "relationship_to_next": "TEXT AND IMAGE CONTINUE: The numbered faceless men illustration spans both 081 and 082. The Caterpillar's question '...and who are you?' on 081 is answered by Alice's response on 082.",
    },
    "spread_082": {
        "relationship_to_previous": "TEXT AND IMAGE CONTINUE from 081: Alice's reply ('I--I hardly know, sir, just at present...') answers the Caterpillar's question from 081. The numbered faceless men illustration continues from 081, surrounding the Alice dialogue with anonymous figures.",
    },
}

# =============================================================================
# APPLICATION LOGIC
# =============================================================================

def load_database():
    """Load the analysis database."""
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_database(db):
    """Save the analysis database."""
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def create_backup(db):
    """Create a timestamped backup."""
    backup_dir = os.path.dirname(DB_PATH)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'analysis_database_backup_corrections_{timestamp}.json')
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print(f"Backup created: {backup_path}")
    return backup_path


def apply_corrections(db):
    """Apply all corrections to the database."""
    spreads = db['spreads']

    stats = {
        'font_fixed': 0,
        'treatments_fixed': 0,
        'text_fixed': 0,
        'relationships_fixed': 0,
        'no_text_cleaned': 0,
    }

    for spread in spreads:
        sid = spread['id']

        # --- 1. Fix body_font_style to "sans-serif" for ALL spreads ---
        old_font = spread.get('design', {}).get('typography', {}).get('body_font_style', '')
        if old_font != 'sans-serif':
            spread['design']['typography']['body_font_style'] = 'sans-serif'
            stats['font_fixed'] += 1

        # --- 2. Fix special_treatments ---
        if sid in SPECIAL_TREATMENTS:
            old_treatments = spread.get('design', {}).get('typography', {}).get('special_treatments', [])
            new_treatments = SPECIAL_TREATMENTS[sid]
            if old_treatments != new_treatments:
                spread['design']['typography']['special_treatments'] = new_treatments
                stats['treatments_fixed'] += 1

        # --- 3. Fix OCR/text errors ---
        if sid in TEXT_CORRECTIONS:
            corrections = TEXT_CORRECTIONS[sid]
            for field, value in corrections.items():
                if field in spread.get('text', {}):
                    spread['text'][field] = value
                    stats['text_fixed'] += 1

        # --- 4. Clean up [No text detected] in body_text ---
        # Replace placeholder with empty string for image-only spreads
        body = spread.get('text', {}).get('body_text', '')
        if body == '[No text detected in the image.]':
            spread['text']['body_text'] = ''
            stats['no_text_cleaned'] += 1

        # --- 5. Update cross-spread relationships ---
        if sid in RELATIONSHIP_UPDATES:
            updates = RELATIONSHIP_UPDATES[sid]
            for field, value in updates.items():
                if field in spread.get('progression', {}):
                    spread['progression'][field] = value
                    stats['relationships_fixed'] += 1

    # Update metadata
    db['metadata']['analysis_date'] = datetime.now().strftime('%Y-%m-%d')
    db['metadata']['analysis_model'] = 'claude-opus-4-6+qwen3-vl (phase_b_v2 enrichment + corrections)'

    return stats


def verify_corrections(db):
    """Verify corrections were applied correctly."""
    spreads = db['spreads']
    issues = []

    # Check body_font_style
    non_sans = [s['id'] for s in spreads
                if s.get('design', {}).get('typography', {}).get('body_font_style') != 'sans-serif']
    if non_sans:
        issues.append(f"body_font_style not 'sans-serif': {non_sans}")

    # Check special_treatments against our corrections
    for spread in spreads:
        sid = spread['id']
        if sid in SPECIAL_TREATMENTS:
            actual = spread.get('design', {}).get('typography', {}).get('special_treatments', [])
            expected = SPECIAL_TREATMENTS[sid]
            if actual != expected:
                issues.append(f"{sid}: special_treatments mismatch. Expected {expected}, got {actual}")

    # Check no [No text detected] remains
    no_text = [s['id'] for s in spreads
               if s.get('text', {}).get('body_text') == '[No text detected in the image.]']
    if no_text:
        issues.append(f"[No text detected] still present in: {no_text}")

    # Check relationship updates
    for sid, updates in RELATIONSHIP_UPDATES.items():
        spread = next((s for s in spreads if s['id'] == sid), None)
        if spread:
            for field, expected in updates.items():
                actual = spread.get('progression', {}).get(field, '')
                if actual != expected:
                    issues.append(f"{sid}.progression.{field}: not updated correctly")

    return issues


def print_summary(stats, issues):
    """Print a summary of corrections applied."""
    print("\n" + "=" * 60)
    print("CORRECTION SUMMARY")
    print("=" * 60)
    print(f"  body_font_style fixed:    {stats['font_fixed']}")
    print(f"  special_treatments fixed: {stats['treatments_fixed']}")
    print(f"  text corrections applied: {stats['text_fixed']}")
    print(f"  relationships updated:    {stats['relationships_fixed']}")
    print(f"  [No text] cleaned:        {stats['no_text_cleaned']}")
    print(f"  Total changes:            {sum(stats.values())}")
    print()

    if issues:
        print(f"[!] VERIFICATION ISSUES ({len(issues)}):")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("[OK] All corrections verified successfully.")

    # Print special_treatments distribution
    print("\n" + "-" * 60)
    print("SPECIAL TREATMENTS DISTRIBUTION (after corrections):")
    treatment_counts = {}
    for treatments in SPECIAL_TREATMENTS.values():
        if not treatments:
            treatment_counts['(none)'] = treatment_counts.get('(none)', 0) + 1
        for t in treatments:
            treatment_counts[t] = treatment_counts.get(t, 0) + 1

    for treatment, count in sorted(treatment_counts.items(), key=lambda x: -x[1]):
        print(f"  {treatment}: {count} spreads")


if __name__ == '__main__':
    print("Loading database...")
    db = load_database()

    print(f"Database loaded: {len(db['spreads'])} spreads")

    print("Creating backup...")
    create_backup(db)

    print("Applying corrections...")
    stats = apply_corrections(db)

    print("Verifying corrections...")
    issues = verify_corrections(db)

    print("Saving database...")
    save_database(db)

    print_summary(stats, issues)
