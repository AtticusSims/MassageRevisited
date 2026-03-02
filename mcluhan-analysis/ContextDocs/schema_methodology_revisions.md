# Required Revisions to Schema and Methodology

**Purpose:** Align analysis_schema_v1.1 and phase_b_methodology with the theoretical and methodological standards described in the visual rhetoric working paper, ensuring the system produces publishable data.

**Revision scope:** Schema v1.1 → v1.2; Methodology v1.0 → v2.0

**Principle:** Every revision below serves at least one of three goals: (a) grounding a schema field in an explicit theoretical construct, (b) improving inter-rater reliability by constraining interpretive freedom, or (c) satisfying a journal reviewer's expected methodological standard. Revisions that would improve elegance but serve none of these goals are excluded.

---

## A. Schema Revisions (analysis_schema_v1.1 → v1.2)

### A1. New top-level metadata fields

**Add `schema_theoretical_basis`** — a string or array naming the theoretical frameworks the schema operationalizes. Reviewers will expect this.

```json
"schema_theoretical_basis": {
  "type": "array",
  "items": { "type": "string" },
  "description": "Theoretical frameworks operationalized by this schema.",
  "default": [
    "Kress & van Leeuwen 2006 (visual grammar)",
    "Barthes 1977; Martinec & Salway 2005 (image-text relations)",
    "Drucker 2014 (performative design)",
    "Bateman 2008; Hiippala 2015 (GeM framework)"
  ]
}
```

**Add per-entry `analyst` and `analysis_method` fields** — required for reproducibility reporting. Currently the metadata records only a single `analysis_model` for the entire database. Reliability testing requires knowing *who* (or what) analyzed *each* spread.

```json
"analyst": {
  "type": "string",
  "description": "Identifier for the analyst (human name, model ID, or 'multi' for collaborative)."
},
"analysis_method": {
  "type": "string",
  "enum": ["human_only", "vlm_assisted", "llm_primary_human_reviewed", "multi_model"],
  "description": "The human-AI collaboration mode used for this entry."
}
```

**Rationale:** The Development Log documents a specific layered collaboration model (automated → AI-assisted → AI-primary → human-primary → human-only). The published paper must report this per entry, not just globally.

---

### A2. Convert `images[].relationship_to_text` from free text to controlled vocabulary

**Current state:** Free text with suggestive examples in the description ("illustrates, contradicts, amplifies, ironizes, literalizes, provides atmosphere, serves as metaphor, etc.").

**Problem:** The "etc." makes this effectively unbounded, which kills reliability. Analysts will coin different terms for the same relationship.

**Revision:** Convert to an enumeration aligned with Barthes and Martinec-Salway.

```json
"relationship_to_text": {
  "type": "object",
  "properties": {
    "primary_relation": {
      "type": "string",
      "enum": [
        "illustrates",
        "amplifies",
        "literalizes",
        "contradicts",
        "ironizes",
        "provides_atmosphere",
        "serves_as_metaphor",
        "extends",
        "independent",
        "decorative"
      ],
      "description": "The dominant relationship between this image and the spread's text."
    },
    "barthes_mode": {
      "type": "string",
      "enum": ["anchorage", "relay", "neither"],
      "description": "Barthes' classification: does the text fix the image's meaning (anchorage), or do text and image contribute complementary information (relay)?"
    },
    "description": {
      "type": "string",
      "description": "Prose elaboration of the relationship. Required when primary_relation is 'contradicts', 'ironizes', 'literalizes', or 'serves_as_metaphor'."
    }
  }
}
```

**Impact on existing entries:** The current sample entry's `relationship_to_text` prose maps cleanly. Spread_011's fingerprint is `primary_relation: "literalizes"`, `barthes_mode: "relay"`. The bullseye is `primary_relation: "literalizes"`, `barthes_mode: "relay"`. The prose descriptions migrate to the new `description` sub-field. All 10 existing entries need this restructuring.

**Theoretical warrant:** Barthes 1977; Martinec & Salway 2005. A reviewer in Visual Communication or DSH will expect at minimum the anchorage/relay distinction.

---

### A3. Add Kress & van Leeuwen interactive meaning fields to `images[]`

**Current state:** `composition` is a free-text prose field ("framing, angle, contrast, key visual qualities"). This buries Kress & van Leeuwen's most systematic contribution — the interactive metafunction — inside unstructured prose.

**Revision:** Add three structured sub-fields alongside the existing `composition` prose.

```json
"interactive_meaning": {
  "type": "object",
  "description": "Kress & van Leeuwen's interactive metafunction: the relationship between depicted participant and viewer.",
  "properties": {
    "contact": {
      "type": "string",
      "enum": ["demand", "offer", "not_applicable"],
      "description": "Does the depicted participant gaze at the viewer (demand) or not (offer)? Not applicable for abstract/symbolic images."
    },
    "social_distance": {
      "type": "string",
      "enum": ["intimate", "close_social", "far_social", "impersonal", "not_applicable"],
      "description": "Implied distance: intimate (face/head only), close social (head and shoulders), far social (full figure), impersonal (many figures or wide view)."
    },
    "attitude_angle": {
      "type": "string",
      "enum": ["frontal", "oblique", "overhead", "low_angle", "not_applicable"],
      "description": "Viewer's implied orientation: frontal (involvement), oblique (detachment), overhead (viewer power), low angle (depicted power)."
    }
  }
}
```

**Impact on existing entries:** For spread_011's fingerprint: `contact: "not_applicable"`, `social_distance: "intimate"`, `attitude_angle: "frontal"`. For the bullseye: all `"not_applicable"` (abstract symbol). Many spreads containing photographs will benefit significantly — the interactive meaning fields capture what the current prose `composition` field captures inconsistently.

**Keep `composition` as-is:** The existing free-text field captures things the Kress-van Leeuwen framework doesn't (contrast, tonal quality, aesthetic qualities). Retain it alongside the structured fields.

---

### A4. Convert `rhetoric.rhetorical_strategy` to controlled vocabulary with primary/secondary structure

**Current state:** Free text with examples ("assertion, provocation, juxtaposition, accumulation, disruption, humor, sensory overload, quieting, etc.").

**Problem:** This is the single biggest reliability vulnerability in the schema. Two analysts will use different words for the same strategy, and the same word for different strategies. The working paper's Appendix B proposed a 15-term vocabulary; the schema should enforce it.

**Revision:**

```json
"rhetorical_strategy": {
  "type": "object",
  "properties": {
    "primary": {
      "type": "string",
      "enum": [
        "assertion", "confrontation", "juxtaposition", "accumulation",
        "disruption", "provocation", "invocation", "dramatization",
        "quieting", "sensory_overload", "humor", "demonstration",
        "interpellation", "defamiliarization", "call_and_response"
      ],
      "description": "The dominant rhetorical strategy on this spread."
    },
    "secondary": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "assertion", "confrontation", "juxtaposition", "accumulation",
          "disruption", "provocation", "invocation", "dramatization",
          "quieting", "sensory_overload", "humor", "demonstration",
          "interpellation", "defamiliarization", "call_and_response"
        ]
      },
      "maxItems": 2,
      "description": "Up to two secondary strategies operating simultaneously."
    }
  }
}
```

**Impact on existing entries:** Spread_011's "Confrontation" becomes `primary: "confrontation"`, `secondary: ["dramatization", "accumulation"]`. The existing prose description remains valuable and should be preserved — see A5 below.

---

### A5. Add `rhetoric.strategy_description` field

**Problem:** Converting `rhetorical_strategy` to a controlled vocabulary (A4) sacrifices the analytical prose that the current free-text field contains. Spread_011's current value is not just a label but a complete analytical paragraph: "The spread opens with aggressive interrogation questions... The pronoun 'you' — as both display text and repeated in the body — makes the reader the subject of surveillance, not a passive observer of it."

**Revision:** Add a dedicated prose description field that preserves the analytical content.

```json
"strategy_description": {
  "type": "string",
  "description": "Prose elaboration of how the rhetorical strategy operates on this spread. Required when primary strategy is 'confrontation', 'demonstration', 'interpellation', or 'defamiliarization'. Should name specific formal mechanisms."
}
```

This separates the *classifiable* component (the enum, testable for reliability) from the *analytical* component (the prose, evaluated for insight quality).

---

### A6. Add `rhetoric.multi_spread_patterns` field

**Current state:** The analysis instructions (claude_code_analysis_instructions.md) describe a Pass 2 task: "Add `rhetoric.multi_spread_patterns` (string or null): if this spread participates in a rhetorical sequence spanning multiple spreads, describe the pattern and which spreads are involved." But this field does not exist in the schema.

**Problem:** The instructions define a field the schema does not contain. This is a straightforward oversight that should be corrected.

**Revision:**

```json
"multi_spread_patterns": {
  "type": ["string", "null"],
  "description": "If this spread participates in a rhetorical pattern spanning multiple spreads (e.g., progressive density increase, dark/light alternation, thematic accumulation across 3+ spreads), describe the pattern and reference the spread IDs involved. Null if the spread operates independently."
}
```

---

### A7. Convert `mcluhan_concepts` from open array to enumeration

**Current state:** Free-text array with examples in the description. The description lists 10 concepts but the array accepts any string.

**Problem:** Without a closed vocabulary, analysts will use synonyms (`electric_age` vs. `electronic_information` vs. `electric_technology`), variant spellings, and idiosyncratic concept names. The methodology document does not include a concept vocabulary. Reliability will suffer.

**Revision:** Enumerate all McLuhan concepts relevant to *The Medium is the Massage*, drawing from the book's own vocabulary.

```json
"mcluhan_concepts": {
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "medium_is_the_message",
      "extensions_of_man",
      "global_village",
      "hot_and_cool",
      "rear_view_mirror",
      "figure_ground",
      "acoustic_space",
      "visual_space",
      "electric_age",
      "print_culture",
      "tribal",
      "pattern_recognition",
      "sense_ratios",
      "environment_as_invisible",
      "obsolescence_and_retrieval",
      "participation",
      "implosion",
      "anti_environment",
      "allatonceness"
    ]
  },
  "description": "Which McLuhan concepts are active on this spread. Select from the enumerated list."
}
```

The list should be finalized after Pass 1 of all 85 spreads, when the full range of concepts McLuhan deploys is known. A small `other` escape hatch (as an additional string field) could accommodate edge cases, but the primary array should be enumerated.

---

### A8. Add `design.information_value` structured field

**Current state:** The Given/New structure (Kress & van Leeuwen's information value) is captured implicitly in `left_right_relationship` but not explicitly named. The working paper's analysis of spread_011 identified this as a textbook Given-New structure, but this theoretical identification depends on the analyst's training — it is not prompted by the schema.

**Revision:** Add a structured field that explicitly solicits information value analysis.

```json
"information_value": {
  "type": "object",
  "description": "Kress & van Leeuwen's information value: the meaning carried by spatial placement on the spread.",
  "properties": {
    "left_right": {
      "type": "string",
      "enum": ["given_new", "new_given", "balanced", "single_page", "not_applicable"],
      "description": "Does the spread follow the conventional Given (left) / New (right) structure, reverse it, balance both sides equally, or operate as effectively a single page?"
    },
    "top_bottom": {
      "type": "string",
      "enum": ["ideal_real", "real_ideal", "balanced", "not_applicable"],
      "description": "Does the spread follow the Ideal (top) / Real (bottom) structure?"
    },
    "center_margin": {
      "type": "string",
      "enum": ["centered", "marginal", "distributed", "not_applicable"],
      "description": "Is there a dominant center with subordinate margins, or is information distributed?"
    }
  }
}
```

**Keep `left_right_relationship`** as a prose field alongside this. The structured field captures the *type* of compositional structure; the prose field captures the *specific content* of that structure ("The left page asks the question, the right page answers with the target").

**Impact on existing entries:** Spread_011 becomes `left_right: "given_new"`, `top_bottom: "ideal_real"` (the display text "you" at top is the conceptual/ideal, the body text below is the elaborated/real), `center_margin: "distributed"`.

---

### A9. Add confidence/certainty indicators to interpretive fields

**Current state:** No field in the schema records the analyst's confidence in their own judgment. Every entry presents its analysis with the same implicit certainty, whether the analyst is sure or guessing.

**Problem:** Reviewers will ask how the analysts handled ambiguity. The methodology document acknowledges uncertainty in the quality checklist ("notes include any cross-references, credits, or uncertainties") but this is a catch-all rather than a systematic approach. For reliability testing, knowing *which* judgments analysts found difficult is as valuable as the judgments themselves.

**Revision:** Add an optional `confidence` field to the three most interpretive sections.

```json
"confidence": {
  "type": "string",
  "enum": ["high", "moderate", "low"],
  "description": "Analyst's self-reported confidence in this section's analysis. 'high' = unambiguous, any competent analyst would agree. 'moderate' = reasonable alternatives exist. 'low' = best guess, significant uncertainty."
}
```

Add this to `rhetoric`, `themes`, and `progression` objects. Do not add it to `text`, `images`, or `design` — those sections are primarily descriptive and confidence is better captured by flagging specific uncertain transcriptions in `notes`.

**Methodological value:** This data enables a correlation analysis between self-reported confidence and actual inter-rater agreement, testing whether analysts can accurately predict where disagreement will occur.

---

### A10. Add `design.compositional_framing` field

**Current state:** Kress and van Leeuwen's three compositional systems are information value (partially captured — see A8), salience (partially captured in `visual_density` and the prose `layout_description`), and framing (not captured at all).

**Problem:** Framing — how strongly elements are connected or disconnected through frames, vectors, color continuity, spatial separation, or gutter — is central to how spreads create meaning, particularly across the gutter that divides left and right pages. In *The Medium is the Massage*, Fiore deliberately manipulates gutter-crossing to merge or separate content. This is not captured anywhere in the current schema.

**Revision:**

```json
"compositional_framing": {
  "type": "string",
  "enum": ["strongly_framed", "weakly_framed", "mixed"],
  "description": "Kress & van Leeuwen's framing: how strongly elements on the spread are separated from one another. 'Strongly framed' = clear boundaries between elements (frames, white space, color breaks). 'Weakly framed' = elements flow into one another (overlaps, shared backgrounds, cross-gutter continuity). 'Mixed' = some elements framed, others flowing."
}
```

---

### A11. Revise `spread_type` with boundary decision rules

**Current state:** 13-value enumeration with no definitions beyond the enum labels themselves. The schema description for the `spread_type` field is simply "The dominant compositional mode of this spread."

**Problem identified in working paper Section 2.4:** The boundary between `text_with_mood_image` and `text_with_specific_image` requires distinguishing whether an image provides "atmosphere" or makes a "specific" point. The boundary between `image_dominant` and `text_with_specific_image` depends on an area threshold. Without definitions, two coders will classify the same spread differently.

**Revision:** Add a `description` property for each enum value within the JSON Schema, or — since JSON Schema's `enum` doesn't natively support per-value descriptions — add a companion field:

```json
"spread_type": {
  "type": "string",
  "enum": [ /* existing 13 values */ ],
  "description": "The dominant compositional mode. Classification rules: 'image_dominant' = image occupies >=70% of spread area AND text is subordinate (captions, small overlaid text only). 'text_with_specific_image' = substantial text paragraph + image that makes a specific claim related to the text content. 'text_with_mood_image' = substantial text + image that establishes tone without specific referential content. 'typography_as_design' = text IS the visual content (no separate images; typographic form carries the argument). 'collage' = 3+ distinct visual elements from different sources combined on a single spread. 'symbol_or_graphic' = abstract or symbolic visual element dominates (no photographic content). 'quote_only' = attributed quotation with no body text by the authors."
}
```

The full decision rules from Appendix C of the working paper should be incorporated into the methodology document's codebook section.

---

### A12. Minor schema field refinements

**`design.white_space` and `design.visual_density` — add percentage guidelines to descriptions:**
These ordinal scales currently have no anchoring. Revise descriptions to include the thresholds proposed in the working paper's codebook rules (white_space: abundant ≥40%, moderate 15–40%, minimal 5–15%, none <5%). Note that these are estimates, not measurements — but providing numeric ranges anchors the ordinal scale and improves reliability.

**`design.color_and_tone` — convert to structured object:**
Currently a prose field that mixes two distinct properties: chromatic information (this is a black-and-white book, so always monochrome, but the ratio of black to white varies significantly) and contrast level. Splitting these improves both precision and reliability:

```json
"color_and_tone": {
  "type": "object",
  "properties": {
    "contrast": {
      "type": "string",
      "enum": ["high", "moderate", "low"],
      "description": "Degree of tonal contrast between darkest and lightest areas."
    },
    "dominant_tone": {
      "type": "string",
      "enum": ["dark", "light", "balanced"],
      "description": "Whether the spread reads as predominantly dark, predominantly light, or balanced."
    },
    "description": {
      "type": "string",
      "description": "Optional prose elaboration for unusual tonal treatments."
    }
  }
}
```

**`progression.pace_shift` — add relative anchor to description:**
Current description says "relative to preceding spreads" but does not specify how many. A single preceding spread? The last three? The overall trend? Revise: "relative to the immediately preceding spread (spread N-1). Consider: amount of text, number of visual elements, visual density, and demand on reader attention."

---

## B. Methodology Revisions (phase_b_methodology v1.0 → v2.0)

### B1. Add a formal Codebook section

**Current state:** The methodology document contains "guiding questions" for themes and progression, and a quality checklist. These function as an informal codebook but are not structured as one.

**Problem:** A journal paper presenting this schema as a methodological contribution must include or reference a codebook — the document that defines every analytical category and provides decision rules for ambiguous cases. The guiding questions are excellent raw material but need formalization.

**Required addition:** A new section titled "Codebook: Decision Rules for Ambiguous Classifications" containing:

1. Definitions and exemplars for every enum value in the schema (all spread_types, all relationship_to_text values, all rhetorical_strategy values, all information_value structures).
2. Boundary decision rules for adjacent categories on ordinal scales (working paper Appendix C provides five initial rules — expand to cover all ordinal fields).
3. Positive and negative exemplars for the `design_enacts_argument` boolean, including the "form-only test" proposed in the working paper: "If you could not read the text, would the design alone communicate something related to the argument? If yes, assign `true`."
4. A vocabulary consistency index for `original_themes` — a maintained list of all theme tags used across the database, updated as new tags are introduced, with definitions for each.

### B2. Add an inter-rater reliability protocol

**Current state:** The methodology describes a single-analyst workflow. No procedure for reliability testing exists.

**Required addition:** A new section titled "Inter-Rater Reliability Protocol" specifying:

1. **Coder recruitment criteria:** Graduate-level training in graphic design, visual communication, rhetoric, or media studies. Not McLuhan specialists (to test schema generalizability).
2. **Sample stratification:** 15–20 spreads, minimum one instance of each major spread_type.
3. **Calibration procedure:** Three rounds (described in working paper Section 2.3). Specify that calibration spreads are drawn from the full 85 and excluded from the final reliability sample.
4. **Measurement specification:** Field-by-field, which variant of α applies — nominal α for enum fields, ordinal α for ranked scales, set-Jaccard α for multi-label fields. For open-text fields, specify the decomposition or expert-panel method.
5. **Threshold acceptance criteria:** α ≥ 0.80 for Tier 1 fields, α ≥ 0.75 for Tier 2, α ≥ 0.60 for Tier 3. Fields failing threshold → revise codebook and recalibrate.
6. **Reporting format:** Table of field-level α values with 95% bootstrap confidence intervals.

### B3. Add a VLM validation protocol

**Current state:** The methodology describes a "VLM correlation strategy" — two independent VLMs whose agreement increases confidence. But this is qualitative ("Where the two models agree, confidence is high. Where they diverge, Claude performs manual arbitration"). The Technical Notes document a quantitative model comparison (Qwen2.5-VL vs Qwen3-VL) but only for OCR accuracy, not for analytical field agreement.

**Required additions:**

1. **OCR accuracy metrics:** Compute Character Error Rate (CER) and Word Error Rate (WER) for Qwen3-VL OCR against human-verified transcriptions across all 85 spreads. Report as a table stratified by text type (body text, display text, quotations, captions) and spread characteristics (dense serif, large sans, text-on-image).

2. **VLM-as-rater protocol for categorical fields:** Prompt a vision-language model to independently classify `spread_type`, `white_space`, `visual_density`, `images[].scale`, `images[].source_type`, and the new `information_value` fields for the reliability sample. Compute α between VLM and human analyst, treating the VLM as an additional coder.

3. **LLM-as-Judge protocol for interpretive fields:** For Tier 3–4 fields, present a separate LLM with the spread image and two independent analyses (human + human, or human + LLM), and ask it to rate agreement and identify divergence points. Report ICC(3,k) as primary metric, α and Gwet's AC2 as secondary.

### B4. Add explicit perception/interpretation separation

**Current state:** The field-by-field methodology table classifies each field by "Primary Method" (Automated, Manual cross-reference, VLM OCR, Visual analysis, Interpretive analysis, etc.) but does not explicitly distinguish between *perceptual* tasks (what is on the page?) and *interpretive* tasks (what does it mean?).

**Problem:** This distinction is fundamental to both reliability (perceptual tasks should achieve higher α) and theoretical framing (the schema bridges document AI's perceptual capabilities with humanistic interpretive analysis). Making it explicit strengthens both.

**Required addition:** Add a column to the field-by-field methodology table:

| Field | Primary Method | Tool(s) | Analytical Level | Notes |
|---|---|---|---|---|
| `text.body_text` | VLM OCR | Qwen3-VL | **Perception** | Raw text extraction |
| `images[].subject` | VLM + interpretive | Qwen3-VL + Claude | **Perception + identification** | VLM describes, Claude contextualizes |
| `images[].relationship_to_text` | Interpretive analysis | Claude | **Interpretation** | Requires rhetorical judgment |
| `rhetoric.argument` | Interpretive analysis | Claude | **Interpretation** | Core analytical work |
| `rhetoric.design_enacts_argument` | Interpretive analysis | Claude | **Theoretical judgment** | Requires Drucker's framework |

The four levels — Perception, Identification, Interpretation, Theoretical Judgment — map to increasingly theory-dependent analytical operations and to the reliability tiers.

### B5. Add theoretical grounding statements to guiding questions

**Current state:** The guiding questions for themes and progression are analytically rigorous but theoretically implicit. They ask the right questions without naming the theoretical frameworks that motivate those questions.

**Problem:** A journal reviewer will ask: "Why these questions and not others? What theory generates this analytical protocol?" The guiding questions are currently vulnerable to the charge of being ad hoc.

**Required additions** (examples — apply the pattern to all guiding question sets):

*Before the `original_themes` guiding questions, add:*
"Theme identification follows Kress and van Leeuwen's compositional metafunction (what the spread's formal properties foreground) and Barthes' principle that images are polysemous and require thematic anchoring. The analyst's task is to identify what the spread's compositional salience structure makes prominent, not to impose a theme from external knowledge."

*Before the `progression` guiding questions, add:*
"Progression analysis operationalizes Bateman's GeM navigation layer: how the document guides reading paths across its sequence. The `pace_shift` field adapts Genette's narrative duration (the ratio between story time and discourse time) to visual rhetoric: a spread that demands prolonged attention 'decelerates'; one that can be absorbed at a glance 'accelerates.' The `thematic_function` field adapts Barthes' narrative functions (S/Z) to non-narrative argumentative structures."

*Before the `design_enacts_argument` quality checklist item, add:*
"This field operationalizes Drucker's (2014) distinction between representational and performative visualization. The test is formal, not semantic: does the visual form itself — independent of the text's propositional content — produce an experience isomorphic to the argument? If a spread argues for disruption, does its layout disrupt? If it argues for intimacy, does its scale create closeness?"

### B6. Add a versioned vocabulary registry

**Current state:** The methodology asks analysts to "use consistent vocabulary across all 85 spreads" for `original_themes` and provides a non-exhaustive starter list of 24 terms. But there is no maintained, versioned registry that accumulates new terms as analysis proceeds.

**Problem:** Over 85 spreads, the vocabulary will drift. Early spreads may use `electric_information` while later spreads use `electronic_media` for the same concept. Without a registry, cleaning this requires a retrospective normalization pass.

**Required addition:** Maintain a living `theme_vocabulary.json` file in the repository:

```json
{
  "version": "1.0",
  "updated": "2026-03-02",
  "terms": {
    "privacy": {
      "definition": "The condition of being unobserved; control over personal information",
      "first_used": "spread_011",
      "related_terms": ["surveillance", "public_private_collapse"]
    },
    "surveillance": {
      "definition": "Systematic observation by institutions or technologies",
      "first_used": "spread_011",
      "related_terms": ["privacy", "electric_information"]
    }
  }
}
```

Update this file after each batch of spread analyses. At the completion of all 85 spreads, normalize any inconsistencies before computing distributional statistics.

### B7. Expand quality checklist with theory-aligned items

**Current state:** 13-item checklist. Covers accuracy (OCR, attribution, image description), analytical substance (argument not just description, mapping earned not forced), and consistency (vocabulary, encoding).

**Missing items (add to checklist):**

- [ ] `images[].interactive_meaning` fields populated for all photographic images (Kress & van Leeuwen)
- [ ] `images[].relationship_to_text.barthes_mode` assigned for all images (Barthes)
- [ ] `design.information_value.left_right` assigned for all landscape spreads (Kress & van Leeuwen)
- [ ] `rhetoric.rhetorical_strategy.primary` selected from controlled vocabulary
- [ ] `rhetoric.design_enacts_argument` passes the form-only test (Drucker): would the design communicate the argument's essence without readable text?
- [ ] `rhetoric.confidence` self-assessment recorded
- [ ] `progression.pace_shift` assessed relative to immediately preceding spread (not global trend)
- [ ] If `design_enacts_argument` is `true`, `rhetorical_strategy.secondary` includes `"demonstration"`
- [ ] New theme tags added to `theme_vocabulary.json` with definition and first-use reference

---

## C. Sample Entry Revisions (spread_011)

The gold-standard sample entry must be updated to demonstrate the revised schema. Key changes:

### C1. Restructure `images[].relationship_to_text`

**Current (fingerprint):**
```json
"relationship_to_text": "Literalizes the theme of individual identity under surveillance..."
```

**Revised:**
```json
"relationship_to_text": {
  "primary_relation": "literalizes",
  "barthes_mode": "relay",
  "description": "Literalizes the theme of individual identity under surveillance. The fingerprint is the most basic biometric identifier — the thing that makes 'you' uniquely trackable. Placed right next to text about dossier banks and surveillance, it concretizes the abstract threat."
}
```

### C2. Add `interactive_meaning` to both images

**Fingerprint:**
```json
"interactive_meaning": {
  "contact": "not_applicable",
  "social_distance": "intimate",
  "attitude_angle": "frontal"
}
```

**Bullseye:**
```json
"interactive_meaning": {
  "contact": "demand",
  "social_distance": "impersonal",
  "attitude_angle": "frontal"
}
```

Note: the bullseye is classified as `contact: "demand"` despite being abstract. The concentric circles create an "eye" effect that appears to look at the viewer — this is a borderline case that should be documented in the codebook as an example of symbolic demand.

### C3. Restructure `rhetoric.rhetorical_strategy`

**Current:**
```json
"rhetorical_strategy": "Confrontation. The spread opens with aggressive interrogation questions..."
```

**Revised:**
```json
"rhetorical_strategy": {
  "primary": "confrontation",
  "secondary": ["dramatization", "accumulation"]
},
"strategy_description": "The spread opens with aggressive interrogation questions ('How much do you make? Have you ever contemplated suicide?') that mimic the invasive questioning of surveillance systems. The pronoun 'you' — as both display text and repeated in the body — makes the reader the subject of surveillance, not a passive observer of it."
```

### C4. Add `information_value`, `compositional_framing`

```json
"information_value": {
  "left_right": "given_new",
  "top_bottom": "ideal_real",
  "center_margin": "distributed"
},
"compositional_framing": "weakly_framed"
```

Weakly framed because the fingerprint, text, and "you" flow together without strong borders, and the bullseye bleeds to the page edge — the only strong frame is the gutter itself.

### C5. Add `multi_spread_patterns`, `confidence`, `analyst`

```json
"multi_spread_patterns": null,
"confidence": "high",
"analyst": "claude-opus-4-6",
"analysis_method": "llm_primary_human_reviewed"
```

### C6. Enumerate `mcluhan_concepts`

Verify that all three current values exist in the new enumeration. They do: `electric_age`, `global_village`, `pattern_recognition`. Consider adding `environment_as_invisible` (the surveillance apparatus is the invisible environment) and `figure_ground` (the spread makes the usually-invisible surveillance infrastructure visible as figure).

### C7. Restructure `color_and_tone`

**Current:** `"High contrast throughout. The right page is especially stark — pure black and white with no gray tones."`

**Revised:**
```json
"color_and_tone": {
  "contrast": "high",
  "dominant_tone": "balanced",
  "description": "The right page is especially stark — pure black and white with no gray tones."
}
```

---

## D. Revision Priority and Sequencing

Not all revisions need to happen simultaneously. The following priority ordering minimizes disruption to the 10 existing entries while preparing for publication:

**Priority 1 — Before analyzing spreads 011–085:**
- A4 (controlled rhetorical strategy vocabulary) — highest reliability impact
- A5 (strategy_description field)
- A6 (multi_spread_patterns — already referenced in analysis instructions)
- A7 (enumerated mcluhan_concepts)
- A11 (spread_type boundary rules in descriptions)
- B1 (codebook decision rules)

**Priority 2 — Before reliability testing:**
- A2 (structured relationship_to_text with Barthes mode)
- A3 (interactive_meaning fields)
- A8 (information_value)
- A9 (confidence indicators)
- A12 (ordinal scale anchoring, color_and_tone restructure)
- B2 (inter-rater reliability protocol)
- B4 (perception/interpretation level column)
- B6 (theme vocabulary registry)

**Priority 3 — Before paper submission:**
- A1 (metadata fields)
- A10 (compositional_framing)
- B3 (VLM validation protocol with quantitative metrics)
- B5 (theoretical grounding statements)
- B7 (expanded quality checklist)
- C1–C7 (sample entry updates)

**Retroactive work required:** All 10 existing entries (spreads 001–010) will need to be updated to v1.2 schema structure after Priority 1 revisions. This is a one-time migration: add the new fields, restructure the modified fields, verify existing values map to the new enumerations. Estimated effort: 30–60 minutes per entry, or 5–10 hours total. Should be done before continuing to spread 011, so the entire database is internally consistent.

---

*This document supersedes the revision notes in the visual rhetoric working paper's appendices. All codebook rules proposed there are incorporated here by reference.*
