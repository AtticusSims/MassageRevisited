# Claude Code Instructions: Planning Engine & Review Interface (Steps 5–6)

## Revision Notes (March 2026)

> **What changed and why:** This document revises the original planning instructions to reflect two developments: (a) the analysis schema is upgrading from v1.1 to v1.2, giving the planning engine significantly richer input data, and (b) research into the publication trajectory has established a theoretical vocabulary (Kress & van Leeuwen, Barthes, Drucker, Bateman) that the planning engine can use to make more precise design directions — without turning the planning process into an academic exercise.
>
> **What did NOT change:** The book's creative goals, the three-movement structure, the six convergences, the thinker map, the page-by-page mapping approach, the meta/pages architecture, and the review workflow are all preserved. The framework is the framework. The revisions make the planning engine a better reader of the analysis and a more articulate writer of design directions.
>
> **Guiding principle:** Every revision serves the *book*. Where the theoretical vocabulary helps the planning engine give a more specific design instruction, it's used. Where it would add bureaucratic overhead without improving the plan, it's not. The paper comes later; the book comes first.

---

## What This Document Is

You are building the Planning Engine for a book project — taking the completed Analysis Database of McLuhan's *The Medium is the Massage* and producing a page-by-page content plan for a contemporary AI-focused companion book. You are also building a review interface (static site, deployable to GitHub Pages) with feedback capabilities.

You will do the planning yourself — read the analysis data, read the theoretical framework, and write the content plan directly. No API calls. You are the planning engine.

Read this entire document before doing anything.

---

## 1. Project Context

This is Step 5 of the project. Current status:

- **Step 1:** Source PDF secured (85 pages of the original McLuhan book) `✅ COMPLETE`
- **Step 2:** Analysis schema designed (v1.1 → upgrading to v1.2) `✅ COMPLETE`
- **Step 3:** Analysis Database produced — **10 of 85 spreads analyzed; remaining 75 in progress** `🔶 IN PROGRESS`
- **Step 4:** Theoretical Framework developed (three-movement structure, 20+ thinkers, 150+ quotations, six convergences) `✅ COMPLETE`

**Prerequisite:** Step 5 requires the complete analysis database (all 85 spreads + thematic_arc summary). Do not begin page-by-page planning until Step 3 is fully complete. The meta-level overviews (Section 3.1) can be drafted in parallel with the final analysis batches, since they draw primarily from the theoretical framework rather than individual spread analyses.

> **CHANGED from original:** The original instructions stated Steps 1–4 were complete. Step 3 is still in progress (10/85 spreads). The execution sequence (Section 7) has been updated accordingly.

Your job: use the Analysis Database and Theoretical Framework to produce a content plan for the new book. Every spread of the original has been analyzed. Every spread of the new book needs a plan.

The plan has two layers:
1. **Page-by-page mapping** — for each of the 85 original spreads, what should the corresponding contemporary spread contain?
2. **Meta-level overviews** — the larger arcs, rhythms, convergence threads, and structural decisions that span the entire book

Both layers are essential. The page-by-page mapping without the meta view produces 85 disconnected pages. The meta view without the page mapping is abstract architecture with no ground truth.

---

## 2. File Inventory

You need these files. If any are missing, ask the human.

| File | Description |
|---|---|
| `analysis_database.json` | The completed Analysis Database from Step 3. All 85 spreads + thematic_arc summary. **Must be schema v1.2.** |
| `analysis_schema_v1.2.json` | The schema reference (for understanding the analysis fields). |
| `image_credits_lookup.json` | Original image credits (useful reference for image direction). |

> **CHANGED:** Schema reference updated to v1.2.

The following should be in the `ContextDocs/` folder:
| File | Description |
|---|---|
| `framework_v3.md` | The primary theoretical framework. Three-movement structure, thinker profiles, 150+ quotations, six convergences. **This is your most important reference.** |
| `framework_v3_addendum.md` | Supplementary material: design-page candidates, pull quotes, case studies. |
| `theorist_reference.md` | Deep thinker profiles for the media-theory wing. |
| `Medium_is_Massage_Revisited_-_Project_Plan_v3.md` | The overall project plan. |

Supplementary reference (read once, consult as needed):
| File | Description |
|---|---|
| `visual_rhetoric_and_reliability.md` | Theoretical grounding of the analysis schema. Appendix B contains the controlled vocabulary for rhetorical strategies; Appendix A maps schema fields to visual rhetoric constructs. Useful when writing design directions. |
| `schema_methodology_revisions.md` | Revision log for schema v1.1 → v1.2. Documents what changed and why. |

> **ADDED:** Two supplementary reference files from the publication research. These are reference material for the planning engine, not documents it needs to process end-to-end.

You should also have access to the rendered PNGs from Step 3 in `rendered/` — you may want to re-view specific spreads when planning their contemporary equivalents.

---

## 3. Planning Output Structure

You will produce a single JSON file: `content_plan.json`. It has two top-level sections: `meta` and `pages`.

### 3.1 Meta-Level Overviews (`meta`)

These provide the bird's-eye view of the new book. Generate these FIRST, before the page-by-page mapping.

```json
{
  "meta": {
    "movement_plan": { ... },
    "convergence_map": { ... },
    "rhythm_plan": { ... },
    "quotation_distribution": { ... },
    "image_strategy": { ... },
    "structural_decisions": { ... }
  },
  "pages": [ ... ]
}
```

#### `movement_plan`

Maps the original book's arc onto the new book's Prologue + three-Movement structure. Specifies which spreads belong to which movement and describes the transitions.

```json
{
  "movement_plan": {
    "prologue": {
      "spread_range": "spread_001–spread_0XX",
      "page_count": N,
      "arc_description": "How the prologue opens the book. What the reader should feel and understand by its end.",
      "key_themes": ["..."],
      "primary_thinkers": ["McLuhan", "Crawford", "Haraway", "Bratton"],
      "opening_strategy": "How the very first spread should land — what's the reader's first encounter?",
      "closing_transition": "How the prologue hands off to Movement 1."
    },
    "movement_1_environment": {
      "spread_range": "spread_0XX–spread_0XX",
      "page_count": N,
      "arc_description": "How Movement 1 builds the picture of computation as invisible environment.",
      "key_themes": ["..."],
      "primary_thinkers": ["Bratton", "Kittler", "Hayles", "Steyerl"],
      "stack_layer_mapping": "How the six Stack layers (Earth, Cloud, City, Address, Interface, User) are distributed across the movement's spreads.",
      "closing_transition": "How M1 hands off to M2."
    },
    "movement_2_acceleration": {
      "spread_range": "spread_0XX–spread_0XX",
      "page_count": N,
      "arc_description": "How Movement 2 demonstrates the recursive loop accelerating.",
      "key_themes": ["..."],
      "primary_thinkers": ["Kurzweil", "Vervaeke", "Lanier"],
      "escalation_strategy": "How the sense of acceleration builds across the movement's spreads.",
      "closing_transition": "How M2 reaches the hinge."
    },
    "hinge": {
      "spread_range": "spread_0XX–spread_0XX",
      "page_count": N,
      "description": "The Copernican trauma. The moment the book pivots from describing acceleration to entering the dreamscape. How does this feel? What is the reader's experience at this turning point?",
      "primary_thinkers": ["Vervaeke", "Bratton"]
    },
    "movement_3_dreamscape": {
      "spread_range": "spread_0XX–spread_0XX",
      "page_count": N,
      "arc_description": "How Movement 3 ventures past the event horizon.",
      "key_themes": ["..."],
      "primary_thinkers": ["McKenna", "Davis", "Gibson", "Bach", "Hoffman"],
      "irresolution_strategy": "How the book holds the central question ('deluded or detecting something real?') without resolving it.",
      "closing_strategy": "How the book ends. What is the final spread? What does the reader take away?"
    }
  }
}
```

#### `convergence_map`

Plans how the six convergences thread through the book. Each convergence should appear in multiple movements, building as the book progresses.

> **ADDED:** The six convergence IDs are now explicitly enumerated. The original instructions provided only a template with `reality_as_interface` as an example.

The six convergences (from `framework_v3.md`):

| ID | Name | Core Claim |
|---|---|---|
| `reality_as_interface` | Reality as Interface | Perception is always mediated; AI adds a layer to a stack that was already nothing but interfaces (Hoffman, Bach, Kittler, Gibson, Bratton) |
| `intelligence_substrate_independent` | Intelligence as Substrate-Independent | Mind is pattern, not material — cells, code, planets can all be intelligent (Levin, Friston, Bach, Wolfram, Bratton) |
| `failure_of_propositions` | The Failure of Propositions | AI is the ultimate propositional machine: infinite facts, zero wisdom (Vervaeke, Bratton, Stephenson) |
| `recursive_acceleration` | Recursive Acceleration | The loop is closing — technology improving the technology that improves technology (Kurzweil, McKenna, Wolfram, Bratton) |
| `return_of_the_numinous` | The Return of the Numinous | Every new medium produces spiritual responses; AI is no exception — now empirically documented (Davis, Gibson, @janus, Vervaeke) |
| `accidental_megastructure` | The Accidental Megastructure | The Stack connects all three movements — it is the medium that is the massage (Bratton, threading through everything) |

```json
{
  "convergence_map": {
    "convergences": [
      {
        "id": "reality_as_interface",
        "name": "Reality as Interface",
        "appearances": [
          {
            "spread_id": "spread_0XX",
            "movement": "movement_1_environment",
            "manifestation": "How this convergence appears on this specific spread.",
            "intensity": "introduced | developed | culminating"
          }
        ],
        "arc": "How this convergence builds across the book — where it's seeded, where it develops, where it peaks."
      }
    ]
  }
}
```

#### `rhythm_plan`

*No changes from original.* The planned pacing of the new book — where it's loud and where it's quiet, where it's dense and where it breathes.

```json
{
  "rhythm_plan": {
    "description": "Overall rhythm strategy — how the book's pacing mirrors and departs from the original.",
    "segments": [
      {
        "spread_range": "spread_0XX–spread_0XX",
        "character": "e.g., 'rapid-fire provocations', 'slow contemplation', 'building density', 'explosive rupture followed by silence'",
        "design_pattern": "e.g., 'alternating full-bleed images with white-space text pages', 'progressive darkening', 'typography growing larger'"
      }
    ],
    "key_rhythmic_moments": [
      {
        "spread_id": "spread_0XX",
        "type": "rupture | climax | silence | acceleration | pivot",
        "description": "What happens here and why it matters to the book's rhythm."
      }
    ]
  }
}
```

#### `quotation_distribution`

*No changes from original.* Plans which thinkers are quoted where, ensuring balance and building across the book. No thinker should be front-loaded or appear only once. The framework's 150+ quotations are the arsenal — this is the deployment plan.

```json
{
  "quotation_distribution": {
    "by_thinker": [
      {
        "thinker": "Bratton",
        "total_appearances": N,
        "spreads": ["spread_0XX", "spread_0XX", "..."],
        "arc": "How Bratton's quotations build through the book."
      }
    ],
    "by_movement": {
      "prologue": { "thinker_count": N, "primary_voices": ["..."] },
      "movement_1": { "thinker_count": N, "primary_voices": ["..."] },
      "movement_2": { "thinker_count": N, "primary_voices": ["..."] },
      "hinge": { "thinker_count": N, "primary_voices": ["..."] },
      "movement_3": { "thinker_count": N, "primary_voices": ["..."] }
    },
    "historical_quotes": {
      "description": "Where historical/presaging quotes (Turing, Wiener, Borges, Blake, Lovelace, etc.) appear.",
      "spreads": ["spread_0XX", "..."]
    }
  }
}
```

#### `image_strategy`

*Minor addition.* Plans the overall image approach across the book.

```json
{
  "image_strategy": {
    "found_vs_generated_ratio": "Approximate split across the whole book.",
    "by_movement": {
      "prologue": "Image character for this movement — e.g., 'intimate, bodily, close-up'",
      "movement_1": "e.g., 'infrastructural, architectural, diagrammatic'",
      "movement_2": "e.g., 'kinetic, blurred, layered, accelerating'",
      "hinge": "e.g., 'void, cosmos, scale shift'",
      "movement_3": "e.g., 'ethereal, liminal, ambiguous between organic and digital'"
    },
    "key_found_image_needs": [
      {
        "spread_id": "spread_0XX",
        "subject": "What the found image needs to show.",
        "why_found": "Why this must be a real photograph rather than generated."
      }
    ],
    "self_referential_images": "Where and how the book's own production process becomes visible in the imagery — screenshots of Claude conversations, pipeline diagrams, the analysis database itself rendered as visual artifact. This is the self-referential thread manifested visually.",
    "tonal_arc": "How the image palette/mood shifts across the book — e.g., from documentary realism to abstraction."
  }
}
```

> **ADDED:** `self_referential_images` field. The framework emphasizes the book's self-referential nature (an AI system critiquing AI). The original image_strategy had no place to plan where this thread surfaces visually. The `structural_decisions.self_referential_placement` field covers the editorial *decision*, but image_strategy needs to plan the visual *execution*.

#### `structural_decisions`

*No changes from original.*

```json
{
  "structural_decisions": {
    "self_referential_placement": "Where and how the book acknowledges its own AI-produced nature. Which spread(s), what tone.",
    "mcluhan_echo_strategy": "How and where direct McLuhan quotes or echoes of the original appear in the new book.",
    "whitehead_bookend": "The original opens and closes with Whitehead. What is the contemporary equivalent? Who bookends the new book?",
    "rotated_page": "The original has one rotated spread (PDF p.14). Will the new book include a rotated spread? If so, what goes there?",
    "credits_and_colophon": "How the new book handles credits, especially acknowledging the AI systems involved.",
    "open_questions": ["Any unresolved editorial decisions that need human input."]
  }
}
```

### 3.2 Page-by-Page Mapping (`pages`)

One entry per original spread (85 entries). Each maps the original to its contemporary equivalent.

> **CHANGED:** Two additions to the page schema: (1) `original_summary` is enriched to include the original's rhetorical strategy and design-enactment mechanism, giving the planning engine richer input; (2) `design_direction` gains a `rhetorical_strategy` field from the controlled vocabulary, making design instructions more precise. (3) A lightweight `paper_trace` field is added for downstream academic reference — this is NOT an analytical task during planning; it's a quick tag so the published paper can later locate exemplar spreads without re-reading all 85 plans.

```json
{
  "pages": [
    {
      "spread_id": "spread_001",
      "original_summary": {
        "book_pages": [0],
        "spread_type": "title_page",
        "argument": "Brief restatement of the original spread's core argument from the analysis database.",
        "rhetorical_strategy": "The original spread's primary rhetorical strategy (from v1.2 controlled vocabulary: assertion, confrontation, juxtaposition, accumulation, disruption, provocation, invocation, dramatization, quieting, sensory_overload, humor, demonstration, interpellation, defamiliarization, call_and_response).",
        "design_intelligence": "How the original's design enacts its argument — the mechanism, stated concisely. Pulled from analysis database rhetoric.design_argument_description. This is the design intelligence the contemporary spread must respond to.",
        "key_elements": "The defining features of the original — what must be echoed, inverted, or transformed."
      },
      "contemporary_plan": {
        "movement": "prologue",
        "theme": "The primary thematic territory for this spread.",
        "argument": "What the contemporary spread should argue or convey. Be specific — not 'something about surveillance' but 'The reader's face has been scanned 47 times today without their knowledge. The biometric dossier has replaced McLuhan's computerized dossier bank.'",
        "text_direction": {
          "approach": "original_prose | quotation | combination | display_text_only | no_text",
          "description": "What the text should say or do. If original prose: the argument, tone, and register. If quotation: specific candidate quotes from the framework (cite thinker and source). If combination: how prose and quotation interact.",
          "candidate_quotes": [
            {
              "text": "The exact quote from the framework.",
              "author": "Thinker name",
              "source": "Source attribution",
              "rationale": "Why this quote works here."
            }
          ],
          "voice_notes": "Specific tonal guidance — e.g., 'McLuhan's confrontational second-person address', 'quiet and devastating', 'playful accumulation building to a punch'."
        },
        "image_direction": {
          "approach": "found | generated | graphic_symbol | typography_only | none",
          "subject": "What the image should depict or evoke.",
          "mood": "The emotional/visual quality — e.g., 'clinical', 'overwhelming', 'intimate', 'uncanny'.",
          "relationship_to_text": "How the image should interact with the text: literalizes, amplifies, contradicts, ironizes, provides_atmosphere, serves_as_metaphor, extends, independent.",
          "composition_notes": "Specific spatial/compositional guidance if relevant.",
          "found_image_reference": "If found: what kind of real-world image to source (e.g., 'satellite photograph of data center clusters', 'press photo of Anthropic office').",
          "generation_prompt_seed": "If generated: a starting direction for the image generation prompt."
        },
        "design_direction": {
          "layout_approach": "How the spread should be composed — e.g., 'mirror the original's left-text/right-image split', 'full-bleed image with overlaid text', 'typography-as-architecture filling the spread'.",
          "rhetorical_strategy": "The primary rhetorical strategy for this spread (from controlled vocabulary). Use this to name the strategy the design should enact. If the original used 'confrontation' and the contemporary spread should too, say so explicitly. If the contemporary spread should depart — e.g., the original used 'accumulation' but the contemporary version should use 'quieting' as a counterpoint — name the departure and why.",
          "typography_notes": "Any specific typographic direction.",
          "design_enacts_argument": "How the layout should perform the argument — the most important design instruction. Be as specific as you were in the analysis. Name the mechanism: 'The spread should perform surveillance on the reader by...' not 'The design should feel surveillance-y.'",
          "relationship_to_original": "echo | inversion | transformation | departure — how this spread relates to its McLuhan counterpart."
        },
        "convergences_active": ["List of convergence IDs active on this spread, from the convergence_map."],
        "thinkers_present": ["Names of any thinkers whose ideas or quotes appear on this spread."],
        "adjacent_dependencies": "Does this spread depend on or affect what's on adjacent spreads? If so, describe the dependency."
      },
      "paper_trace": {
        "primary_construct": "One-line tag for downstream academic reference. Which theoretical construct does this spread most clearly exemplify? e.g., 'Drucker: design as performance (surveillance enacted through form)', 'Kress & van Leeuwen: Given/New inversion', 'Barthes: literalizing relay'. Quick and informal — not an analytical paragraph. Null for spreads that don't clearly exemplify a single construct.",
        "framework_convergence_note": "If this spread is a particularly strong instance of one of the six convergences, note which one and why in one sentence. Null otherwise."
      },
      "reviewer_feedback": {
        "status": "pending",
        "comments": "",
        "tags": [],
        "revision_needed": false
      }
    }
  ]
}
```

**Field-by-field rationale for changes:**

`original_summary.rhetorical_strategy` — **ADDED.** The v1.2 analysis database captures the original spread's primary rhetorical strategy from a 15-term controlled vocabulary. Surfacing this in the planning context means the planning engine can make an informed decision about whether the contemporary spread should echo, invert, or depart from that strategy. Without it, the planning engine is flying blind about *how* the original argued, not just *what* it argued.

`original_summary.design_intelligence` — **ADDED.** Renamed from the implicit reference to "key_elements." This field pulls the original's `rhetoric.design_argument_description` — the mechanism by which design enacts argument. This is the single most important analytical insight from the analysis phase, and the planning engine needs it front-and-center when writing the contemporary `design_enacts_argument` field.

`image_direction.relationship_to_text` — **ADDED.** The v1.2 schema captures image-text relationships using a controlled vocabulary (illustrates, amplifies, literalizes, contradicts, ironizes, etc.). Using this same vocabulary in the *planning* output creates consistency: the analysis describes how the original's images relate to text, the plan specifies how the contemporary images should relate to text, and the downstream authoring engine has an explicit instruction rather than an implicit assumption.

`design_direction.rhetorical_strategy` — **ADDED.** Names the strategy the design should employ, from the same 15-term vocabulary used in the analysis. This is NOT an analytical label — it's a design instruction. "Use confrontation" tells the design engine something specific: address the reader directly, break the fourth wall, create unease. "Use quieting" tells it the opposite: reduce density, create breathing room, let the reader recover. The vocabulary is a creative tool, not an academic checkbox.

`paper_trace` — **ADDED.** This is the only field added purely for downstream academic use. It records, in a single line, which theoretical construct a spread exemplifies — so the published paper can locate its illustrative examples without re-reading all 85 plans. The instructions below (Section 4) specify that this field is filled *after* the creative plan is complete, not during it. It is a tag, not an analysis. Many spreads will have null values. Only spreads that happen to be particularly clear exemplars of a specific construct need a tag.

**All other fields are unchanged from the original planning instructions.**

---

## 4. How to Generate the Plan

### Step 1: Read everything

Before generating any output:
1. Read the complete `analysis_database.json` — all 85 spread analyses AND the `thematic_arc` summary.
2. Read `framework_v3.md` in full — internalize the three-movement structure, the thinker map, the six convergences, and the 150+ quotations.
3. Read `framework_v3_addendum.md` — note the design-page candidates and supplementary material.
4. Read `theorist_reference.md` for additional thinker depth.

> **ADDED:** Step 1.5 below.

**Step 1.5: Familiarize yourself with the rhetorical strategy vocabulary.**

Read Appendix B of `visual_rhetoric_and_reliability.md` (the controlled vocabulary table). You will use these 15 terms when writing `original_summary.rhetorical_strategy` and `design_direction.rhetorical_strategy`. You do not need to read the full working paper — Appendix B is a one-page reference table. The terms:

assertion, confrontation, juxtaposition, accumulation, disruption, provocation, invocation, dramatization, quieting, sensory_overload, humor, demonstration, interpellation, defamiliarization, call_and_response.

Each has a one-sentence definition and an example from the original book. Use these as a creative vocabulary when writing design directions, not as analytical labels to be checked off.

### Step 2: Generate the meta-level overviews

*No changes from original.* Produce the entire `meta` section first. This is your architectural plan — the blueprint before you lay bricks. Work through each sub-section:

1. **`movement_plan`**: Decide where each movement begins and ends. The original book's `thematic_arc` sections (from the analysis) should guide this — but the new book is not a 1:1 mapping. Some original sections may compress, others may expand. The movement boundaries should feel natural, not forced.

2. **`convergence_map`**: Thread each of the six convergences through the movement plan. Each should appear at least 3 times across the book, building in intensity. Don't cluster all appearances in one movement.

3. **`rhythm_plan`**: Design the pacing. Use the original book's `rhythm_pattern` (from the thematic_arc) as reference. McLuhan's book alternates between loud/quiet, dense/spare, confrontational/contemplative. The new book should have its own rhythm that rhymes with the original without slavishly copying it.

4. **`quotation_distribution`**: Allocate the framework's quotation arsenal across the book. Ensure each primary thinker has a meaningful arc — Bratton might appear in all three movements, but his early quotes should establish the Stack while his later quotes should invoke planetary sapience. Avoid dumping all quotations into the movement where the thinker is "primary."

5. **`image_strategy`**: Plan the visual character of each movement and the overall tonal arc. Include the self-referential thread: where does the book's own AI-produced nature become visible in the imagery?

6. **`structural_decisions`**: Make (or flag for human decision) the high-level editorial calls.

### Step 3: Generate page-by-page mapping

Working sequentially through all 85 spreads, generate the `pages` array. For each:

1. Re-read the original spread's analysis from the database.
2. Re-view the rendered PNG if you need to refresh your memory of the original's visual character.
3. **Note the original's rhetorical strategy and design-enactment mechanism.** Write these into `original_summary.rhetorical_strategy` and `original_summary.design_intelligence`. These are the design properties your contemporary spread must respond to — echoing, inverting, transforming, or departing from them.
4. Consult the meta-level overviews to ensure this spread serves the movement plan, the convergence threads, and the rhythm.
5. Write the contemporary plan — argument, text direction, image direction, design direction.
6. **Name the rhetorical strategy** in `design_direction.rhetorical_strategy`. This is a creative decision, not an analytical label. Which of the 15 strategies should the design *employ*? If you're not sure, ask: "What should the reader *experience* on this spread?" Then pick the strategy that produces that experience.
7. Be specific. "Something about algorithms" is useless. "The spread argues that recommendation algorithms have replaced the editorial judgment McLuhan worried about losing — but instead of human editors selecting what's 'fit to print,' we now have fitness functions selecting what's fit to engage. The design should mirror the original's newspaper-layout spread but replace the headlines with algorithmically ranked content cards" is useful.

> **CHANGED:** Steps 3 and 6 are new. The rest is unchanged.

### Step 4: Cross-check

After completing all 85 page plans, verify:
- Every convergence appears where the convergence_map says it should.
- Every thinker appears where the quotation_distribution says they should.
- The rhythm_plan's segments match what the page plans actually describe.
- No movement is starved of strong spreads while another is bloated.
- The adjacent_dependencies make sense — no spread assumes content from a neighbor that doesn't plan to deliver it.
- **The rhetorical strategy distribution is varied.** Check that you haven't assigned "confrontation" to 30 spreads and "quieting" to 2. The book needs the full range.
- **The `relationship_to_original` values are distributed.** A book that is all "echo" is a copy; all "departure" loses the McLuhan thread. Aim for a mix, with "transformation" as the most common.

> **ADDED:** Last two checks. Without them, the controlled vocabulary could produce monotony.

Fix any inconsistencies before presenting to the human.

### Step 5: Fill `paper_trace` tags

**After** the creative plan is complete and cross-checked, make one more pass through the 85 entries and fill the `paper_trace` fields. For each spread, ask:

1. Does this spread happen to be a particularly clear example of a specific theoretical construct in action? If yes, tag it in `primary_construct` with a one-line note. If no (most spreads), leave null.
2. Is this spread a particularly strong instance of one of the six convergences? If yes, note which one in `framework_convergence_note`. If no, leave null.

This should take 5–10 minutes for the full book. The tags are informal — they exist so the paper can later point to "see spread_014 for a clear instance of Druckerian performative design" without having to search all 85 plans. Expect roughly 15–25 spreads to get tagged; the rest should be null.

> **ADDED:** This is the only new step in the generation process. It is explicitly sequenced AFTER the creative work is done — the book comes first, the paper tags come second. The tags serve the book's documentary needs as a human-AI collaboration project, not the planning process itself.

---

## 5. Web Interface

> **CHANGED:** This section is significantly revised. The original instructions described extending a Flask viewer with server-side templates. The project has migrated to a GitHub Pages static site (see Development Log, Session 5). The viewer architecture is now fully client-side.

### Architecture

The review interface is a static site built in `docs/` and deployed to GitHub Pages. All data is loaded via `fetch()` from JSON files. All state (review feedback) is stored in `localStorage`.

**Build pipeline:**
```
output/content_plan.json + output/analysis_database.json + rendered/
  → python source/build_static_site.py
  → docs/
    ├── index.html          # Unified viewer (analysis + planning + overview)
    ├── style.css           # Dark theme CSS
    ├── data/
    │   ├── index.json      # Navigation metadata
    │   ├── spread_NNN.json # Per-spread merged data (analysis + OCR + visual + plan)
    │   └── meta.json       # Meta-level overviews from content_plan.json
    └── images/
        └── spread_NNN.jpg  # Compressed spread images
```

### Navigation Structure

The interface has three modes, switchable via tabs:

- **Analysis View** — The existing viewer (original spread image + analysis JSON rendered as HTML). Keep this intact.
- **Planning View** — The new view (original spread image + content plan rendered as HTML + feedback panel).
- **Overview View** — Displays the meta-level overviews: movement plan, convergence map, rhythm plan, quotation distribution, image strategy, structural decisions. Each as its own collapsible section.

### Planning View Layout

Two panels (not three — the feedback panel is integrated into the right panel to match the existing static site's two-panel layout):

- **Left panel (~45%):** The rendered original spread image (with zoom controls).
- **Right panel (~55%):** The content plan for this spread, rendered as formatted HTML, with the feedback section at the bottom.

> **CHANGED:** Simplified from a three-panel layout to match the existing static site architecture. The feedback panel sits below the plan content, not alongside it. This avoids a major UI rewrite and keeps the review interface consistent with the analysis view.

### Right Panel Formatting

Display the content plan with clear visual hierarchy:

**Header area:**
- Spread ID and book pages
- Movement badge (color-coded: prologue=blue, M1=green, M2=orange, hinge=red, M3=purple)
- Spread type badge from the original analysis
- Rhetorical strategy badge (from `design_direction.rhetorical_strategy`)

**Original Summary** (collapsible, collapsed by default):
- The original spread's argument, rhetorical strategy, and design intelligence, for quick reference without switching to Analysis View.

**Contemporary Plan:**
- `theme` — prominent display
- `argument` — the most important field, displayed large and readable
- `text_direction` — the approach badge (original_prose / quotation / combination / etc.), description, candidate quotes displayed as cards, voice notes
- `image_direction` — approach badge, subject, mood, relationship_to_text badge, composition notes, found/generated details
- `design_direction` — layout approach, rhetorical strategy badge, typography notes, design-enacts-argument (highlighted as in the analysis view), relationship-to-original badge
- `convergences_active` — tag badges
- `thinkers_present` — tag badges
- `adjacent_dependencies` — info box, highlighted if non-empty
- `paper_trace` — small, muted display at the bottom (if non-null). This is metadata, not creative content — display it unobtrusively.

**Feedback Section** (below the plan content):
- **Status selector:** Four states — `approved` (green), `needs_revision` (amber), `flagged` (red), `pending` (gray, default). Stored in `localStorage`.
- **Revision tags** (multi-select buttons): Pre-defined tags:
  - `argument_weak` — the proposed argument needs sharpening
  - `wrong_movement` — this spread is assigned to the wrong movement
  - `wrong_tone` — tonal direction doesn't fit
  - `better_quote_needed` — the candidate quotes aren't strong enough
  - `image_rethink` — the image direction needs reworking
  - `design_rethink` — the design direction needs reworking
  - `dependency_issue` — conflict with an adjacent spread
  - `too_vague` — the plan isn't specific enough
  - `too_similar_to_original` — needs more creative departure
  - `love_it` — explicitly marking something as particularly strong
- **Comment box:** Text area, auto-saves on blur.

> **CHANGED:** Removed the separate comment box for each page's `reviewer_feedback` in the JSON. Feedback is stored in `localStorage` (consistent with the existing analysis review workflow) rather than written back to `content_plan.json`. The Export Revision Prompt function (below) pulls from `localStorage`.

### Overview View Feedback

The overview pages (movement plan, convergence map, etc.) also have feedback sections. Same structure — status, tags, comment box — with overview-appropriate tags:
- `movement_balance` — the movement boundaries need adjusting
- `convergence_gap` — a convergence is underrepresented
- `rhythm_issue` — the pacing plan needs work
- `quotation_balance` — thinker distribution is off
- `image_direction` — overall image strategy needs adjustment
- `structural_question` — a structural decision needs discussion

### Status Dashboard

At the top of every view, display a compact status bar:
- Total spreads: 85
- Approved: N (green)
- Needs revision: N (amber)
- Flagged: N (red)
- Pending review: N (gray)
- A mini progress bar showing the ratio

### Export: Revision Prompt

This is the crucial feature. When the human has finished reviewing, there must be a button — **"Export Revision Prompt"** — that generates a structured document Claude Code can consume to make revisions.

The export collects all pages and overviews where status is `needs_revision` or `flagged` (from `localStorage`) and formats them as a single markdown document:

```markdown
# Content Plan Revision Request

## Summary
- Total items needing revision: N
- Overviews needing revision: [list]
- Pages needing revision: [list of spread IDs]

---

## Overview Revisions

### Movement Plan
**Status:** needs_revision
**Tags:** movement_balance
**Reviewer comments:**
Movement 2 feels too short — only 12 spreads. Consider extending it by...

---

## Page Revisions

### spread_014 (Book pages 18–19)
**Movement:** movement_1_environment
**Rhetorical strategy:** confrontation
**Status:** needs_revision
**Tags:** better_quote_needed, image_rethink
**Current argument:** [the current argument text from the plan]
**Reviewer comments:**
The argument is good but the quote from Bratton feels forced here — he's already heavily quoted on the previous two spreads. Can we use Steyerl instead? Also the image direction is too literal.

### spread_023 (Book pages 36–37)
**Movement:** movement_1_environment
**Rhetorical strategy:** accumulation
**Status:** needs_revision
**Tags:** too_vague
**Current argument:** [the current argument text from the plan]
**Reviewer comments:**
This is way too generic. "Something about the cloud" is not a plan. What specifically about cloud infrastructure? What's the McLuhan connection? What's the image?

...
```

> **CHANGED:** Added `Rhetorical strategy` to the revision prompt's per-page header. This gives the revision agent context for the *kind* of design work needed, not just the content.

This exported document should be saved as a downloadable file and also displayed in a modal/overlay so the reviewer can copy it directly.

After Claude Code processes the revisions, it updates `content_plan.json`, the build script regenerates `docs/`, and all revised entries reset to `pending` — ready for another review cycle.

---

## 6. Directory Structure

> **CHANGED:** Updated to reflect the static site architecture.

```
mcluhan-analysis/
├── source/                          # Scripts, schema, methodology
│   ├── analysis_schema_v1.2.json    # Updated schema
│   ├── phase_b_methodology.md       # Updated methodology (v2.0)
│   ├── build_static_site.py         # Updated to merge content_plan data
│   └── ...
├── rendered/                        # Rendered book pages (PNG, 200 DPI)
├── output/
│   ├── analysis_database.json       # Completed analysis (all 85 spreads)
│   ├── content_plan.json            # NEW — the planning output
│   └── vlm_extractions/             # VLM outputs
├── docs/                            # Static site for GitHub Pages (generated)
│   ├── index.html                   # Unified viewer
│   ├── style.css
│   ├── data/
│   │   ├── index.json
│   │   ├── meta.json                # NEW — meta overviews
│   │   └── spread_NNN.json          # Merged analysis + plan data
│   └── images/
├── ContextDocs/                     # Theoretical framework documents
├── DEVELOPMENT_LOG.md
├── TECHNICAL_NOTES.md
└── README.md
```

---

## 7. Execution Sequence

> **CHANGED:** Updated to reflect current project state (Step 3 in progress) and static site architecture.

### Phase A: Complete Prerequisites
1. **Finish Step 3** — analyze remaining 75 spreads (batches of 10–15 with human review). Generate thematic_arc summary.
2. **Implement Priority 1 schema revisions** — upgrade analysis_schema to v1.2, migrate existing 10 entries.
3. Verify all prerequisite files exist (analysis_database.json with 85 entries, framework docs, rendered PNGs).

### Phase A.5: Early Meta Planning (can overlap with late Step 3)
4. Once ≥60 spreads are analyzed and the thematic_arc is taking shape, begin drafting the `meta` section of `content_plan.json`. This is possible because the meta overviews draw primarily from the framework, not from individual spread analyses. Having the thematic_arc emerging from the analysis provides the structural input needed.
5. Initialize `content_plan.json` with `meta` and empty `pages`.

> **ADDED:** Phase A.5 allows meta planning to overlap with the final analysis batches — a practical efficiency that doesn't sacrifice quality, since the meta-level draws from the framework (complete) rather than individual analyses (still in progress).

### Phase B: Meta-Level Planning
6. Finalize the complete `meta` section of `content_plan.json`.
7. Build the Overview View in the static site.

**STOP. Tell the human:** "The meta-level overviews (movement plan, convergence map, rhythm plan, quotation distribution, image strategy, structural decisions) are ready for review. Please review and provide feedback on the overall architecture before I generate the page-by-page plans."

8. Wait for approval (or process revisions if feedback is provided).

### Phase C: Page-by-Page Planning
9. Generate all 85 page entries in the `pages` array.
10. Run the cross-check (Section 4, Step 4).
11. Fill `paper_trace` tags (Section 4, Step 5).
12. Update the static site build script to merge content plan data into per-spread JSON files.
13. Rebuild the static site.

**STOP. Tell the human:** "The complete content plan — 85 page mappings plus meta overviews — is ready for review. Review at your own pace. When finished, use the 'Export Revision Prompt' button to generate a revision document."

14. Wait for revisions (or approval if none needed).

### Phase D: Revision Cycles
15. When the human exports a revision prompt, process each revision.
16. Update `content_plan.json` with revised entries.
17. Rebuild the static site.
18. All revised entries reset to `pending` for re-review.
19. Repeat until the human approves all pages and overviews.

---

## 8. Key Reminders

**Be specific.** The downstream Authoring Engine will use your plans to generate actual text and design. "Something about privacy" gives it nothing to work with. "McLuhan's 'womb-to-tomb surveillance' has been realized as algorithmic behavioral prediction — Zuboff's 'behavioral surplus' harvested from every scroll, pause, and keystroke. The spread should confront the reader with the specific data points collected about them in a single day, typeset as an invasive interrogation mirroring the original's 'How much do you make?' opening" gives it everything.

**Use the framework's quotations.** You have 150+ precisely attributed quotes organized by thinker and movement. When suggesting quotations for a spread, cite the specific quote from the framework (text, author, source). Don't gesture vaguely — "maybe a Bratton quote here." Which Bratton quote? Why this one? How does it interact with the page's argument?

**Respect the original's design intelligence.** Each spread of the original was analyzed for how its design enacts its argument. The contemporary plan should maintain this principle — the `design_direction.design_enacts_argument` field should describe a specific mechanism, not a vague aspiration. The original's `design_intelligence` (in the `original_summary`) tells you what mechanism the original used; your job is to find the contemporary equivalent.

**Name the rhetorical strategy.** You have a 15-term vocabulary for how a spread argues. Use it. When you write "confrontation" in `design_direction.rhetorical_strategy`, you're giving the design engine a specific instruction: address the reader directly, break the fourth wall, create unease. When you write "quieting," you're saying: reduce density, create breathing room, let the reader recover. These terms are design tools.

> **ADDED.** This reminder ensures the controlled vocabulary is actually used as a creative instrument during planning, not treated as a metadata field to fill after the fact.

**Plan for rhythm.** A book is a sequence, not a collection. After three dense, text-heavy spreads, the reader needs a visual breath. After a quiet contemplative page, the next can hit harder. Your rhythm_plan should be reflected in the actual page plans — check that you're not producing 10 consecutive text-heavy spreads. The rhetorical strategy vocabulary helps here: after three spreads of "accumulation" or "sensory_overload," plan a spread of "quieting" or "demonstration."

**Flag dependencies.** If a spread's argument depends on the reader having seen something on a previous spread, or if a design choice (like a color shift or typographic change) needs to be coordinated across multiple pages, note it in `adjacent_dependencies`. The human reviewer needs to see these connections.

**Don't force mappings.** Some original spreads will map beautifully to contemporary equivalents. Others will need creative departure. If an original spread about the telephone doesn't have a natural AI analogue, don't force it — propose something that serves the same structural/rhetorical function in the new book, even if the content departs significantly. Set `relationship_to_original` to `departure` and explain why in the argument.

**The meta overviews are living documents.** If page-by-page planning reveals that a meta-level decision doesn't work (e.g., you planned 20 spreads for Movement 1 but there isn't enough material to fill them), update the meta section. The cross-check in Step 4 should catch these inconsistencies.

**The paper_trace is a tag, not an essay.** Fill it after the creative work is done. One line or null. Don't let it slow down the planning. If a spread doesn't obviously exemplify a single theoretical construct, it's null — that's fine and expected for most spreads.

> **ADDED.** Prevents the `paper_trace` field from becoming a distraction during the creative planning process.

---

## Appendix: Changelog from Original Instructions

| Section | Change | Rationale |
|---|---|---|
| 1. Project Context | Step 3 marked as in-progress (10/85) | Reflects actual state |
| 2. File Inventory | Schema reference → v1.2; two supplementary docs added | Schema is upgrading; theoretical vocabulary available |
| 3.1 convergence_map | Six convergences explicitly enumerated with IDs and core claims | Prevents ambiguity; planning engine needs exact references |
| 3.1 image_strategy | `self_referential_images` field added | The book's self-referential nature needs visual planning |
| 3.2 original_summary | `rhetorical_strategy` and `design_intelligence` fields added | Gives planning engine richer input from the analysis |
| 3.2 image_direction | `relationship_to_text` field added | Consistent vocabulary between analysis and planning |
| 3.2 design_direction | `rhetorical_strategy` field added | More precise design instructions using controlled vocabulary |
| 3.2 paper_trace | New section added to page schema | Lightweight academic reference tags for downstream paper |
| 3.2 reviewer_feedback | `tags` array added to schema | Was present in Section 5 UI spec but missing from data schema |
| 4 Step 1.5 | Familiarize with rhetorical strategy vocabulary | Ensures vocabulary is used as creative tool |
| 4 Step 3 | Steps 3 and 6 added (strategy + naming) | Uses richer analysis data; names design strategy |
| 4 Step 4 | Two new cross-checks (strategy distribution, relationship distribution) | Prevents monotony from controlled vocabulary |
| 4 Step 5 | New step: fill paper_trace tags | Sequenced AFTER creative work |
| 5 | Rewritten for static site architecture | Project migrated from Flask to GitHub Pages |
| 6 | Updated directory structure | Reflects static site and schema v1.2 |
| 7 | Execution sequence updated | Accounts for Step 3 in progress; adds Phase A.5 overlap |
| 8 | Two reminders added (strategy naming, paper_trace restraint) | Supports new fields |
