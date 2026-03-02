"""
Web viewer for McLuhan analysis database.
Reads analysis_database.json, OCR extractions, and rendered PNGs.
Serves a review interface for manual checking.
"""

import json
import os
import glob
from flask import Flask, render_template, send_from_directory, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
VLM_DIR = os.path.join(OUTPUT_DIR, "vlm_extractions")
RENDERED_DIR = os.path.join(BASE_DIR, "rendered")
DB_PATH = os.path.join(OUTPUT_DIR, "analysis_database.json")
REVIEW_PATH = os.path.join(OUTPUT_DIR, "review_status.json")


def load_database():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_review_status():
    if os.path.exists(REVIEW_PATH):
        with open(REVIEW_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_review_status(data):
    with open(REVIEW_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_ocr_files(spread_id):
    """Load all OCR extraction files for a spread (both qwen2.5 and qwen3)."""
    result = {}
    # Original Qwen2.5 OCR
    path_25 = os.path.join(VLM_DIR, f"{spread_id}_ocr.json")
    if os.path.exists(path_25):
        with open(path_25, "r", encoding="utf-8") as f:
            result["qwen25"] = json.load(f)
    # Qwen3 OCR
    path_3 = os.path.join(VLM_DIR, f"{spread_id}_ocr_qwen3.json")
    if os.path.exists(path_3):
        with open(path_3, "r", encoding="utf-8") as f:
            result["qwen3"] = json.load(f)
    return result


@app.route("/")
def index():
    db = load_database()
    spreads = db.get("spreads", [])
    metadata = db.get("metadata", {})
    total_pages = metadata.get("total_pdf_pages", 85)
    review = load_review_status()

    analyzed_ids = {s["id"] for s in spreads}
    nav_items = []
    for i in range(1, total_pages + 1):
        sid = f"spread_{i:03d}"
        nav_items.append({
            "id": sid,
            "pdf_page": i,
            "analyzed": sid in analyzed_ids,
            "review_status": review.get(sid, {}).get("status", "pending"),
            "book_pages": next(
                (s.get("book_pages", []) for s in spreads if s["id"] == sid),
                []
            ),
        })

    return render_template(
        "viewer.html",
        nav_items=nav_items,
        metadata=metadata,
        total_analyzed=len(spreads),
        total_pages=total_pages,
        review_counts={
            "approved": sum(1 for n in nav_items if n["review_status"] == "approved"),
            "flagged": sum(1 for n in nav_items if n["review_status"] == "flagged"),
            "pending": sum(1 for n in nav_items if n["review_status"] == "pending" and n["analyzed"]),
        },
    )


@app.route("/api/spread/<spread_id>")
def get_spread(spread_id):
    db = load_database()
    for s in db.get("spreads", []):
        if s["id"] == spread_id:
            return jsonify(s)
    return jsonify(None)


@app.route("/api/ocr/<spread_id>")
def get_ocr(spread_id):
    return jsonify(load_ocr_files(spread_id))


@app.route("/api/review/<spread_id>", methods=["GET"])
def get_review(spread_id):
    review = load_review_status()
    return jsonify(review.get(spread_id, {"status": "pending", "notes": ""}))


@app.route("/api/review/<spread_id>", methods=["POST"])
def set_review(spread_id):
    review = load_review_status()
    data = request.get_json()
    review[spread_id] = {
        "status": data.get("status", "pending"),
        "notes": data.get("notes", ""),
    }
    save_review_status(review)
    return jsonify({"ok": True})


@app.route("/rendered/<filename>")
def serve_rendered(filename):
    return send_from_directory(RENDERED_DIR, filename)


if __name__ == "__main__":
    print(f"Database: {DB_PATH}")
    print(f"Rendered: {RENDERED_DIR}")
    print(f"OCR dir:  {VLM_DIR}")
    print(f"Starting viewer at http://localhost:5001")
    app.run(host="127.0.0.1", port=5001, debug=False)
