# Development Log

> Chronological record of the development process for the McLuhan Analysis Pipeline.
> This project analyzes Marshall McLuhan & Quentin Fiore's *The Medium is the Massage* (1967) to produce a structured database for creating a contemporary AI-era companion book.
>
> **Primary developer:** Human researcher (AtticusSims) + Claude Opus 4.6 (via Claude Code)
> **Repository:** https://github.com/AtticusSims/MassageRevisited

---

## Session 1 — 2026-03-02, ~13:00 (Phase A: Infrastructure)

**Commit:** `124653c` — "Phase A setup: project structure, schema, viewer, context docs"

### Objectives
- Set up the project repository and directory structure
- Render all 85 PDF pages as high-resolution PNGs
- Initialize the analysis database
- Build the first version of the web viewer
- Push to GitHub

### Work Completed

1. **Repository initialization**
   - Created `mcluhan-analysis/` directory structure: `source/`, `output/`, `rendered/`, `viewer/`, `ContextDocs/`
   - Initialized git repo, connected to GitHub remote

2. **PDF rendering**
   - Used PyMuPDF (`fitz`) to render all 85 pages of the compressed source PDF at 200 DPI
   - Output: 65 PNG files in `rendered/` directory (spread_001.png through spread_065.png)
   - Naming convention: `spread_NNN.png` with zero-padded three-digit PDF page numbers

3. **Schema design**
   - Created `analysis_schema_v1.1.json` (JSON Schema draft-07)
   - Schema version 1.1 includes `movement_mapping` field added during framework development
   - Designed 9 top-level sections per spread entry: identification, text, quotations, images, design, rhetoric, themes, progression, notes
   - Created two gold-standard sample entries (`sample_entry_spread_008.json`, `sample_entry_spread_011.json`) to define the quality bar

4. **Analysis instructions**
   - Wrote `claude_code_analysis_instructions.md` — comprehensive instructions defining the three-pass analysis process
   - Specified the quality bar, field-by-field methodology, and execution sequence

5. **Image credits lookup**
   - Transcribed credits from PDF page 84 (book pages 158-159) into `image_credits_lookup.json`
   - Keyed by book page numbers for cross-referencing during analysis

6. **Database initialization**
   - Created `analysis_database.json` with metadata header (schema version 1.1, 85 total PDF pages, 160 total book pages)

7. **Web viewer (v1)**
   - Built Flask application (`viewer/app.py`) serving on `localhost:5001`
   - Two-panel layout: spread image (left) + analysis data (right)
   - Dark theme CSS (`viewer/static/style.css`) with amber accent
   - Navigation: previous/next buttons, dropdown selector, keyboard shortcuts
   - Formatted display for all schema sections with appropriate visual treatment (tags, badges, cards)
   - Rhetoric section visually highlighted as the most important analytical layer

8. **Context documents**
   - Placed framework documents in `ContextDocs/`:
     - `framework_v3.md` — complete intellectual architecture with 150+ curated quotations
     - `framework_v3_addendum.md` — supplementary framework material
     - `theorist_reference.md` — deep profiles of 20+ thinkers with quotable works
     - `Medium_is_Massage_Revisited_-_Project_Plan_v3.md` — full project specification
     - `MassageRevisited_conceptOutline.pdf` — concept outline

### Technical Decisions
- **Rendering DPI:** 200 DPI chosen as balance between file size and readability for both human review and VLM processing
- **Flask over alternatives:** Chosen for zero-dependency simplicity; no build step required
- **Single HTML template:** All rendering logic in JavaScript within the template to keep the viewer self-contained
- **Dark theme:** Chosen to reduce eye strain during extended review sessions; also aesthetically appropriate for a book about media

### Known Issues
- The PDF has varying page dimensions (portrait covers, landscape body spreads, one rotated page)
- Not all 85 pages rendered as expected (65 files generated) — may relate to PDF structure

---

## Session 2 — 2026-03-02, ~14:00 (Phase B: First Analytical Batch)

**Commit:** `d801622` — "Phase B batch 1: analysis entries for spreads 001-010"

### Objectives
- Establish the VLM pipeline for OCR and image description
- Analyze the first 10 spreads (PDF pages 1-10) as a review checkpoint
- Test the viewer with real data

### Work Completed

1. **VLM pipeline setup**
   - Created `vlm_tools.py` — modular VLM utility supporting OCR, structured OCR, image description, and layout analysis
   - Primary OCR model: **Qwen2.5-VL-7B** via Ollama (`qwen2.5vl:7b`)
   - Secondary model planned: **Molmo2-8B** via HuggingFace Transformers
   - Ollama running locally on `localhost:11434`

2. **OCR extraction (batch 1)**
   - Ran Qwen2.5-VL-7B on all 10 spreads
   - Two prompts per spread: raw OCR extraction + structured OCR (categorized by DISPLAY_TEXT, BODY_TEXT, QUOTATIONS, CAPTIONS, PAGE_NUMBERS)
   - Output saved to `output/vlm_extractions/spread_001_ocr.json` through `spread_010_ocr.json`

3. **Analysis entries (spreads 001-010)**
   - Created `build_batch_001_010.py` — script generating all 10 structured analysis entries
   - Each entry follows the v1.1 schema with all 9 sections populated
   - OCR text used as starting point, then manually refined by Claude for accuracy
   - Rhetoric, themes, and progression sections written interpretively by Claude

4. **Content filter workaround**
   - Some VLM prompts triggered content filters on the blurred face image (spread_001)
   - Resolved by adjusting prompt wording to avoid terms that triggered filters

5. **Molmo2-8B initial setup**
   - Downloaded model weights from HuggingFace (`allenai/Molmo2-8B`)
   - Created conda environment (`molmo`) with Python 3.11, transformers 4.57.1, torch 2.10.0+cu128
   - Encountered compatibility issues with cached model files (rope_type parameter)

### Technical Decisions
- **Two-model approach:** Using Qwen for OCR (fast, via Ollama API) and Molmo for image description (more detailed, via Transformers) to enable cross-validation
- **Structured OCR prompt:** Designed to separate text by function (display, body, quotation, caption, page number) — enables automated field population
- **Ollama chat endpoint:** Used `/api/chat` rather than `/api/generate` — better results for vision models

### Analysis Notes
- Spreads 001-005: Front matter (cover, dust jacket, title page, copyright, epigraph)
- Spreads 006-010: Begin body content with dense prose text and the first quotation (A.N. Whitehead)
- The book's argument begins immediately with the cover — the blurred face IS the first argument about mediation

---

## Session 3 — 2026-03-02, ~15:00 (Quality Improvements & Methodology)

**Commit:** `f26c3bc` — "Phase B improvements: OCR fixes, methodology template, Molmo2-8B integration"

### Objectives
- Fix OCR errors discovered during spot-checking
- Get Molmo2-8B working for image description correlation
- Create detailed methodology documentation
- Strengthen weak analysis fields

### Work Completed

1. **Molmo2-8B integration**
   - Fixed compatibility issues: reverted `rope_type` from "linear" to "default" in cached `modeling_molmo2.py` (lines 543, 964)
   - Fixed `torch_dtype` deprecation warning in `run_molmo_conda.py` (changed to `dtype`)
   - Successfully tested: model loads in ~20s, generates descriptions in ~165s
   - Tested on spread_007 (hand photograph): produced coherent description
   - Tested on spread_005 (egg/branded product): **missed the egg entirely**, only described typography
   - Layout analysis weak — misidentified elements on spread_007
   - **Conclusion:** Molmo useful for secondary correlation but not reliable as primary image descriptor

2. **OCR error corrections**
   - **Spread 009** — Three corrections to body text:
     - "psychological responses conditionally" → "...and concepts conditioned by the former technology—mechanization"
     - "co-operations and feelings" → "confusions and a profound feeling of despair"
     - Garbled bottom paragraph → corrected "Youth instinctively understands..." text
   - **Spread 010** — Corrected garbled final paragraph ("evaders", "substance", "Survival")
   - Root cause: Qwen2.5-VL struggled with dense serif text, especially near the gutter/spine

3. **Methodology documentation**
   - Created `source/phase_b_methodology.md` — comprehensive methodology template
   - Field-by-field table mapping each schema field to primary method, tools used, and notes
   - VLM correlation strategy documented (two-model approach with manual arbitration)
   - Detailed guiding questions for interpretive sections:
     - Themes: 4 questions for `original_themes`, 4 for `contemporary_domain_candidates`, 3 for `movement_mapping`
     - Progression: 3 questions each for `pace_shift`, `thematic_function`, `relationship_to_previous/next`
   - Quality checklist with 12 verification items per entry
   - Good/weak examples for `mapping_rationale` and `relationship_to_previous`

4. **Database corrections**
   - Spread 006: Changed `spread_type` from "other" to "credits_or_colophon", `section` from "body" to "front_matter"
   - Spreads 002, 003: Strengthened `mapping_rationale` with specific contemporary parallels
   - Spreads 009, 010: Updated `notes` fields to document OCR corrections

### Technical Decisions
- **Molmo2-8B role downgraded:** From planned co-primary to secondary correlation tool. Image description inconsistent; layout analysis unreliable. Kept for cases where cross-validation is valuable.
- **OCR corrections via Python script:** Edit tool couldn't handle Unicode em dashes in the JSON — used `json.load()`/`json.dump()` for programmatic text replacement
- **Methodology-first approach:** Created detailed methodology documentation before proceeding to batch 2, ensuring consistent analytical quality

### Observations for Research
- VLM OCR quality varies dramatically with text density and font characteristics
- Dense serif body text near the gutter/spine produces the most OCR errors
- Display text (large, high-contrast) is reliably extracted by both Qwen2.5 and Molmo
- The book's design creates specific challenges: reversed text (white on black), text overlaid on photographs, text spanning the gutter

---

## Session 4 — 2026-03-02, ~16:00 (Qwen3-VL Upgrade & Review Interface)

**Commit:** `cbaddad` — "Switch to Qwen3-VL, add OCR comparison viewer with review workflow"

### Objectives
- Evaluate Qwen3-VL against Qwen2.5-VL for OCR quality
- Switch pipeline to better model if justified
- Re-run OCR on all 10 spreads with the new model
- Build a manual review interface with approve/flag workflow

### Work Completed

1. **Qwen3-VL evaluation**
   - Pulled `qwen3-vl` model via Ollama (6.1 GB)
   - Created `source/compare_qwen_versions.py` — systematic comparison script
   - Tested on 5 representative spreads:

   | Spread | Task | Qwen 2.5 | Qwen 3 | Winner |
   |--------|------|----------|--------|--------|
   | 001 (cover) | Raw OCR | Partial text (117ch) | **Empty (0ch)** | 2.5 |
   | 001 (cover) | Structured OCR | Partial | Complete | Qwen3 |
   | 009 (dense text) | Raw OCR | Garbled (104ch) | **Clean (1958ch)** | Qwen3 |
   | 009 (dense text) | Structured OCR | Garbled | **Clean** | Qwen3 |
   | 010 (dense text) | Raw OCR | Garbled | **Perfect** | Qwen3 |
   | 005 (egg/branding) | Image description | Missed egg | Missed egg | Tie (both poor) |
   | 007 (hand photo) | Image + Layout | Basic | **Detailed** | Qwen3 |

   - **Speed:** Qwen3-VL is 2-7x slower than Qwen2.5-VL consistently
   - **Quality verdict:** Qwen3 dramatically better on difficult OCR (dense text, serif fonts, gutter-spanning words). Fixed every error that 2.5 produced. Occasional empty responses on some images (spread_001 raw OCR).

2. **Pipeline switch**
   - Changed `OLLAMA_MODEL` in `vlm_tools.py` from `"qwen2.5vl:7b"` to `"qwen3-vl"`
   - Updated docstrings and comments

3. **Qwen3 OCR batch (all 10 spreads)**
   - Generated `spread_001_ocr_qwen3.json` through `spread_010_ocr_qwen3.json`
   - Implemented retry logic for empty responses (retry once if raw OCR returns empty)
   - Kept original Qwen2.5 files alongside for comparison
   - Notable results:
     - Spread 008: Only 130 chars even after retry (minimal visible text on this spread — working as expected)
     - Spread 009: 1,958 chars clean text vs 104 chars garbled from Qwen2.5
     - Spread 010: 1,425 chars clean text vs garbled output from Qwen2.5

4. **Review interface (v2)**
   - Rewrote `viewer/app.py`:
     - New endpoint `/api/ocr/<spread_id>` — loads both Qwen2.5 and Qwen3 OCR files
     - New endpoints `/api/review/<spread_id>` (GET/POST) — review status management
     - Review status persisted to `output/review_status.json`
   - Rewrote `viewer/templates/viewer.html`:
     - **Tab bar:** Analysis | OCR Compare tabs
     - **Review controls:** Approve / Flag / Reset buttons + notes text input
     - **OCR Compare view:** Side-by-side Qwen 2.5 vs Qwen 3 columns, both raw and structured OCR, with timing and character count metadata
     - **Keyboard shortcuts:** Arrow keys or a/d (navigate), 1/2 (switch tabs), y (approve), f (flag)
     - **Review status indicators:** Checkmark/flag icons in dropdown, header counters for approved/flagged/pending
   - Updated `viewer/static/style.css`:
     - Tab bar styles (`.tab-bar`, `.tab`, `.tab.active`, `.tab-spacer`)
     - Review control styles (`.review-btn`, `.review-notes`, `.review-stat`)
     - OCR comparison layout (`.ocr-compare`, `.ocr-col`, `.ocr-col-header`, `.ocr-text`, `.ocr-time`)

### Technical Decisions
- **Qwen3-VL over Qwen2.5-VL:** The OCR quality improvement on dense text is decisive. The 2-7x speed penalty is acceptable for batch processing. The occasional empty response issue is mitigated by retry logic.
- **Keep both OCR versions:** Storing Qwen2.5 and Qwen3 files side-by-side enables comparative analysis and documents the model evaluation process
- **Review status persistence:** Simple JSON file (`review_status.json`) rather than a database — minimal overhead, human-readable, version-controllable
- **Tab-based viewer architecture:** Separates analytical review (Analysis tab) from OCR quality checking (OCR Compare tab) — different cognitive tasks with different UI needs

### Observations for Research
- **Model size vs. quality tradeoff:** Both Qwen models are 7-8B parameters. The generational improvement (2.5 → 3) produced dramatic OCR quality gains on the same hardware with the same prompts. This suggests prompt engineering was not the bottleneck — model capability was.
- **Empty response phenomenon:** Qwen3-VL occasionally returns empty strings for images that Qwen2.5 handles (though with errors). This may relate to the model's confidence threshold or image preprocessing. Requires investigation.
- **Human-in-the-loop design:** The review interface implements a lightweight quality assurance workflow. The approve/flag/pending states map to a simple triage: verified accurate, needs correction, not yet reviewed.

---

## Session 5 — 2026-03-02, ~17:00 (Static Site & Visual Analysis)

**Commit:** *(pending)*

### Objectives
- Convert Flask viewer to a static site deployable on GitHub Pages
- Replace OCR Compare tab with Visual Analysis tab (Qwen3-VL image descriptions + layout analysis)
- Add image zoom functionality
- Simplify review workflow (remove notes textarea, use localStorage)
- Generate compressed JPEG images for web delivery

### Work Completed

1. **Qwen3-VL visual analysis generation**
   - Created `source/generate_visual_analysis.py` — generates image descriptions and layout analysis for each spread using Qwen3-VL via Ollama
   - Reuses prompts from `compare_qwen_versions.py` (IMAGE_DESCRIBE_PROMPT, LAYOUT_PROMPT)
   - Generated 10 files: `output/vlm_extractions/spread_NNN_visual_qwen3.json`
   - Each file contains: `image_description`, `layout_analysis`, timing metadata, model name
   - Typical generation time: 10-20s per task per spread

2. **Static site build script**
   - Created `source/build_static_site.py` — generates `docs/` directory at repo root
   - Four build steps:
     1. Load analysis database, build `data/index.json` with navigation metadata
     2. Merge analysis + OCR + visual analysis into per-spread JSON files (`data/spread_NNN.json`)
     3. Compress rendered PNGs → JPEG quality 85 (`images/spread_NNN.jpg`)
     4. Copy static HTML and CSS from `viewer/`
   - Image compression results: 85 images, 77.6MB PNG → 19.1MB JPEG (25% of original)
   - Supports `--no-images` flag for faster rebuilds, `--clean` for fresh builds

3. **Static HTML viewer (pure client-side)**
   - Created `viewer/static_viewer.html` — complete rewrite removing all Jinja2 and Flask dependencies
   - Data loading via `fetch()` API: `data/index.json` on init, `data/spread_NNN.json` per spread
   - **Two tabs:**
     - **Analysis** — full structured analysis rendering (all 9 schema sections)
     - **Visual Analysis** — image description, layout analysis, collapsible OCR extraction (Qwen3 only)
   - **Image zoom:** scroll wheel (cursor-centered), click toggle (1x↔2x), drag-to-pan when zoomed, keyboard (+/-/0), zoom controls bar
   - **Review:** localStorage-based (key `mcluhan_review`), approve/flag/reset buttons, no notes textarea
   - **Keyboard shortcuts:** arrow keys (nav), 1/2 (tabs), y/f (review), +/-/0 (zoom)
   - Unanalyzed spreads show "Not yet analyzed" placeholder in both tabs

4. **Static CSS**
   - Created `viewer/static_style.css` — standalone dark theme CSS
   - Removed: `.review-notes`, `.ocr-compare`, `.ocr-col`, `.ocr-col-header` (Qwen2.5 comparison UI)
   - Added: `.image-wrapper`, `.zoom-controls`, `.visual-text`, `.vlm-meta`, `.collapsible-header`, `.ocr-subsection`
   - Image panel restructured with flex-direction: column for zoom controls bar

5. **Build output**
   - `docs/` directory: 98 files, 19.2MB total
     - `index.html` + `style.css` (viewer)
     - `data/`: 11 JSON files (1 index + 10 spread data)
     - `images/`: 85 JPEG images (all spreads, including unanalyzed)
   - Verified locally via `python -m http.server 8000 --directory docs`

6. **Bug fixes during testing**
   - Fixed `db.get("entries", [])` → `db.get("spreads", [])` in build script (database uses "spreads" key)
   - Fixed dropdown select not syncing when `loadSpread()` called directly
   - Fixed visual tab not clearing content when navigating to unanalyzed spreads

### Technical Decisions
- **Static over Flask:** GitHub Pages requires static files. All dynamic rendering moved to client-side JavaScript, all API endpoints replaced with static JSON file fetches.
- **JPEG quality 85:** Produces ~25% of PNG file size while maintaining readability for close review. All 85 images tracked in git (19.1MB total — acceptable for GitHub).
- **localStorage for review:** Simpler than a server-side JSON file for a static deployment. Review state is per-browser, which is acceptable for a single-reviewer workflow.
- **Visual Analysis tab replaces OCR Compare:** Qwen2.5-VL is no longer part of the pipeline. The new tab surfaces Qwen3-VL's image description and layout analysis — more useful for analytical review than side-by-side OCR comparison.
- **Collapsible OCR:** Raw and structured OCR hidden behind a collapsible header to keep the Visual Analysis tab focused on interpretive content.

### Architecture Change

**Before (Session 4):**
```
User → Flask (localhost:5001) → Jinja2 templates → reads JSON + PNG files from output/rendered/
```

**After (Session 5):**
```
User → GitHub Pages (static) → fetch() → docs/data/*.json + docs/images/*.jpg
Build: python source/build_static_site.py → generates docs/ from output/ + rendered/
```

---

## Cumulative Statistics (End of Session 5)

| Metric | Value |
|--------|-------|
| Total commits | 5 |
| Spreads analyzed | 10 of 85 (11.8%) |
| OCR extractions (Qwen2.5) | 10 (archived, no longer in pipeline) |
| OCR extractions (Qwen3) | 10 |
| Visual analysis (Qwen3) | 10 (image description + layout analysis) |
| VLM models evaluated | 3 (Qwen2.5-VL, Qwen3-VL, Molmo2-8B) |
| Active VLM pipeline | Qwen3-VL only |
| Schema version | 1.1 |
| Gold standard samples | 2 (spreads 008, 011) |
| Review status | 0 approved, 0 flagged, 10 pending |
| Code files | 9 Python scripts, 2 HTML files, 2 CSS files |
| Documentation files | 6 markdown documents + 1 PDF |
| Static site | 98 files, 19.2MB (docs/) |
| Deployment target | GitHub Pages (main branch, /docs folder) |

---

## Appendix: File Changelog

| File | Created | Last Modified | Description |
|------|---------|---------------|-------------|
| `source/analysis_schema_v1.1.json` | Session 1 | Session 1 | JSON Schema for analysis entries |
| `source/claude_code_analysis_instructions.md` | Session 1 | Session 1 | Analysis methodology instructions |
| `source/image_credits_lookup.json` | Session 1 | Session 1 | Image credits cross-reference |
| `source/sample_entry_spread_008.json` | Session 1 | Session 1 | Gold standard: typography spread |
| `source/sample_entry_spread_011.json` | Session 1 | Session 1 | Gold standard: surveillance spread |
| `source/build_batch_001_010.py` | Session 2 | Session 2 | Batch 1 analysis script |
| `source/vlm_tools.py` | Session 2 | Session 4 | VLM utilities (OCR, description, layout) |
| `source/test_molmo.py` | Session 2 | Session 2 | Molmo2-8B testing script |
| `source/run_molmo_conda.py` | Session 2 | Session 3 | Molmo execution wrapper for conda env |
| `source/phase_b_methodology.md` | Session 3 | Session 3 | Detailed analysis methodology |
| `source/compare_qwen_versions.py` | Session 4 | Session 4 | Qwen 2.5 vs 3 comparison script |
| `source/generate_visual_analysis.py` | Session 5 | Session 5 | Qwen3-VL visual analysis generation |
| `source/build_static_site.py` | Session 5 | Session 5 | Static site build script |
| `viewer/app.py` | Session 1 | Session 4 | Flask web viewer (retained for local dev) |
| `viewer/templates/viewer.html` | Session 1 | Session 4 | Flask viewer UI (retained for local dev) |
| `viewer/static/style.css` | Session 1 | Session 4 | Flask viewer CSS (retained for local dev) |
| `viewer/static_viewer.html` | Session 5 | Session 5 | Static HTML viewer (GitHub Pages) |
| `viewer/static_style.css` | Session 5 | Session 5 | Static CSS (GitHub Pages) |
| `output/analysis_database.json` | Session 1 | Session 3 | Main structured analysis (10 entries) |
| `output/review_status.json` | Session 4 | Session 4 | Review approve/flag/pending tracking |
| `output/vlm_extractions/*_ocr.json` | Session 2 | Session 2 | Qwen2.5-VL OCR (10 files, archived) |
| `output/vlm_extractions/*_ocr_qwen3.json` | Session 4 | Session 4 | Qwen3-VL OCR (10 files) |
| `output/vlm_extractions/*_visual_qwen3.json` | Session 5 | Session 5 | Qwen3-VL visual analysis (10 files) |
| `docs/` (generated) | Session 5 | Session 5 | Static site (98 files, 19.2MB) |

---

*This document is updated after each development session.*
