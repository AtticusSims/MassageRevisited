"""
fix_truncated_text.py — Re-OCR spreads with truncated body_text and update database.

Identified truncated spreads:
  - spread_039: ends with "The" (mid-sentence)
  - spread_051: ends with "the best" (mid-sentence)
  - spread_061: ends with "a technique" (mid-sentence)
  - spread_062: ends with "putting on the" + missing right-column advertisement

For spread_025: text continues in display_text field ("men change.") — this is a
field-split issue, not a truncation. No fix needed.

Usage:
  python source/fix_truncated_text.py          # Re-OCR all truncated spreads
  python source/fix_truncated_text.py --dry-run  # Show what would change without saving
"""

import json
import os
import sys
import time
import shutil
from datetime import datetime

# Add source dir to path
sys.path.insert(0, os.path.dirname(__file__))
from vlm_tools import _ollama_chat, image_to_base64

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
DB_PATH = os.path.join(BASE_DIR, 'output', 'analysis_database.json')
RENDERED_DIR = os.path.join(BASE_DIR, 'rendered')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'ocr_recheck')

# Spreads to re-OCR with their known issues
TRUNCATED_SPREADS = [39, 51, 61, 62]

# The advertisement text for spread_062 right column (already OCR'd and saved)
SPREAD_062_AD_TEXT = """Develop A Powerful Memory?

A noted publisher in Chicago reports there is a simple technique for acquiring a powerful memory which can pay you real dividends in both business and social advancement and works like magic to give you added poise, necessary self-confidence and greater popularity.

According to this publisher, many people do not realize how much they could influence others simply by remembering accurately everything they see, hear, or read. Whether in business, at social functions or even in casual conversations with new acquaintances, there are ways in which you can dominate each situation by your ability to remember.

To acquaint the readers of this paper with the easy-to-follow rules for developing skill in remembering anything you choose to remember, the publishers have printed full details of their self-training method in a new book, "Adventures in Memory," which will be mailed free to anyone who requests it. No obligation. Send your name, address and zip code to: Memory Studies, 835 Diversey Parkway, Dept. 8183, Chicago, Ill. 60614. A postcard will do."""


def load_database():
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_database(db):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def create_backup():
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = DB_PATH.replace('.json', f'_backup_textfix_{ts}.json')
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup: {backup_path}")
    return backup_path


def get_spread_entry(db, spread_num):
    sid = f"spread_{spread_num:03d}"
    for s in db['spreads']:
        if s['id'] == sid:
            return s
    return None


def ocr_spread(spread_num, prompt=None, suffix="reocr_fix"):
    """Run OCR on a spread using _ollama_chat with a simple, direct prompt.
    Uses cached results if available."""
    # Check for cached result first
    cache_path = os.path.join(OUTPUT_DIR, f"spread_{spread_num:03d}_{suffix}.txt")
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            cached = f.read().strip()
        if len(cached) > 20:
            print(f"  Using cached OCR from {os.path.basename(cache_path)} ({len(cached)} chars)")
            return cached

    image_path = os.path.join(RENDERED_DIR, f"spread_{spread_num:03d}.png")
    if not os.path.exists(image_path):
        print(f"  [!] Image not found: {image_path}")
        return None

    if prompt is None:
        prompt = (
            "Read and transcribe ALL text visible in this image. "
            "Include every word, preserving exact spelling and punctuation. "
            "Organize top to bottom, left to right. "
            "Do not describe images or layout."
        )

    print(f"  OCR on spread_{spread_num:03d}...")
    t0 = time.time()
    text = _ollama_chat(image_path, prompt)
    elapsed = time.time() - t0
    print(f"    Got {len(text)} chars in {elapsed:.1f}s")

    # Save raw result
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"spread_{spread_num:03d}_{suffix}.txt")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"    Saved: {out_path}")

    return text


def compare_texts(old_text, new_text, spread_num):
    """Compare old and new text, showing what's different."""
    old_len = len(old_text)
    new_len = len(new_text)
    print(f"  Old body_text: {old_len} chars")
    print(f"  New OCR text:  {new_len} chars")

    if new_len > old_len:
        # Find where they diverge
        min_len = min(old_len, new_len)
        diverge_at = min_len
        for i in range(min_len):
            if i < len(old_text) and i < len(new_text) and old_text[i] != new_text[i]:
                diverge_at = i
                break

        extra = new_text[old_len:] if new_len > old_len else ""
        if extra:
            preview = extra[:200].strip()
            print(f"  NEW TEXT FOUND (additional {new_len - old_len} chars):")
            print(f"    ...{preview}...")
    elif new_len < old_len * 0.5:
        print(f"  [!] Warning: New OCR is much shorter. May have failed.")
    else:
        print(f"  [OK] Similar length")


def extract_body_text_from_ocr(raw_ocr, spread_num):
    """
    Extract just the body_text portion from raw OCR output.
    This strips page numbers, section headers that are display_text, etc.
    Returns the extracted body_text or None if OCR failed.
    """
    if not raw_ocr or raw_ocr.startswith("ERROR:") or len(raw_ocr) < 20:
        return None

    # Strip thinking tags if present (Qwen3-VL issue)
    import re
    text = re.sub(r'<think>.*?</think>', '', raw_ocr, flags=re.DOTALL).strip()
    if not text:
        return None

    return text


def process_spread_062(db, dry_run=False):
    """Special handling for spread_062: left column text + right column ad."""
    print("\n=== SPREAD 062 (special handling) ===")
    entry = get_spread_entry(db, 62)
    if not entry:
        print("  [!] Not found in database!")
        return False

    old_body = entry.get('text', {}).get('body_text', '')
    print(f"  Current body_text: {len(old_body)} chars")
    print(f"  Ends with: ...{old_body[-50:]}")

    # Re-OCR the left column specifically
    image_path = os.path.join(RENDERED_DIR, "spread_062.png")
    prompt_left = (
        "Read and transcribe ALL text in the LEFT column of this image. "
        "This is a book page about education, myth, and media. "
        "Include the complete text, preserving exact wording and punctuation. "
        "The text continues from a previous page and discusses mimetic form, "
        "myth, the Beatles, and youth. Transcribe everything you can read."
    )
    left_text = ocr_spread(62, prompt_left)

    # Also try full page OCR
    prompt_full = (
        "Transcribe ALL text on both pages of this book spread. "
        "Left page has body text about education, myth, and media. "
        "Right page has a newspaper advertisement titled 'Develop A Powerful Memory'. "
        "Transcribe both pages completely."
    )
    full_text = ocr_spread(62, prompt_full)

    # Save results for review
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, 'spread_062_left_reocr.txt'), 'w', encoding='utf-8') as f:
        f.write(left_text or '')
    with open(os.path.join(OUTPUT_DIR, 'spread_062_full_reocr.txt'), 'w', encoding='utf-8') as f:
        f.write(full_text or '')

    # Determine the best text for the left column
    # Use the longer of left_text vs old_body, as long as it's reasonable
    best_left = old_body
    if left_text and len(left_text) > len(old_body):
        best_left = left_text
        print(f"  Left column: using new OCR ({len(left_text)} chars vs old {len(old_body)} chars)")
    elif full_text and len(full_text) > len(old_body):
        # Try to extract left column from full text
        # The ad text starts with "Develop A Powerful Memory"
        if "Develop A Powerful Memory" in full_text:
            left_part = full_text[:full_text.index("Develop A Powerful Memory")].strip()
            if len(left_part) > len(old_body):
                best_left = left_part
                print(f"  Left column: extracted from full OCR ({len(left_part)} chars)")
    else:
        print(f"  Left column: keeping existing text (new OCR wasn't better)")

    # The right column advertisement text is already verified
    ad_text = SPREAD_062_AD_TEXT.strip()
    print(f"  Right column (ad): {len(ad_text)} chars")

    # Combine: body_text gets left column, ad goes in captions or a separate field
    # The ad is part of the page content, best placed in body_text after the main text
    combined_body = best_left.rstrip()
    if not combined_body.endswith('.') and not combined_body.endswith('"') and not combined_body.endswith('?'):
        # Text is still truncated - note this
        print(f"  [!] Left column text still appears truncated: ...{combined_body[-40:]}")

    # Add the ad as a clearly separated section in body_text
    new_body = combined_body + "\n\n[Advertisement on facing page:]\n" + ad_text

    print(f"\n  New combined body_text: {len(new_body)} chars")

    if not dry_run:
        entry['text']['body_text'] = new_body
        print(f"  [OK] Updated spread_062 body_text in database")
    else:
        print(f"  [DRY RUN] Would update body_text to {len(new_body)} chars")

    return True


def process_truncated_spread(db, spread_num, dry_run=False):
    """Re-OCR a truncated spread and update if better text is found."""
    print(f"\n=== SPREAD {spread_num:03d} ===")
    entry = get_spread_entry(db, spread_num)
    if not entry:
        print(f"  [!] Not found in database!")
        return False

    old_body = entry.get('text', {}).get('body_text', '')
    print(f"  Current body_text: {len(old_body)} chars")
    if old_body:
        print(f"  Ends with: ...{old_body[-60:]}")

    # Run OCR
    new_text = ocr_spread(spread_num)
    if not new_text or len(new_text) < 20:
        print(f"  [!] OCR returned insufficient text ({len(new_text) if new_text else 0} chars)")
        # Try with a more specific prompt
        new_text = ocr_spread(spread_num,
            "Please read and transcribe every word of text visible in this book page image. "
            "Include all paragraphs, quotes, and any other text. "
            "Output only the transcribed text, nothing else."
        )
        if not new_text or len(new_text) < 20:
            print(f"  [!] Second OCR attempt also failed. Skipping.")
            return False

    # Clean the OCR text
    cleaned = extract_body_text_from_ocr(new_text, spread_num)
    if not cleaned:
        print(f"  [!] Could not extract usable text from OCR.")
        return False

    compare_texts(old_body, cleaned, spread_num)

    # If new text is longer, it likely captured what was missing
    if len(cleaned) > len(old_body) * 1.05 and len(cleaned) - len(old_body) > 20:
        print(f"  >> New OCR has {len(cleaned) - len(old_body)} more characters")
        if not dry_run:
            entry['text']['body_text'] = cleaned
            print(f"  [OK] Updated spread_{spread_num:03d} body_text")
        else:
            print(f"  [DRY RUN] Would update body_text")
        return True
    else:
        print(f"  >> New OCR is not significantly longer. Keeping existing text.")
        # Save the comparison for manual review
        return False


if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv

    print("Fix Truncated Text")
    print("=" * 60)
    if dry_run:
        print("[DRY RUN MODE - no database changes]")
    print()

    db = load_database()

    if not dry_run:
        backup = create_backup()

    changes = 0

    # Process the regular truncated spreads first
    for num in [39, 51, 61]:
        if process_truncated_spread(db, num, dry_run):
            changes += 1

    # Process spread_062 with special handling
    if process_spread_062(db, dry_run):
        changes += 1

    print("\n" + "=" * 60)
    print(f"Total changes: {changes}")

    if changes > 0 and not dry_run:
        save_database(db)
        print(f"Database saved to: {DB_PATH}")
    elif changes == 0:
        print("No changes needed.")

    print(f"\nRaw OCR outputs saved in: {OUTPUT_DIR}")
