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

### Model Inventory
| Model | Size | Interface | Primary Use |
|-------|------|-----------|-------------|
| Qwen2.5-VL-7B | 6.0 GB | Ollama (`qwen2.5vl:7b`) | OCR (deprecated as primary) |
| Qwen3-VL | 6.1 GB | Ollama (`qwen3-vl`) | OCR + image description (current primary) |
| Molmo2-8B | ~16 GB | HuggingFace Transformers | Image description (secondary) |
| Claude Opus 4.6 | Cloud | Claude Code CLI | Interpretive analysis, orchestration |

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

## 7. Reproducibility Notes

### 7.1 Model Versioning
- Qwen2.5-VL-7B: Ollama tag `qwen2.5vl:7b` (pulled 2026-03-02)
- Qwen3-VL: Ollama tag `qwen3-vl` (pulled 2026-03-02, 6.1 GB)
- Molmo2-8B: HuggingFace `allenai/Molmo2-8B` (specific commit hash in cache: `e28fa28597e5ec5e0cca2201dd8ab33d48bc4a1b`)

### 7.2 Non-Determinism
- VLM outputs are non-deterministic even at `temperature=0.1`
- Qwen3-VL occasionally returns empty responses for the same image on different runs
- Retry logic mitigates but does not eliminate this issue
- All outputs are saved with timestamps for audit trail

### 7.3 Human-AI Interaction Model
The pipeline uses a layered human-AI collaboration:
1. **Automated:** PDF rendering, VLM inference, web serving
2. **AI-assisted:** OCR post-processing, text categorization, initial analysis drafting
3. **AI-primary:** Rhetoric analysis, theme mapping, progression analysis (Claude Opus 4.6)
4. **Human-primary:** Review, approval, error correction, quality assurance
5. **Human-only:** Theoretical framework development, project direction, publication decisions

This layering is documented in `source/phase_b_methodology.md` (field-by-field methodology table).

---

*This document is updated when significant technical decisions are made or new model evaluations are conducted.*
