"""
Extract spread JSON data from agent tool-results file.
Reads the persisted JSON, finds the embedded spread array, and writes clean JSON.
"""
import json
import re
import sys

INPUT_PATH = r"C:\Users\attic\.claude\projects\C--Users-attic-Documents-ClaudeCode-MassageRevisited\b65a9528-c6ba-4bb9-ae30-f76803915266\tool-results\toolu_01PBkEAKmWf46DorjmrtC58U.json"
OUTPUT_PATH = r"C:\Users\attic\Documents\ClaudeCode\MassageRevisited\mcluhan-analysis\output\spreads_011_017_text_options.json"

def main():
    # Step 1: Read and parse the outer JSON wrapper
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        outer = json.load(f)

    print(f"Outer structure: list of {len(outer)} items")

    # Step 2: Find the text content containing spread data
    text_content = None
    for item in outer:
        if item.get("type") == "text" and "spread_011" in item.get("text", ""):
            text_content = item["text"]
            break

    if text_content is None:
        print("ERROR: Could not find text content with spread_011")
        sys.exit(1)

    print(f"Found text content: {len(text_content)} chars")

    # Step 3: Find the JSON array in the text
    # The text starts with agent prose, then has a JSON array starting with [
    # We need to find the first [ that begins the spread array
    # Look for the pattern where [ is followed by spread object

    # Find the start of the JSON array - look for the opening [ before the first spread object
    # The agent prose ends and then the JSON array begins
    match = re.search(r'\n\[[\s\n]*\{[\s\n]*"spread_id"', text_content)
    if not match:
        # Try without newline prefix
        match = re.search(r'\[[\s\n]*\{[\s\n]*"spread_id"', text_content)

    if not match:
        print("ERROR: Could not find start of spread JSON array")
        sys.exit(1)

    # Find the actual [ character position
    array_start = text_content.index('[', match.start())
    print(f"Array starts at position {array_start}")

    # Now find the matching closing ] by counting brackets
    depth = 0
    array_end = None
    for i in range(array_start, len(text_content)):
        ch = text_content[i]
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                array_end = i + 1
                break

    if array_end is None:
        print("ERROR: Could not find matching ] for the array")
        sys.exit(1)

    json_str = text_content[array_start:array_end]
    print(f"Extracted JSON string: {len(json_str)} chars")

    # Step 4: Parse to validate
    spreads = json.loads(json_str)
    print(f"Parsed {len(spreads)} spread objects")

    # Verify spread IDs
    spread_ids = [s["spread_id"] for s in spreads]
    print(f"Spread IDs: {spread_ids}")

    # Verify expected fields
    for s in spreads:
        keys = set(s.keys())
        expected = {"spread_id", "movement", "theme", "text_options", "design_specs"}
        missing = expected - keys
        extra = keys - expected
        if missing:
            print(f"  WARNING: {s['spread_id']} missing fields: {missing}")
        if extra:
            print(f"  INFO: {s['spread_id']} extra fields: {extra}")
        print(f"  {s['spread_id']}: {len(s.get('text_options', []))} text options, "
              f"design_specs={'yes' if 'design_specs' in s else 'no'}")

    # Step 5: Write clean JSON
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(spreads, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to: {OUTPUT_PATH}")
    print("Done!")

if __name__ == "__main__":
    main()
