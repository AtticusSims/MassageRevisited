#!/usr/bin/env python3
"""
generate_wireframes.py
Generates SVG wireframes for each spread in authoring_output.json
and embeds them into the design_specs[0].svg_wireframe field.

Each wireframe is 640x400 px representing a two-page spread.
"""

import json
import html
import os
import sys

# ── Paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
INPUT_PATH = os.path.join(PROJECT_DIR, "output", "authoring_output.json")
OUTPUT_PATH = INPUT_PATH  # overwrite in place

W = 640   # total width
H = 400   # total height
MID = W // 2  # gutter x
MARGIN = 16
TITLE_BAR_H = 28
CONTENT_TOP = TITLE_BAR_H + 8
CONTENT_H = H - CONTENT_TOP - MARGIN

# ── Color palette ──────────────────────────────────────────────────────
TEXT_ZONE_FILL   = "#E0E0E0"
TEXT_ZONE_STROKE = "#BDBDBD"
IMAGE_ZONE_FILL  = "#999999"
IMAGE_ZONE_STROKE = "#777777"
LABEL_COLOR      = "#555555"
LABEL_SIZE       = 10
TITLE_SIZE       = 11
PAGE_STROKE      = "#333333"
GRID_STROKE      = "#CCCCCC"


def esc(text: str) -> str:
    """Escape text for safe SVG embedding."""
    return html.escape(str(text), quote=True)


def build_defs(tone: str) -> str:
    """Build SVG <defs> with hatching pattern and optional filters."""
    return f"""<defs>
  <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <line x1="0" y1="0" x2="0" y2="6" stroke="{'#666' if tone != 'dark' else '#AAA'}" stroke-width="1"/>
  </pattern>
</defs>"""


def bg_color(tone: str, color_treatment: str) -> str:
    if tone == "dark" or color_treatment in ("white_on_black", "reversed"):
        return "#222222"
    if tone == "high_contrast":
        return "#F5F5F5"
    return "#FFFFFF"


def fg_color(tone: str, color_treatment: str) -> str:
    if tone == "dark" or color_treatment in ("white_on_black", "reversed"):
        return "#EEEEEE"
    return "#333333"


def text_fill_for_tone(tone: str, color_treatment: str) -> str:
    if tone == "dark" or color_treatment in ("white_on_black", "reversed"):
        return "#3A3A3A"
    return TEXT_ZONE_FILL


def text_stroke_for_tone(tone: str, color_treatment: str) -> str:
    if tone == "dark" or color_treatment in ("white_on_black", "reversed"):
        return "#555555"
    return TEXT_ZONE_STROKE


def image_fill_for_tone(tone: str, color_treatment: str) -> str:
    if tone == "dark" or color_treatment in ("white_on_black", "reversed"):
        return "#555555"
    return IMAGE_ZONE_FILL


def gutter_line(gutter_treatment: str, tone: str) -> str:
    """Generate the center gutter line based on treatment type."""
    color = "#666" if tone == "dark" else "#AAA"
    if gutter_treatment == "continuous":
        # no visible line
        return ""
    elif gutter_treatment == "divided":
        return f'<line x1="{MID}" y1="0" x2="{MID}" y2="{H}" stroke="{color}" stroke-width="2.5"/>'
    elif gutter_treatment == "bridged":
        return f'<line x1="{MID}" y1="0" x2="{MID}" y2="{H}" stroke="{color}" stroke-width="1" stroke-dasharray="6,4"/>'
    return f'<line x1="{MID}" y1="0" x2="{MID}" y2="{H}" stroke="{color}" stroke-width="1" stroke-dasharray="3,3"/>'


def title_bar(spread_id: str, layout_type: str, label: str, tone: str, color_treatment: str) -> str:
    """Top bar with spread ID, layout type, and label."""
    bar_bg = "#333" if tone == "dark" or color_treatment in ("white_on_black", "reversed") else "#F0F0F0"
    bar_fg = "#DDD" if tone == "dark" or color_treatment in ("white_on_black", "reversed") else "#444"
    return f"""<rect x="0" y="0" width="{W}" height="{TITLE_BAR_H}" fill="{bar_bg}"/>
<text x="{MARGIN}" y="18" font-size="{TITLE_SIZE}" font-family="monospace" fill="{bar_fg}" font-weight="700">{esc(spread_id)}</text>
<text x="110" y="18" font-size="{TITLE_SIZE - 1}" font-family="sans-serif" fill="{bar_fg}">{esc(layout_type)}</text>
<text x="{W - MARGIN}" y="18" font-size="{TITLE_SIZE - 2}" font-family="sans-serif" fill="{bar_fg}" text-anchor="end">{esc(label[:50])}</text>"""


def text_rect(x, y, w, h, label_text, tone, color_treatment, rx=4):
    """A rounded rectangle representing a text zone."""
    fill = text_fill_for_tone(tone, color_treatment)
    stroke = text_stroke_for_tone(tone, color_treatment)
    lbl_fill = "#888" if tone == "dark" else LABEL_COLOR
    label_x = x + w / 2
    label_y = y + h / 2 + 3
    return f"""<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>
<text x="{label_x}" y="{label_y}" font-size="{LABEL_SIZE}" font-family="sans-serif" fill="{lbl_fill}" text-anchor="middle">{esc(label_text)}</text>"""


def image_rect(x, y, w, h, label_text, tone, color_treatment, rx=0):
    """A rectangle with hatching representing an image zone."""
    fill = image_fill_for_tone(tone, color_treatment)
    stroke = IMAGE_ZONE_STROKE if tone != "dark" else "#888"
    lbl_fill = "#EEE" if tone == "dark" else "#333"
    label_x = x + w / 2
    label_y = y + h / 2 + 3
    return f"""<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#hatch)" opacity="0.4"/>
<text x="{label_x}" y="{label_y}" font-size="{LABEL_SIZE}" font-family="sans-serif" fill="{lbl_fill}" text-anchor="middle" font-weight="600">{esc(label_text)}</text>"""


def display_scale_to_font_size(scale: str) -> int:
    return {
        "architectural": 42,
        "headline": 28,
        "subhead": 20,
        "body": 14,
        "caption": 11,
    }.get(scale, 20)


def page_border(tone: str) -> str:
    """Outer page border."""
    color = "#555" if tone == "dark" else PAGE_STROKE
    return f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{color}" stroke-width="1.5" rx="2"/>'


# ── Layout generators ──────────────────────────────────────────────────

def layout_full_bleed_typography(spec, spread_id):
    tone = spec.get("tone", "light")
    ct = spec.get("typography", {}).get("color_treatment", "black_on_white")
    scale = spec.get("typography", {}).get("display_scale", "headline")
    font_size = display_scale_to_font_size(scale)
    fg = fg_color(tone, ct)

    # Zones: one big display text spanning both pages
    display_y = CONTENT_TOP + CONTENT_H * 0.3
    body_zone_y = CONTENT_TOP + CONTENT_H * 0.7

    parts = []
    # Big display text placeholder spanning both pages
    parts.append(text_rect(MARGIN, CONTENT_TOP + 20, W - 2*MARGIN, CONTENT_H * 0.5,
                           "DISPLAY TEXT", tone, ct, rx=6))
    # Simulated large typography lines
    for i in range(3):
        ly = CONTENT_TOP + 40 + i * (font_size + 6)
        lw = W - 4 * MARGIN - (i * 30)
        parts.append(f'<rect x="{MARGIN*2}" y="{ly}" width="{lw}" height="{font_size * 0.6}" rx="2" fill="{fg}" opacity="0.15"/>')

    # Optional body text at bottom
    parts.append(text_rect(MID + MARGIN, body_zone_y, MID - 2*MARGIN, CONTENT_H * 0.2,
                           "BODY", tone, ct))
    return "\n".join(parts)


def layout_full_bleed_image(spec, spread_id):
    tone = spec.get("tone", "dark")
    ct = spec.get("typography", {}).get("color_treatment", "black_on_white")

    parts = []
    # Full-bleed image spanning both pages
    parts.append(image_rect(MARGIN//2, CONTENT_TOP, W - MARGIN, CONTENT_H,
                            "FULL-BLEED IMAGE", tone, ct))
    # Small caption overlay
    parts.append(text_rect(MID + 40, CONTENT_TOP + CONTENT_H - 50, MID - 60, 36,
                           "CAPTION", tone, ct))
    return "\n".join(parts)


def layout_split_asymmetric(spec, spread_id):
    tone = spec.get("tone", "light")
    ct = spec.get("typography", {}).get("color_treatment", "black_on_white")
    img_approach = spec.get("image_direction", {}).get("approach", "none")
    img_scale = spec.get("image_direction", {}).get("scale", "half_page")

    parts = []
    # Left page: text (narrower side, ~40%)
    left_w = MID - MARGIN * 1.5
    right_x = MID + MARGIN * 0.5
    right_w = MID - MARGIN * 1.5

    # Display text at top-left
    parts.append(text_rect(MARGIN, CONTENT_TOP + 8, left_w * 0.8, 30,
                           "DISPLAY", tone, ct))
    # Body text block
    parts.append(text_rect(MARGIN, CONTENT_TOP + 50, left_w, CONTENT_H * 0.5,
                           "BODY TEXT", tone, ct))
    # Caption at bottom-left
    parts.append(text_rect(MARGIN, CONTENT_TOP + CONTENT_H - 40, left_w * 0.6, 28,
                           "CAPTION", tone, ct))

    # Right page: image
    if img_approach in ("typography_only", "none"):
        parts.append(text_rect(right_x, CONTENT_TOP + 8, right_w, CONTENT_H - 16,
                               "TEXT / GRAPHIC", tone, ct))
    elif img_scale == "full_bleed":
        parts.append(image_rect(right_x, CONTENT_TOP, right_w + MARGIN//2, CONTENT_H,
                                "IMAGE", tone, ct))
    elif img_scale == "half_page":
        parts.append(image_rect(right_x, CONTENT_TOP + 8, right_w, CONTENT_H * 0.55,
                                "IMAGE", tone, ct))
        parts.append(text_rect(right_x, CONTENT_TOP + CONTENT_H * 0.6 + 16, right_w, CONTENT_H * 0.3,
                               "CAPTION / TEXT", tone, ct))
    else:
        parts.append(image_rect(right_x, CONTENT_TOP + 20, right_w, CONTENT_H * 0.7,
                                "IMAGE", tone, ct))

    return "\n".join(parts)


def layout_split_symmetric(spec, spread_id):
    tone = spec.get("tone", "light")
    ct = spec.get("typography", {}).get("color_treatment", "black_on_white")

    parts = []
    left_w = MID - MARGIN * 1.5
    right_x = MID + MARGIN * 0.5
    right_w = MID - MARGIN * 1.5

    # Left page: text
    parts.append(text_rect(MARGIN, CONTENT_TOP + 8, left_w, 30,
                           "DISPLAY", tone, ct))
    parts.append(text_rect(MARGIN, CONTENT_TOP + 50, left_w, CONTENT_H * 0.6,
                           "BODY TEXT", tone, ct))

    # Right page: image
    parts.append(image_rect(right_x, CONTENT_TOP + 8, right_w, CONTENT_H - 16,
                            "IMAGE", tone, ct))
    return "\n".join(parts)


def layout_text_dominant(spec, spread_id):
    tone = spec.get("tone", "light")
    ct = spec.get("typography", {}).get("color_treatment", "black_on_white")
    img_scale = spec.get("image_direction", {}).get("scale", "quarter_page")

    parts = []
    # Left page: display + body text
    parts.append(text_rect(MARGIN, CONTENT_TOP + 8, MID - 2*MARGIN, 30,
                           "DISPLAY", tone, ct))
    parts.append(text_rect(MARGIN, CONTENT_TOP + 50, MID - 2*MARGIN, CONTENT_H * 0.65,
                           "BODY TEXT (primary)", tone, ct))

    # Right page: more body text + small image
    parts.append(text_rect(MID + MARGIN, CONTENT_TOP + 8, MID - 2*MARGIN, CONTENT_H * 0.45,
                           "BODY TEXT (cont.)", tone, ct))

    if img_scale in ("half_page", "full_bleed"):
        img_h = CONTENT_H * 0.35
    else:
        img_h = CONTENT_H * 0.25

    parts.append(image_rect(MID + MARGIN, CONTENT_TOP + CONTENT_H - img_h - 8,
                            MID - 2*MARGIN, img_h,
                            "IMAGE", tone, ct))
    # Caption
    parts.append(text_rect(MARGIN, CONTENT_TOP + CONTENT_H - 28, MID * 0.4, 20,
                           "CAPTION", tone, ct))
    return "\n".join(parts)


def layout_image_dominant(spec, spread_id):
    tone = spec.get("tone", "dark")
    ct = spec.get("typography", {}).get("color_treatment", "black_on_white")
    gutter = spec.get("layout", {}).get("gutter_treatment", "continuous")

    parts = []

    if gutter == "continuous":
        # Full-bleed image across both pages
        parts.append(image_rect(MARGIN//2, CONTENT_TOP, W - MARGIN, CONTENT_H,
                                "FULL-BLEED IMAGE", tone, ct))
        # Display text floating over image (upper area)
        parts.append(text_rect(MARGIN * 2, CONTENT_TOP + 16, MID * 0.6, 32,
                               "DISPLAY", tone, ct))
        # Caption at bottom
        parts.append(text_rect(MID + 20, CONTENT_TOP + CONTENT_H - 44, MID - 40, 32,
                               "CAPTION", tone, ct))
    else:
        # Left page: text with generous whitespace
        parts.append(text_rect(MARGIN, CONTENT_TOP + 16, MID - 2*MARGIN, 28,
                               "DISPLAY", tone, ct))
        parts.append(text_rect(MARGIN, CONTENT_TOP + 56, MID * 0.7, CONTENT_H * 0.35,
                               "BODY", tone, ct))
        parts.append(text_rect(MARGIN, CONTENT_TOP + CONTENT_H - 32, MID * 0.5, 22,
                               "CAPTION", tone, ct))
        # Right page: large image
        parts.append(image_rect(MID + MARGIN//2, CONTENT_TOP, MID - MARGIN, CONTENT_H,
                                "IMAGE", tone, ct))

    return "\n".join(parts)


def layout_text_over_image(spec, spread_id):
    tone = spec.get("tone", "balanced")
    ct = spec.get("typography", {}).get("color_treatment", "mixed")

    parts = []
    # Full background image
    parts.append(image_rect(MARGIN//2, CONTENT_TOP, W - MARGIN, CONTENT_H,
                            "BACKGROUND IMAGE", tone, ct))
    # Text zones overlaid
    parts.append(text_rect(MARGIN * 3, CONTENT_TOP + 30, MID * 0.7, 36,
                           "DISPLAY (overlay)", tone, ct))
    parts.append(text_rect(MID - 40, CONTENT_TOP + CONTENT_H * 0.4, MID * 0.8, CONTENT_H * 0.35,
                           "BODY TEXT (overlay)", tone, ct))
    parts.append(text_rect(MID + 60, CONTENT_TOP + CONTENT_H - 40, MID * 0.5, 28,
                           "CAPTION", tone, ct))
    return "\n".join(parts)


def layout_minimal_sparse(spec, spread_id):
    tone = spec.get("tone", "light")
    ct = spec.get("typography", {}).get("color_treatment", "black_on_white")

    parts = []
    # Small centered elements with lots of whitespace
    center_x = W // 2 - 80
    center_y = H // 2 - 20

    parts.append(text_rect(center_x, center_y - 40, 160, 28,
                           "DISPLAY", tone, ct))
    parts.append(text_rect(center_x + 20, center_y + 10, 120, 50,
                           "BODY", tone, ct))
    # Small image element
    parts.append(image_rect(W - MARGIN * 6, CONTENT_TOP + CONTENT_H - 80, 60, 60,
                            "IMG", tone, ct))
    return "\n".join(parts)


def layout_dense_collage(spec, spread_id):
    tone = spec.get("tone", "balanced")
    ct = spec.get("typography", {}).get("color_treatment", "mixed")

    parts = []
    # Multiple overlapping zones
    parts.append(image_rect(MARGIN, CONTENT_TOP + 5, MID * 0.6, CONTENT_H * 0.5,
                            "IMAGE A", tone, ct))
    parts.append(image_rect(MID * 0.5, CONTENT_TOP + CONTENT_H * 0.35, MID * 0.7, CONTENT_H * 0.5,
                            "IMAGE B", tone, ct))
    parts.append(text_rect(MARGIN * 2, CONTENT_TOP + 15, MID * 0.5, 30,
                           "DISPLAY", tone, ct))
    parts.append(image_rect(MID + MARGIN, CONTENT_TOP + 5, MID * 0.5, CONTENT_H * 0.45,
                            "IMAGE C", tone, ct))
    parts.append(text_rect(MID + MARGIN * 3, CONTENT_TOP + CONTENT_H * 0.4, MID * 0.6, CONTENT_H * 0.35,
                           "BODY", tone, ct))
    parts.append(text_rect(MID * 0.8, CONTENT_TOP + CONTENT_H - 36, MID * 0.4, 26,
                           "CAPTION", tone, ct))
    parts.append(image_rect(MID + MID * 0.4, CONTENT_TOP + CONTENT_H * 0.6, MID * 0.5, CONTENT_H * 0.35,
                            "IMAGE D", tone, ct))
    return "\n".join(parts)


def layout_diagram_with_text(spec, spread_id):
    tone = spec.get("tone", "light")
    ct = spec.get("typography", {}).get("color_treatment", "black_on_white")

    parts = []
    # Left page: text
    parts.append(text_rect(MARGIN, CONTENT_TOP + 8, MID - 2*MARGIN, 28,
                           "DISPLAY", tone, ct))
    parts.append(text_rect(MARGIN, CONTENT_TOP + 48, MID - 2*MARGIN, CONTENT_H * 0.55,
                           "BODY TEXT", tone, ct))

    # Right page: diagram (represented as image with grid lines)
    dx = MID + MARGIN
    dw = MID - 2*MARGIN
    dy = CONTENT_TOP + 8
    dh = CONTENT_H - 16
    parts.append(image_rect(dx, dy, dw, dh, "DIAGRAM", tone, ct))
    # Grid lines inside diagram
    for i in range(1, 4):
        gy = dy + (dh * i) // 4
        parts.append(f'<line x1="{dx+4}" y1="{gy}" x2="{dx+dw-4}" y2="{gy}" stroke="{"#AAA" if tone == "dark" else "#666"}" stroke-width="0.5" stroke-dasharray="2,2"/>')
    for i in range(1, 3):
        gx = dx + (dw * i) // 3
        parts.append(f'<line x1="{gx}" y1="{dy+4}" x2="{gx}" y2="{dy+dh-4}" stroke="{"#AAA" if tone == "dark" else "#666"}" stroke-width="0.5" stroke-dasharray="2,2"/>')

    return "\n".join(parts)


# ── Layout dispatcher ──────────────────────────────────────────────────

LAYOUT_GENERATORS = {
    "full_bleed_typography": layout_full_bleed_typography,
    "full_bleed_image":      layout_full_bleed_image,
    "split_asymmetric":      layout_split_asymmetric,
    "split_symmetric":       layout_split_symmetric,
    "text_dominant":         layout_text_dominant,
    "image_dominant":        layout_image_dominant,
    "text_over_image":       layout_text_over_image,
    "minimal_sparse":        layout_minimal_sparse,
    "dense_collage":         layout_dense_collage,
    "diagram_with_text":     layout_diagram_with_text,
}


def density_annotation(density: str, tone: str) -> str:
    """Add a small density indicator in the bottom-left corner."""
    fill = "#666" if tone != "dark" else "#AAA"
    dots = {"sparse": 1, "moderate": 2, "dense": 3, "overwhelming": 4}.get(density, 2)
    parts = []
    for i in range(dots):
        cx = MARGIN + 6 + i * 10
        cy = H - 8
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{fill}" opacity="0.5"/>')
    parts.append(f'<text x="{MARGIN + dots * 10 + 8}" y="{H - 5}" font-size="8" font-family="sans-serif" fill="{fill}" opacity="0.6">{density}</text>')
    return "\n".join(parts)


def tone_annotation(tone_val: str, ct: str) -> str:
    """Add a small tone indicator in the bottom-right corner."""
    fill = "#666" if tone_val != "dark" else "#AAA"
    return f'<text x="{W - MARGIN}" y="{H - 5}" font-size="8" font-family="sans-serif" fill="{fill}" opacity="0.6" text-anchor="end">{tone_val} | {ct}</text>'


def generate_wireframe(spread_id: str, spec: dict) -> str:
    """Generate a complete SVG wireframe for one design spec."""
    layout = spec.get("layout", {})
    layout_type = layout.get("type", "split_asymmetric")
    gutter = layout.get("gutter_treatment", "divided")
    tone = spec.get("tone", "light")
    ct = spec.get("typography", {}).get("color_treatment", "black_on_white")
    density = spec.get("density", "moderate")
    label = spec.get("label", "")

    background = bg_color(tone, ct)

    # Get the appropriate layout generator
    gen_fn = LAYOUT_GENERATORS.get(layout_type, layout_split_asymmetric)

    # Build SVG
    svg_parts = [
        f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Helvetica, Arial, sans-serif">',
        build_defs(tone),
        # Background
        f'<rect width="{W}" height="{H}" fill="{background}"/>',
        # Page border
        page_border(tone),
        # Title bar
        title_bar(spread_id, layout_type, label, tone, ct),
        # Gutter
        gutter_line(gutter, tone),
        # Content zones
        gen_fn(spec, spread_id),
        # Annotations
        density_annotation(density, tone),
        tone_annotation(tone, ct),
        '</svg>',
    ]

    return "\n".join(svg_parts)


def main():
    # Load
    print(f"Reading {INPUT_PATH}")
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    spreads = data.get("spreads", [])
    print(f"Found {len(spreads)} spreads")

    generated = 0
    replaced = 0
    errors = []

    for spread in spreads:
        spread_id = spread.get("spread_id", "unknown")
        design_specs = spread.get("design_specs", [])

        if not design_specs:
            errors.append(f"{spread_id}: no design_specs found")
            continue

        spec = design_specs[0]
        had_existing = bool(spec.get("svg_wireframe"))

        try:
            svg = generate_wireframe(spread_id, spec)
            spec["svg_wireframe"] = svg
            generated += 1
            if had_existing:
                replaced += 1
            status = "REPLACED" if had_existing else "GENERATED"
            layout_type = spec.get("layout", {}).get("type", "?")
            print(f"  {spread_id}: {status} ({layout_type})")
        except Exception as e:
            errors.append(f"{spread_id}: {e}")
            print(f"  {spread_id}: ERROR - {e}")

    # Save
    print(f"\nSaving to {OUTPUT_PATH}")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\n{'='*50}")
    print(f"Wireframe Generation Summary")
    print(f"{'='*50}")
    print(f"  Total spreads:     {len(spreads)}")
    print(f"  Generated (new):   {generated - replaced}")
    print(f"  Replaced:          {replaced}")
    print(f"  Total written:     {generated}")
    print(f"  Errors:            {len(errors)}")
    if errors:
        print(f"\nErrors:")
        for e in errors:
            print(f"  - {e}")
    print(f"\nDone.")


if __name__ == "__main__":
    main()
