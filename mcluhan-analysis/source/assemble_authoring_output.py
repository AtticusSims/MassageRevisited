#!/usr/bin/env python3
"""
Assemble authoring output from three source files into a single
authoring_output.json matching the schema.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "output"

def load_spreads_006_010():
    """Load from full-schema wrapper format."""
    with open(BASE / "spreads_006_010_text_options.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["spreads"]

def load_bare_array(filename):
    """Load from bare JSON array format."""
    with open(BASE / filename, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_spread(s):
    """Ensure each spread has all required fields with defaults."""
    # Required fields
    assert "spread_id" in s, f"Missing spread_id"
    assert "text_options" in s, f"Missing text_options in {s['spread_id']}"

    # Ensure movement is set
    if "movement" not in s:
        sid = int(s["spread_id"].split("_")[1])
        if sid <= 10:
            s["movement"] = "prologue"
        elif sid <= 35:
            s["movement"] = "movement_1_environment"
        elif sid <= 60:
            s["movement"] = "movement_2_acceleration"
        elif sid <= 65:
            s["movement"] = "hinge"
        else:
            s["movement"] = "movement_3_dreamscape"

    # Ensure design_specs exists (even if empty)
    if "design_specs" not in s:
        s["design_specs"] = []

    # Default nullable fields
    s.setdefault("theme", "")
    s.setdefault("selected_text", None)
    s.setdefault("selected_design", None)
    s.setdefault("reviewer_notes", None)
    s.setdefault("dependency_flags", [])

    # Normalize text options
    for opt in s["text_options"]:
        opt.setdefault("caption_text", None)
        opt.setdefault("quotations_used", [])
        opt.setdefault("voice_register", "declarative")
        opt.setdefault("rhetorical_strategy", "assertion")
        opt.setdefault("word_count", 0)
        # Calculate word_count if 0
        if opt["word_count"] == 0:
            words = 0
            for field in ["display_text", "body_text", "caption_text"]:
                if opt.get(field):
                    words += len(opt[field].split())
            opt["word_count"] = words

    # Normalize design specs
    for spec in s["design_specs"]:
        spec.setdefault("density", "moderate")
        spec.setdefault("tone", "balanced")
        spec.setdefault("svg_wireframe", "")

    return s

def validate_spread_ids(spreads):
    """Check we have exactly spreads 006-025 in order."""
    expected = [f"spread_{i:03d}" for i in range(6, 26)]
    actual = [s["spread_id"] for s in spreads]

    missing = set(expected) - set(actual)
    extra = set(actual) - set(expected)

    if missing:
        print(f"WARNING: Missing spreads: {sorted(missing)}")
    if extra:
        print(f"WARNING: Extra spreads: {sorted(extra)}")

    # Sort by spread_id
    spreads.sort(key=lambda s: s["spread_id"])
    return spreads

def main():
    print("Loading spreads 006-010...")
    s1 = load_spreads_006_010()
    print(f"  Got {len(s1)} spreads: {[s['spread_id'] for s in s1]}")

    print("Loading spreads 011-017...")
    s2 = load_bare_array("spreads_011_017_text_options.json")
    print(f"  Got {len(s2)} spreads: {[s['spread_id'] for s in s2]}")

    print("Loading spreads 018-025...")
    s3 = load_bare_array("spreads_018_025_text_options.json")
    print(f"  Got {len(s3)} spreads: {[s['spread_id'] for s in s3]}")

    # Combine
    all_spreads = s1 + s2 + s3
    print(f"\nTotal spreads: {len(all_spreads)}")

    # Normalize
    all_spreads = [normalize_spread(s) for s in all_spreads]

    # Validate
    all_spreads = validate_spread_ids(all_spreads)

    # Build output
    output = {
        "version": "1.0",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "claude-opus-4-6",
        "spread_range": "spread_006-spread_025",
        "spreads": all_spreads
    }

    # Stats
    total_options = sum(len(s["text_options"]) for s in all_spreads)
    total_specs = sum(len(s["design_specs"]) for s in all_spreads)
    total_words = sum(
        opt["word_count"]
        for s in all_spreads
        for opt in s["text_options"]
    )

    print(f"\n--- Assembly Stats ---")
    print(f"Spreads: {len(all_spreads)}")
    print(f"Text options: {total_options}")
    print(f"Design specs: {total_specs}")
    print(f"Total words across all options: {total_words}")

    # Write
    outpath = BASE / "authoring_output.json"
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    size_kb = outpath.stat().st_size / 1024
    print(f"\nWritten to: {outpath}")
    print(f"File size: {size_kb:.1f} KB")

    return 0

if __name__ == "__main__":
    sys.exit(main())
