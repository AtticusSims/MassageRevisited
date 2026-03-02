# Claude Code Instructions: Phase 1 Analysis Pipeline

## What This Document Is

You are analyzing a scanned PDF of Marshall McLuhan and Quentin Fiore's *The Medium is the Massage* (1967) and producing a structured JSON database. You will also build a localhost web viewer so the human can review your work.

You will do the analysis yourself — view each page image directly and write the structured JSON. No API calls to external models. You are the analysis engine.

Read this entire document before doing anything.

---

## 1. Project Context

This analysis is Step 3 of a larger project to create a contemporary companion to McLuhan's book, mirroring its page-by-page structure with new content about artificial intelligence. The analysis database you produce will be used downstream to plan, write, and design every page of the new book. The quality of your analysis determines the quality of the entire project.

The book you're analyzing is not a conventional text. It is a designed object where visual layout, typography, and image placement ARE the argument. A spread about speed feels fast. A spread about fragmentation is fragmented. The most important thing you can capture is HOW THE DESIGN ENACTS THE ARGUMENT — not just what the text says, but what the spread DOES to the reader.

---

## 2. File Inventory

You need these files in your working directory. If any are missing, ask the human.

| File | Description |
|---|---|
| `themediumisthemassage_marshallmcluhan_quentinfiorecompressed.pdf` | The source PDF. 85 pages. Scanned images, no embedded text. |
| `analysis_schema_v1.1.json` | The JSON schema defining the structure of every analysis entry. |
| `image_credits_lookup.json` | Lookup table mapping book page numbers to image credits. |
| `sample_entry_spread_011.json` | Gold-standard sample: "you" surveillance spread. |
| `sample_entry_spread_008.json` | Gold-standard sample: "and how!" typography spread. |

---

## 3. PDF Structure

The PDF has 85 pages:

| PDF Pages | Type | Dimensions | Content |
|---|---|---|---|
| 1 | Cover | Portrait (441×777 pts) | Front cover: title/authors over blurred face |
| 2 | Dust jacket text | Portrait (504×777 pts) | Descriptive blurb |
| 3 | Title page | Portrait (441×777 pts) | Title, authors, publisher |
| 4–5 | Front matter | Various | Copyright, epigraph |
| 6–84 | Body | Landscape (882×777 pts) | 79 spreads = ~158 book pages |
| 14 | Exception | Portrait (777×882 pts) | Rotated spread — reader turns book sideways |
| 84 | Credits | Landscape | Image credits (book pages 158–159). Analyze briefly. |
| 85 | Final page | Portrait (630×1092 pts) | A. N. Whitehead closing quote over satellite imagery |

**Page numbering:** The book's own page numbers start at the first body spread. PDF page 6 corresponds approximately to book pages 1–2. Not every spread has visible page numbers. When a page number IS visible on the spread, record it in `page_numbers_visible`. Use visible page numbers and the credits lookup to triangulate the book page mapping. For spreads without visible numbers, interpolate from surrounding spreads (each landscape spread = 2 book pages).

---

## 4. Image Credits Lookup

Transcribed from PDF page 84 (book pages 158–159). Use this to populate the `source_credit` field for every image. The lookup is in `image_credits_lookup.json`, keyed by book page number(s).

**How to use:** Once you determine which book pages a spread covers, check whether any of those page numbers appear as keys in the lookup (including range keys like "27-31"). If a match exists, use that credit string. If no match, set `source_credit` to `null`.

---

## 5. The Analysis Schema

The full schema is in `analysis_schema_v1.1.json`. Here is what you must produce for each spread:

### Identification
- `id`: Format `spread_NNN` (zero-padded PDF page number)
- `pdf_page`: 1-indexed PDF page number
- `book_pages`: Array of book page numbers. `[]` if unnumbered front/back matter.
- `section`: `front_matter`, `body`, or `back_matter`
- `spread_type`: One of: `typography_as_design`, `image_dominant`, `text_with_mood_image`, `text_with_specific_image`, `collage`, `press_photo_with_title`, `symbol_or_graphic`, `quote_only`, `text_only`, `rotated_page`, `credits_or_colophon`, `title_page`, `other`
- `orientation`: `landscape_spread`, `portrait_single`, or `rotated`

### Text
- `body_text`: McLuhan/Fiore's prose, transcribed verbatim. Include unusual spellings and typographic effects (like "buzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzing"). Empty string if none.
- `display_text`: Text used as typographic design element (giant words, section titles). Empty string if none.
- `captions`: Array of captions, visible photo credits, small contextual text.
- `page_numbers_visible`: Array of page numbers actually printed on the spread.

### Quotations (array)
For each quotation from a named author:
- `text`: Verbatim
- `author`: As attributed on the page
- `author_context`: Brief identification
- `source_work`: The work it's from, if identifiable. Null if unknown.
- `relationship_to_argument`: How the quote functions on this spread
- `visual_treatment`: How it's typographically presented

### Images (array)
For each distinct image (photographs, illustrations, symbols — NOT typography-as-design):
- `position`: `left_page`, `right_page`, `full_bleed`, `spanning_gutter`, `inset_left`, `inset_right`, etc.
- `subject`: What the image depicts. Be specific.
- `source_type`: `press_photo`, `art_photograph`, `fine_art_reproduction`, `editorial_cartoon`, `illustration`, `advertisement`, `technical_diagram`, `graphic_symbol`, `historical_document`, `film_still`, `unknown`
- `source_credit`: From the credits lookup. Null if not listed.
- `estimated_date`: Approximate date/era if determinable. Null otherwise.
- `composition`: Framing, angle, contrast, key visual qualities.
- `scale`: `full_bleed`, `dominant`, `half_page`, `quarter_page`, `small_inset`, `icon`
- `relationship_to_text`: How this image relates to the text — analytical, not just descriptive.

### Design
- `layout_description`: Prose description of spatial arrangement.
- `typography.body_font_style`: Body text typography description.
- `typography.display_font_style`: Display/headline typography. Null if none.
- `typography.special_treatments`: Array of unusual typographic choices.
- `color_and_tone`: Tonal quality.
- `white_space`: `abundant`, `moderate`, `minimal`, `none`
- `visual_density`: `sparse`, `moderate`, `dense`, `overwhelming`
- `left_right_relationship`: How the two pages relate.

### Rhetoric — THE MOST IMPORTANT SECTION
- `argument`: The core claim, stated plainly. What is McLuhan saying?
- `rhetorical_strategy`: HOW the argument is made (assertion, provocation, juxtaposition, accumulation, disruption, humor, sensory overload, quieting, etc.)
- `design_enacts_argument`: Boolean. Does the visual design PERFORM the argument?
- `design_argument_description`: If true, explain HOW. **This is the single most valuable field in the entire schema.** Explain the specific mechanism by which the layout, typography, image placement, or spatial arrangement embodies the intellectual content. Not a generic sentence — a precise explanation of the design-as-argument mechanism.
- `reader_experience`: What the spread does to the reader emotionally/cognitively.
- `mcluhan_concepts`: Array. Use consistent tags: `extensions_of_man`, `global_village`, `medium_is_the_message`, `hot_and_cool`, `rear_view_mirror`, `figure_ground`, `acoustic_space`, `electric_age`, `tribal`, `pattern_recognition`, `obsolescence`, `tetrad`

### Themes
- `original_themes`: Free-text tags. Use consistent vocabulary across spreads.
- `contemporary_domain_candidates`: From closed enum: `algorithmic_identity`, `attention_and_cognition`, `synthetic_media_and_post_truth`, `ambient_intelligence`, `post_literacy_and_language`, `authorship_and_creativity`, `surveillance_and_control`, `public_private_collapse`, `embodiment_and_disembodiment`, `labor_and_value`, `global_village_revisited`, `agency_and_autonomy`. Can be empty for structural/transitional spreads.
- `movement_mapping`: From closed enum: `prologue`, `movement_1_environment`, `movement_2_acceleration`, `hinge_m2_m3`, `movement_3_dreamscape`. Which movement in the contemporary book this spread most naturally maps to. Guidelines:
  - `prologue` — establishing the reader's personal relationship to technology, making the invisible visible
  - `movement_1_environment` — the computational infrastructure as invisible environment
  - `movement_2_acceleration` — recursive acceleration, meaning crisis, the system outpacing comprehension
  - `hinge_m2_m3` — the Copernican trauma: we are not the point of this story
  - `movement_3_dreamscape` — consciousness, AI as numinous presence, boundaries dissolving
- `mapping_rationale`: Brief explanation of the conceptual bridge.

### Progression
- `pace_shift`: `accelerating`, `decelerating`, `steady`, `rupture`
- `thematic_function`: `introduces_theme`, `develops_theme`, `layers_themes`, `climax`, `resolution`, `transition`, `coda`, `interruption`
- `relationship_to_previous`: How this connects to the preceding spread.
- `relationship_to_next`: How this sets up what follows. On Pass 1, give your best inference. You'll refine this in Pass 2.

### Notes (optional)
Any additional observations: OCR uncertainties, cross-references, interesting details.

---

## 6. Quality Bar: The Gold-Standard Samples

Read `sample_entry_spread_011.json` and `sample_entry_spread_008.json` in full before starting. These define the quality every entry must match.

**Sample 1: spread_011** (PDF page 11, book pages 12–13) — The "you" surveillance spread. Body text about electronic surveillance, fingerprint inset, full-page concentric-circle target. The rhetoric analysis explains how the spread performs surveillance on the reader: the giant "you" singles them out, the fingerprint identifies them, the target aims at them.

**Sample 2: spread_008** (PDF page 8, book pages 6–7) — The "and how!" spread. Full-bleed black, giant white text, Whitehead quote split across the gutter. No images — typography IS the visual content. The rhetoric analysis explains how the spread itself "wrecks" conventional book design, enacting the Whitehead quote about civilization-wrecking advances.

Quality indicators to match:
- `body_text` is verbatim including typographic effects
- `relationship_to_text` on images is analytical — what the image DOES, not just what it shows
- `design_argument_description` identifies the specific mechanism
- `rhetorical_strategy` is precisely named
- `notes` captures historical context and cross-references

---

## 7. Three-Pass Process

### Pass 1: Individual Spread Analysis

Process every PDF page sequentially, 1 through 85.

For each page:
1. View the rendered PNG.
2. Read the image carefully — extract all text, identify all images, analyze the design.
3. Write the complete JSON analysis entry following the schema.
4. Before analyzing each spread, re-read the previous 3 completed entries from the database file to maintain continuity for the `progression` fields.

**For `relationship_to_next`:** Give your best inference based on the current spread's momentum. You'll refine this in Pass 2.

**Batch checkpoint:** After completing the first 10 spreads (PDF pages 1–10), STOP. Start the web viewer and tell the human the first batch is ready for review. Wait for approval before continuing with the remaining 75 spreads.

### Pass 2: Rhetoric Refinement

After all 85 spreads are analyzed, go through each one again with a wider lens. For each spread:

1. Re-read the current spread's analysis.
2. Re-read the 5 spreads before and 5 after it.
3. With this wider context, refine:
   - `rhetorical_strategy` — does a multi-spread pattern emerge (accumulation across several spreads, call-and-response, rhythm of loud/quiet)?
   - `design_enacts_argument` / `design_argument_description` — are there design patterns spanning multiple spreads (progressive density increase, dark/light alternation)?
   - `relationship_to_next` — now that you know what follows, update accurately.
4. Add `rhetoric.multi_spread_patterns` (string or null): if this spread participates in a rhetorical sequence spanning multiple spreads, describe the pattern and which spreads are involved.

Only modify fields where the wider context reveals something new. Do not weaken good analysis.

### Pass 3: Thematic Arc Summary

After Pass 2, generate the `thematic_arc` object by reviewing the complete database:
- Identify the book's implicit sections (groups of consecutive spreads sharing thematic focus)
- For each: title, spread range, book page range, dominant themes, summary, movement_correspondence
- Write the `overall_arc` narrative
- Describe the `rhythm_pattern`
- Identify `recurring_motifs` with appearances and functions

Append the `thematic_arc` to the top level of `analysis_database.json`.

---

## 8. Web Viewer

Build a localhost web application for reviewing results. The human uses this to verify the first batch before approving the full run.

### Technology
Python Flask server. Single HTML template. No build step. Reads directly from `analysis_database.json` and the rendered PNGs.

### Layout
Two-panel view, side by side:
- **Left panel (~50%):** The rendered spread image. Should scale to fit comfortably. Zoomable or scrollable if large.
- **Right panel (~50%):** The analysis data, rendered as formatted HTML — NOT raw JSON.

### Navigation
- Previous / Next buttons
- Dropdown or numbered list to jump to any spread
- Header showing spread ID and book pages

### Right Panel Formatting
- Section headers for each block: Text, Quotations, Images, Design, Rhetoric, Themes, Progression
- **Rhetoric section visually prominent** — larger text, highlighted background, or other emphasis. This is the most important section.
- `design_enacts_argument`: Display as clear YES/NO badge with description immediately below
- `body_text`: Readable prose, not a code block
- Enum fields (spread_type, orientation, pace_shift, etc.): Styled as colored tags/badges
- Arrays (mcluhan_concepts, themes, domain candidates, movement_mapping): Tag clouds or badge lists
- Quotations and images: Displayed as distinct cards within their sections
- `notes`: Info box at the bottom, if present

### Status
- Show which spreads are analyzed (filled) vs pending (empty) in navigation
- Show current pass and progress (e.g., "42/85 spreads analyzed")

Read-only — no editing capability needed.

---

## 9. Directory Structure

```
mcluhan-analysis/
├── source/
│   ├── themediumisthemassage_marshallmcluhan_quentinfiorecompressed.pdf
│   ├── analysis_schema_v1.1.json
│   ├── image_credits_lookup.json
│   ├── sample_entry_spread_011.json
│   └── sample_entry_spread_008.json
├── rendered/                    # PNG renders of each PDF page (you create these)
│   ├── spread_001.png
│   ├── spread_002.png
│   └── ...
├── output/
│   ├── analysis_database.json   # The main output — grows incrementally
│   └── analysis_log.json        # Processing log with timestamps and status
└── viewer/                      # Web viewer application
    ├── app.py
    ├── templates/
    │   └── viewer.html
    └── static/
        └── style.css
```

---

## 10. Execution Sequence

### Phase A: Setup
1. Create the directory structure.
2. Copy/link source files into `source/`.
3. Install dependencies: `pymupdf` (for PDF rendering), `flask` (for viewer).
4. Render all 85 PDF pages as PNGs at 200 DPI into `rendered/`. Use PyMuPDF:
```python
import fitz
doc = fitz.open("source/themediumisthemassage_marshallmcluhan_quentinfiorecompressed.pdf")
for i in range(doc.page_count):
    page = doc[i]
    pix = page.get_pixmap(dpi=200)
    pix.save(f"rendered/spread_{i+1:03d}.png")
doc.close()
```
5. Initialize `analysis_database.json`:
```json
{
  "metadata": {
    "source_pdf": "themediumisthemassage_marshallmcluhan_quentinfiorecompressed.pdf",
    "total_pdf_pages": 85,
    "total_book_pages": 160,
    "analysis_date": "YYYY-MM-DD",
    "analysis_model": "claude-opus-4-6-claude-code",
    "schema_version": "1.1"
  },
  "spreads": []
}
```
6. Read both sample entries in full. Internalize the quality bar.
7. Read the credits lookup. Understand the format.
8. Build the web viewer (it can be built now and will display entries as they're added).

### Phase B: First Batch (Review Checkpoint)
9. Analyze PDF pages 1–10 (spreads 001–010). For each:
   - View the rendered PNG
   - Re-read the previous 3 entries (where available) for progression context
   - Write the complete analysis entry
   - Append to `analysis_database.json`
10. Start the web viewer.
11. **STOP.** Tell the human: "The first 10 spreads are analyzed and the viewer is running at http://localhost:XXXX. Please review and let me know if the quality is acceptable."
12. Wait for approval.

### Phase C: Main Run
13. Analyze the remaining pages (PDF pages 11–85, spreads 011–085).
14. Run Pass 2 (rhetoric refinement) on all spreads.
15. Run Pass 3 (thematic arc summary).
16. Notify the human that analysis is complete.

---

## 11. Key Reminders

**Transcription accuracy matters.** Read every word on every page. This is scanned text — there is no OCR to fall back on. You are the OCR. If text is unclear, give your best reading and note uncertainty in `notes`.

**The rhetoric section is the most important part.** Spend real analytical effort here. The `design_argument_description` field should be the most carefully written text in each entry. Generic descriptions like "the design supports the text" are worthless. Explain the MECHANISM.

**Be specific about images.** Don't write "a photograph of people." Write "A black-and-white press photograph showing a crowd of young men in suits and academic gowns, several standing or turning away from an unseen speaker on the right. The framing is tight, shot from within the crowd at eye level."

**Use the credits lookup for every image.** Cross-reference the book page numbers to find the credit. This is factual data, not analysis — get it right.

**Maintain progression continuity.** Before each spread, re-read the previous 3 entries. The `progression` fields should read as a continuous narrative across the book, not as isolated observations.

**Be honest about uncertainty.** If you can't read text clearly, say so. If you're not sure what an image depicts, describe what you see and note the ambiguity. If a thematic mapping feels forced, explain why in `mapping_rationale` rather than forcing a bad fit.
