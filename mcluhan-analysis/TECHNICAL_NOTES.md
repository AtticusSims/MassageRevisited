# Technical Notes: VLM Evaluation & Infrastructure

> Research-oriented technical documentation for the McLuhan Analysis Pipeline.
> Records model evaluations, architectural decisions, failure modes, and infrastructure details
> relevant to academic publication on human-AI collaborative analysis methods.

---

## 1. System Architecture

### Hardware
- **GPU:** NVIDIA RTX 5090 (32 GB VRAM)
- **RAM:** 64 GB system memory
- **OS:** Windows (development environment)
- **CUDA:** 12.8

### Software Stack
| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.12 (main), 3.11 (molmo conda env) | Runtime |
| PyMuPDF (fitz) | Latest | PDF rendering |
| Flask | Latest | Web viewer |
| Ollama | Latest | Local VLM inference server |
| Transformers | 4.57.1 | HuggingFace model inference |
| PyTorch | 2.10.0+cu128 (molmo) | Deep learning framework |
| Claude Code | Opus 4.6 | Orchestration + interpretive analysis |
| Pillow | Latest | Image compression for static site build (PNG→JPEG) |

### Model Inventory
| Model | Size | Interface | Primary Use |
|-------|------|-----------|-------------|
| Qwen2.5-VL-7B | 6.0 GB | Ollama (`qwen2.5vl:7b`) | OCR (archived — replaced by Qwen3-VL) |
| Qwen3-VL | 6.1 GB | Ollama (`qwen3-vl`) | OCR + image description + layout analysis (sole VLM) |
| Molmo2-8B | ~16 GB | HuggingFace Transformers | Image description (archived — inconsistent quality) |
| Gemini 2.5 Pro | Cloud | Google AI SDK (`google-generativeai`) | Visual descriptions (85 spreads) |
| Claude Opus 4.6 | Cloud | Claude Code CLI | Interpretive analysis, content planning, orchestration |

---

## 2. VLM Model Evaluation

### 2.1 Qwen2.5-VL-7B vs Qwen3-VL

**Evaluation date:** 2026-03-02
**Methodology:** Identical prompts run on both models across 5 representative spreads. Results saved to `output/vlm_extractions/qwen_version_comparison.json`.

#### Test Spreads Selected
| Spread | Selection Rationale | Characteristics |
|--------|-------------------|-----------------|
| spread_001 | Cover — text overlaid on photograph | Low-contrast text, warm tones, blurred background |
| spread_009 | Dense body text — the hardest OCR challenge | Small serif text, justified columns, gutter-spanning |
| spread_010 | Dense text + image combination | Mixed content, body text with adjacent photograph |
| spread_005 | Image-heavy — branded product | Egg photograph with stamped text, minimal body text |
| spread_007 | Full photograph — hand close-up | B&W photograph with minimal caption text |

#### OCR Quality Results

**Raw OCR (unstructured text extraction):**

| Spread | Qwen 2.5 | Qwen 3 | Assessment |
|--------|----------|--------|------------|
| 001 | 117 chars, partial | **0 chars (FAILURE)** | 2.5 wins — Qwen3 returned empty |
| 009 | 104 chars, garbled nonsense | **1,958 chars, clean** | Qwen3 dramatically better |
| 010 | ~200 chars, garbled final paragraph | **1,425 chars, perfect** | Qwen3 dramatically better |

**Structured OCR (categorized by function):**

| Spread | Qwen 2.5 | Qwen 3 | Assessment |
|--------|----------|--------|------------|
| 001 | Partial, misread "jeremy hoaglon" | Correct "jerome agel", complete categories | Qwen3 better |
| 009 | Garbled quotation fragments | **Clean quotation with correct attribution** | Qwen3 dramatically better |
| 010 | Garbled body text | **Clean, complete** | Qwen3 dramatically better |

**Image Description:**

| Spread | Qwen 2.5 | Qwen 3 | Assessment |
|--------|----------|--------|------------|
| 005 | Missed egg entirely | Missed egg entirely | Tie (both poor on this image) |
| 007 | Basic description | **More detailed, more observant** | Qwen3 better |

**Layout Analysis:**

| Spread | Qwen 2.5 | Qwen 3 | Assessment |
|--------|----------|--------|------------|
| 005 | Limited | More detailed | Qwen3 slightly better |
| 007 | Weak, misidentified elements | More accurate | Qwen3 better |

#### Timing Comparison
| Spread | Task | Qwen 2.5 (seconds) | Qwen 3 (seconds) | Ratio |
|--------|------|---------------------|-------------------|-------|
| 001 | Raw OCR | 7.0 | 49.3 | 7.0x |
| 009 | Raw OCR | 7.0 | 42.7 | 6.1x |
| 009 | Structured OCR | 7.0 | 28.7 | 4.1x |
| 010 | Raw OCR | ~7 | 29.6 | ~4.2x |
| 005 | Image describe | ~15 | ~45 | ~3x |
| 007 | Layout | ~12 | ~35 | ~2.9x |

**Speed summary:** Qwen3-VL is consistently 2-7x slower than Qwen2.5-VL. The slowdown is more pronounced on simpler images (cover) and less pronounced on complex content (layout analysis).

#### Decision
**Switched to Qwen3-VL as primary.** The OCR quality improvement on dense text (the critical use case) is decisive. Every OCR error that Qwen2.5 produced on spreads 009-010 was resolved by Qwen3. The speed penalty (2-7x) is acceptable for batch processing where accuracy matters more than throughput.

**Mitigation for empty responses:** Implemented retry logic — if raw OCR returns empty, retry once before saving.

### 2.2 Molmo2-8B Evaluation

**Evaluation date:** 2026-03-02
**Model:** `allenai/Molmo2-8B` via HuggingFace Transformers 4.57.1
**Environment:** Conda env `molmo` (Python 3.11, PyTorch 2.10.0+cu128)

#### Setup Challenges
- Required separate conda environment due to dependency conflicts
- Cached model files had incompatible `rope_type` parameter ("default" vs "linear") — required manual patching of `modeling_molmo2.py` (lines 543, 964)
- `torch_dtype` parameter renamed to `dtype` in newer transformers — required code update
- Model loads in ~20 seconds, inference takes ~2-3 minutes per prompt

#### Image Description Quality
| Spread | Result | Assessment |
|--------|--------|------------|
| 007 (hand photo) | Coherent description of woman's hand, jewelry, advertising style | Good — captures subject and mood |
| 005 (branded egg) | **Missed the egg entirely** — only described typography | Poor — failed on primary visual element |

#### Layout Analysis Quality
| Spread | Result | Assessment |
|--------|--------|------------|
| 007 | Misidentified several elements, weak spatial analysis | Poor — not reliable for layout |

#### Decision
**Molmo2-8B downgraded to secondary correlation role.** Image description is sometimes useful but inconsistent. Layout analysis is unreliable. The model is retained for cases where cross-validation between two independent VLMs adds confidence, but it cannot serve as a primary descriptor.

### 2.3 Qwen3-VL Image Description Limitations

**Evaluation date:** 2026-03-03
**Context:** While Qwen3-VL dramatically outperforms Qwen2.5-VL for OCR, its image description capabilities have significant accuracy issues.

#### Observed Failures

| Spread | Error | Severity |
|--------|-------|----------|
| spread_050 | Misidentified a **foot** as a **hand** | High — fundamentally wrong object identification |
| spread_050 | Misidentified a **big toe** as a **nose ring** | High — implausible identification |
| General | Tendency toward generic descriptions lacking visual specificity | Medium |
| General | Poor identification of human body parts in non-standard compositions | Medium |

#### Assessment
Qwen3-VL (7B parameters, local inference) is adequate for OCR but **unreliable for detailed image identification**. The foot/hand misidentification on spread_050 is not a marginal error — it represents a fundamental failure in visual understanding. This motivated the evaluation of Gemini 2.5 Pro for visual descriptions.

### 2.4 Gemini 2.5 Pro Evaluation (Visual Descriptions)

**Evaluation date:** 2026-03-03
**Model:** `gemini-2.5-pro` via Google AI SDK
**API tier:** Paid (no rate limiting required)
**Context window:** 1M tokens (system instruction used ~51K tokens, ~5% of capacity)

#### Setup
- Client module: `source/gemini_tools.py`
- API key: `GEMINI_API_KEY` in `source/.env` (gitignored)
- Temperature: 0.2, max output: 16384 tokens
- System instruction includes: `phase_b_methodology_v2.md`, `analysis_schema_v1.2.json`, 2 gold standard samples

#### Visual Description Quality

Gemini 2.5 Pro was evaluated against the existing Qwen3-VL descriptions. A full comparison across all 85 spreads was generated (`output/gemini_comparison_report.md`).

| Metric | Result |
|--------|--------|
| Spreads with visual descriptions | 85/85 (100%) |
| Image identification accuracy | Significantly better than Qwen3-VL |
| Object/body part identification | Correct (foot identified as foot, not hand) |
| Design field differences | 290 field-level differences from existing analysis |
| Conciseness | More focused than Qwen3-VL's verbose descriptions |

#### Key Differences from Existing Analysis

| Field | Gemini Tendency | Existing (Qwen3-VL + Claude) |
|-------|----------------|-------------------------------|
| `visual_density` | More conservative ("moderate") | More dramatic ("overwhelming") |
| `left_right_relationship` | Correctly identifies single pages | Sometimes assigns two-page relationships to single pages |
| `layout_description` | Concise, spatially precise | Verbose, interpretive |
| Image subjects | Accurate identification | Occasional misidentification (spread_050) |

#### Decision
**Gemini 2.5 Pro adopted for visual descriptions.** The model's 1M context window allowed including full methodology + schema + samples in every request, ensuring consistent quality. Image identification is materially better than the local 7B model.

**Gemini independent analysis was NOT executed.** Only Phase 2 (visual descriptions) of the planned 4-phase Gemini integration was completed. The user directed that content planning use Claude Opus exclusively.

#### Deviation from Plan
The original plan specified `gemini-3.1-pro-preview` but `gemini-2.5-pro` was used — the 3.1 model was not yet available at time of execution.

---

## 3. OCR Error Taxonomy

Errors observed across the VLM OCR pipeline, categorized by type. This taxonomy is useful for understanding the failure modes of vision-language models on historical print material.

### 3.1 Error Types (Qwen2.5-VL)

| Error Type | Example | Spread | Likely Cause |
|------------|---------|--------|-------------|
| **Character substitution** | "quantin fin" for "quentin fiore" | 001 | Low contrast text on photograph |
| **Garbled reconstruction** | "that puck e:IVII" for actual body text | 009 | Dense serif text near gutter |
| **Semantic hallucination** | "jeremy hoaglon" for "jerome agel" | 001 | Model confabulating plausible name |
| **Truncation** | Missing final paragraphs | 009, 010 | Long text exceeds model attention |
| **Complete failure** | Empty or near-empty output | Various | Image preprocessing issues |
| **Gutter interference** | Words split across spine misread | 009 | Physical book artifact |

### 3.2 Error Types (Qwen3-VL)

| Error Type | Example | Spread | Likely Cause |
|------------|---------|--------|-------------|
| **Empty response** | 0 characters returned | 001 (raw) | Possible confidence threshold issue |
| **Retry success** | Empty on first attempt, content on retry | 008 | Non-deterministic model behavior |

### 3.3 Factors Affecting OCR Quality

**Text characteristics that increase error rate:**
- Dense serif body text (vs. sans-serif display text)
- Small font size
- Justified text with hyphenation
- Text spanning the gutter/spine
- Low contrast (dark text on dark background)
- Text overlaid on photographic images

**Text characteristics that produce reliable OCR:**
- Large display text (>24pt equivalent)
- High contrast (white text on black, or black text on white)
- Sans-serif typefaces
- Isolated text elements (captions, page numbers)

---

## 4. Prompt Engineering

### 4.1 OCR Prompts

Two complementary prompts are used for each spread:

**Raw OCR prompt** — Optimized for completeness:
```
You are an expert OCR system. Extract ALL text visible in this image,
preserving the exact wording, spelling, punctuation, and capitalization.
Include all text: titles, body text, captions, page numbers, credits,
quotation marks, attribution lines, and any text used as design elements
(e.g., large display words). Organize the extracted text by its position
on the page (top to bottom, left to right). For text that spans across
a gutter/spine, reconstruct the complete words. Mark any text you're
uncertain about with [?]. Do NOT describe the images or layout — only
extract text.
```

**Structured OCR prompt** — Optimized for categorization:
```
You are an expert OCR and document analysis system. Extract ALL text
from this image and categorize it into these sections:

DISPLAY_TEXT: Any text used as a large typographic design element
BODY_TEXT: Main prose/paragraph text by the authors
QUOTATIONS: Any quoted text with attribution
CAPTIONS: Image captions, photo credits, small contextual text
PAGE_NUMBERS: Any visible page numbers

For each section, transcribe the text EXACTLY as it appears...
```

**Design rationale:** The raw prompt catches text the structured prompt might miscategorize. The structured prompt provides functional metadata that maps directly to schema fields. Using both provides redundancy.

### 4.2 Inference Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `temperature` | 0.1 | Low temperature for OCR accuracy — want deterministic, faithful transcription |
| `num_predict` | 4096 | High token limit to accommodate dense text spreads |
| `timeout` | 300s | Generous timeout for Qwen3-VL's slower inference |

---

## 5. Data Architecture

### 5.1 File Naming Conventions

| Pattern | Example | Description |
|---------|---------|-------------|
| `spread_NNN.png` | `spread_001.png` | Rendered PDF page (NNN = zero-padded page number) |
| `spread_NNN_ocr.json` | `spread_001_ocr.json` | Qwen2.5-VL OCR extraction |
| `spread_NNN_ocr_qwen3.json` | `spread_001_ocr_qwen3.json` | Qwen3-VL OCR extraction |
| `spread_NNN_vlm.json` | (future) | Combined VLM analysis (OCR + description + layout) |

### 5.2 OCR JSON Structure (Qwen3)
```json
{
  "spread_id": "spread_009",
  "model": "qwen3-vl",
  "ocr_raw": "...",
  "ocr_raw_time": 42.7,
  "ocr_structured": "...",
  "ocr_structured_time": 28.7,
  "timestamp": "2026-03-02T16:15:00"
}
```

### 5.3 Review Status Structure
```json
{
  "spread_009": {
    "status": "approved|flagged|pending",
    "notes": "Free-text review notes"
  }
}
```

### 5.4 Analysis Database Structure (v1.2)

```json
{
  "metadata": {
    "schema_version": "1.2",
    "schema_theoretical_basis": [
      "Kress & van Leeuwen 2006 (visual grammar)",
      "Barthes 1977; Martinec & Salway 2005 (image-text relations)",
      "Drucker 2014 (performative design)",
      "Bateman 2008; Hiippala 2015 (GeM framework)"
    ],
    "analysis_model": "claude-opus-4-6+qwen3-vl"
  },
  "spreads": [
    {
      "id": "spread_NNN",
      "analyst": "claude-opus-4-6+qwen3-vl",
      "analysis_method": "llm_primary_human_reviewed",
      "images": [{
        "relationship_to_text": {
          "primary_relation": "enum (illustrates|amplifies|literalizes|...)",
          "barthes_mode": "anchorage|relay",
          "description": "..."
        },
        "interactive_meaning": {
          "contact": "demand|offer|not_applicable",
          "social_distance": "intimate|social|public|not_applicable",
          "attitude_angle": "frontal|oblique|vertical_power|not_applicable"
        }
      }],
      "design": {
        "color_and_tone": {
          "contrast": "high|low|mixed",
          "dominant_tone": "dark|light|mixed",
          "description": "..."
        },
        "information_value": {
          "left_right": "given_new|balanced|reversed|not_applicable",
          "top_bottom": "ideal_real|balanced|not_applicable",
          "center_margin": "centered|distributed|not_applicable"
        },
        "compositional_framing": "strongly_framed|weakly_framed|mixed|not_applicable"
      },
      "rhetoric": {
        "rhetorical_strategy": {
          "primary": "one of 15-term controlled vocabulary",
          "secondary": "nullable, from same vocabulary"
        },
        "strategy_description": "...",
        "multi_spread_patterns": "...",
        "confidence": "high|medium|low"
      },
      "themes": { "confidence": "high|medium|low" },
      "progression": { "confidence": "high|medium|low" }
    }
  ]
}
```

**v1.1 → v1.2 Changes:** 12 revisions (A1-A12) adding controlled vocabularies, Barthes image-text taxonomy, Kress & van Leeuwen visual grammar fields, confidence indicators, and per-entry analyst metadata. Full revision details in `ContextDocs/schema_methodology_revisions.md`.

### 5.5 Controlled Vocabularies (v1.2)

The v1.2 schema introduces controlled vocabularies grounded in multimodal discourse analysis literature:

**Rhetorical Strategies (15 terms):**
assertion, confrontation, juxtaposition, accumulation, disruption, provocation, invocation, dramatization, quieting, sensory_overload, humor, demonstration, interpellation, defamiliarization, call_and_response

**McLuhan Concepts (19 terms):**
medium_is_the_message, extensions_of_man, global_village, hot_and_cool, rear_view_mirror, figure_ground, acoustic_space, visual_space, electric_age, print_culture, tribal, pattern_recognition, sense_ratios, environment_as_invisible, obsolescence_and_retrieval, participation, implosion, anti_environment, allatonceness

**Image-Text Relationship (primary_relation):**
illustrates, amplifies, literalizes, contradicts, ironizes, provides_atmosphere, serves_as_metaphor, extends, independent, anchorage, relay

**Barthes Mode:** anchorage, relay (from Barthes 1977; Martinec & Salway 2005)

**Interactive Meaning (Kress & van Leeuwen 2006):**
- Contact: demand, offer, not_applicable
- Social distance: intimate, social, public, not_applicable
- Attitude angle: frontal, oblique, vertical_power, not_applicable

The vocabulary registry is maintained in `source/theme_vocabulary.json` (59 terms with definitions and related_terms).

---

## 6. Infrastructure Notes

### 6.1 Ollama Configuration
- Server: `http://localhost:11434`
- API endpoint: `/api/chat` (not `/api/generate` — critical for vision models)
- Models stored locally (standard Ollama model directory)
- No GPU memory management needed — Ollama handles VRAM allocation

### 6.2 Conda Environment (Molmo)
```
Name: molmo
Python: 3.11
Key packages:
  - transformers==4.57.1
  - torch==2.10.0+cu128
  - accelerate
  - einops
  - Pillow
```
**Usage:** `conda run -n molmo python source/run_molmo_conda.py describe rendered/spread_007.png`

### 6.3 Flask Viewer
- Port: 5001
- Reads directly from `output/analysis_database.json`, `output/vlm_extractions/`, and `rendered/`
- No database — all state in JSON files
- Review status in `output/review_status.json`

---

## 7. Static Site Architecture (GitHub Pages)

### 7.1 Overview

The review viewer was converted from a Flask server-rendered application to a pure static site deployable on GitHub Pages. All dynamic rendering was moved to client-side JavaScript.

**Build pipeline:**
```
source data (output/, rendered/)
  → python source/build_static_site.py
  → docs/ (static site root)
    ├── index.html          # Single-page viewer (client-side JS)
    ├── style.css           # Dark theme CSS
    ├── data/
    │   ├── index.json      # Navigation metadata (85 spreads)
    │   └── spread_NNN.json # Merged analysis + OCR + visual per spread
    └── images/
        └── spread_NNN.jpg  # Compressed JPEGs (quality 85)
```

### 7.2 Data Merging Strategy

Each `spread_NNN.json` file merges three data sources:
- **Analysis**: from `output/analysis_database.json` (the `spreads` array)
- **OCR**: from `output/vlm_extractions/spread_NNN_ocr_qwen3.json` (raw + structured)
- **Visual**: from `output/vlm_extractions/spread_NNN_visual_qwen3.json` (image description + layout analysis)

Only spreads with at least one data source present get a data file generated.

### 7.3 Image Compression

| Metric | Value |
|--------|-------|
| Source format | PNG (200 DPI renders) |
| Output format | JPEG (quality 85, optimized) |
| Total images | 85 |
| Source size | 77.6 MB |
| Compressed size | 19.1 MB |
| Compression ratio | 25% of original |
| Average per image | 225 KB |

Pillow handles RGBA → RGB conversion (JPEG doesn't support alpha channel).
Build script skips re-compression if JPEG is newer than PNG source.

### 7.4 Client-Side Review

Review state is stored in `localStorage` under key `mcluhan_review`:
```json
{
  "spread_001": {"status": "approved"},
  "spread_005": {"status": "flagged"}
}
```

Review counts (approved/flagged/pending) are computed on page load from localStorage. This replaces the server-side `review_status.json` approach used in the Flask viewer.

### 7.5 Deployment

- **Platform:** GitHub Pages
- **Source:** `main` branch, `/docs` folder
- **Paths:** All asset references are relative (no leading `/`)
- **Configuration:** GitHub repo Settings → Pages → Source: main, /docs

---

## 8. Reproducibility Notes

### 8.1 Model Versioning
- Qwen2.5-VL-7B: Ollama tag `qwen2.5vl:7b` (pulled 2026-03-02)
- Qwen3-VL: Ollama tag `qwen3-vl` (pulled 2026-03-02, 6.1 GB)
- Molmo2-8B: HuggingFace `allenai/Molmo2-8B` (specific commit hash in cache: `e28fa28597e5ec5e0cca2201dd8ab33d48bc4a1b`)

### 8.2 Non-Determinism
- VLM outputs are non-deterministic even at `temperature=0.1`
- Qwen3-VL occasionally returns empty responses for the same image on different runs
- Retry logic mitigates but does not eliminate this issue
- All outputs are saved with timestamps for audit trail

### 8.3 Human-AI Interaction Model
The pipeline uses a layered human-AI collaboration:
1. **Automated:** PDF rendering, VLM inference, web serving
2. **AI-assisted:** OCR post-processing, text categorization, initial analysis drafting
3. **AI-primary:** Rhetoric analysis, theme mapping, progression analysis (Claude Opus 4.6)
4. **Human-primary:** Review, approval, error correction, quality assurance
5. **Human-only:** Theoretical framework development, project direction, publication decisions

This layering is documented in `source/phase_b_methodology.md` (field-by-field methodology table).

---

## 9. Schema Version History

| Version | Date | Changes | Key Files |
|---------|------|---------|-----------|
| 1.0 | 2026-03-02 | Initial schema design (8 sections per spread) | `analysis_schema_v1.0.json` (superseded) |
| 1.1 | 2026-03-02 | Added `movement_mapping` field, 9 sections per spread | `analysis_schema_v1.1.json` |
| 1.2 | 2026-03-02 | Theoretical grounding: 12 revisions (A1-A12), controlled vocabularies, structured objects, confidence indicators | `analysis_schema_v1.2.json` |

### v1.2 Theoretical Framework

The v1.2 schema maps to four established theoretical frameworks in multimodal discourse analysis:

| Framework | Fields Added/Modified | Purpose |
|-----------|----------------------|---------|
| Kress & van Leeuwen (2006) | `interactive_meaning`, `information_value`, `compositional_framing` | Visual grammar — systematic analysis of visual composition |
| Barthes (1977) / Martinec & Salway (2005) | `relationship_to_text.barthes_mode` | Image-text relations — anchorage vs relay taxonomy |
| Drucker (2014) | `design_enacts_argument`, `design_argument_description` (retained from v1.1) | Performative design — design as meaning-making |
| Bateman (2008) / Hiippala (2015) | Schema architecture (multi-layered annotation) | GeM framework — computational multimodal annotation |

The theoretical grounding enables potential academic publication. See `ContextDocs/visual_rhetoric_and_reliability.md` for the full mapping and `ContextDocs/schema_methodology_revisions.md` for the revision rationale.

---

## 10. Content Plan Architecture (Phase C)

### 10.1 Overview

The content plan maps each of the 85 original spreads to a contemporary AI-era equivalent. The plan is the primary input for downstream authoring and design phases.

**Generator script:** `source/generate_content_plan.py`
**Output:** `output/content_plan.json` (402KB, 85 entries + meta section)

### 10.2 Content Plan Schema

```json
{
  "version": "1.0",
  "generated": "2026-03-03T...",
  "generator": "merge_sections.py (improved plans)",
  "schema_version": "planning_v1",
  "meta": {
    "movement_plan": { /* 5 movements with arc descriptions, themes, thinkers */ },
    "convergence_map": { /* 6 convergences with appearances across spreads */ },
    "rhythm_plan": { /* Segments defining pace and energy by movement */ },
    "quotation_distribution": { /* By thinker (20) and by movement (5) */ },
    "image_strategy": { /* Image approach per movement */ },
    "structural_decisions": { /* Boundary decisions, open questions */ }
  },
  "pages": [
    {
      "spread_id": "spread_NNN",
      "movement": "prologue|movement_1_environment|movement_2_acceleration|hinge|movement_3_dreamscape",
      "original_summary": "Brief summary of the original spread's content and argument",
      "contemporary_plan": {
        "theme": "AI-era theme title",
        "argument": "100-150 word argument (the 'why' of this spread)",
        "text": { "display_text": "...", "body_text_direction": "...", "quotation": {...} },
        "image": { "concept": "...", "visual_style": "...", "relationship_to_text": "..." },
        "rhetoric": { "strategy": "one of 15 terms", "design_enacts": "mechanism description" },
        "mapping": {
          "relationship_to_original": "echo|inversion|transformation|departure",
          "convergences": ["convergence_id", ...],
          "thinkers": ["Thinker Name", ...]
        }
      },
      "paper_trace": { "citation": "...", "convergence_tag": "..." },
      "reviewer_feedback": null
    }
  ]
}
```

### 10.3 Movement Assignments

| Movement | Spreads | Count | Arc |
|----------|---------|-------|-----|
| Prologue | 001-010 | 10 | Individual → data shadow → planetary infrastructure |
| M1: Environment | 011-035 | 25 | Bratton's Stack: Earth → Cloud → City → Address → Interface → User |
| M2: Acceleration | 036-060 | 25 | Generated reality, synthetic media, recursive acceleration |
| Hinge | 061-065 | 5 | Copernican trauma, meaning crisis, threshold crossing |
| M3: Dreamscape | 066-085 | 20 | Consciousness, numinous return, maelstrom, coda |

### 10.4 Controlled Vocabularies (Content Plan)

**Rhetorical Strategies (15 terms, same as analysis schema):**
assertion, confrontation, juxtaposition, accumulation, disruption, provocation, invocation, dramatization, quieting, sensory_overload, humor, demonstration, interpellation, defamiliarization, call_and_response

**Relationship to Original (4 terms):**
- `echo` — contemporary content that parallels the original's structure and argument
- `inversion` — the original's logic reversed or contradicted by AI-era developments
- `transformation` — the original's concern fundamentally altered by AI context
- `departure` — new territory with no direct parallel in the original

**Convergences (6):**
reality_as_interface, intelligence_substrate_independent, failure_of_propositions, recursive_acceleration, return_of_the_numinous, accidental_megastructure

### 10.5 Distribution Targets and Actuals

| Metric | Target | Actual |
|--------|--------|--------|
| Strategies | All 15 used, no adjacent duplicates | 15/15 used, 0 adjacent duplicates |
| Relationships | Balanced across 4 types | echo=33, transformation=29, inversion=15, departure=8 |
| Convergences | All 6 present in every movement | All 6 present across all movements |
| Thinkers | 20+ with framework-sourced quotations | 20 thinkers with named works and quotations |
| Argument length | 100-150 words | min=76, max=166, avg=115 words |
| Paper traces | Present for every entry | 85/85 entries have citations |

### 10.6 Parallel Subagent Architecture

The content plan was generated using a parallel subagent architecture — a significant deviation from the sequential approach originally envisioned.

**Architecture:**
```
generate_content_plan.py → baseline content_plan.json
                         ↓
     ┌──────────────────────────────────────────┐
     │  4 parallel Claude Code subagents        │
     │  ┌──────────┐ ┌───────┐ ┌───────┐ ┌───┐ │
     │  │ Prologue │ │  M1   │ │  M2   │ │H+3│ │
     │  │  10 pgs  │ │ 25 pg │ │ 25 pg │ │25p│ │
     │  └────┬─────┘ └───┬───┘ └───┬───┘ └─┬─┘ │
     └───────┼────────────┼────────┼────────┼───┘
             ↓            ↓        ↓        ↓
     prologue_plans  m1_plans  m2_plans  hinge_m3_plans
                         ↓
     merge_sections.py → merged content_plan.json
                         ↓
     update_meta.py → final content_plan.json (meta section updated)
```

**Why parallel:** Each section + framework docs (~200KB context documents) consumes significant context. Running all 85 spreads sequentially in a single context would exceed practical limits. The parallel approach also enables independent quality review per section.

**Each subagent receives:**
- Framework documents: `framework_v3.md` (65KB), `theorist_reference.md` (46KB)
- Per-spread analysis data extracted from the analysis database
- Quality requirements: named thinkers with exact quotations, varied strategies, concrete image/design directions
- Reference entry from a completed section (for quality calibration)

**Resilience challenge:** One subagent's output was lost during context compaction (Hinge+M3 in Session 8). The recovery strategy was to launch a dedicated rewrite subagent in Session 9 with explicit output file targeting. This produced the highest-quality section (110KB, all 15 strategies used).

---

## 11. Deviations from Original Plans

This section documents significant deviations from the original project plans and planning engine instructions.

### 11.1 Gemini Integration

**Original plan:** Full 4-phase Gemini integration (visual descriptions → independent analysis → comparison → merge) using `gemini-3.1-pro-preview`.

**Actual:** Only Phase 2 (visual descriptions) was executed, using `gemini-2.5-pro`. User directed that content planning use Claude Opus exclusively: "I want your expertise, as you are the best, not another model's."

**Impact:** Gemini visual descriptions (85 files) are available for downstream use, but the independent analysis and automated merge were not performed. The content plan reflects Claude's interpretation, not a consensus of multiple models.

### 11.2 Content Plan Schema

**Original (planning engine instructions):** Field names `text_direction`, `image_direction`, `design_direction` with specific subfield structures.

**Actual:** Uses `text`, `image`, `rhetoric` to maintain compatibility with `build_static_site.py` and the existing viewer infrastructure. The semantic content is equivalent but the field names differ.

### 11.3 Subagent Architecture

**Original:** Sequential, single-agent process working through spreads in order.

**Actual:** 4 parallel subagents (one per movement section), with a merge-and-validate step. This was necessary for context management and also produced better results since each agent could maintain full framework context for its section.

### 11.4 Qwen3-VL Role

**Original plan:** Qwen3-VL handles all VLM tasks (OCR, image description, layout analysis).

**Actual:** Qwen3-VL retained for OCR only. Image descriptions supplemented by Gemini 2.5 Pro due to accuracy issues (spread_050 foot/hand misidentification).

---

## 12. Authoring Notes

### 12.1 Easter Eggs & Embedded Details

| Spread | Element | Note |
|--------|---------|------|
| spread_011 | Hash string `2d:61:70:3e:43:d1:4a:e9:2d:b0:d1:ca:4f:4a:06:b4:c7:79:51:e5` | Preimage: "You are the fingerprint". The hash appears as the closing element of the revised body text, visually echoing the original spread's fingerprint/bullseye imagery. It represents the reader's identity reduced to a data signature — the "you" of the title rendered as machine-readable output. |

---

*Last updated: Phase 3 authoring (spread revisions in progress).*
