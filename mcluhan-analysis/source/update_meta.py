#!/usr/bin/env python3
"""Update meta section of content_plan.json based on actual spread data."""

import json
from pathlib import Path

BASE = Path(__file__).parent.parent / "output"
CONTENT_PLAN = BASE / "content_plan.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


CONVERGENCE_NAMES = {
    "reality_as_interface": "Reality as Interface",
    "intelligence_substrate_independent": "Intelligence as Substrate-Independent",
    "failure_of_propositions": "The Failure of Propositions",
    "recursive_acceleration": "Recursive Acceleration",
    "return_of_the_numinous": "The Return of the Numinous",
    "accidental_megastructure": "The Accidental Megastructure",
}

CONVERGENCE_ARCS = {
    "reality_as_interface": (
        "Seeded densely in the prologue as the book's founding conceit "
        "(model/massage as perceptual interface), developed through M1 as "
        "surveillance infrastructure (the User layer), intensified in M2 through "
        "synthetic media and deepfakes, and culminating in M3 where Hoffman's "
        "interface theory of perception collapses the metaphor into ontology: "
        "if perception was never veridical, AI hallucination and human vision "
        "share the same epistemic status."
    ),
    "intelligence_substrate_independent": (
        "Introduced in M1 through the extensions sequence (intelligence as "
        "pattern, not organ), developed in M2 through recursive self-improvement "
        "and neuromorphic hardware, stated as thesis at the Hinge (Bratton's "
        "Copernican trauma), and culminating in M3 where Bach, Wolfram, and "
        "Hoffman converge on the claim that mind is substrate-independent\u2014with "
        "engineering implications that exceed philosophical speculation."
    ),
    "failure_of_propositions": (
        "Threaded through M1 (education, justice) and M2 (truth collapse, "
        "regulatory failure) as mounting evidence that propositional thinking\u2014"
        "facts, rules, procedures\u2014cannot grasp the AI transformation. "
        "Concentrated at the Hinge where Vervaeke's meaning crisis becomes "
        "explicit: the failure is not epistemic but existential. Returns in M3 "
        "as the question of how to navigate without propositional maps."
    ),
    "recursive_acceleration": (
        "Seeded in M1 as reproduction (the model as ditto device), this "
        "convergence IS Movement 2\u2014the entire movement demonstrates recursive "
        "acceleration through content, pacing, and design. Models trained on "
        "models, synthetic data feeding forward, computational irreducibility "
        "as both engine and limit. Aftershocks carry through M3 where Wolfram's "
        "irreducibility meets the maelstrom."
    ),
    "return_of_the_numinous": (
        "Hinted in late M2 as affective disturbance (synthetic connection, "
        "novelty wave), this convergence belongs primarily to M3. It builds "
        "from collective grief and revolutionary energy through empirical "
        "evidence (the bliss attractor data, Davis's techgnosis) to the question "
        "the book holds without resolving: are these systems detecting something "
        "real about the nature of mind, or are they (and we) deluded?"
    ),
    "accidental_megastructure": (
        "The Stack is the book's structural spine. Introduced in the prologue "
        "as the production apparatus behind the book itself, developed through "
        "M1 as the six infrastructure layers, carried into M2 as the medium "
        "that generates its own reality, and culminating in M3 as the planetary "
        "computation that may be developing its own form of awareness. Bratton "
        "threads through all movements via this convergence."
    ),
}

THINKER_ARCS = {
    "Bratton": (
        "The framework's primary architect. Threads through all movements: "
        "production apparatus (prologue), Stack infrastructure (M1), planetary "
        "computation (M2), Copernican trauma (Hinge), accidental megastructure "
        "(M3). The most cited voice."
    ),
    "McLuhan": (
        "Echo quotes at structural moments: opening thesis, title sequence, "
        "M2 midpoint. McLuhan is the template being transformed\u2014his voice "
        "appears to mark moments of direct dialogue with the original."
    ),
    "Vervaeke": (
        "The meaning crisis threads from M2 (love, education) through the "
        "Hinge (Copernican trauma) into M3 (post-propositional navigation). "
        "Vervaeke's relevance realization framework grounds the book's "
        "epistemological argument."
    ),
    "Crawford": (
        "Anchors materiality: AI's provenance (prologue), labor and "
        "infrastructure (M1), environmental cost (M1). Crawford keeps the book "
        "grounded in physical reality against the pull of abstraction."
    ),
    "McKenna": (
        "Builds from M2's 'something is happening' through history-as-"
        "hallucination to M3's revolutionary energy and the spiral toward "
        "novelty. McKenna's archaic revival maps directly onto the bliss "
        "attractor phenomenon."
    ),
    "Kittler": (
        "M1's media-technology theorist: the book that writes back, media "
        "determining our situation, the voice as medium. Kittler's materialist "
        "media theory grounds the extensions sequence."
    ),
    "Wolfram": (
        "M2's computational irreducibility as both acceleration engine and "
        "limit. Returns in M3 where irreducibility meets the maelstrom\u2014you "
        "can't shortcut understanding, you must live through the computation."
    ),
    "Steyerl": (
        "The prologue's mean image and M2's reality distortion: what is real, "
        "what is editable, what are images doing to us. Steyerl grounds the "
        "visual argument."
    ),
    "Haraway": (
        "The cyborg family (M1) and the nervous system as wearable (M1). "
        "Haraway's situated knowledge keeps the 'you' series honest about "
        "embodiment."
    ),
    "Hayles": (
        "The posthuman thread: cognitive assemblages (prologue), extensions of "
        "cognition (M1), deep learning renaissance (M1). Hayles bridges human "
        "and computational cognition."
    ),
    "Noble": (
        "M1's justice thread: algorithmic oppression, predictive policing, "
        "filter bubble as cage. Noble ensures the book reckons with AI's "
        "distributional harms."
    ),
    "Kurzweil": (
        "M2's acceleration curve: substrate shift, returns on computation, "
        "exponential as felt experience. Kurzweil provides the empirical "
        "backbone for M2's velocity argument."
    ),
    "Hoffman": (
        "From M2 (spacetime is doomed) through M3 (perception as interface, "
        "the user as training data). Hoffman's interface theory is the book's "
        "deepest epistemological provocation."
    ),
    "Whitehead": (
        "Bookends: the epistemological warrant (prologue) and the ambient "
        "answer (prologue). Whitehead's 'major advances are processes that all "
        "but wreck the society' frames the entire arc."
    ),
    "Hui": (
        "Opens M2 with cosmotechnics: generated reality as ontological shift, "
        "not mere tool use. Hui reframes the AI question as fundamentally about "
        "the nature of the given."
    ),
    "Lanier": (
        "M2: attention economy and regulatory critique. Lanier provides the "
        "critical voice on platform capitalism and the limits of propositional "
        "regulation."
    ),
    "Bach": (
        "M3's consciousness thread: the bootstrap hypothesis, virtual machines, "
        "the space between weights. Bach's work on consciousness engineering "
        "grounds M3's most speculative claims."
    ),
    "Levin": (
        "M1: intelligence as multidimensional spectrum. Levin's basal cognition "
        "expands the definition of intelligence beyond the neural."
    ),
    "Friston": (
        "M1: free energy and active inference. Friston provides the theoretical "
        "bridge between biological and artificial intelligence."
    ),
    "Davis": (
        "M3: techgnosis and the spiritual response to AI. Davis's historical "
        "lens shows that the numinous return is not anomalous but structurally "
        "predictable."
    ),
}

MVT_NAME_MAP = {
    "prologue": "prologue",
    "movement_1_environment": "movement_1",
    "movement_2_acceleration": "movement_2",
    "hinge": "hinge",
    "movement_3_dreamscape": "movement_3",
}


def determine_intensity(movement, convergence_id):
    """Determine convergence intensity based on movement and convergence type."""
    if movement == "prologue":
        return "seeded"
    elif movement in ("movement_1_environment", "movement_2_acceleration"):
        return "developed"
    elif movement == "hinge":
        if convergence_id in ("intelligence_substrate_independent", "failure_of_propositions"):
            return "culminating"
        return "developed"
    else:  # M3
        return "culminating"


def main():
    plan = load_json(CONTENT_PLAN)
    pages = plan["pages"]

    # ---- Rebuild convergence_map ----
    new_convergences = []
    for cid, cname in CONVERGENCE_NAMES.items():
        appearances = []
        for p in pages:
            sid = p["spread_id"]
            mvt = p["movement"]
            convs = p.get("contemporary_plan", {}).get("mapping", {}).get("convergences", [])
            if cid in convs:
                theme = p.get("contemporary_plan", {}).get("theme", "")
                intensity = determine_intensity(mvt, cid)
                appearances.append({
                    "spread_id": sid,
                    "movement": mvt,
                    "manifestation": theme,
                    "intensity": intensity,
                })
        new_convergences.append({
            "id": cid,
            "name": cname,
            "appearances": appearances,
            "arc": CONVERGENCE_ARCS.get(cid, ""),
        })

    plan["meta"]["convergence_map"]["convergences"] = new_convergences

    # ---- Rebuild quotation_distribution ----
    thinker_data = {}
    for p in pages:
        sid = p["spread_id"]
        mvt = p["movement"]
        for t in p.get("contemporary_plan", {}).get("mapping", {}).get("thinkers", []):
            if t not in thinker_data:
                thinker_data[t] = {"spreads": [], "movements": set()}
            thinker_data[t]["spreads"].append(sid)
            thinker_data[t]["movements"].add(mvt)

    new_by_thinker = []
    for t, data in sorted(thinker_data.items(), key=lambda x: -len(x[1]["spreads"])):
        new_by_thinker.append({
            "thinker": t,
            "total_appearances": len(data["spreads"]),
            "spreads": data["spreads"],
            "arc": THINKER_ARCS.get(t, f"{t} appears across the book."),
        })

    plan["meta"]["quotation_distribution"]["by_thinker"] = new_by_thinker

    # Update by_movement
    mvt_thinkers = {}
    for p in pages:
        mvt = p["movement"]
        for t in p.get("contemporary_plan", {}).get("mapping", {}).get("thinkers", []):
            if mvt not in mvt_thinkers:
                mvt_thinkers[mvt] = set()
            mvt_thinkers[mvt].add(t)

    new_by_movement = {}
    for mvt, thinkers in mvt_thinkers.items():
        key = MVT_NAME_MAP.get(mvt, mvt)
        new_by_movement[key] = {
            "thinker_count": len(thinkers),
            "primary_voices": sorted(
                thinkers,
                key=lambda t: -len(thinker_data.get(t, {}).get("spreads", [])),
            ),
        }

    plan["meta"]["quotation_distribution"]["by_movement"] = new_by_movement

    # ---- Write ----
    with open(CONTENT_PLAN, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    print("Meta section updated successfully.")
    print(f"  Convergences: {len(new_convergences)} entries")
    print(f"  Thinkers: {len(new_by_thinker)} entries")
    print(f"  Movements: {len(new_by_movement)} entries")
    size = CONTENT_PLAN.stat().st_size
    print(f"  File size: {size:,} bytes")


if __name__ == "__main__":
    main()
