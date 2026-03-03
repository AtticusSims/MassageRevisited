"""
reocr_check.py — Re-run OCR on specific spreads and compare with database text.

Usage:
  python source/reocr_check.py 62          # Re-OCR spread 062 only
  python source/reocr_check.py all         # Re-OCR all 85 spreads and flag differences
  python source/reocr_check.py 1-85        # Re-OCR a range
"""

import json
import os
import sys
import time

# Add source dir to path
sys.path.insert(0, os.path.dirname(__file__))
from vlm_tools import run_ocr, run_structured_ocr

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'output', 'analysis_database.json')
RENDERED_DIR = os.path.join(os.path.dirname(__file__), '..', 'rendered')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'ocr_recheck')


def load_database():
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_spread_text(db, spread_num):
    """Get current text fields for a spread."""
    sid = f"spread_{spread_num:03d}"
    for s in db['spreads']:
        if s['id'] == sid:
            return {
                'body_text': s.get('text', {}).get('body_text', ''),
                'display_text': s.get('text', {}).get('display_text', ''),
                'captions': s.get('text', {}).get('captions', []),
            }
    return None


def reocr_spread(spread_num):
    """Run OCR on a single spread and return results."""
    image_path = os.path.join(RENDERED_DIR, f"spread_{spread_num:03d}.png")
    if not os.path.exists(image_path):
        return None, None

    print(f"  Running OCR on spread_{spread_num:03d}...")
    t0 = time.time()
    raw_text = run_ocr(image_path)
    t1 = time.time()
    print(f"    Raw OCR: {t1-t0:.1f}s ({len(raw_text)} chars)")

    print(f"  Running structured OCR on spread_{spread_num:03d}...")
    structured_text = run_structured_ocr(image_path)
    t2 = time.time()
    print(f"    Structured OCR: {t2-t1:.1f}s ({len(structured_text)} chars)")

    return raw_text, structured_text


def save_result(spread_num, raw_text, structured_text, current_db_text):
    """Save OCR results for review."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    result = {
        'spread_id': f"spread_{spread_num:03d}",
        'current_db': current_db_text,
        'new_raw_ocr': raw_text,
        'new_structured_ocr': structured_text,
    }
    path = os.path.join(OUTPUT_DIR, f"spread_{spread_num:03d}_reocr.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"    Saved: {path}")
    return path


def update_db_text(db, spread_num, body_text=None, display_text=None, captions=None):
    """Update text fields in database for a spread."""
    sid = f"spread_{spread_num:03d}"
    for s in db['spreads']:
        if s['id'] == sid:
            if body_text is not None:
                s['text']['body_text'] = body_text
            if display_text is not None:
                s['text']['display_text'] = display_text
            if captions is not None:
                s['text']['captions'] = captions
            return True
    return False


def parse_range(arg):
    """Parse spread numbers from argument."""
    if arg.lower() == 'all':
        return list(range(1, 86))
    if '-' in arg:
        start, end = arg.split('-')
        return list(range(int(start), int(end) + 1))
    return [int(arg)]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python source/reocr_check.py <spread_num|range|all>")
        sys.exit(1)

    spread_nums = parse_range(sys.argv[1])
    db = load_database()

    print(f"Re-OCR check for {len(spread_nums)} spread(s)")
    print("=" * 60)

    for num in spread_nums:
        print(f"\n--- Spread {num:03d} ---")
        current = get_spread_text(db, num)
        if current is None:
            print(f"  [!] Spread {num:03d} not found in database")
            continue

        raw, structured = reocr_spread(num)
        if raw is None:
            print(f"  [!] Image not found for spread {num:03d}")
            continue

        save_result(num, raw, structured, current)

        # Simple comparison: check if new OCR is significantly longer
        old_len = len(current['body_text']) + len(current['display_text'])
        new_len = len(raw)
        if new_len > old_len * 1.3 and new_len - old_len > 50:
            print(f"  [!] NEW OCR significantly longer: {old_len} -> {new_len} chars (+{new_len-old_len})")
        elif old_len > 0 and new_len < old_len * 0.5:
            print(f"  [?] NEW OCR significantly shorter: {old_len} -> {new_len} chars")
        else:
            print(f"  [OK] Text lengths comparable: DB={old_len}, New={new_len}")

    print("\n" + "=" * 60)
    print(f"Results saved to: {OUTPUT_DIR}")
