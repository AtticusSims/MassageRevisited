# McLuhan Analysis Pipeline

Structured analysis of Marshall McLuhan & Quentin Fiore's *The Medium is the Massage: An Inventory of Effects* (1967) — producing a page-by-page database for creating a contemporary AI-era companion book.

**Status:** Phase B (analysis) — Batch 1 complete (spreads 001-010 of 85)

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
# Start the review viewer
python viewer/app.py
# Open http://localhost:5001

# Run OCR on a single spread (requires Ollama with qwen3-vl)
python source/vlm_tools.py ocr rendered/spread_009.png

# Run Molmo description (requires conda env 'molmo')
conda run -n molmo python source/run_molmo_conda.py describe rendered/spread_007.png
```

---

## Repository Structure

```
mcluhan-analysis/
├── source/                          # Source materials, schemas, and scripts
│   ├── analysis_schema_v1.1.json    # JSON Schema defining entry structure
│   ├── claude_code_analysis_instructions.md  # Analysis methodology
│   ├── phase_b_methodology.md       # Detailed field-by-field methodology
│   ├── image_credits_lookup.json    # Credits cross-reference table
│   ├── sample_entry_spread_008.json # Gold standard: typography spread
│   ├── sample_entry_spread_011.json # Gold standard: surveillance spread
│   ├── vlm_tools.py                 # VLM utilities (OCR, description, layout)
│   ├── run_molmo_conda.py           # Molmo2-8B execution wrapper
│   ├── compare_qwen_versions.py     # Model comparison tool
│   ├── build_batch_001_010.py       # Batch 1 analysis script
│   └── *.pdf                        # Source PDF (not tracked in git)
│
├── output/                          # Generated analysis data
│   ├── analysis_database.json       # Main structured database (10 entries)
│   ├── review_status.json           # Approve/flag/pending tracking
│   └── vlm_extractions/             # VLM OCR outputs
│       ├── spread_*_ocr.json        # Qwen2.5-VL extractions (10 files)
│       ├── spread_*_ocr_qwen3.json  # Qwen3-VL extractions (10 files)
│       └── qwen_version_comparison.json  # Model comparison data
│
├── rendered/                        # Rendered book pages (PNG, 200 DPI)
│   └── spread_001.png ... spread_065.png
│
├── viewer/                          # Flask web review interface
│   ├── app.py                       # Server with API endpoints
│   ├── templates/viewer.html        # Tabbed viewer UI
│   └── static/style.css             # Dark theme styles
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

1. **Qwen3-VL over Qwen2.5-VL:** Dramatic OCR quality improvement on dense serif text outweighs 2-7x speed penalty. See [`TECHNICAL_NOTES.md`](TECHNICAL_NOTES.md) for evaluation data.

2. **Three-model architecture:** Qwen3-VL (OCR primary), Molmo2-8B (image description secondary), Claude Opus 4.6 (interpretive analysis). Each model handles what it does best.

3. **Human-in-the-loop review:** Approve/flag/pending workflow ensures no analysis enters the downstream pipeline without human verification. See the web viewer at `localhost:5001`.

4. **Rhetoric as primary analytical layer:** The `design_enacts_argument` field is the most important in the schema — capturing how McLuhan & Fiore's design performs their argument, not just illustrates it.

---

## Requirements

- Python 3.10+
- Flask
- PyMuPDF (fitz)
- Ollama with `qwen3-vl` model
- (Optional) Conda environment `molmo` with HuggingFace Transformers 4.57.1 for Molmo2-8B

---

## License

This analysis pipeline and its outputs are part of an ongoing research project. The source material (*The Medium is the Massage*, 1967) is under copyright by the McLuhan estate and Penguin Random House. The analysis database, code, and documentation in this repository are original work.
