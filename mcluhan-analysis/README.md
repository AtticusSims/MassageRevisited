# McLuhan Analysis Pipeline

Structured analysis of Marshall McLuhan & Quentin Fiore's *The Medium is the Massage: An Inventory of Effects* (1967) — producing a page-by-page database for creating a contemporary AI-era companion book.

**Status:** Phase B (analysis) — Batch 1 complete (spreads 001-010 of 85)
**Live viewer:** [GitHub Pages](https://atticussims.github.io/MassageRevisited/) (static site, hosted from `docs/`)

---

## Project Overview

This repository contains the analysis infrastructure for **Step 3** of a larger creative-research project: a new book that mirrors the page-by-page structure of McLuhan's 1967 classic, replacing "electric media" concerns with AI-era equivalents. The analysis database produced here feeds directly into downstream planning, authoring, and design phases.

The pipeline combines:
- **Local VLMs** (Qwen3-VL, Molmo2-8B) for OCR and image description
- **Claude Opus 4.6** (via Claude Code) for interpretive analysis and orchestration
- **Human review** for quality assurance and approval

Every spread receives a structured JSON entry covering identification, text, quotations, images, design, rhetoric, themes, and progression — with rhetoric (how the design enacts the argument) as the most analytically weighted section.

---

## Quick Start

```bash
# Build the static site (requires Pillow for image compression)
pip install Pillow
python source/build_static_site.py

# Serve locally and open in browser
python -m http.server 8000 --directory docs
# Open http://localhost:8000

# Or use the Flask viewer for development
python viewer/app.py
# Open http://localhost:5001

# Run OCR on a single spread (requires Ollama with qwen3-vl)
python source/vlm_tools.py ocr rendered/spread_009.png

# Generate visual analysis for all spreads
python source/generate_visual_analysis.py
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
│   │   └── spread_NNN.json          # Per-spread merged data (10 files)
│   └── images/                      # Compressed JPEGs (85 files, ~19 MB)
│       └── spread_NNN.jpg
│
├── source/                          # Source materials, schemas, and scripts
│   ├── analysis_schema_v1.1.json    # JSON Schema defining entry structure
│   ├── claude_code_analysis_instructions.md  # Analysis methodology
│   ├── phase_b_methodology.md       # Detailed field-by-field methodology
│   ├── image_credits_lookup.json    # Credits cross-reference table
│   ├── sample_entry_spread_008.json # Gold standard: typography spread
│   ├── sample_entry_spread_011.json # Gold standard: surveillance spread
│   ├── vlm_tools.py                 # VLM utilities (OCR, description, layout)
│   ├── generate_visual_analysis.py  # Qwen3-VL visual analysis generation
│   ├── build_static_site.py         # Static site build script
│   ├── build_batch_001_010.py       # Batch 1 analysis script
│   ├── compare_qwen_versions.py     # Model comparison tool
│   ├── run_molmo_conda.py           # Molmo2-8B execution wrapper
│   └── *.pdf                        # Source PDF (not tracked in git)
│
├── output/                          # Generated analysis data
│   ├── analysis_database.json       # Main structured database (10 entries)
│   ├── review_status.json           # Approve/flag/pending tracking
│   └── vlm_extractions/             # VLM outputs
│       ├── spread_*_ocr.json        # Qwen2.5-VL OCR (10 files, archived)
│       ├── spread_*_ocr_qwen3.json  # Qwen3-VL OCR (10 files)
│       ├── spread_*_visual_qwen3.json # Qwen3-VL visual analysis (10 files)
│       └── qwen_version_comparison.json  # Model comparison data
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
│   └── Medium_is_Massage_Revisited_-_Project_Plan_v3.md  # Project spec
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
| [`source/phase_b_methodology.md`](source/phase_b_methodology.md) | Field-by-field methodology for the analysis schema. Includes guiding questions for interpretive sections, VLM correlation strategy, and quality checklist. | Analysts, methodologists |
| [`source/claude_code_analysis_instructions.md`](source/claude_code_analysis_instructions.md) | Complete analysis instructions: three-pass process, quality bar, schema field definitions, execution sequence. The operating manual for the analysis pipeline. | Pipeline operators |

### Theoretical Framework
| Document | Description | Audience |
|----------|-------------|----------|
| [`ContextDocs/framework_v3.md`](ContextDocs/framework_v3.md) | Complete intellectual architecture for the companion book: three movements, six convergences, 20+ thinker profiles, 150+ curated quotations with attribution. | Researchers, editors |
| [`ContextDocs/theorist_reference.md`](ContextDocs/theorist_reference.md) | Deep profiles of each thinker: salient ideas, relevant domains, key works with quotability notes. | Writers, researchers |
| [`ContextDocs/Medium_is_Massage_Revisited_-_Project_Plan_v3.md`](ContextDocs/Medium_is_Massage_Revisited_-_Project_Plan_v3.md) | Full project specification: concept, scope, five-phase pipeline, system architecture, target output. | Project stakeholders |

### Data & Schema
| Document | Description | Audience |
|----------|-------------|----------|
| [`source/analysis_schema_v1.1.json`](source/analysis_schema_v1.1.json) | JSON Schema (draft-07) defining the structure of every analysis entry. 9 sections, 50+ fields per spread. | Developers, data consumers |
| [`source/sample_entry_spread_008.json`](source/sample_entry_spread_008.json) | Gold standard sample: "and how!" typography spread — defines quality bar. | Analysts |
| [`source/sample_entry_spread_011.json`](source/sample_entry_spread_011.json) | Gold standard sample: "you" surveillance spread — defines quality bar. | Analysts |
| [`output/vlm_extractions/qwen_version_comparison.json`](output/vlm_extractions/qwen_version_comparison.json) | Raw data from Qwen2.5-VL vs Qwen3-VL comparison across 5 spreads. | Researchers |

---

## Key Technical Decisions

1. **Qwen3-VL as sole VLM:** Handles OCR, image description, and layout analysis. Dramatic quality improvement over Qwen2.5-VL on dense serif text outweighs 2-7x speed penalty. Molmo2-8B archived due to inconsistent results. See [`TECHNICAL_NOTES.md`](TECHNICAL_NOTES.md) for evaluation data.

2. **Two-model architecture:** Qwen3-VL (all VLM tasks — OCR, image description, layout analysis) + Claude Opus 4.6 (interpretive analysis, orchestration). Simplified from original three-model approach.

3. **Static site deployment:** GitHub Pages serves the review viewer from `docs/`. Build script merges analysis + OCR + visual data into per-spread JSON files, compresses PNGs to JPEG. No server required.

4. **Human-in-the-loop review:** Approve/flag/pending workflow ensures no analysis enters the downstream pipeline without human verification. Review state stored in browser localStorage.

5. **Rhetoric as primary analytical layer:** The `design_enacts_argument` field is the most important in the schema — capturing how McLuhan & Fiore's design performs their argument, not just illustrates it.

---

## Requirements

**For building the static site:**
- Python 3.10+
- Pillow (image compression)

**For running VLM analysis:**
- Ollama with `qwen3-vl` model
- PyMuPDF (fitz) for PDF rendering

**For local Flask development (optional):**
- Flask

---

## License

This analysis pipeline and its outputs are part of an ongoing research project. The source material (*The Medium is the Massage*, 1967) is under copyright by the McLuhan estate and Penguin Random House. The analysis database, code, and documentation in this repository are original work.
