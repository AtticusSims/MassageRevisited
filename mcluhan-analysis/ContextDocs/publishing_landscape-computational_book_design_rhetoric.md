# Publishing landscape for computational book design rhetoric

A paper applying AI methods and a JSON schema to analyze visual rhetoric in McLuhan and Fiore's *The Medium is the Massage* sits at an unusually productive intersection of five fields — and faces **no direct competition**. No published work computationally analyzes book design as rhetorical argument, no AI-based study of McLuhan's visual works exists, and no structured JSON schema for graphic design rhetoric has been proposed. The opportunity is genuine: this is a first-mover paper that can define a subfield. Below is a detailed map of the venues, literature, and methods needed to publish it well.

---

## The strongest journals span design, digital humanities, and rhetoric

The paper's interdisciplinary nature means it could credibly land in at least six journal categories. The most important decision is **which disciplinary audience to prioritize**, since framing will differ substantially. Here are the top venues, organized into tiers based on thematic fit, indexing quality, and practical publishing considerations.

### Tier 1: highest fit and recommended first submissions

**Visible Language** (University of Cincinnati consortium) is the single best match. Founded in 1967 — the same year as *The Medium is the Massage* — as the *Journal of Typographic Research*, it is the world's oldest peer-reviewed design journal. Its scope explicitly covers typography, visual communication design, and interdisciplinary approaches bridging design with linguistics, anthropology, and technology. It is **diamond open access with no author fees**, indexed in Scopus, and operates double-blind review with reportedly rapid turnaround (~3 weeks). The CiteScore is low (~0.3), but its field reputation is unmatched for typography-focused scholarship.

**Journal of Cultural Analytics** (McGill University) is purpose-built for computational analysis of cultural objects. It publishes work using quantitative and computational methods applied to cultural artifacts including images and texts, seeking "thought-provoking and original arguments about how culture works at significantly larger scales." It is **diamond open access with no fees** and listed in DOAJ. Though not currently indexed in Scopus or Web of Science, it is highly respected in the growing cultural analytics community and would position the work at the vanguard of computational humanities.

**Visual Communication** (SAGE) is the most established journal for visual rhetoric and multimodal analysis. Indexed in both Scopus (Q1 Visual Arts) and SSCI with a **JIF of 1.4** and CiteScore of ~2.1, it has published directly relevant work including Pflaeging and Stöckl's work on multimodal rhetoric (2021) and articles on typographic text presentation in picturebooks. It is a hybrid journal with optional gold OA at ~$3,000. This is the venue if bibliometric visibility matters most.

**Kairos: A Journal of Rhetoric, Technology, and Pedagogy** is thematically ideal. Its founding principle — that "the design of the webtext should forward the argument as much as the textual content" — mirrors the paper's core thesis about design-as-rhetoric. It publishes multimodal "webtexts" where form enacts argument, has a **~10–30% acceptance rate**, and is **fully open access with no fees**. The limitation: it is not indexed in Scopus or Web of Science, so it serves rhetorical-community visibility rather than bibliometric positioning.

### Tier 2: strong fit with different disciplinary framings

| Journal | Publisher | Scopus/WoS | CiteScore / JIF | APC | Best framing angle |
|---------|-----------|------------|-----------------|-----|-------------------|
| **Digital Scholarship in the Humanities** | Oxford UP | Scopus + AHCI + SSCI | 2.5 / 1.1 | Hybrid ~$3,650 | Computational methodology for humanities |
| **Design Issues** | MIT Press | Scopus + AHCI | ~1.9 / ~0.4 | No (subscription) | Design theory and criticism |
| **Rhetoric Society Quarterly** | Taylor & Francis | Scopus + AHCI + SSCI | ~1.3 / 1.1 | Hybrid | Visual rhetoric theory contribution |
| **Computers and Composition** | Elsevier | Scopus | 2.0 / N/A | Hybrid $3,620 | AI + multimodal composition |
| **Information Design Journal** | John Benjamins | Scopus | ~0.5 / N/A | Optional €1,800 | Typography + document design practice |
| **Book History** | Johns Hopkins UP | Scopus + AHCI | ~0.7 / N/A | Subscription | McLuhan as book-historical case study |

**Digital Scholarship in the Humanities** deserves special attention. It explicitly requires theoretical relevance beyond tool description, so the paper must foreground the rhetoric theory, not just the JSON schema. If framed as "here is how computational methods reveal rhetorical structures invisible to close reading alone," DSH is excellent.

### Tier 3: worth considering for specific strategic goals

**She Ji** (Tongji University / Elsevier) offers an unusual combination: diamond OA with no fees, Scopus + ESCI indexing, and a **CiteScore of 6.2** — making it the highest-impact free option. Its focus on design-driven innovation is less directly relevant, but a framing emphasizing the JSON schema as a methodological innovation for design research could work. **Design Studies** (Elsevier) has the highest raw metrics (CiteScore 10.5, JIF 4.8) but focuses on design processes and cognition rather than visual rhetoric — it would require substantial reframing toward design methodology. **Digital Humanities Quarterly** is fully open access with no fees and recently accepted for Scopus indexing; it is more flexible than DSH in format and approach.

### Conference opportunities

The **ADHO Digital Humanities 2026 conference** (Daejeon, South Korea, July 27–31, 2026) is the premier venue for computational humanities and would provide excellent visibility. Selected papers are published in DSH. **ACM DIS** (Designing Interactive Systems) and **CHI** workshops occasionally accept design analysis work, though their interactive-systems focus is less aligned.

---

## The literature reveals five distinct research streams to cite

The paper needs to position itself at the convergence of several bodies of work. No single existing paper occupies the same space, but the foundations are well-established in adjacent fields.

### Multimodal document analysis: the GeM framework is the closest ancestor

The most directly relevant prior work is **Tuomo Hiippala's** program of research building on John Bateman's **Genre and Multimodality (GeM) framework**. Bateman's *Multimodality and Genre* (Palgrave, 2008) established a **multi-layered XML annotation schema** for page-based multimodal documents with four layers: base (content elements), layout (spatial arrangement and typography), rhetorical (discourse relations via Rhetorical Structure Theory), and navigation (reading paths). Hiippala's *The Structure of Multimodal Documents* (Routledge, 2015) applied this empirically to tourist brochures over four decades. Critically, Hiippala's "Semiotically-grounded Distant Viewing of Diagrams" in *Digital Scholarship in the Humanities* (2022, with Bateman) combines multimodality theory with computational methods — and his 2021 piece "Distant Viewing and Multimodality Theory" in *Multimodality & Society* explicitly argues that computational models based on simple text/image distinctions "lack sufficient reach" for semiotically-oriented research.

The GeM framework is the **most important reference point** for the JSON schema. It establishes the precedent for structured annotation of page-based design, but uses XML and is oriented toward linguistic multimodality rather than design-specific properties like typographic weight, grid systems, or visual hierarchy as rhetorical devices. A JSON schema that captures these design-specific rhetorical properties while maintaining GeM's multi-layered architecture would represent a genuine methodological advance.

### Visual rhetoric theory provides the interpretive scaffolding

The theoretical foundation rests on several pillars. **Kress and van Leeuwen's** *Reading Images: The Grammar of Visual Design* (Routledge, 1996/2006/2021) provides the systematic "visual grammar" based on Halliday's metafunctions — representational, interactive, and compositional — that has become the standard framework for analyzing visual meaning. **Barthes' "Rhetoric of the Image"** (1964/1977) establishes the crucial distinction between **anchorage** (text fixes image meaning) and **relay** (text and image in complementary relationship). Martinec and Salway's "A System for Image–Text Relations" (*Visual Communication*, 2005) extends Barthes into a more granular taxonomy directly useful for computational operationalization.

**Johanna Drucker's** body of work is essential for the design-as-rhetoric argument. Her *Graphesis: Visual Forms of Knowledge Production* (Harvard UP, 2014) argues for understanding visualization as "performative" rather than "representational" — shifting from what an artifact *is* to what it *does*. Her earlier *The Visible Word* (University of Chicago Press, 1994) analyzes how avant-garde typography emphasized materiality as the heart of experimental representation. Drucker's *Visualization and Interpretation* (MIT Press, 2020) extends this into digital contexts. **Ellen Lupton's** *Thinking with Type* (Princeton Architectural Press, 2004/2024) treats typography as "the convergence of art and language" — a design system rather than decoration. **Sonja Foss's** "Framing the Study of Visual Rhetoric" (2004) provides the theoretical warrant for treating visual design as rhetorical artifact.

### Document AI has matured but ignores rhetoric

The computer science literature on document understanding is vast and technically mature but operates in a completely different paradigm from visual rhetoric. **LayoutLM** (Xu et al., KDD 2020) pioneered jointly learning text and layout for document understanding; **LayoutLMv2** (2021) and **LayoutLMv3** (Huang et al., 2022) added progressively deeper visual features. **DiT** (Li et al., ACM Multimedia 2022) applies self-supervised pre-training to 42 million document images. **DocLayout-YOLO** (2024) introduces efficient layout analysis with synthetic pretraining. Major benchmarks include **PubLayNet** (360,000+ annotated pages) and **DocLayNet** (IBM, 80,863 pages with 11 element categories).

These models detect layout elements — text blocks, figures, tables, headers — but make **no rhetorical claims** about what those elements *do*. Bridging this gap is a key opportunity. The paper can argue that document AI provides the *perception* layer (what elements exist and where) while the JSON schema provides the *interpretation* layer (what those elements argue and how).

### Vision-language models now enable design critique at scale

The most exciting recent development is using multimodal LLMs for design analysis. **Duan et al.** ("Generating Automatic Feedback on UI Mockups with Large Language Models," CHI 2024) built a Figma plugin querying GPT-4 with JSON representations of UI mockups. Their follow-up **UICrit** (UIST 2024) created a dataset of 3,059 design critiques from 7 professional designers, achieving a **55% performance gain** in LLM-generated UI feedback using few-shot and visual prompting. Critique categories included layout (696 critiques), typography, color, hierarchy, and spacing — directly parallel to the proposed schema's domains.

A comprehensive survey — "From Fragment to One Piece: A Survey on AI-Driven Graphic Design" (*Journal of Imaging*, 2025) — reviews ~500 papers across perception and generation tasks, covering layout analysis, typography, color theory, aesthetic evaluation, and visual hierarchy. In computational visual rhetoric specifically, **Ye et al.** ("Interpreting the Rhetoric of Visual Advertisements," *IEEE TPAMI*, 2021) annotated 64,832 image ads for persuasive arguments and symbolic associations. A 2023 Pittsburgh PhD dissertation modeled Aristotelian modes of persuasion (ethos, pathos, logos) in visual media using CLIP and spatial attention models.

### McLuhan scholarship awaits computational treatment

The most substantial scholarly analysis of *The Medium is the Massage* is **Kenneth Allan's** "Marshall McLuhan and the Counterenvironment" (*Art Journal*, 2014), which argues the book functions as a counterenvironment whose experimental form directs attention to usually unnoticed aspects of media. **J. Abbott Miller's** interview with Fiore in *Eye Magazine* (1992) remains the definitive primary source on the book's design process, revealing that Fiore controlled all texts, images, their order, and arrangement — McLuhan revised only one word. The book's self-referential design operates at multiple levels: the medium of the book argues about media, the disruption of linear reading performs the argument about the end of typographic linearity, and the famous thumbs-holding-the-book spread collapses the distinction between representation and experience.

**No computational or AI-based analysis of McLuhan's works exists in the literature.** This gap makes the proposed paper genuinely novel.

---

## Methodological rigor requires three validation layers

The paper's methodology must address a fundamental challenge: visual rhetoric claims are interpretive, but the JSON schema imposes structure on interpretation. Three validation approaches, used together, would establish credibility.

### Schema reliability through Krippendorff's alpha

**Krippendorff's alpha (α)** is the recommended universal reliability measure for content analysis (Hayes & Krippendorff, *Communication Methods and Measures*, 2007). It handles any number of coders, works with nominal, ordinal, interval, and ratio data, and manages missing data — all advantages over Cohen's kappa for design analysis where judgments span multiple scales. The threshold for reliable conclusions is **α ≥ 0.800**; tentative conclusions require α ≥ 0.667.

The practical workflow: recruit **3–5 design experts** to independently apply the JSON schema to a sample of 10–15 spreads from *The Medium is the Massage*. Conduct iterative codebook refinement — expect lower initial agreement on subjective categories like "rhetorical function of whitespace" and plan 2–3 rounds of calibration. The **K-Alpha Calculator** (Marzi et al., 2024, k-alpha.org) provides web-based computation with bootstrap confidence intervals. For ordinal variables (e.g., typography expressiveness on a scale), use weighted alpha.

### AI validation through the LLM-as-Judge paradigm

If using GPT-4V or similar vision-language models to generate design analyses, validation against expert human judgment follows the emerging **LLM-as-Judge** framework. Strong LLM judges achieve **80–90% agreement** with human evaluators, comparable to inter-annotator agreement between humans (~81%) per Zheng et al. (2023). The recommended metrics are **ICC(3,k)** (intraclass correlation coefficient, two-way mixed effects) as the primary measure, with Krippendorff's alpha and Gwet's AC2 as secondary measures. A 2025 clinical summarization study achieved ICC = 0.818 using GPT-o3-mini with 5-shot prompting — a useful benchmark target.

The **EvalGen** framework (Shankar et al., 2024) offers a practical "validate the validators" approach: iteratively align LLM-generated evaluation functions with human requirements through human grading of subsets. For design analysis specifically, the UICrit approach of creating a expert-critique dataset and then measuring LLM performance against it provides a proven template.

### Ground truth through empirical behavioral evidence

Eye-tracking studies can provide the strongest empirical evidence that design choices function rhetorically as claimed. A 2024 review of eye-tracking for design evaluation (PMC11673074) documents how **fixation duration, saccade patterns, and pupil dilation** validate whether visual hierarchies function as designers intend. Particularly relevant is Gkiouzepas et al.'s study in the *Journal of Eye Movement Research* demonstrating that typographic rhetorical figures attract significantly more attention than non-figurative typefaces — direct evidence that typography operates rhetorically.

For a single case study like *The Medium is the Massage*, think-aloud protocols with 15–20 participants examining the book's spreads would provide reader-response data validating interpretive claims. This is complementary to, not a substitute for, schema reliability testing.

---

## Presenting the JSON schema as a methodological contribution

The JSON schema itself constitutes a significant contribution if positioned correctly. The most effective approach draws from several conventions.

**Model the architecture on GeM's multi-layered structure** (base, layout, rhetorical, navigation layers) but implement in JSON/JSON-LD rather than XML for modern interoperability. Align with existing standards: **IIIF Presentation API 3.0** for image references (book pages as IIIF Canvases), **W3C Web Annotation Data Model** for linking design analysis to specific page regions, and **JSON-LD** contexts for RDF interoperability. This standards alignment dramatically strengthens the schema's credibility as a reusable contribution.

Schema methodology papers should include: **competency questions** (what questions can the schema answer?), **design rationale** (why each field exists and what theoretical framework it maps to), **formal specification** (JSON Schema with clear types, enumerations, and constraints), **alignment tables** mapping to GeM layers and IIIF, **reliability testing results**, and **worked examples** on diverse books. The SciData model (Chalk, *Journal of Cheminformatics*, 2016) — a JSON-LD data model with associated ontology — provides a useful template for how data schemas are presented as first-class methodological contributions in information science.

Publish the schema on GitHub with semantic versioning, assign a DOI via Zenodo, and include sample annotated data. Apply the **FAIREST principles** for digital humanities (Joyeux-Prunel, *International Journal of Digital Humanities*, 2024) — extending FAIR with Ethics, Expertise, Source mention, and Timestamp requirements — and acknowledge the interpretive dimensions that resist full computational reproducibility.

---

## Statistical and computational methods worth adopting

For the computational analysis pipeline, several established approaches from cultural analytics are directly applicable. **Lev Manovich's cultural analytics** methodology — extracting visual features, projecting into feature space, applying dimensionality reduction — provides the foundational framework. Extract visual features using CNN architectures (Inception v3 or ResNet), apply **UMAP** (preferred over t-SNE for preserving global structure) for 2D projection, and use **k-means or DBSCAN clustering** to identify design "families" across spreads. A DHQ article on "More than Distant Viewing" (2023) demonstrates this pipeline with appropriate caveats about interpretation.

For typography classification, **DeepFont** (Wang et al., Adobe Research, 2015) remains the reference CNN-based font recognition system, trained on 2,383 font categories. For layout element detection, **YOLOv8** (outperforming DiT and LayoutLMv3 by 8.95% and 38.48% IoU respectively in recent benchmarks) or **DiT** are current state-of-the-art. **GraphLayoutLM** (Li et al., 2023) models spatial and hierarchical relationships between document elements as graph nodes and edges — applicable to analyzing how design elements relate structurally across a book's spreads.

---

## Conclusion: a clear path forward

The proposed paper occupies an **uncontested scholarly niche**. Five key takeaways guide the path to publication. First, submit to **Visible Language** or **Visual Communication** for design-community impact, or **Digital Scholarship in the Humanities** for computational-humanities positioning — the choice depends on which audience matters most for the author's career. Second, cite **Hiippala and Bateman's GeM framework** as the primary methodological ancestor, positioning the JSON schema as its modern, design-rhetoric-specific successor. Third, cite the **document AI literature** (LayoutLM, DiT) as the computational perception layer and the **visual rhetoric theory** (Kress & van Leeuwen, Drucker, Barthes) as the interpretive layer — the paper's contribution is bridging these. Fourth, validate with **Krippendorff's alpha ≥ 0.80** on expert schema application, and if using VLMs, benchmark against human expert agreement using ICC(3,k). Fifth, the complete absence of computational McLuhan analysis means the case study itself carries novelty — but frame it as demonstrating a generalizable method, not just an interesting one-off reading of a famous book.