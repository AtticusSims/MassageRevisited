#!/usr/bin/env python3
"""Merge improved section plans into content_plan.json."""

import json
import sys
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent / "output"

SECTION_FILES = {
    "prologue": BASE / "prologue_plans_improved.json",
    "m1": BASE / "movement1_plans_improved.json",
    "m2": BASE / "m2_spread_plans.json",
    "hinge_m3": BASE / "hinge_m3_plans_rewritten.json",
}

CONTENT_PLAN = BASE / "content_plan.json"
BACKUP_SUFFIX = f"_backup_premerge_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_entries(entries, section_name):
    """Validate that entries have required fields."""
    required_top = ["spread_id", "movement", "original_summary", "contemporary_plan"]
    required_plan = ["theme", "argument", "text", "image", "rhetoric", "mapping"]
    required_mapping = ["relationship_to_original", "convergences"]

    issues = []
    for i, entry in enumerate(entries):
        sid = entry.get("spread_id", f"entry_{i}")
        for field in required_top:
            if field not in entry:
                issues.append(f"{sid}: missing top-level field '{field}'")

        plan = entry.get("contemporary_plan", {})
        for field in required_plan:
            if field not in plan:
                issues.append(f"{sid}: missing contemporary_plan.{field}")

        mapping = plan.get("mapping", {})
        for field in required_mapping:
            if field not in mapping:
                issues.append(f"{sid}: missing mapping.{field}")

        # Check strategy vocabulary
        valid_strategies = {
            "assertion", "confrontation", "juxtaposition", "accumulation",
            "disruption", "provocation", "invocation", "dramatization",
            "quieting", "sensory_overload", "humor", "demonstration",
            "interpellation", "defamiliarization", "call_and_response"
        }
        strategy = plan.get("rhetoric", {}).get("strategy", "")
        if strategy and strategy not in valid_strategies:
            issues.append(f"{sid}: non-standard strategy '{strategy}'")

        # Check relationship_to_original vocabulary
        valid_rels = {"echo", "inversion", "transformation", "departure"}
        rel = mapping.get("relationship_to_original", "")
        if rel and rel not in valid_rels:
            issues.append(f"{sid}: invalid relationship '{rel}'")

    if issues:
        print(f"\n[{section_name}] Validation issues ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"[{section_name}] All {len(entries)} entries valid.")

    return issues


def main():
    # Load current content plan
    print("Loading current content_plan.json...")
    plan = load_json(CONTENT_PLAN)

    # Backup
    backup_path = CONTENT_PLAN.with_name(f"content_plan{BACKUP_SUFFIX}.json")
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    print(f"Backup saved to {backup_path.name}")

    # Load all sections
    all_entries = []
    all_issues = []

    for section_name, path in SECTION_FILES.items():
        if not path.exists():
            print(f"ERROR: {path.name} not found!")
            sys.exit(1)

        entries = load_json(path)
        print(f"Loaded {section_name}: {len(entries)} entries from {path.name}")
        issues = validate_entries(entries, section_name)
        all_issues.extend(issues)
        all_entries.extend(entries)

    # Verify we have exactly 85
    print(f"\nTotal entries: {len(all_entries)}")
    if len(all_entries) != 85:
        print(f"WARNING: Expected 85 entries, got {len(all_entries)}")

    # Verify spread IDs are sequential
    expected_ids = [f"spread_{i:03d}" for i in range(1, 86)]
    actual_ids = [e["spread_id"] for e in all_entries]
    if actual_ids != expected_ids:
        missing = set(expected_ids) - set(actual_ids)
        extra = set(actual_ids) - set(expected_ids)
        if missing:
            print(f"Missing spread IDs: {sorted(missing)}")
        if extra:
            print(f"Extra spread IDs: {sorted(extra)}")
    else:
        print("All 85 spread IDs present and sequential.")

    # Distribution stats
    print("\n--- Distribution Stats ---")

    # Strategies
    strategies = {}
    for e in all_entries:
        s = e.get("contemporary_plan", {}).get("rhetoric", {}).get("strategy", "unknown")
        strategies[s] = strategies.get(s, 0) + 1
    print("\nRhetorical strategies:")
    for s, count in sorted(strategies.items(), key=lambda x: -x[1]):
        print(f"  {s}: {count}")

    # Relationships
    rels = {}
    for e in all_entries:
        r = e.get("contemporary_plan", {}).get("mapping", {}).get("relationship_to_original", "unknown")
        rels[r] = rels.get(r, 0) + 1
    print("\nRelationship to original:")
    for r, count in sorted(rels.items(), key=lambda x: -x[1]):
        print(f"  {r}: {count}")

    # Convergences
    conv_counts = {}
    for e in all_entries:
        for c in e.get("contemporary_plan", {}).get("mapping", {}).get("convergences", []):
            conv_counts[c] = conv_counts.get(c, 0) + 1
    print("\nConvergence appearances:")
    for c, count in sorted(conv_counts.items(), key=lambda x: -x[1]):
        print(f"  {c}: {count}")

    # Thinkers
    thinker_counts = {}
    for e in all_entries:
        for t in e.get("contemporary_plan", {}).get("mapping", {}).get("thinkers", []):
            thinker_counts[t] = thinker_counts.get(t, 0) + 1
    print("\nThinker appearances:")
    for t, count in sorted(thinker_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}")

    if all_issues:
        print(f"\n{'='*50}")
        print(f"TOTAL VALIDATION ISSUES: {len(all_issues)}")
        print("Fix these before merging? (continuing anyway for now)")

    # Replace pages array
    plan["pages"] = all_entries
    plan["generated"] = datetime.now().isoformat()
    plan["generator"] = "merge_sections.py (improved plans)"

    # Write merged plan
    with open(CONTENT_PLAN, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    print(f"\nMerged content_plan.json written: {len(all_entries)} entries")
    print(f"File size: {CONTENT_PLAN.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
