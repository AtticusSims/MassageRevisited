# Phase B: Analysis Methodology (v2.0)

## Overview

Each spread in *The Medium is the Massage* receives a structured JSON entry per `analysis_schema_v1.2.json`. This document describes the methodology used for each field, the tools involved, the theoretical framework grounding the interpretive work, codebook decision rules for ambiguous classifications, and guiding questions for the sections that require the most analytical rigor.

### What Changed in v2.0

This revision upgrades the methodology from v1.0 (which accompanied schema v1.1 and batch 1) to align with three developments:

1. **Schema upgrade to v1.2.** New fields: `images[].interactive_meaning`, `images[].relationship_to_text` (restructured from free text to controlled vocabulary + Barthes mode), `design.information_value`, `design.compositional_framing`, `design.color_and_tone` (restructured), `rhetoric.rhetorical_strategy` (controlled vocabulary with primary/secondary), `rhetoric.strategy_description`, `rhetoric.multi_spread_patterns`, `rhetoric.confidence`, per-entry `analyst` and `analysis_method`, enumerated `mcluhan_concepts`. See `schema_methodology_revisions.md` for the full change log.

2. **Theoretical grounding.** The visual rhetoric working paper (`visual_rhetoric_and_reliability.md`) established that the schema operationalizes four bodies of theory: Kress & van Leeuwen's visual grammar, Barthes/Martinec-Salway's image-text relations, Drucker's performative design, and Bateman's GeM framework. This methodology now names the theoretical warrant for each interpretive field, giving analysts a framework for their judgments and giving reviewers a basis for evaluating them.

3. **Planning-phase foresight.** The downstream Planning Engine (Step 5) will read the analysis database and use specific fields to generate contemporary equivalents. Fields that the Planning Engine reads are marked with ⚡ in the methodology table. Getting these right during analysis directly affects the quality of the book plan.

### Guiding Principle

The theoretical vocabulary exists to make the analyst *more precise*, not more bureaucratic. When the methodology says "classify using Kress & van Leeuwen's contact variable," it means: "does the depicted participant look at the viewer or not?" That's a concrete visual question with a concrete answer. The theory gives it a name (`demand` vs. `offer`) so that the same judgment gets the same label across all 85 spreads.

---

## Field-by-Field Methodology

### Analytical Levels

Every field operates at one of four levels, from least to most interpretive:

| Level | Definition | Expected Reliability | Example Fields |
|---|---|---|---|
| **Perception** | What is physically present on the page. Answerable from the image alone. | α ≥ 0.90 | `text.body_text`, `images[].position`, `images[].scale` |
| **Identification** | What the perceived elements *are* — classifying, naming, dating. Requires knowledge beyond the image. | α ≥ 0.80 | `images[].source_type`, `quotations[].author`, `spread_type` |
| **Interpretation** | What the elements *mean* — how they function rhetorically, what argument they advance. Requires analytical judgment. | α ≥ 0.70 | `images[].relationship_to_text`, `rhetoric.argument`, `themes.mapping_rationale` |
| **Theoretical Judgment** | Whether a specific theoretical construct applies. Requires familiarity with the relevant framework. | α ≥ 0.60 | `rhetoric.design_enacts_argument`, `rhetoric.rhetorical_strategy`, `design.information_value` |

Analysts should expect near-perfect agreement on Perception fields, substantial agreement on Identification, and legitimate disagreement on Interpretation and Theoretical Judgment. Disagreement at the higher levels is not failure — it signals where the codebook needs refinement.

### Field Table

Fields marked ⚡ are read by the Planning Engine in Step 5.

| Field | Level | Primary Method | Tool(s) | Theoretical Warrant | Notes |
|---|---|---|---|---|---|
| `id`, `pdf_page` | — | Automated | Script | — | Sequential from PDF page number |
| `book_pages` | Perception | Manual cross-reference | Claude + visual | — | Checked against visible page numbers |
| `section` | Identification | Manual classification | Claude | — | `front_matter`, `body`, `back_matter` |
| `spread_type` ⚡ | Identification | Manual classification | Claude + VLM | GeM base layer | See Codebook Rule 1 for boundary decisions |
| `orientation` | Perception | Visual inspection | Claude | — | From image dimensions and content |
| `analyst` | — | Manual | — | — | Identifier: human name, model ID, or `multi` |
| `analysis_method` | — | Manual | — | — | `human_only`, `vlm_assisted`, `llm_primary_human_reviewed`, `multi_model` |
| | | | | | |
| **Text** | | | | | |
| `text.body_text` | Perception | VLM OCR | Qwen3-VL (via Ollama) | — | Raw extraction, spot-checked against images |
| `text.display_text` ⚡ | Perception | VLM OCR + manual | Qwen3-VL + Claude | Lupton: typography as meaning | Large/display text identified from OCR, verified visually |
| `text.captions` | Perception | VLM OCR + manual | Qwen3-VL + Claude | — | Separated from body text during analysis |
| `text.page_numbers_visible` | Perception | Visual inspection | Claude | — | Checked against rendered image |
| | | | | | |
| **Quotations** | | | | | |
| `quotations[].text` | Perception | VLM OCR + verification | Qwen3-VL + Claude | — | Verified against known sources where possible |
| `quotations[].author` | Identification | Research + OCR | Claude | — | From attribution on page or research |
| `quotations[].author_context` | Identification | Research | Claude | — | Historical/biographical context |
| `quotations[].source_work` | Identification | Research | Claude | — | Source identification (sometimes speculative — note uncertainty) |
| `quotations[].relationship_to_argument` ⚡ | Interpretation | Interpretive analysis | Claude | Foss: visual rhetoric | How the quote functions in the spread's argument |
| `quotations[].visual_treatment` | Perception + Interpretation | Visual analysis | Claude + VLM | Lupton: typography as meaning | How the quote is typographically presented |
| | | | | | |
| **Images** | | | | | |
| `images[].position` | Perception | Visual analysis | Claude + VLM | — | Spatial location on spread |
| `images[].subject` | Identification | VLM + interpretive | Qwen3-VL + Claude | Kress & van Leeuwen: representational | VLM describes, Claude refines and contextualizes |
| `images[].source_type` | Identification | Classification | Claude | Genre theory | Enum from schema. See source type guidance below |
| `images[].source_credit` | Identification | Cross-reference | Claude + `image_credits_lookup.json` | — | Matched page numbers to credit database |
| `images[].estimated_date` | Identification | Research | Claude | — | Approximate date or era, if determinable |
| `images[].composition` | Perception + Interpretation | Visual analysis | Claude + VLM | Kress & van Leeuwen: interactive | Framing, angle, contrast, key visual qualities |
| `images[].interactive_meaning.contact` | Theoretical Judgment | Visual analysis | Claude | Kress & van Leeuwen: interactive | `demand` (gaze at viewer), `offer` (no gaze), `not_applicable` |
| `images[].interactive_meaning.social_distance` | Theoretical Judgment | Visual analysis | Claude | Kress & van Leeuwen: interactive | `intimate`, `close_social`, `far_social`, `impersonal`, `not_applicable` |
| `images[].interactive_meaning.attitude_angle` | Theoretical Judgment | Visual analysis | Claude | Kress & van Leeuwen: interactive | `frontal`, `oblique`, `overhead`, `low_angle`, `not_applicable` |
| `images[].scale` | Perception | Visual analysis | Claude | Kress & van Leeuwen: interactive (social distance via page area) | `full_bleed`, `dominant`, `half_page`, `quarter_page`, `small_inset`, `icon` |
| `images[].relationship_to_text.primary_relation` ⚡ | Interpretation | Interpretive analysis | Claude | Barthes; Martinec & Salway | Controlled vocabulary: `illustrates`, `amplifies`, `literalizes`, `contradicts`, `ironizes`, `provides_atmosphere`, `serves_as_metaphor`, `extends`, `independent`, `decorative` |
| `images[].relationship_to_text.barthes_mode` | Theoretical Judgment | Interpretive analysis | Claude | Barthes 1977 | `anchorage` (text fixes image meaning), `relay` (complementary), `neither` |
| `images[].relationship_to_text.description` ⚡ | Interpretation | Interpretive analysis | Claude | — | Prose elaboration. Required when primary_relation is `contradicts`, `ironizes`, `literalizes`, or `serves_as_metaphor` |
| | | | | | |
| **Design** | | | | | |
| `design.layout_description` | Perception + Interpretation | Visual analysis | Claude + VLM | Kress & van Leeuwen: compositional | Prose description of spatial arrangement |
| `design.typography.body_font_style` | Perception | Visual analysis | Claude + VLM | Lupton | Serif/sans, approximate size, weight, column width, justification |
| `design.typography.display_font_style` | Perception | Visual analysis | Claude + VLM | Lupton | Typography of display/headline text if present |
| `design.typography.special_treatments` | Perception | Visual analysis | Claude + VLM | Lupton; Drucker: *The Visible Word* | Unusual typographic choices (reversed, rotated, overlaid, etc.) |
| `design.color_and_tone.contrast` | Perception | Visual analysis | Claude | Kress & van Leeuwen: compositional (salience) | `high`, `moderate`, `low` |
| `design.color_and_tone.dominant_tone` | Perception | Visual analysis | Claude | Kress & van Leeuwen: compositional | `dark`, `light`, `balanced` |
| `design.color_and_tone.description` | Perception | Visual analysis | Claude | — | Optional prose for unusual tonal treatments |
| `design.white_space` | Perception | Visual analysis | Claude | Kress & van Leeuwen: compositional (framing) | See Codebook Rule 2 for thresholds |
| `design.visual_density` | Perception | Visual analysis | Claude | Kress & van Leeuwen: compositional (salience) | `sparse`, `moderate`, `dense`, `overwhelming` |
| `design.information_value.left_right` | Theoretical Judgment | Visual analysis | Claude | Kress & van Leeuwen: compositional (information value) | `given_new`, `new_given`, `balanced`, `single_page`, `not_applicable` |
| `design.information_value.top_bottom` | Theoretical Judgment | Visual analysis | Claude | Kress & van Leeuwen: compositional | `ideal_real`, `real_ideal`, `balanced`, `not_applicable` |
| `design.information_value.center_margin` | Theoretical Judgment | Visual analysis | Claude | Kress & van Leeuwen: compositional | `centered`, `marginal`, `distributed`, `not_applicable` |
| `design.compositional_framing` | Theoretical Judgment | Visual analysis | Claude | Kress & van Leeuwen: compositional (framing) | `strongly_framed`, `weakly_framed`, `mixed`. See Codebook Rule 6 |
| `design.left_right_relationship` ⚡ | Interpretation | Visual analysis | Claude | Kress & van Leeuwen: compositional | Prose describing how left and right pages relate |
| | | | | | |
| **Rhetoric** | | | | | |
| `rhetoric.argument` ⚡ | Interpretation | Interpretive analysis | Claude | Foss: visual rhetoric | Core argument stated plainly |
| `rhetoric.rhetorical_strategy.primary` ⚡ | Theoretical Judgment | Interpretive analysis | Claude | Foss; classical rhetoric | From controlled vocabulary (15 terms). See Appendix A |
| `rhetoric.rhetorical_strategy.secondary` | Theoretical Judgment | Interpretive analysis | Claude | Foss; classical rhetoric | Up to 2 secondary strategies from same vocabulary |
| `rhetoric.strategy_description` ⚡ | Interpretation | Interpretive analysis | Claude | — | Prose elaboration of how the strategy operates on this spread |
| `rhetoric.design_enacts_argument` ⚡ | Theoretical Judgment | Interpretive analysis | Claude | Drucker: performative design | Boolean. See Codebook Rule 3. The most important analytical judgment in the schema |
| `rhetoric.design_argument_description` ⚡ | Interpretation | Interpretive analysis | Claude | Drucker | If `true`, explain the mechanism. The most valuable analytical insight |
| `rhetoric.reader_experience` ⚡ | Interpretation | Interpretive analysis | Claude | Reception aesthetics (Iser) | Intended effect on the reader |
| `rhetoric.mcluhan_concepts` | Identification | Interpretive analysis | Claude | McLuhan | From enumerated list. See schema for full vocabulary |
| `rhetoric.multi_spread_patterns` | Interpretation | Interpretive analysis | Claude | GeM: navigation layer | Patterns spanning multiple spreads. Null if independent |
| `rhetoric.confidence` | — | Self-assessment | Analyst | — | `high`, `moderate`, `low`. Analyst's own certainty |
| | | | | | |
| **Themes** | | | | | |
| `themes.original_themes` | Interpretation | Interpretive analysis | Claude | — | Free-text tags. See Theme Vocabulary Registry |
| `themes.contemporary_domain_candidates` ⚡ | Interpretation | Interpretive analysis | Claude | — | From 12-domain enum. See guiding questions below |
| `themes.movement_mapping` ⚡ | Interpretation | Interpretive analysis | Claude | — | From 5-movement enum. See guiding questions below |
| `themes.mapping_rationale` ⚡ | Interpretation | Interpretive analysis | Claude | — | Conceptual bridge. See guiding questions below |
| | | | | | |
| **Progression** | | | | | |
| `progression.pace_shift` | Interpretation | Interpretive analysis | Claude | Genette: narrative duration | Relative to immediately preceding spread |
| `progression.thematic_function` | Interpretation | Interpretive analysis | Claude | Barthes: narrative functions | Role in thematic arc |
| `progression.relationship_to_previous` | Interpretation | Interpretive analysis | Claude | GeM: navigation layer | Specific cross-reference to previous spread's content |
| `progression.relationship_to_next` | Interpretation | Interpretive analysis | Claude | GeM: navigation layer | Specific cross-reference to next spread's setup |
| | | | | | |
| `notes` | — | Research + observation | Claude | — | Cross-references, uncertainties, contextual detail |

### VLM Pipeline

**Primary VLM: Qwen3-VL** (via Ollama, `qwen3-vl`, 6.1 GB). Handles all VLM tasks: OCR (raw + structured), image description, and layout analysis. Dramatic quality improvement over Qwen2.5-VL on dense serif text (see `TECHNICAL_NOTES.md` for evaluation data). Accepts 2–7× speed penalty for significantly higher accuracy.

**Orchestration: Claude Opus 4.6** (via Claude Code CLI). All interpretive analysis, cross-referencing, theme mapping, progression tracking, and quality assurance. Claude also performs manual arbitration when VLM output is ambiguous or incomplete.

**Retired:** Qwen2.5-VL-7B (archived — replaced by Qwen3-VL). Molmo2-8B (archived — inconsistent quality; see `TECHNICAL_NOTES.md`).

**OCR protocol per spread:**
1. Run raw OCR (Qwen3-VL) — captures all text, preserving exact wording
2. Run structured OCR (Qwen3-VL) — categorizes text by function (DISPLAY_TEXT, BODY_TEXT, QUOTATIONS, CAPTIONS, PAGE_NUMBERS)
3. If raw OCR returns empty, retry once (Qwen3-VL occasionally returns empty responses nondeterministically)
4. Claude spot-checks extracted text against rendered image, corrects errors
5. Structured OCR categories map directly to schema text fields

**Inference parameters:** temperature 0.1 (low for faithful transcription), num_predict 4096 (high for dense text spreads), timeout 300s.

---

## Codebook: Decision Rules for Ambiguous Classifications

These rules resolve anticipated boundary cases. Apply them before finalizing any entry. Rules are numbered for cross-reference from the quality checklist.

### Rule 1: `spread_type` Boundaries

The `spread_type` field classifies the dominant compositional mode. When a spread could plausibly fit multiple types, apply these decision rules:

| If the spread contains... | And... | Then classify as... |
|---|---|---|
| Text + image | Image occupies ≥70% of spread area AND text is subordinate (captions, small overlay only) | `image_dominant` |
| Text + image | Text constitutes a substantial paragraph or argument AND image makes a specific claim related to the text | `text_with_specific_image` |
| Text + image | Text constitutes a substantial paragraph or argument AND image establishes tone without specific referential content | `text_with_mood_image` |
| Text as primary visual content | No separate photographic/illustrative images; the typographic form IS the visual content | `typography_as_design` |
| 3+ distinct visual elements from different sources | Elements combined on a single spread | `collage` |
| Abstract or symbolic visual element | No photographic content; graphic dominates | `symbol_or_graphic` |
| Attributed quotation | No body text by the authors | `quote_only` |

**Test for `text_with_mood_image` vs. `text_with_specific_image`:** Does the image make a claim that could be stated as a proposition? If yes → `specific`. If the image creates an atmosphere or emotional quality without making a specific point → `mood`. A fingerprint next to surveillance text = specific (the fingerprint *claims* "you are identifiable"). A blurred cityscape next to the same text = mood (it *evokes* without claiming).

### Rule 2: `white_space` Thresholds

Estimate visually — do not measure precisely.

| Classification | Approximate Threshold | Description |
|---|---|---|
| `abundant` | ≥40% of spread area is empty | The spread breathes; elements float in space |
| `moderate` | 15–40% empty | Breathing room between elements but no vast emptiness |
| `minimal` | 5–15% empty | Elements are tightly packed; margins are narrow |
| `none` | <5% empty | The spread is saturated edge-to-edge |

White space includes margins, gutters, and space between elements. It does NOT include the interior of large solid-fill images (a full-bleed black photograph has `none` white space even though the image itself has dark areas).

### Rule 3: `design_enacts_argument` (The Form-Only Test)

This is the most important analytical judgment in the schema. It operationalizes Drucker's (2014) distinction between representational and performative design.

**The test:** If you could not read the text, would the design alone communicate something related to the argument?

| If... | Then... |
|---|---|
| A spread argues for disruption AND the layout is disrupted (broken columns, overlapping elements, rotated text) | `true` — the form performs the argument |
| A spread argues for disruption BUT the layout is calm and orderly | `false` — the form represents the argument conventionally |
| A spread argues for surveillance AND the design targets/addresses the reader (giant "you," bullseye, direct gaze) | `true` — the reader experiences being surveilled |
| A spread argues for surveillance AND the design shows a photograph of a camera | `false` — the design illustrates the argument; it doesn't enact it |

**Calibration:** Err on the side of `false`. The insight is more valuable when reserved for spreads where the design genuinely performs. Over-assigning `true` dilutes the field's analytical power.

When `true`, the paired `design_argument_description` field must name the *mechanism* — not "the design feels surveillance-y" but "the giant 'you' singles the reader out, the fingerprint identifies them, the bullseye targets them."

When `true`, `rhetorical_strategy.secondary` should include `demonstration` (see Appendix A).

### Rule 4: `relationship_to_text` Vocabulary

Use the most specific applicable term from the controlled vocabulary:

| Term | Use when... | Barthes mode |
|---|---|---|
| `illustrates` | Image restates what the text already says, in visual form. No new information. | Anchorage |
| `amplifies` | Image intensifies the text's claim beyond what the text alone states. The effect is *more* with the image than without. | Relay |
| `literalizes` | Image makes a textual metaphor concrete. The text discusses surveillance abstractly; the image is a fingerprint. The image doesn't add information — it materializes the abstract. | Relay |
| `contradicts` | Image undermines or opposes the text's claim. Straightforward opposition. | Relay |
| `ironizes` | Image reframes the text's claim as absurd, self-defeating, or more complex than stated. Self-aware commentary on the contradiction. | Relay |
| `provides_atmosphere` | Image establishes mood, tone, or emotional quality without making a specific claim. Could accompany many different texts. | Anchorage (weak) |
| `serves_as_metaphor` | Image provides a figurative parallel to the text's argument. Not a literal depiction but an analogical one. | Relay |
| `extends` | Image adds genuinely new propositional content not present in the text. | Relay |
| `independent` | Image and text address different subjects with no clear relationship. | Neither |
| `decorative` | Image serves a purely aesthetic function with no semantic content. Rare in *The Medium is the Massage*. | Neither |

**Preference order:** Prefer `literalizes` over `illustrates` when the image makes a metaphor concrete. Prefer `amplifies` over `illustrates` when the image intensifies beyond what the text states. Prefer `contradicts` over `ironizes` when the opposition is straightforward; `ironizes` implies self-aware commentary.

### Rule 5: `contemporary_domain_candidates` (The One-Sentence Test)

Assign a domain only when the conceptual bridge between the original concern and the contemporary domain can be stated in one sentence. If the bridge requires more than one inferential step, the mapping is likely forced.

Maximum three domains per spread in normal cases. Four only when the spread genuinely engages multiple distinct contemporary issues (not when a single issue could be slotted into multiple domains).

If no domain mapping feels earned, leave the array empty. Some spreads (especially transitional or structural ones) do not map to contemporary domains, and that's fine.

### Rule 6: `compositional_framing`

| Classification | Visual Indicators |
|---|---|
| `strongly_framed` | Clear borders between elements: white space, rule lines, color breaks, distinct image frames. Elements feel contained and separate. |
| `weakly_framed` | Elements flow into one another: overlaps, shared backgrounds, images bleeding to edge, text overlapping image, cross-gutter continuity. |
| `mixed` | Some elements strongly framed (e.g., a boxed quotation), others weakly framed (e.g., a full-bleed image behind). |

In *The Medium is the Massage*, the gutter (book spine) functions as the primary frame. Spreads where visual content crosses the gutter are `weakly_framed`. Spreads where the left and right pages are compositionally independent are `strongly_framed`.

---

## Guiding Questions: Rhetoric

The `rhetoric` section is the core analytical work — what the spread DOES, not just what it contains. The theoretical framework is Drucker's performative design: visual form as action, not representation.

### `argument`

State the core argument plainly. What is McLuhan saying here?

Ask:
1. **If you had to summarize this spread in one sentence for someone who hadn't seen it, what would you say?** That sentence is the argument.
2. **Is this a claim, a question, a provocation, or a demonstration?** Claims can be stated propositionally. Questions frame a problem. Provocations challenge assumptions. Demonstrations show rather than tell.
3. **Is the argument in the text, the images, or the design?** Often all three, but which carries the most weight?

**Good:** "Electronic information technology has created a universal surveillance apparatus that threatens individual privacy. The 'computerized dossier bank' is an unforgiving, permanent record."

**Weak:** "This spread is about surveillance and technology."

### `rhetorical_strategy` (Controlled Vocabulary)

*Theoretical grounding: Sonja Foss's (2004) framework treats visual artifacts as rhetorical objects — symbolic, designed, and communicative. The strategy vocabulary names HOW the spread argues.*

Select one **primary** and up to two **secondary** strategies from the 15-term vocabulary (see Appendix A for definitions and examples). Then write a **strategy_description** explaining how the strategy operates on this specific spread.

Ask:
1. **What should the reader experience on this spread?** Unease → confrontation or interpellation. Overwhelm → sensory_overload or accumulation. Surprise → disruption or defamiliarization. Contemplation → quieting. Recognition → demonstration or humor.
2. **Is the spread making its point through form or content?** If form → likely `demonstration`. If content → one of the other 14.
3. **Does the strategy change partway through the spread?** If the spread opens with accumulation (listing invasive questions) and closes with a typographic punch ("you"), the primary might be `confrontation` with secondary `accumulation`.

### `design_enacts_argument` and `design_argument_description`

*Theoretical grounding: Johanna Drucker's Graphesis (2014) distinguishes design as representation (showing what something looks like) from design as performance (doing something to the viewer through formal properties). This boolean captures whether the spread's design performs its argument.*

Apply the Form-Only Test (Codebook Rule 3). If `true`, write the mechanism in `design_argument_description`.

Ask:
1. **Strip away the text. What does the design alone communicate?** If the answer is "nothing in particular" → `false`. If the answer relates to the spread's argument → `true`.
2. **Name the formal mechanism.** Not "the design feels like surveillance" but "the giant 'you' singles the reader out, the fingerprint identifies them, the bullseye targets them."
3. **Is the reader's body involved?** If the reader must rotate the book, lean closer, or physically interact differently with this spread → strong candidate for `true`.

### `reader_experience`

*Theoretical grounding: Reception aesthetics (Iser, 1978). The reader is not a passive recipient but an active participant whose phenomenological encounter with the spread IS part of the spread's meaning.*

Describe what the reader feels/experiences on this spread. Use the analytical vocabulary: confrontation, disorientation, recognition, amusement, unease, exhilaration, contemplation, intimacy, overwhelm, relief, complicity, etc.

### `mcluhan_concepts` (Enumerated)

Select from the enumerated list in the schema. The full vocabulary:

`medium_is_the_message`, `extensions_of_man`, `global_village`, `hot_and_cool`, `rear_view_mirror`, `figure_ground`, `acoustic_space`, `visual_space`, `electric_age`, `print_culture`, `tribal`, `pattern_recognition`, `sense_ratios`, `environment_as_invisible`, `obsolescence_and_retrieval`, `participation`, `implosion`, `anti_environment`, `allatonceness`

Ask: Which of these concepts is *active* — not just mentioned, but structurally at work — on this spread? A spread can discuss surveillance without activating `figure_ground`; but if the spread makes the invisible infrastructure of surveillance *visible*, then `figure_ground` is active (the invisible ground becomes visible figure).

### `multi_spread_patterns`

If this spread participates in a rhetorical sequence spanning multiple spreads — such as progressive density increase, alternating dark/light, a three-spread argument that introduces/develops/resolves — describe the pattern and reference the spread IDs involved. Null if the spread operates independently.

This field becomes more valuable as analysis progresses. Early batches will have more nulls; later batches will retroactively identify patterns.

### `confidence`

Self-report: `high` (any competent analyst would agree), `moderate` (reasonable alternatives exist), `low` (best guess, significant uncertainty). This is not a judgment of quality — a low-confidence analysis of a genuinely ambiguous spread is more valuable than a false high-confidence one.

---

## Guiding Questions: Themes

The `themes` section maps each spread's content to both original thematic concerns and contemporary AI-era domains. This is the most forward-looking analytical work — it directly feeds the Planning Engine's mapping of original spreads to contemporary equivalents.

*Theoretical grounding: Theme identification follows Kress and van Leeuwen's compositional metafunction (what the spread's formal properties foreground) and Barthes' principle that images are polysemous and require thematic anchoring. The analyst's task is to identify what the spread's compositional salience structure makes prominent, not to impose a theme from external knowledge.*

### `original_themes` (free-text tags)

Ask yourself:
1. **What is this spread fundamentally about?** Not the surface topic, but the underlying concern. A spread about TV is really about passivity, or participation, or the blurring of public and private.
2. **What recurring McLuhan concern does this address?** (e.g., sensory ratios, extensions of man, hot vs. cool media, figure-ground, the global village, obsolescence, retrieval)
3. **Would someone reading only this spread understand what McLuhan is arguing?** If not, what theme connects it to the broader argument?
4. **Use consistent vocabulary across all 85 spreads.** Before assigning a theme, consult the **Theme Vocabulary Registry** (`theme_vocabulary.json`). Prefer existing tags over inventing new ones unless the concept is genuinely new. If you add a new tag, update the registry with a definition and note this spread as first use.

### `contemporary_domain_candidates` (enum values)

For each spread, ask:
1. **Which of the 12 domains does this spread's argument map to most naturally?**
   - `algorithmic_identity` — How AI/algorithms construct, classify, and define us
   - `attention_and_cognition` — How technology reshapes how we think, focus, remember
   - `synthetic_media_and_post_truth` — Deepfakes, AI-generated content, epistemic crisis
   - `ambient_intelligence` — IoT, smart environments, always-on computation
   - `post_literacy_and_language` — LLMs, voice interfaces, death of reading/writing as we know it
   - `authorship_and_creativity` — AI art, generative models, who creates?
   - `surveillance_and_control` — Data harvesting, facial recognition, algorithmic governance
   - `public_private_collapse` — Social media, always-on visibility, loss of interiority
   - `embodiment_and_disembodiment` — VR/AR, telepresence, the body in digital space
   - `labor_and_value` — Automation, gig economy, AI replacing human work
   - `global_village_revisited` — Interconnection, filter bubbles, digital tribalism
   - `agency_and_autonomy` — Who decides? Human vs. algorithmic choice
2. **Apply the One-Sentence Test** (Codebook Rule 5). Can you state the bridge in one sentence?
3. **Could this spread belong to multiple domains?** If so, list all that apply (max 3, normally). The goal is a rich thematic map, not one-to-one correspondence.
4. **Does the mapping feel earned or forced?** A good mapping makes the reader think "of course." A forced mapping makes the reader think "really?" If in doubt, leave it out.

### `movement_mapping` (enum values)

*The five-movement structure comes from the Theoretical Framework (framework_v3.md). These movements organize the contemporary book, not the original. The mapping indicates where in the NEW book's arc this original spread's concerns most naturally belong.*

Assign the spread to one (or occasionally two) of:

- **`prologue`** — Framing, thesis statement, setting the terms. "Everything is changing — you, your family, your neighborhood..."
- **`movement_1_environment`** — "The Medium as Environment." How technology becomes our invisible surround. Bratton's Stack as organizing architecture. Surveillance, ambient intelligence, infrastructure.
- **`movement_2_acceleration`** — "Speed, Scale, Saturation." The recursive loop accelerating. Attention collapse, information overload, the pre-paradigmatic moment.
- **`hinge_m2_m3`** — The Copernican trauma. Transitional spreads pivoting from diagnosis to vision. Vervaeke + Bratton.
- **`movement_3_dreamscape`** — "The Dreamscape of Possibility." What comes after? New forms of consciousness, creativity, numinous technology. McKenna, Davis, Gibson, Bach, Hoffman.

Ask:
1. **Is this spread primarily diagnostic (what's happening) or generative (what could happen)?** Diagnostic → M1 or M2. Generative → M3.
2. **Does this spread describe the environment or the speed?** Environment → M1. Speed/overwhelm → M2.
3. **Does this spread feel like a beginning, middle, or end?** Beginning → Prologue. Middle (problem) → M1/M2. Middle (pivot) → Hinge. End (vision) → M3.

### `mapping_rationale`

This is the **conceptual bridge** — 2-4 sentences explaining why the mapping works. The Planning Engine reads this field directly when generating the contemporary equivalent. Make it count.

Requirements:
1. Name the specific original concern
2. Name the specific contemporary parallel
3. Explain the conceptual link
4. Be concise but substantive

**Good** (from gold standard spread_011):
> McLuhan's 'computerized dossier bank' maps directly to today's algorithmic profiling, data brokerage, and AI-driven surveillance systems. The 'womb-to-tomb surveillance' he describes in 1967 has been realized in ways he could not have imagined — browser histories, location tracking, facial recognition, social media graphs. The 'unforgiving, unforgetful' quality of the dossier bank is today's internet permanence. The buzzing at the end anticipates the ambient, always-on quality of digital surveillance.

**Weak** (too vague):
> This spread is about technology and privacy, which is still relevant today.

---

## Guiding Questions: Progression

The `progression` section tracks how the book builds its argument sequentially. Each spread is a beat in a rhythm.

*Theoretical grounding: Progression analysis operationalizes Bateman's GeM navigation layer (how the document guides reading paths across its sequence). `pace_shift` adapts Genette's narrative duration — the ratio between story time and discourse time — to visual rhetoric: a spread that demands prolonged attention "decelerates"; one absorbed at a glance "accelerates." `thematic_function` adapts Barthes' narrative functions (S/Z) to non-narrative argumentative structures.*

### `pace_shift`

Assess relative to the **immediately preceding spread** (spread N-1), considering: amount of text, number of visual elements, visual density, and demand on reader attention.

| Value | Indicators |
|---|---|
| `accelerating` | Less text than previous, simpler composition, quick typographic splash, reader moves on fast |
| `decelerating` | More text, denser composition, requires careful reading, reader slows down |
| `steady` | Similar pacing to previous spread |
| `rupture` | Sudden, dramatic break in established rhythm — full-bleed photograph after pages of text, silence after noise, etc. |

### `thematic_function`

| Value | Question to Ask |
|---|---|
| `introduces_theme` | Is this the first time this idea appears in the book? |
| `develops_theme` | Does this build on a theme already introduced? |
| `layers_themes` | Does this combine multiple previously-introduced themes into something new? |
| `climax` | Is this a peak moment — maximum intensity or confrontation on a theme? |
| `resolution` | Does this ease tension or provide closure? |
| `transition` | Is this a bridge between different thematic sections? |
| `coda` | Does this echo or revisit something from earlier, with new resonance? |
| `interruption` | Does this break the flow entirely — a non sequitur, a palette cleanser? |

### `relationship_to_previous`

Be **specific** — reference the actual content of the previous spread.

**Good**: "Shifts from the intimate close-up of hands (spread_007) to the stark typographic confrontation of 'and how!' — moving from sensory/tactile mode to declarative/verbal mode."

**Weak**: "Continues from the previous spread."

Ask:
1. What was the reader **experiencing** on the previous spread? (an image, dense text, silence, humor?)
2. How does THIS spread **change** that experience? (continuation, escalation, contrast, pivot, relief?)
3. Is there a **visual or thematic rhyme**? (same palette, same theme from different angle?)

### `relationship_to_next`

Be **specific** about what the next spread introduces. If you haven't analyzed the next spread yet, note what you expect based on the current spread's setup.

**Good**: "The exclamation sets up the exploratory mode that follows — having established that 'advances wreck societies,' the book proceeds to inventory the wreckage."

**Weak**: "Sets up the next spread."

Ask:
1. What does this spread **leave the reader wanting?** More information? Resolution? Contrast?
2. What **expectation** does it create? If the spread asks a question, the next spread likely answers it (or deliberately doesn't).
3. Is there a **cliffhanger, open loop, or setup?**

If you haven't analyzed the adjacent spread yet, note what you expect and flag for retroactive update. Cross-spread progression quality improves when the full sequence is visible.

---

## Guiding Questions: Design (New Fields)

### `information_value` (Kress & van Leeuwen)

*In Western reading cultures, spatial placement carries meaning: left = Given (known, accepted), right = New (at issue, problematic); top = Ideal (conceptual, aspirational), bottom = Real (concrete, grounded); center = Nucleus (essential), margin = Dependent (subordinate).*

For each axis, ask:

**Left/Right:** Does the left page present what the reader already knows or accepts, with the right page introducing the new, problematic, or confrontational element? If yes → `given_new`. If reversed → `new_given`. If both pages are compositionally equal → `balanced`.

**Top/Bottom:** Is the top area more abstract/conceptual and the bottom more concrete/detailed? If yes → `ideal_real`. Display text at top + body text below is a common `ideal_real` pattern. If reversed → `real_ideal`.

**Center/Margin:** Is there a single dominant element with subordinate elements around it? → `centered`. Is information distributed across the spread without a clear center? → `distributed`.

For single-page spreads (front matter, back matter), use `single_page` for left_right. For spreads where an axis genuinely doesn't apply (e.g., a completely symmetrical composition), use `not_applicable`.

### `compositional_framing`

See Codebook Rule 6. Ask: How strongly are the elements on this spread separated from one another? Do they flow together or are they contained in distinct zones?

---

## Theme Vocabulary Registry

Maintain a living file: `source/theme_vocabulary.json`. Structure:

```json
{
  "version": "1.0",
  "updated": "2026-03-03",
  "terms": {
    "privacy": {
      "definition": "The condition of being unobserved; control over personal information",
      "first_used": "spread_011",
      "related_terms": ["surveillance", "public_private_collapse"]
    }
  }
}
```

**Protocol:** Before assigning any `original_themes` tag, check the registry. If the tag exists, use the established form. If it doesn't, add it with a definition and note the current spread as first use. After each batch, review the registry for near-duplicates (e.g., `electric_information` vs. `electronic_media`) and normalize.

**Starter vocabulary** (from batch 1 and gold standards):
`privacy`, `surveillance`, `identity`, `electric_information`, `education`, `the_child`, `speed`, `environment`, `technology_as_extension`, `authorship`, `electric_age`, `participation`, `obsolescence`, `perception`, `the_body`, `sensory_experience`, `disruption`, `transformation`, `mediation`, `the_individual_vs_the_collective`, `figure_ground`, `hot_and_cool_media`, `print_culture`, `acoustic_space`, `visual_space`

---

## Quality Checklist (Per Entry)

Before finalizing each entry, verify:

**Perception layer:**
- [ ] `body_text` matches OCR extraction (spot-check against image)
- [ ] `display_text` accurately captures large/prominent text
- [ ] `quotations` have correct attribution and source identification
- [ ] `images` descriptions match what's visible in the spread
- [ ] `source_credit` cross-referenced against `image_credits_lookup.json`
- [ ] No encoding artifacts (em dashes should be U+2014, not garbled)

**New structured fields (v1.2):**
- [ ] `images[].interactive_meaning` populated for all photographic images (`not_applicable` for abstract/symbolic)
- [ ] `images[].relationship_to_text.barthes_mode` assigned for all images
- [ ] `images[].relationship_to_text.primary_relation` uses controlled vocabulary (not free text)
- [ ] `design.information_value.left_right` assigned for all landscape spreads
- [ ] `design.compositional_framing` assigned
- [ ] `design.color_and_tone` uses structured object (contrast + dominant_tone), not free text
- [ ] `analyst` and `analysis_method` recorded

**Interpretive layer:**
- [ ] `rhetoric.argument` is substantive (not just a description of content)
- [ ] `rhetoric.rhetorical_strategy.primary` selected from controlled vocabulary
- [ ] `rhetoric.strategy_description` explains how the strategy operates on *this specific spread* (not generic)
- [ ] `rhetoric.design_enacts_argument` passes the Form-Only Test (Codebook Rule 3)
- [ ] If `design_enacts_argument` is `true`, `design_argument_description` names the *mechanism*
- [ ] If `design_enacts_argument` is `true`, `rhetorical_strategy.secondary` includes `demonstration`
- [ ] `rhetoric.mcluhan_concepts` uses enumerated values only (no free-text variants)
- [ ] `rhetoric.confidence` self-assessment recorded

**Themes and progression:**
- [ ] `themes.original_themes` use vocabulary from Theme Registry (new tags added to registry)
- [ ] `themes.contemporary_domain_candidates` pass the One-Sentence Test (Codebook Rule 5)
- [ ] `themes.mapping_rationale` names specific original AND contemporary parallels
- [ ] `progression.pace_shift` assessed relative to immediately preceding spread (not global trend)
- [ ] `progression.relationship_to_previous/next` reference specific content (not generic)

**Cross-checks (after batch completion):**
- [ ] `rhetorical_strategy.primary` distribution is varied across the batch (not all `assertion`)
- [ ] `design_enacts_argument` is `true` on no more than ~40-50% of spreads (if higher, recalibrate against Rule 3)
- [ ] `multi_spread_patterns` checked — any emerging patterns identified in earlier entries retroactively noted
- [ ] Theme vocabulary registry updated with any new tags

---

## Appendix A: Rhetorical Strategy Vocabulary

The 15-term controlled vocabulary for `rhetoric.rhetorical_strategy`. Select one primary and up to two secondary strategies per spread.

| Strategy | Definition | Example from *The Medium is the Massage* |
|---|---|---|
| `assertion` | Direct declarative claim, stated without hedging | "The medium is the message" thesis statements |
| `confrontation` | Directly addressing/challenging the reader; breaking the fourth wall | "you" spread (spread_011): reader targeted by surveillance design |
| `juxtaposition` | Placing unlike elements side by side to generate meaning from contrast | Press photo vs. body text on most image-text spreads |
| `accumulation` | Building force through repetition, listing, or serial layering | Interrogation questions in spread_011: "How much do you make?..." |
| `disruption` | Breaking established visual rhythm; formal surprise | The rotated page — reader must physically turn the book |
| `provocation` | Claim designed to unsettle or challenge received wisdom | "There is absolutely no inevitability as long as there is a willingness to contemplate what is happening" |
| `invocation` | Summoning authority through quotation or allusion | Named quotations throughout (Whitehead, de Chardin, etc.) |
| `dramatization` | Staging a scene or scenario that makes an abstract point concrete | The surveillance interrogation staging in spread_011 |
| `quieting` | Reducing visual density to create contemplative space | Sparse spreads following dense sequences |
| `sensory_overload` | Overwhelming the reader's processing capacity through density or complexity | Collage spreads with multiple competing elements |
| `humor` | Using wit, irony, or absurdity to disarm before making a point | "and how!" as punchline/exclamation |
| `demonstration` | Making the form itself an instance of the argument's content | Any spread where `design_enacts_argument` = true |
| `interpellation` | Addressing the reader in a way that constitutes them as a particular kind of subject | "you" (constituting the reader as surveillance subject) |
| `defamiliarization` | Making the familiar strange through formal distortion | Inverted/reversed text; unusual orientations |
| `call_and_response` | One element poses a question or setup; another answers or resolves | Left-right page dynamics (spread_011: identity/targeting) |

**Note on `demonstration`:** This overlaps with `design_enacts_argument` = true. When the boolean is true, the primary strategy is often *something else* (confrontation, accumulation, etc.) with `demonstration` as secondary. The design may enact the argument *through* confrontation — in which case `confrontation` is primary and `demonstration` is secondary.

---

## Appendix B: Source Type Guidance

For the `images[].source_type` enumeration:

| Source Type | Key Indicators | Common in McLuhan? |
|---|---|---|
| `press_photo` | Photojournalistic composition; captures a moment of public significance; typically has wire-service quality; identifiable events or public figures | Yes — many press/news images throughout |
| `art_photograph` | Formal compositional intent; artistic framing, lighting, or subject treatment; may be credited to a named photographer | Yes — several credited art photographs |
| `fine_art_reproduction` | Painting, sculpture, or other fine art reproduced photographically | Occasional |
| `editorial_cartoon` | Drawn/illustrated satirical commentary | Occasional |
| `illustration` | Drawn or painted image created specifically for the publication or a similar context | Occasional |
| `advertisement` | Commercial product promotion; includes branding, slogans, product shots | Yes — several found advertisements used ironically |
| `technical_diagram` | Schematic, blueprint, circuit diagram, or other functional illustration | Rare |
| `graphic_symbol` | Abstract or symbolic graphic element: target, fingerprint, geometric pattern, Op Art | Yes — several throughout (bullseye, fingerprint, patterns) |
| `historical_document` | Reproduced historical text, manuscript, or official document | Rare |
| `film_still` | Frame captured from a motion picture | Occasional |
| `unknown` | Cannot be confidently classified | Use sparingly; note uncertainty in `notes` |

---

## Version History

- **v1.0** (2026-03-02): Initial methodology for Phase B batch 1 (spreads 001-010). Accompanied schema v1.1. VLM pipeline: Qwen2.5-VL (primary) + Molmo2-8B (correlation).

- **v2.0** (2026-03-03): Major revision for schema v1.2. Added: theoretical grounding statements for all interpretive fields; codebook decision rules (6 rules); analytical level classification (perception/identification/interpretation/theoretical judgment); controlled vocabulary for rhetorical strategy (15 terms) and image-text relationships (10 terms); theme vocabulary registry protocol; new fields methodology (interactive_meaning, information_value, compositional_framing, confidence, multi_spread_patterns, analyst/analysis_method); expanded quality checklist (from 13 to 30 items); source type guidance appendix. Updated: VLM pipeline (Qwen3-VL sole VLM, Molmo2-8B retired); field table (added analytical level and theoretical warrant columns, ⚡ markers for Planning Engine dependencies). Removed: references to Qwen2.5-VL as active pipeline component; two-VLM correlation strategy (replaced by single higher-quality model).
