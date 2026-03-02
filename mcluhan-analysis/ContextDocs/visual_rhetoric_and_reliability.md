# Visual Rhetoric Theory and Schema Reliability: A Methodological Foundation for Computational Analysis of Book Design

**Working Paper — March 2026**
**Project:** Computational Analysis of *The Medium is the Massage* (McLuhan & Fiore, 1967)

---

## Abstract

This document establishes the theoretical and methodological foundations for a structured JSON schema designed to capture how graphic design functions as rhetorical argument in published books. Part I maps the schema's nine analytical sections to four bodies of visual rhetoric theory, demonstrating through a worked example (spread_011 of *The Medium is the Massage*) how each schema field operationalizes a specific theoretical construct. Part II develops a reliability framework using Krippendorff's alpha, classifying all schema fields by measurement level and expected inter-rater agreement, and conducting a preliminary ambiguity analysis to identify where coder disagreement will concentrate. Together, these sections provide the interpretive scaffolding and validation methodology required for a publishable study of computational book design rhetoric.

---

## Part I: Visual Rhetoric Theory as Interpretive Scaffolding

### 1.1 The Schema's Theoretical Problem

The analysis schema (v1.1) contains 50+ fields organized into nine sections: identification, text, quotations, images, design, rhetoric, themes, progression, and notes. These fields range from the nearly mechanical (extracting visible page numbers) to the deeply interpretive (describing how visual design "enacts" an argument). The schema's central claim — encoded in its field descriptions and the methodology document's insistence that rhetoric is "the most important section" — is that graphic design in books functions as rhetorical argument, not merely as aesthetic decoration or information organization.

This claim requires theoretical warrant. Without it, the schema is an ad hoc coding instrument whose categories reflect one analyst's intuitions rather than a systematic framework that other researchers could apply, critique, or extend. Four bodies of theory provide this warrant, each grounding a different stratum of the schema.

The theoretical architecture maps as follows:

| Theory | Primary Contribution | Schema Stratum Grounded |
|--------|---------------------|------------------------|
| Kress & van Leeuwen (visual grammar) | Systematic metafunctions for visual meaning-making | `design.*`, `images[].composition`, `images[].scale` |
| Barthes; Martinec & Salway (image-text relations) | Taxonomies of how images and text interact | `images[].relationship_to_text`, `design.left_right_relationship` |
| Drucker (performative design) | Design as action, not representation | `rhetoric.design_enacts_argument`, `rhetoric.design_argument_description` |
| Bateman & Hiippala (GeM framework) | Multi-layered annotation of multimodal documents | Overall schema architecture; layer separation |

Each body of theory is examined below, with its operationalization in the schema demonstrated through a worked analysis of spread_011 — the "you" surveillance spread from *The Medium is the Massage*.


### 1.2 Kress and van Leeuwen's Visual Grammar

Gunther Kress and Theo van Leeuwen's *Reading Images: The Grammar of Visual Design* (1996; 3rd ed. 2021) provides the most systematic framework for analyzing visual compositions as meaning-making systems. Drawing on M.A.K. Halliday's systemic functional linguistics, they propose that visual compositions realize three simultaneous metafunctions:

**Representational meaning** concerns what is depicted — the participants, processes, and circumstances of the visual world. Kress and van Leeuwen distinguish between *narrative* representations (where vectors connect participants in action) and *conceptual* representations (where participants are classified, structured, or analyzed taxonomically). This metafunction grounds the schema's `images[].subject` and `images[].source_type` fields, which together capture *what* is depicted and *what kind of visual artifact* it is. The schema's source type enumeration (press_photo, art_photograph, fine_art_reproduction, editorial_cartoon, illustration, advertisement, technical_diagram, graphic_symbol, historical_document, film_still) functions as a genre classification that shapes how a reader processes the image's representational claims — a press photograph asserts documentary reality; a graphic symbol asserts conceptual abstraction.

*Application to spread_011:* The spread contains two images. The fingerprint is classified as `graphic_symbol` — a conceptual representation that abstracts individual identity into a biometric mark. The concentric-circle target is also `graphic_symbol`, but where the fingerprint represents through indexical trace (this particular finger made this particular mark), the target represents through symbolic convention (the bullseye signifies "aim here"). The two images thus mobilize different representational logics — indexicality and symbolism — in service of the same argument about surveillance.

**Interactive meaning** concerns the relationship between the image and its viewer. Kress and van Leeuwen's key variables are *contact* (does the represented participant "look at" the viewer, creating a demand, or not, creating an offer?), *social distance* (intimate close-up, social medium shot, impersonal long shot), and *attitude* (frontal involvement vs. oblique detachment, high angle viewer power vs. low angle represented participant power). This metafunction grounds the schema's `images[].composition` field ("framing, angle, contrast, key visual qualities") and `images[].scale` field (full_bleed, dominant, half_page, quarter_page, small_inset, icon).

The schema's scale enumeration deserves particular attention as a Kress-van Leeuwen operationalization. "Full_bleed" creates maximum intimacy — the image fills the reader's visual field, collapsing social distance. "Small_inset" creates maximum impersonality — the image is contained, controlled, subordinated to surrounding text. The choice between these is not a neutral layout decision but a statement about the reader's relationship to the depicted content.

*Application to spread_011:* The fingerprint occupies `small_inset` scale — intimate in subject (a body part at extreme close-up) but contained in presentation. The target occupies `full_bleed` — impersonal in subject (an abstract pattern) but overwhelming in presentation. This inversion is rhetorically productive: the most personal image (your fingerprint, your identity) is the smallest element, while the most abstract image (a target) dominates the visual field. The reader's own identity is reduced; the apparatus of surveillance is amplified. This scalar inversion enacts the power asymmetry that McLuhan's text describes.

**Compositional meaning** concerns how elements are arranged to form a coherent whole. Kress and van Leeuwen identify three interrelated systems: *information value* (the meaning carried by spatial placement — left/right, top/bottom, center/margin), *salience* (what draws the eye through size, sharpness, color, foreground placement), and *framing* (how strongly elements are connected or disconnected through frames, vectors, color continuity, or spatial separation). This metafunction grounds the schema's entire `design` section — `layout_description`, `typography`, `color_and_tone`, `white_space`, `visual_density`, and critically `left_right_relationship`.

The schema's `left_right_relationship` field directly operationalizes Kress and van Leeuwen's information value system. In Western reading cultures, left position carries "Given" information (what the reader already knows or is assumed to accept) while right position carries "New" information (what the reader is being told, what is at issue, what is problematic). The schema's prompt for this field — "mirror, contrast, continuation, call-and-response, independent, one dominates" — asks the analyst to characterize the *type* of Given-New relationship without requiring them to use Kress and van Leeuwen's terminology, making the field accessible to analysts without formal training in social semiotics while remaining theoretically grounded.

*Application to spread_011:* The sample entry describes the left-right relationship as "Call-and-response. The left page asks the question ('you' — who are you? what do they know about you?), and the right page answers with the target: you are being aimed at." This is a textbook Given-New structure: the left page presents the Given (the fact of surveillance, the reader's identity under scrutiny) and the right page presents the New (the consequence — you are a target). The fingerprint-to-bullseye progression across the gutter literalizes the trajectory from identification to targeting.


### 1.3 Barthes and the Image-Text Relation

Roland Barthes' "Rhetoric of the Image" (1964; English translation in *Image—Music—Text*, 1977) establishes two fundamental modes of image-text interaction:

**Anchorage** occurs when text fixes the meaning of an inherently polysemous image. The text tells the viewer which of the image's many possible meanings to activate. Barthes describes this as a "vice" of control — text constrains interpretive freedom.

**Relay** occurs when text and image stand in complementary relationship, each contributing information the other does not contain. Neither is subordinate; meaning emerges from the *gap* between them. Barthes associates relay primarily with narrative forms (comic strips, film dialogue) where image and text advance different aspects of the same story.

The schema's `images[].relationship_to_text` field operationalizes and extends this Barthesian framework. Its prompt asks the analyst to characterize how each image "relates to the text on the spread: illustrates, contradicts, amplifies, ironizes, literalizes, provides atmosphere, serves as metaphor, etc." This vocabulary expands Barthes' binary into a richer taxonomy:

| Schema vocabulary | Barthesian mode | Rhetorical function |
|---|---|---|
| *illustrates* | Anchorage | Text constrains image meaning (redundancy) |
| *amplifies* | Relay | Image intensifies textual claim (escalation) |
| *contradicts* | Relay (adversarial) | Image undermines textual claim (irony, dialectic) |
| *ironizes* | Relay (adversarial) | Image reframes textual claim as absurd or self-defeating |
| *literalizes* | Neither (Barthes did not theorize this) | Image makes textual metaphor concrete |
| *provides atmosphere* | Anchorage (weak) | Image establishes mood without specifying content |
| *serves as metaphor* | Relay | Image provides figurative parallel to textual argument |

The category "literalizes" merits particular attention because it describes a relationship Barthes did not anticipate but that is pervasive in *The Medium is the Massage*. When the text discusses surveillance and the image is a fingerprint, the image is neither fixing the text's meaning (the text is already explicit) nor providing complementary information (the fingerprint adds no new propositional content). Instead, the image *makes material* what the text discusses abstractly — it literalizes. This is a distinctive feature of graphic design rhetoric as opposed to, say, photojournalism or advertising, where Barthes developed his framework. In designed books, text-image relationships frequently operate in this literalizing mode, and the schema's inclusion of this term as an analytical option represents a genuine extension of Barthesian theory.

Martinec and Salway's "A System for Image–Text Relations in New (and Old) Media" (*Visual Communication*, 2005) provides a more granular alternative to Barthes' binary. Building on Halliday's logico-semantic relations, they distinguish *elaboration* (image and text express the same level of generality), *extension* (image adds new information), and *enhancement* (image provides circumstantial detail — where, when, how). Each category is further subdivided by whether the image or text is dominant, creating a 2×3 matrix that can be extended to account for the scale asymmetries the schema captures.

The schema does not adopt Martinec and Salway's taxonomy directly, and there are strategic reasons for this. Their framework was designed for linguists analyzing multimodal corpora and assumes familiarity with Hallidayan functional grammar. The schema's free-text vocabulary ("illustrates, contradicts, amplifies, ironizes, literalizes") is designed for design analysts and cultural critics who may not share this theoretical background. However, a formal alignment between the schema's vocabulary and Martinec-Salway categories would strengthen the schema's theoretical credibility and is recommended for the published paper's methodology section.

*Application to spread_011:* The sample entry characterizes the fingerprint's relationship to text as "Literalizes the theme of individual identity under surveillance. The fingerprint is the most basic biometric identifier — the thing that makes 'you' uniquely trackable." The target's relationship is characterized as "The target/bullseye directly enacts the argument about surveillance — 'you' are the target." Both are literalizing relationships — the text discusses surveillance abstractly, and the images make it concrete. But they literalize *different aspects* of the surveillance argument: the fingerprint literalizes *identification* (the mechanism) while the target literalizes *targeting* (the consequence). A Martinec-Salway analysis would classify both as *elaboration: exposition* (image and text at same generality, restating the same content in different semiotic modes), but this classification misses the rhetorical progression from mechanism to consequence that the schema's free-text descriptions capture.


### 1.4 Drucker and Performative Design

Johanna Drucker's body of work — *The Visible Word* (1994), *Graphesis: Visual Forms of Knowledge Production* (2014), and *Visualization and Interpretation* (2020) — provides the theoretical warrant for the schema's most important and most unusual field: `rhetoric.design_enacts_argument`.

Drucker's central intervention is the distinction between design as *representation* (showing what something looks like, illustrating a pre-existing concept) and design as *performance* (doing something to the viewer, enacting a proposition through the formal properties of the visual artifact itself). In *Graphesis*, she argues that visualizations are not windows onto pre-existing data but "knowledge generators" that produce understanding through their formal operations. Applied to book design, this means that typography, layout, scale, density, and rhythm do not merely *carry* McLuhan's arguments — they *are* arguments.

This is precisely the claim encoded in the schema's boolean field `design_enacts_argument` and its companion description field `design_argument_description`. The methodology document marks these as the "most important" and "most valuable analytical insight" in the entire schema. The field asks: does the visual design itself *perform or embody* the argument? The examples given are telling: "a spread about speed that feels fast, a spread about fragmentation that is fragmented." These are not cases where design illustrates a textual claim but cases where design *is* the claim — where the medium is, quite literally, the message.

Ellen Lupton's *Thinking with Type* (2004; 4th ed. 2024) provides complementary grounding, particularly for typography as rhetorical action. Lupton treats typography not as ornamentation applied to content but as "the convergence of art and language" — a system whose formal properties (weight, scale, spacing, rhythm, contrast) carry meaning independent of the words set. The schema's `typography` sub-object, with its three fields (body_font_style, display_font_style, special_treatments), captures Lupton's insight that typographic choices are rhetorical choices. The `special_treatments` array — which logs "reversed text, rotated text, text overlaid on image, text as texture, letterspacing effects" — is explicitly designed for the expressive typography that characterizes *The Medium is the Massage* and that Lupton's framework helps theorize.

Sonja Foss's "Framing the Study of Visual Rhetoric" (2004) provides the theoretical architecture for treating visual artifacts as rhetorical objects at all. Foss argues that three criteria distinguish visual rhetoric from visual aesthetics or visual communication: the artifact must be *symbolic* (using signs to communicate), *involve human intervention* (produced by a designer making choices), and be *presented to an audience for the purpose of communicating* (not accidental). All three criteria are met by designed books, and the schema's rhetoric section — with its fields for argument, strategy, design enactment, and reader experience — implements Foss's framework by requiring the analyst to articulate *what* the spread communicates, *how* it communicates, and *to what effect* on the reader.

*Application to spread_011:* The sample entry's `design_enacts_argument` is `true`, and the description reads: "The spread performs surveillance on the reader. The giant 'you' singles them out. The fingerprint identifies them. The target on the facing page aims at them. The reader cannot passively read about surveillance — they experience being its object." This is a Druckerian performative analysis: the argument is not that "the design illustrates the text about surveillance" but that "the design *is* surveillance." The spread surveils the reader through the same mechanisms it describes — identification (fingerprint), addressing (the pronoun "you"), and targeting (the bullseye). Form enacts content. The medium is, once again, the message.

The `reader_experience` field — "Confrontation and unease. The reader feels personally addressed, exposed, targeted" — captures the experiential consequence of this performativity. It operationalizes what reception aesthetics (Iser, Jauss) would call the "implied reader's" encounter with the text, grounding the analysis in the reader's phenomenological response rather than the designer's intention alone.


### 1.5 Bateman's GeM Framework as Methodological Ancestor

John Bateman's Genre and Multimodality (GeM) framework, developed in *Multimodality and Genre: A Foundation for the Systematic Analysis of Multimodal Documents* (2008) and extended by Tuomo Hiippala in *The Structure of Multimodal Documents: An Empirical Approach* (2015), provides the most direct methodological precedent for the schema.

GeM proposes four annotation layers for multimodal documents:

| GeM Layer | Function | Closest schema equivalent |
|---|---|---|
| **Base layer** | Identifies all content elements (text blocks, images, layout elements) | `text`, `quotations`, `images` sections |
| **Layout layer** | Captures spatial arrangement, typography, and visual grouping | `design` section |
| **Rhetorical layer** | Annotates discourse relations between elements using RST | `rhetoric` section + `images[].relationship_to_text` |
| **Navigation layer** | Records how the document guides reading paths | `progression` section + `design.left_right_relationship` |

The schema departs from GeM in three significant ways that collectively define its contribution:

First, the schema replaces GeM's XML annotation with JSON, reflecting the shift in computational practice since 2008 toward JSON as the lingua franca of web APIs, data interchange, and AI model input/output. This is not merely a formatting choice: JSON schemas are natively consumable by large language models and vision-language models, enabling the computational pipeline the project requires (VLM extraction → structured JSON → interpretive analysis → downstream generation).

Second, the schema adds a *thematic mapping layer* (the `themes` section) that GeM lacks entirely. GeM was designed for *descriptive* analysis of documents as they are; the schema is designed for *generative* analysis that maps each spread to contemporary equivalents. The twelve-domain enumeration (`algorithmic_identity`, `attention_and_cognition`, `synthetic_media_and_post_truth`, etc.) and the five-movement structural mapping (`prologue`, `movement_1_environment`, `movement_2_acceleration`, `hinge_m2_m3`, `movement_3_dreamscape`) are unique to this schema and serve a creative function that has no precedent in multimodal corpus linguistics.

Third, and most importantly, the schema foregrounds *design-specific rhetorical properties* that GeM's Rhetorical Structure Theory (RST) apparatus does not capture. RST describes relations between propositions (cause, evidence, elaboration, contrast) but does not describe how formal visual properties — weight, scale, density, rhythm, contrast ratio, typographic expressiveness — function as persuasive means. The schema's `rhetoric.design_enacts_argument` field asks a question that RST cannot answer: not "what propositional relation holds between these elements?" but "does the formal design itself constitute an argument?" This is the Druckerian question, and it requires a Druckerian, not an RST, theoretical apparatus.

Hiippala's "Semiotically-grounded Distant Viewing of Diagrams" (published in *Digital Scholarship in the Humanities*, 2022, co-authored with Bateman) is the most recent methodological ancestor, combining multimodality theory with computational methods. Their finding that computational models based on simple text/image distinctions "lack sufficient reach" for semiotically-oriented research directly motivates the schema's granular vocabulary for image-text relationships, typographic treatments, and compositional meaning. The schema can be understood as an attempt to provide the "sufficient reach" that Hiippala and Bateman call for, instantiated as a reusable JSON Schema rather than a project-specific annotation protocol.


### 1.6 Summary: Theoretical Grounding of the Schema

The following table maps every major schema section to its theoretical warrant:

| Schema Section | Fields | Primary Theory | Secondary Theory | What the theory licenses |
|---|---|---|---|---|
| **identification** | id, pdf_page, book_pages, section, spread_type, orientation | GeM base layer | — | Systematic enumeration of content units |
| **text** | body_text, display_text, captions, page_numbers_visible | GeM base layer | Lupton (typography as meaning) | Separation of text by *function* (body vs. display vs. caption), not just content |
| **quotations** | text, author, context, source_work, relationship_to_argument, visual_treatment | Foss (visual rhetoric) | Barthes (anchorage/relay) | Treating quotations as rhetorical moves with visual presentation |
| **images** | position, subject, source_type, credit, date, composition, scale, relationship_to_text | Kress & van Leeuwen (all three metafunctions) | Barthes; Martinec & Salway | Systematic decomposition of visual meaning |
| **design** | layout_description, typography, color_and_tone, white_space, visual_density, left_right_relationship | Kress & van Leeuwen (compositional) | Lupton; GeM layout layer | Formal properties as meaning-carrying systems |
| **rhetoric** | argument, strategy, design_enacts_argument, design_argument_description, reader_experience, mcluhan_concepts | Drucker (performative design) | Foss; reception aesthetics | Design as action, not representation |
| **themes** | original_themes, contemporary_domain_candidates, movement_mapping, mapping_rationale | No direct theoretical precedent (generative/creative layer) | McLuhan's own tetrad framework | Mapping historical design to contemporary equivalents |
| **progression** | pace_shift, thematic_function, relationship_to_previous, relationship_to_next | GeM navigation layer | Narrative theory (Genette: duration, frequency) | Temporal/sequential structure of the book as designed experience |
| **notes** | (free text) | — | — | Epistemic humility: capture what the schema cannot |

---

## Part II: Schema Reliability Through Krippendorff's Alpha

### 2.1 The Reliability Challenge for Design Analysis

Content analysis methodology requires that coding instruments produce reliable results — that different analysts applying the same schema to the same material would produce substantially similar outputs. Klaus Krippendorff's alpha (α) is the recommended universal reliability metric because it handles any number of coders, works across all measurement levels (nominal, ordinal, interval, ratio), and properly accounts for chance agreement. The conventional threshold is α ≥ 0.800 for confident conclusions, with α ≥ 0.667 acceptable for tentative conclusions (Krippendorff, *Content Analysis*, 4th ed., 2019; Hayes & Krippendorff, *Communication Methods and Measures*, 2007).

The schema presents a distinctive reliability challenge because its fields span an unusually wide range from mechanical extraction to deep interpretation. The `text.page_numbers_visible` field requires only that the analyst read a printed number — near-perfect reliability is expected. The `rhetoric.design_argument_description` field requires the analyst to articulate how a visual composition *performs* an intellectual argument — substantial disagreement is likely. A blanket reliability statistic for the schema as a whole would be meaningless; reliability must be assessed field by field or by field clusters at the same interpretive stratum.

The schema also mixes measurement levels within a single entry. Some fields use closed enumerations (nominal: `spread_type` from 13 options; ordinal: `white_space` from a 4-level scale). Others use open text (ratio, in principle, since text can vary continuously). Any reliability study must use the appropriate variant of Krippendorff's alpha for each measurement level: nominal α for categorical fields, ordinal α for ranked scales, and a text-similarity metric (such as ROUGE or BERTScore converted to a distance function) for open-text fields.


### 2.2 Field-by-Field Reliability Classification

The following classification assigns every schema field to a reliability tier based on measurement level, degree of interpretation required, and the expected range of coder disagreement. The tiers are:

**Tier 1 — High Expected Reliability (target α ≥ 0.90):** Fields where competent analysts should agree almost completely. Disagreements indicate coder error or ambiguous source material, not legitimate interpretive difference.

**Tier 2 — Moderate Expected Reliability (target α ≥ 0.75):** Fields requiring judgment but constrained by enumerated options or relatively unambiguous visual evidence. Some disagreement is expected and legitimate.

**Tier 3 — Low Expected Reliability (target α ≥ 0.60):** Fields requiring substantial interpretive judgment. Disagreement reflects genuine analytical differences, not coder failure. These fields require the most careful codebook development and calibration.

**Tier 4 — Not directly testable via α:** Open-text fields where output is free prose. Reliability must be assessed through alternative means (semantic similarity, expert panel evaluation, or decomposition into testable sub-judgments).


#### Tier 1: High Expected Reliability (α ≥ 0.90)

| Field | Measurement Level | Rationale |
|---|---|---|
| `pdf_page` | Ratio | Mechanical assignment |
| `book_pages` | Ratio | Read from page; cross-reference with image |
| `section` | Nominal (3 categories) | Unambiguous: front_matter, body, back_matter |
| `orientation` | Nominal (3 categories) | Determined by page dimensions |
| `text.page_numbers_visible` | Ratio | Read from image |
| `text.captions` | Nominal (present/absent per item) | Visible on page or not |
| `images[].position` | Nominal | Spatial location is directly observable |
| `images[].scale` | Ordinal (6 levels) | Relative page coverage is directly measurable |

These fields involve minimal interpretation. Disagreement would indicate that one coder misread the image, not that the field definition is ambiguous.


#### Tier 2: Moderate Expected Reliability (α ≥ 0.75)

| Field | Measurement Level | Primary Source of Disagreement |
|---|---|---|
| `spread_type` | Nominal (13 categories) | Boundary cases (e.g., is a spread with a large photo and small text `image_dominant` or `text_with_mood_image`?) |
| `text.body_text` | Text (evaluated by character accuracy) | OCR quality; handling of damaged/ambiguous text |
| `text.display_text` | Text | Deciding which text qualifies as "display" vs. "body" |
| `images[].source_type` | Nominal (11 categories) | Distinguishing press_photo from art_photograph; identifying film_stills |
| `images[].estimated_date` | Interval | Different historical knowledge among coders |
| `design.white_space` | Ordinal (4 levels: abundant/moderate/minimal/none) | Boundary between adjacent categories |
| `design.visual_density` | Ordinal (4 levels: sparse/moderate/dense/overwhelming) | Same boundary issue |
| `rhetoric.mcluhan_concepts` | Nominal (multi-label) | Which concepts are "active" is somewhat interpretive |
| `themes.original_themes` | Nominal (multi-label, open vocabulary) | Different granularity of tagging |
| `themes.contemporary_domain_candidates` | Nominal (multi-label, 12 options) | Whether a mapping is "earned" or "forced" |
| `themes.movement_mapping` | Nominal (multi-label, 5 options) | Boundary spreads between movements |
| `progression.pace_shift` | Ordinal (4 levels) | "Steady" vs. "accelerating" is context-dependent |
| `progression.thematic_function` | Nominal (8 categories) | Multiple functions can co-occur |

These fields constrain the analyst through enumerated options but require judgment about category boundaries. The methodology document's "guiding questions" for themes and progression are effectively a codebook — they direct analytical attention and constrain interpretation without eliminating it.

**Key ambiguity clusters to anticipate:**

*Spread type:* The boundary between `text_with_mood_image` and `text_with_specific_image` requires distinguishing whether an image provides "atmosphere" or makes a "specific" point. This distinction maps to Barthes' anchorage/relay boundary and will produce moderate disagreement.

*White space / visual density:* These two ordinal scales are correlated but not identical. A spread can have minimal white space but only moderate density (if filled with a single large image rather than many elements). Coders may conflate the two.

*Contemporary domain candidates:* The methodology's instruction to check whether a mapping "feels earned or forced" introduces an explicitly evaluative criterion. This is methodologically unusual — most codebooks avoid evaluative language — and will increase variance unless calibration sessions establish shared standards for what "earned" means.


#### Tier 3: Low Expected Reliability (α ≥ 0.60)

| Field | Measurement Level | Primary Source of Disagreement |
|---|---|---|
| `quotations[].relationship_to_argument` | Text (short) | How a quote "functions" is inherently interpretive |
| `images[].relationship_to_text` | Text (from vocabulary) | Analysts may characterize the same relationship differently |
| `design.left_right_relationship` | Text (from vocabulary) | Multiple valid descriptions of the same spatial relationship |
| `rhetoric.argument` | Text (short paragraph) | Different analysts may foreground different aspects of the same spread's argument |
| `rhetoric.rhetorical_strategy` | Text (from vocabulary) | Strategy identification is an expert judgment |
| `rhetoric.design_enacts_argument` | Boolean | *Appears* to be Tier 1, but see discussion below |
| `rhetoric.reader_experience` | Text (from vocabulary) | Phenomenological judgment varies across readers |

**The boolean problem:** `design_enacts_argument` is a simple true/false, which should produce high inter-rater reliability. In practice, it is likely to be the most contentious field in the schema. The question is not "do the coders understand the categories?" but "do they share a theory of what counts as design 'enacting' an argument?" A coder trained in visual rhetoric (who reads Drucker) will assign `true` more frequently than a coder trained in information design (who treats layout as functional organization). The boolean is theoretically loaded in a way that `white_space: moderate` is not. Calibration must begin with this field.

The methodology document's quality checklist addresses this directly: "`rhetoric.design_enacts_argument` is `true` only when design genuinely performs the argument." The word "genuinely" does significant work here — it is an invitation to restraint, implying that false positives (over-claiming performativity) are the primary risk. This instruction should be formalized in the codebook with positive and negative exemplars.


#### Tier 4: Not Directly Testable via α

| Field | Alternative Evaluation Method |
|---|---|
| `rhetoric.design_argument_description` | Expert panel rating (1–5 scale for insight quality); semantic similarity between coders |
| `themes.mapping_rationale` | Expert panel rating; decompose into testable sub-claims |
| `progression.relationship_to_previous` | Expert panel rating; check for factual accuracy of cross-references |
| `progression.relationship_to_next` | Same as above |
| `notes` | Not evaluated for reliability (analyst's workspace) |

These open-text fields produce prose that cannot be meaningfully compared using string-distance metrics. Two excellent analyses of the same spread may share no vocabulary while identifying the same rhetorical mechanism. Evaluation options:

(a) **Decomposition.** Convert prose descriptions into testable sub-claims. For example, the `design_argument_description` for spread_011 could be decomposed: (i) Does the spread address the reader directly? [boolean] (ii) Does the fingerprint function as an identity marker? [boolean] (iii) Does the target function as a surveillance metaphor? [boolean] (iv) Does the spread create a reader experience of being surveilled? [boolean]. Each sub-claim can be tested for inter-rater agreement.

(b) **Expert panel consensus.** Three to five design experts independently rate the quality and accuracy of each analyst's description on a Likert scale. Compute α on the ratings.

(c) **LLM-as-Judge.** A large language model evaluates whether two analysts' descriptions identify the same rhetorical mechanisms, even if they use different language. This approach has achieved 80–90% agreement with human evaluators in clinical summarization studies (Zheng et al., 2023) and design critique evaluation (Duan et al., UICrit, UIST 2024).


### 2.3 Proposed Reliability Study Design

A publishable reliability study for this schema requires the following components:

**Coder pool:** 3–5 analysts with graduate-level training in at least one of: graphic design, visual communication, rhetoric, or media studies. Coders should *not* be specialists in McLuhan — the schema is designed to be generalizable beyond this case study, and McLuhan expertise would inflate reliability on theory-specific fields (e.g., `mcluhan_concepts`) without testing the schema's broader applicability.

**Sample:** 15–20 spreads from *The Medium is the Massage*, stratified by spread type to ensure coverage of the full typology. Minimum sample should include at least one instance of each of the most common spread types: typography_as_design, image_dominant, text_with_mood_image, text_with_specific_image, collage, and quote_only.

**Training protocol (iterative calibration):**
- *Round 0:* Coders read the schema, methodology document, and two gold-standard entries. They independently analyze 3 calibration spreads (not included in the reliability sample).
- *Round 1:* Group discussion of calibration results. Identify disagreements, revise codebook where definitions are ambiguous, establish consensus on borderline cases.
- *Round 2:* Coders independently analyze 3 new calibration spreads. Compute preliminary α for Tier 1–3 fields. If any Tier 1 field falls below α = 0.80, revise and recalibrate.
- *Round 3 (if needed):* Additional calibration round focusing on fields that failed to reach threshold.
- *Reliability coding:* All coders independently analyze the 15–20 reliability sample spreads.

**Reporting:** Compute α separately for each tier. Report individual field α values for all Tier 2–3 fields. For Tier 4 fields, report expert panel ratings or decomposition results. Transparently report fields that fail to reach the 0.667 threshold — these represent limitations of the schema that should be acknowledged, not hidden.

**Statistical tools:** The K-Alpha Calculator (Marzi et al., 2024, available at k-alpha.org) provides web-based computation with bootstrap confidence intervals. For ordinal variables, use ordinal weighting. For multi-label nominal fields (e.g., `contemporary_domain_candidates`, which is a set rather than a single value), compute α using set-based distance metrics (e.g., Jaccard distance as the disagreement function).


### 2.4 Preliminary Ambiguity Analysis: Spread_011

To anticipate where inter-rater disagreement will concentrate, the following analysis examines every analytical decision in the gold-standard sample entry for spread_011, identifying points where a second competent analyst might reasonably produce a different result. This is not a critique of the existing entry — which is analytically strong — but a prospective reliability analysis.

#### Decisions likely to produce agreement (Tier 1–2 fields)

The identification fields are unambiguous: PDF page 11, book pages 12–13, body section, landscape spread. `Spread_type` = `text_with_specific_image` is correct but a second analyst might consider `symbol_or_graphic` given the dominance of the bullseye, or might argue for `collage` given the three distinct elements (text, fingerprint, target). This boundary decision is precisely the kind of disagreement that calibration should resolve.

Text extraction is largely mechanical. The `body_text` field appears accurate. The `display_text` = "you" is clearly correct — it is visually dominant and functions as a design element. A second analyst would agree.

The two images are correctly identified and described. The position, source_type, and scale classifications are straightforward. Minor disagreement might arise over whether the fingerprint's scale is `small_inset` or `icon` — the distinction is quantitative (percentage of page area) and could be anchored with measurement guidelines.

#### Decisions likely to produce moderate disagreement (Tier 2–3 fields)

**`design.white_space`: "moderate"** — A second analyst might assign "minimal" given that the left page is text-heavy and the right page is a full-bleed graphic. The "moderate" rating seems to account for the breathing room around the body text column and above/below the "you" display text. This is a calibration item: does white space refer to the spread as a whole (where the full-bleed graphic reduces perceived space) or to areas *between* elements (where the left page layout provides some)?

**`design.visual_density`: "dense"** — Could also be "moderate." The left page is dense with text, but the right page is a single graphic element. A holistic view (one complex page + one simple page = moderate average) and an additive view (lots of information to process = dense) would yield different ratings.

**`rhetoric.mcluhan_concepts`: ["electric_age", "global_village", "pattern_recognition"]** — This is the most likely site of substantive disagreement. A second analyst might argue for including `extensions_of_man` (the dossier bank as extension of memory), `figure_ground` (the spread makes visible the usually invisible surveillance infrastructure), or `hot_and_cool` (the spread is "hot" — high definition, low participation). They might exclude `pattern_recognition` as less directly relevant. The multi-label nature of this field means analysts can agree on *some* concepts while disagreeing on others — set-based agreement metrics are essential.

**`themes.contemporary_domain_candidates`: ["surveillance_and_control", "algorithmic_identity", "public_private_collapse"]** — The first mapping is indisputable. The second is strong. The third could be debated: the text focuses on the *loss* of privacy more than on the *collapse of the public/private boundary*. A second analyst might substitute `agency_and_autonomy` (the text asks "How shall the new environment be programmed?" — a question about who controls the system). Or they might add `ambient_intelligence` to capture the "womb-to-tomb" quality.

#### Decisions likely to produce significant disagreement (Tier 3–4 fields)

**`rhetoric.rhetorical_strategy`: "Confrontation"** — Plausible alternatives include "interpellation" (the Althusserian term for how subjects are constituted by being addressed — the "you" literally hails the reader into subject position), "accumulation" (the list of invasive questions builds momentum), or "dramatization" (the spread stages a scene of interrogation). The methodology document's vocabulary — "assertion, provocation, juxtaposition, accumulation, disruption, humor, sensory overload, quieting" — is a menu, not a taxonomy; analysts can select or coin terms. This freedom increases expressiveness but decreases reliability.

**Recommendation:** For reliability testing, convert the `rhetorical_strategy` field from open text to a controlled vocabulary of 15–20 strategies with definitions and exemplars. Analysts can select one primary and up to two secondary strategies. This sacrifices some analytical nuance for measurable agreement.

**`rhetoric.design_argument_description`** — The existing entry identifies four performative mechanisms: (i) the pronoun "you" singles the reader out, (ii) the fingerprint identifies them, (iii) the target aims at them, (iv) the buzzing mimics electronic surveillance. A second analyst might identify the same mechanisms in different language, or might foreground mechanisms the first analyst omits — for example, the way the justified body text on the left page visually resembles a bureaucratic form or official document, reinforcing the theme of institutional surveillance. Neither analysis would be wrong; they would be differently focused.

**`progression.relationship_to_previous` and `relationship_to_next`** — The existing entry is relatively general: "Continues the early section's pattern of establishing McLuhan's core concerns." A second analyst with access to spread_010's content might provide a more specific comparison. The methodology document explicitly instructs analysts to "reference the actual content of the previous spread" and marks generic descriptions ("Continues from the previous spread") as "weak." This instruction improves specificity but creates a dependency: the quality of progression analysis depends on the analyst's familiarity with adjacent spreads, which may vary if analysis is conducted in batches by different coders.


### 2.5 Computational Validation: The VLM as Independent Rater

The project's technical architecture — in which Qwen3-VL provides OCR, image description, and layout analysis while Claude Opus 4.6 provides interpretive analysis — creates an opportunity for a novel validation approach: treating the VLM pipeline as an independent rater whose outputs can be compared to human expert analysis.

This approach has precedent. The UICrit study (Duan et al., UIST 2024) created a dataset of 3,059 professional design critiques spanning layout, typography, color, hierarchy, and spacing, then measured LLM performance against this ground truth. Their approach — expert-generated critique dataset as gold standard, LLM as evaluand — maps directly onto the analysis pipeline's structure, where the gold-standard entries (spread_008, spread_011) and the human-reviewed analysis database serve as ground truth against which VLM-generated analyses can be measured.

The Development Log records that the pipeline already generates three types of VLM output per spread: raw OCR, structured OCR (categorized by DISPLAY_TEXT, BODY_TEXT, QUOTATIONS, CAPTIONS, PAGE_NUMBERS), and visual analysis (image description + layout analysis). These correspond to Tier 1–2 fields. Measuring agreement between VLM-generated classifications and human-assigned values would establish a baseline for computational reliability.

Specifically, the following cross-validation protocol is recommended:

**For Tier 1 fields (text extraction):** Compute character-level accuracy (CER) and word-level accuracy (WER) of Qwen3-VL OCR against human-verified transcriptions. The Technical Notes already document that Qwen3-VL achieves dramatically better OCR quality than Qwen2.5-VL on dense serif text; quantifying this improvement with standard metrics strengthens the methodology.

**For Tier 2 fields (categorical classification):** Prompt a vision-language model (Claude's multimodal capabilities, or GPT-4V as independent system) to independently classify `spread_type`, `white_space`, `visual_density`, and `images[].scale` for the reliability sample. Compute α between the VLM classifications and the human analyst's classifications, treating the VLM as an additional "coder." This does not replace human inter-rater testing but provides a computational lower bound: if a VLM and a human agree on a classification, the classification is likely unambiguous.

**For Tier 3–4 fields (interpretive analysis):** Use the LLM-as-Judge paradigm. Present a second LLM with (a) the spread image, (b) the schema field definitions, and (c) two analyses — the gold-standard entry and an independently generated analysis — without identifying which is which. Ask it to rate their agreement on a scale and identify specific points of divergence. This approach has achieved ICC (intraclass correlation coefficient) of 0.818 in clinical summarization (comparable to human inter-annotator agreement), making it a credible supplementary validation method.

The two-model architecture documented in the Technical Notes (Qwen3-VL for perception, Claude Opus 4.6 for interpretation) already implements a version of this approach implicitly. Making the validation explicit — with quantified agreement scores — transforms a practical engineering decision into a publishable methodological contribution.


### 2.6 Recommended Reliability Reporting for Publication

A published paper should report reliability at three levels of granularity:

**Level 1 — Tier-level summary:** Average α across all fields in each tier, demonstrating that the schema's mechanical fields are highly reliable and its interpretive fields reach the threshold for tentative conclusions.

**Level 2 — Field-level detail:** Individual α values for every Tier 2 and Tier 3 field, presented in a table with confidence intervals. This is the core reliability evidence.

**Level 3 — Qualitative disagreement analysis:** For the 3–5 fields with the lowest α values, a narrative discussion of *what* disagreements occurred and *why*. This is more informative than the numbers alone and demonstrates that the researchers understand the limits of their instrument.

For Tier 4 fields (open prose), report expert panel inter-rater reliability on quality ratings, plus the decomposition analysis described in Section 2.2. Acknowledge explicitly that these fields serve an analytical function (generating insight) rather than a measurement function (producing replicable data points) and that perfect reliability is neither achievable nor necessary for their purpose.

---

## Appendix A: Mapping Schema Fields to Visual Rhetoric Constructs

The following reference table maps each schema field to its theoretical warrant, the specific construct it operationalizes, and a key citation. This table is designed to be directly usable in a journal article's methodology section.

| Schema Field | Theoretical Framework | Construct Operationalized | Key Citation |
|---|---|---|---|
| `spread_type` | GeM base layer | Document element typology | Bateman 2008 |
| `text.display_text` | Lupton (typography as meaning) | Typography as distinct semiotic mode | Lupton 2004/2024 |
| `images[].subject` | Kress & van Leeuwen (representational) | Depicted participants and processes | Kress & van Leeuwen 2006 |
| `images[].source_type` | Genre theory | Visual genre classification | n/a (schema-specific) |
| `images[].composition` | Kress & van Leeuwen (interactive) | Contact, social distance, attitude | Kress & van Leeuwen 2006 |
| `images[].scale` | Kress & van Leeuwen (interactive) | Social distance (intimate → impersonal) | Kress & van Leeuwen 2006 |
| `images[].relationship_to_text` | Barthes; Martinec & Salway | Anchorage, relay, and extensions | Barthes 1977; Martinec & Salway 2005 |
| `design.layout_description` | Kress & van Leeuwen (compositional) | Information value, salience, framing | Kress & van Leeuwen 2006 |
| `design.typography.*` | Lupton; Drucker | Typography as rhetorical system | Lupton 2004; Drucker 1994 |
| `design.white_space` | Kress & van Leeuwen (compositional) | Framing: degree of visual separation | Kress & van Leeuwen 2006 |
| `design.visual_density` | Kress & van Leeuwen (compositional) | Salience: information load | Kress & van Leeuwen 2006 |
| `design.left_right_relationship` | Kress & van Leeuwen (compositional) | Information value: Given/New | Kress & van Leeuwen 2006 |
| `rhetoric.argument` | Foss (visual rhetoric) | Rhetorical claim | Foss 2004 |
| `rhetoric.rhetorical_strategy` | Foss; classical rhetoric | Persuasive means | Foss 2004 |
| `rhetoric.design_enacts_argument` | Drucker (performative design) | Design as performance, not representation | Drucker 2014 |
| `rhetoric.design_argument_description` | Drucker | Mechanism of performativity | Drucker 2014 |
| `rhetoric.reader_experience` | Reception aesthetics | Implied reader's phenomenological encounter | Iser 1978; Drucker 2014 |
| `themes.contemporary_domain_candidates` | (Project-specific) | Thematic mapping for generative analysis | n/a |
| `themes.movement_mapping` | (Project-specific) | Structural mapping for book architecture | n/a |
| `progression.pace_shift` | Narrative theory | Duration and rhythm | Genette 1980 |
| `progression.thematic_function` | Narrative theory | Story function (Propp; Barthes S/Z) | Barthes 1970 |
| `progression.relationship_to_previous/next` | GeM navigation layer | Reading path and cross-reference | Bateman 2008 |

---

## Appendix B: Recommended Controlled Vocabulary for Rhetorical Strategy

To improve reliability on the `rhetoric.rhetorical_strategy` field, the following controlled vocabulary is proposed. Analysts should select one primary strategy and up to two secondary strategies.

| Strategy | Definition | Example from *The Medium is the Massage* |
|---|---|---|
| **assertion** | Direct declarative claim, stated without evidence or hedging | "The medium is the message" (opening thesis) |
| **confrontation** | Directly addressing/challenging the reader; breaking the fourth wall | "you" spread (spread_011): reader targeted by surveillance design |
| **juxtaposition** | Placing two unlike elements side by side to generate meaning from contrast | Press photo vs. body text (most image-text spreads) |
| **accumulation** | Building force through repetition or serial listing | Interrogation questions in spread_011 |
| **disruption** | Breaking the established visual rhythm; formal surprise | Rotated page (reader must turn the book sideways) |
| **provocation** | Making a claim designed to unsettle or challenge received wisdom | "There is absolutely no inevitability as long as there is a willingness to contemplate what is happening" |
| **invocation** | Summoning authority through quotation or allusion | Named quotations throughout (Whitehead, de Chardin, etc.) |
| **dramatization** | Staging a scene or scenario that makes an abstract point concrete | Surveillance interrogation in spread_011 |
| **quieting** | Reducing visual density to create contemplative space | Sparse spreads following dense sequences |
| **sensory overload** | Overwhelming the reader's processing capacity through density/complexity | Collage spreads with multiple competing elements |
| **humor** | Using wit, irony, or absurdity to disarm before making a point | "and how!" as punchline/exclamation |
| **demonstration** | Making the form itself an instance of the argument's content | Any spread where design_enacts_argument = true |
| **interpellation** | Addressing the reader in a way that constitutes them as a particular kind of subject | "you" (constituting the reader as a surveillance subject) |
| **defamiliarization** | Making the familiar strange through formal distortion | Inverted/reversed text; unusual orientations |
| **call-and-response** | One element poses a question or setup; another answers or resolves | Left-right page dynamics (spread_011: question/target) |

Note: "demonstration" overlaps with `design_enacts_argument = true` and could serve as its textual equivalent. When `design_enacts_argument` is `true`, the primary `rhetorical_strategy` will frequently be "demonstration." However, the design may also enact the argument *through* another strategy (e.g., confrontation, as in spread_011) — in which case "confrontation" is primary and "demonstration" is secondary.

---

## Appendix C: Preliminary Codebook Decision Rules

The following rules resolve anticipated ambiguities identified in Section 2.4. These should be formalized in the codebook distributed to reliability coders.

**Rule 1 (spread_type boundary):** If a spread contains both text and a full-bleed or dominant image, classify as `image_dominant` only if the image occupies ≥70% of the total spread area AND the text is subordinate (captions, small overlaid text). If the text constitutes a substantial paragraph or argument, classify as `text_with_specific_image` (if the image makes a specific claim related to the text) or `text_with_mood_image` (if the image establishes tone without specific reference).

**Rule 2 (white_space threshold):** "Abundant" = ≥40% of spread area is empty; "moderate" = 15–40%; "minimal" = 5–15%; "none" = <5%. Estimate visually; do not measure precisely. White space includes margins, gutters, and space between elements, but not the interior of large solid-fill images.

**Rule 3 (design_enacts_argument threshold):** Assign `true` only when the formal properties of the design (not the content of images or text) produce an effect isomorphic to the argument. A spread *about* speed that uses small, calm typography does not enact its argument even though it discusses speed. A spread about speed that compresses text, eliminates white space, and creates a sense of rushing enacts its argument through form. The test: if you could not read the text, would the design alone communicate something related to the argument?

**Rule 4 (relationship_to_text vocabulary):** Use the most specific applicable term. Prefer "literalizes" over "illustrates" when the image makes a metaphor concrete. Prefer "amplifies" over "illustrates" when the image intensifies a claim beyond what the text states. Prefer "contradicts" over "ironizes" when the contradiction is straightforward; "ironizes" implies self-aware commentary on the contradiction.

**Rule 5 (contemporary_domain_candidates):** Assign a domain only when the conceptual bridge between the original concern and the contemporary domain can be stated in one sentence. If the bridge requires more than one inferential step, the mapping is likely forced. Maximum three domains per spread in normal cases; four only when the spread genuinely engages multiple distinct contemporary issues.

---

*This document is version 1.0. It should be updated following the first round of inter-rater calibration, which will identify additional ambiguity points and codebook requirements.*
