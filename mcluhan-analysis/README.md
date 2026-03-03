# McLuhan Analysis Pipeline

Structured analysis of Marshall McLuhan & Quentin Fiore's *The Medium is the Massage: An Inventory of Effects* (1967) — producing a page-by-page database for creating a contemporary AI-era companion book.

**Status:** Phase B (analysis) and Phase C (content planning) complete — 85 spreads analyzed and mapped to contemporary AI-era equivalents
**Live viewer:** [GitHub Pages](https://atticussims.github.io/MassageRevisited/) (static site, hosted from `docs/`)

---

## Project Overview

This repository contains the analysis and content planning infrastructure for a larger creative-research project: a new book ("The Model is the Massage") that mirrors the page-by-page structure of McLuhan's 1967 classic, replacing "electric media" concerns with AI-era equivalents. The analysis database and content plan produced here feed directly into downstream authoring and design phases.

The pipeline combines:
- **Local VLMs** (Qwen3-VL for OCR; Molmo2-8B archived) plus **Gemini 2.5 Pro** (visual descriptions)
- **Claude Opus 4.6** (via Claude Code) for interpretive analysis, content planning, and orchestration
- **Human review** for quality assurance and approval

**Phase B (Analysis):** Every spread receives a structured JSON entry covering identification, text, quotations, images, design, rhetoric, themes, and progression — with controlled vocabularies grounded in Kress & van Leeuwen (visual grammar), Barthes (image-text relations), Drucker (performative design), and Bateman/Hiippala (GeM framework). Rhetoric (how the design enacts the argument) is the most analytically weighted section.

**Phase C (Content Planning):** Every spread receives a contemporary plan mapping the original's argument to an AI-era equivalent, with specified rhetorical strategy, thinker citations, convergence threads, and concrete text/image/design directions. Plans are organized across five movements (Prologue, M1:Environment, M2:Acceleration, Hinge, M3:Dreamscape) with six convergence threads traced through the entire arc.

---

## Quick Start

```bash
# Build the static site (requires Pillow for image compression)
pip install Pillow
python source/build_static_site.py

# Serve locally and open in browser
python -m http.server 8000 --directory docs
# Open http://localhost:8000

# Re-analyze all 85 spreads with v1.2 schema
python source/batch_create_analysis_v2.py

# Generate the content plan (baseline)
python source/generate_content_plan.py

# Merge improved section plans into content_plan.json
python source/merge_sections.py

# Update meta section from actual plan data
python source/update_meta.py

# Run OCR on a single spread (requires Ollama with qwen3-vl)
python source/vlm_tools.py ocr rendered/spread_009.png

# Generate Gemini visual descriptions (requires GEMINI_API_KEY)
python source/generate_gemini_descriptions.py
```

---

## Repository Structure

```
mcluhan-analysis/
├── docs/                            # Static site for GitHub Pages (generated)
│   ├── index.html                   # Single-page viewer (client-side JS)
│   ├── style.css                    # Dark theme CSS
│   ├── data/                        # JSON data files
│   │   ├── index.json               # Navigation metadata (85 spreads)
│   │   └── spread_NNN.json          # Per-spread merged data (86 files: 1 index + 85 spread data)
│   └── images/                      # Compressed JPEGs (85 files, ~19 MB)
│       └── spread_NNN.jpg
│
├── source/                          # Source materials, schemas, and scripts
│   ├── analysis_schema_v1.2.json    # JSON Schema v1.2 with theoretical grounding
│   ├── analysis_schema_v1.1.json    # JSON Schema v1.1 (retained for reference)
│   ├── claude_code_analysis_instructions.md  # Analysis methodology
│   ├── phase_b_methodology.md       # Detailed field-by-field methodology (Phase B)
│   ├── phase_b_methodology_v2.md    # Updated methodology for planning phase
│   ├── image_credits_lookup.json    # Credits cross-reference table
│   ├── sample_entry_spread_008.json # Gold standard: typography spread
│   ├── sample_entry_spread_011.json # Gold standard: surveillance spread
│   ├── vlm_tools.py                 # VLM utilities (OCR, description, layout)
│   ├── gemini_tools.py              # Gemini API client module
│   ├── generate_visual_analysis.py  # Qwen3-VL visual analysis generation
│   ├── generate_gemini_descriptions.py  # Gemini 2.5 Pro visual descriptions
│   ├── generate_content_plan.py     # Planning Engine: generates content_plan.json
│   ├── merge_sections.py            # Merge improved section plans into content plan
│   ├── update_meta.py               # Rebuild meta section from actual plan data
│   ├── merge_gemini_analysis.py     # Compare Gemini vs existing + merge tools
│   ├── build_static_site.py         # Static site build script
│   ├── batch_create_analysis_v2.py  # Batch analysis script (v1.2 schema)
│   ├── theme_vocabulary.json        # Versioned vocabulary registry
│   ├── build_batch_001_010.py       # Batch 1 analysis script
│   ├── compare_qwen_versions.py     # Model comparison tool
│   ├── run_molmo_conda.py           # Molmo2-8B execution wrapper
│   └── *.pdf                        # Source PDF (not tracked in git)
│
├── output/                          # Generated analysis and planning data
│   ├── analysis_database.json       # Main structured database (85 entries, schema v1.2)
│   ├── content_plan.json            # Complete content plan (85 entries + meta, 402KB)
│   ├── analysis_database_v1.1_archive.json  # Archived v1.1 analysis
│   ├── gemini_comparison_report.md  # Field-by-field Gemini vs existing comparison
│   ├── review_status.json           # Approve/flag/pending tracking
│   ├── *_plans_improved.json        # Per-section improved plan files (4 files)
│   ├── vlm_extractions/             # VLM outputs
│   │   ├── spread_*_ocr.json        # Qwen2.5-VL OCR (10 files, archived)
│   │   ├── spread_*_ocr_qwen3.json  # Qwen3-VL OCR (10 files)
│   │   ├── spread_*_visual_qwen3.json # Qwen3-VL visual analysis (10 files)
│   │   └── qwen_version_comparison.json  # Model comparison data
│   └── gemini_extractions/          # Gemini outputs
│       └── spread_*_visual.json     # Gemini 2.5 Pro visual descriptions (85 files)
│
├── rendered/                        # Rendered book pages (PNG, 200 DPI)
│   └── spread_001.png ... spread_065.png
│
├── viewer/                          # Web review interface
│   ├── static_viewer.html           # Static viewer (→ docs/index.html)
│   ├── static_style.css             # Static CSS (→ docs/style.css)
│   ├── app.py                       # Flask server (local development)
│   ├── templates/viewer.html        # Flask viewer UI
│   └── static/style.css             # Flask viewer CSS
│
├── ContextDocs/                     # Theoretical framework documents
│   ├── framework_v3.md              # Complete intellectual architecture
│   ├── framework_v3_addendum.md     # Supplementary framework
│   ├── theorist_reference.md        # Thinker profiles and quotations
│   ├── Medium_is_Massage_Revisited_-_Project_Plan_v3.md  # Project spec
│   ├── visual_rhetoric_and_reliability.md  # Theoretical grounding and reliability framework
│   ├── publishing_landscape-computational_book_design_rhetoric.md  # Publication landscape analysis
│   ├── schema_methodology_revisions.md     # Schema v1.1 → v1.2 revision log
│   └── claude_code_planningEngine_instructions_v2.md  # Planning engine instructions
│
├── DEVELOPMENT_LOG.md               # Chronological development journal
├── TECHNICAL_NOTES.md               # VLM evaluation and infrastructure
└── README.md                        # This file
```

---

## Documentation Index

This project maintains several documentation files for research and reproducibility purposes.

### Development Process
| Document | Description | Audience |
|----------|-------------|----------|
| [`DEVELOPMENT_LOG.md`](DEVELOPMENT_LOG.md) | Chronological record of all development sessions, decisions made, work completed, and observations. Updated after each session. | Researchers, collaborators |
| [`TECHNICAL_NOTES.md`](TECHNICAL_NOTES.md) | Technical documentation: VLM model evaluations (with quantitative comparisons), OCR error taxonomy, prompt engineering, infrastructure details, reproducibility notes. | Technical readers, peer reviewers |

### Methodology
| Document | Description | Audience |
|----------|-------------|----------|
| [`source/phase_b_methodology.md`](source/phase_b_methodology.md) | Field-by-field methodology for the analysis schema (Phase B). Includes guiding questions for interpretive sections, VLM correlation strategy, and quality checklist. | Analysts, methodologists |
| [`source/phase_b_methodology_v2.md`](source/phase_b_methodology_v2.md) | Updated methodology for the planning phase (Phase C). Covers content plan entry generation, strategy vocabulary, thinker mapping requirements. | Analysts, methodologists |
| [`source/claude_code_analysis_instructions.md`](source/claude_code_analysis_instructions.md) | Complete analysis instructions: three-pass process, quality bar, schema field definitions, execution sequence. The operating manual for the analysis pipeline. | Pipeline operators |
| [`ContextDocs/claude_code_planningEngine_instructions_v2.md`](ContextDocs/claude_code_planningEngine_instructions_v2.md) | Planning engine specification: content plan schema, movement logic, convergence mapping, distribution targets. | Pipeline operators |

### Theoretical Framework
| Document | Description | Audience |
|----------|-------------|----------|
| [`ContextDocs/framework_v3.md`](ContextDocs/framework_v3.md) | Complete intellectual architecture for the companion book: three movements, six convergences, 20+ thinker profiles, 150+ curated quotations with attribution. | Researchers, editors |
| [`ContextDocs/theorist_reference.md`](ContextDocs/theorist_reference.md) | Deep profiles of each thinker: salient ideas, relevant domains, key works with quotability notes. | Writers, researchers |
| [`ContextDocs/Medium_is_Massage_Revisited_-_Project_Plan_v3.md`](ContextDocs/Medium_is_Massage_Revisited_-_Project_Plan_v3.md) | Full project specification: concept, scope, five-phase pipeline, system architecture, target output. | Project stakeholders |

### Data & Schema
| Document | Description | Audience |
|----------|-------------|----------|
| [`source/analysis_schema_v1.2.json`](source/analysis_schema_v1.2.json) | JSON Schema v1.2 with theoretical grounding (12 revisions from v1.1). 9 sections, 50+ fields per spread. | Developers, data consumers |
| [`source/analysis_schema_v1.1.json`](source/analysis_schema_v1.1.json) | JSON Schema v1.1 (retained for reference). | Developers |
| [`source/theme_vocabulary.json`](source/theme_vocabulary.json) | Versioned vocabulary registry (59 terms with definitions). | Analysts, developers |
| [`source/sample_entry_spread_008.json`](source/sample_entry_spread_008.json) | Gold standard sample: "and how!" typography spread — defines quality bar. | Analysts |
| [`source/sample_entry_spread_011.json`](source/sample_entry_spread_011.json) | Gold standard sample: "you" surveillance spread — defines quality bar. | Analysts |
| [`ContextDocs/visual_rhetoric_and_reliability.md`](ContextDocs/visual_rhetoric_and_reliability.md) | Working paper: theoretical foundations and reliability framework. | Researchers, peer reviewers |
| [`ContextDocs/schema_methodology_revisions.md`](ContextDocs/schema_methodology_revisions.md) | Detailed revision log for schema v1.1 → v1.2. | Developers, methodologists |
| [`output/vlm_extractions/qwen_version_comparison.json`](output/vlm_extractions/qwen_version_comparison.json) | Raw data from Qwen2.5-VL vs Qwen3-VL comparison across 5 spreads. | Researchers |
| [`output/content_plan.json`](output/content_plan.json) | Complete content plan: 85 page-by-page entries + meta section (movement plans, convergences, thinker distributions). | Writers, designers |
| [`output/gemini_comparison_report.md`](output/gemini_comparison_report.md) | Field-by-field comparison: Gemini 2.5 Pro visual descriptions vs existing analysis across all 85 spreads. | Researchers |

---

## Key Technical Decisions

1. **Three-model vision architecture:** Qwen3-VL (OCR — dramatic quality improvement over Qwen2.5-VL on dense serif text), Gemini 2.5 Pro (visual descriptions — accurate image identification where Qwen3-VL fails), Claude Opus 4.6 (interpretive analysis, content planning, orchestration). The original plan for a Qwen-only VLM pipeline was revised after Qwen3-VL's image description limitations were identified (e.g., misidentifying a foot as a hand on spread_050). See [`TECHNICAL_NOTES.md`](TECHNICAL_NOTES.md) for evaluation data.

2. **Claude-only content planning:** Despite having Gemini 2.5 Pro available for independent analysis, the content plan was generated entirely by Claude Opus 4.6. The user directed this approach to maintain interpretive consistency with the analytical framework.

3. **Parallel subagent architecture:** Content plan generation uses 4 parallel Claude Code subagents (one per movement section), each loaded with the full intellectual framework (~200KB). This was a deviation from the originally envisioned sequential approach, motivated by context window limits. See [`TECHNICAL_NOTES.md`](TECHNICAL_NOTES.md) Section 10.6.

4. **Static site deployment:** GitHub Pages serves the review viewer from `docs/`. Build script merges analysis + OCR + visual data + content plan into per-spread JSON files, compresses PNGs to JPEG. No server required.

5. **Human-in-the-loop review:** Approve/flag/pending workflow ensures no analysis enters the downstream pipeline without human verification. Review state stored in browser localStorage.

6. **Rhetoric as primary analytical layer:** The `design_enacts_argument` field is the most important in the schema — capturing how McLuhan & Fiore's design performs their argument, not just illustrates it.

7. **Theoretically grounded schema (v1.2):** Analysis schema maps to four established frameworks in multimodal discourse analysis: Kress & van Leeuwen (visual grammar), Barthes (image-text relations), Drucker (performative design), Bateman/Hiippala (GeM framework). Controlled vocabularies (15 rhetorical strategies, 19 McLuhan concepts) constrain analytical output to well-defined terms. See `ContextDocs/visual_rhetoric_and_reliability.md` for the full theoretical mapping.

8. **Distribution-validated content plan:** All 85 entries validated for: 15/15 strategies used with no adjacent duplicates, balanced relationship distribution (echo/transformation/inversion/departure), all 6 convergences threaded across movements, 20 thinkers with named works, and paper traces for every entry.

---

## Requirements

**For building the static site:**
- Python 3.10+
- Pillow (image compression)

**For running VLM analysis:**
- Ollama with `qwen3-vl` model
- PyMuPDF (fitz) for PDF rendering

**For Gemini visual descriptions (optional):**
- `google-generativeai` + `python-dotenv`
- `GEMINI_API_KEY` in `source/.env` or environment variable

**For local Flask development (optional):**
- Flask

---

## License

This analysis pipeline and its outputs are part of an ongoing research project. The source material (*The Medium is the Massage*, 1967) is under copyright by the McLuhan estate and Penguin Random House. The analysis database, code, and documentation in this repository are original work.
