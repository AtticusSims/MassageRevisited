"""
Batch export all rendered spreads as PNG images using Playwright.
Starts a local HTTP server, navigates to each spread, and captures
a screenshot of the rendered spread frame at full resolution (1060x905).
"""
import json
import os
import sys
import http.server
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUT_DIR = PROJECT_ROOT / "output" / "spread_exports"
DATA_FILE = DOCS_DIR / "data" / "authoring_output.json"

PORT = 8765  # Use a distinct port to avoid conflicts

def start_server():
    """Start a local HTTP server for the docs directory."""
    handler = http.server.SimpleHTTPRequestHandler
    os.chdir(str(DOCS_DIR))
    server = http.server.HTTPServer(("127.0.0.1", PORT), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

def export_spreads():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load data to know how many spreads
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    spreads = data["spreads"]
    total = len(spreads)
    print(f"Found {total} spreads in authoring_output.json")

    # Start local server
    server = start_server()
    print(f"HTTP server started on port {PORT}")
    time.sleep(0.5)

    # Analysis report
    report = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Create a page large enough to render the spread at full size
        page = browser.new_page(viewport={"width": 1400, "height": 1100})

        # Navigate to the authoring page
        url = f"http://127.0.0.1:{PORT}/authoring.html"
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(2000)  # Let fonts load

        exported = 0
        skipped = 0

        for idx, spread in enumerate(spreads):
            sid = spread["spread_id"]
            has_specs = bool(spread.get("design_specs"))
            has_text = any(
                (o.get("display_text") or o.get("body_text"))
                for o in spread.get("text_options", [])
            )

            if not has_specs:
                print(f"  [{idx+1}/{total}] {sid} — no design specs, skipping")
                skipped += 1
                report.append({
                    "spread_id": sid,
                    "status": "skipped",
                    "reason": "no_design_specs"
                })
                continue

            # Navigate to spread
            page.evaluate(f"goToSpread({idx})")
            page.wait_for_timeout(300)  # Let render settle

            # Get the design spec info for the report
            spec = spread["design_specs"][0] if spread.get("design_specs") else {}
            layout_type = spec.get("layout", {}).get("type", "unknown")
            tone = spec.get("tone", "unknown")
            display_scale = spec.get("typography", {}).get("display_scale", "unknown")
            color_treatment = spec.get("typography", {}).get("color_treatment", "unknown")
            gutter = spec.get("layout", {}).get("gutter_treatment", "unknown")
            image_approach = spec.get("image_direction", {}).get("approach", "unknown")

            # Capture the spread frame element
            spread_frame = page.query_selector("#spreadFrame")
            if spread_frame:
                out_path = OUTPUT_DIR / f"{sid}.png"
                spread_frame.screenshot(path=str(out_path))
                exported += 1
                print(f"  [{idx+1}/{total}] {sid} — exported ({layout_type}, {tone})")

                report.append({
                    "spread_id": sid,
                    "status": "exported",
                    "has_text": has_text,
                    "layout_type": layout_type,
                    "tone": tone,
                    "display_scale": display_scale,
                    "color_treatment": color_treatment,
                    "gutter_treatment": gutter,
                    "image_approach": image_approach,
                    "file": f"{sid}.png"
                })
            else:
                print(f"  [{idx+1}/{total}] {sid} — FAILED: spread frame not found")
                skipped += 1
                report.append({
                    "spread_id": sid,
                    "status": "failed",
                    "reason": "spread_frame_not_found"
                })

        browser.close()

    server.shutdown()

    # Save report
    report_path = OUTPUT_DIR / "export_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_spreads": total,
            "exported": exported,
            "skipped": skipped,
            "spreads": report
        }, f, indent=2)

    print(f"\nDone! Exported {exported}, skipped {skipped}")
    print(f"Images saved to: {OUTPUT_DIR}")
    print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    export_spreads()
