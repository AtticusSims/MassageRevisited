"""
Web viewer for McLuhan analysis database.
Reads analysis_database.json and rendered PNGs, displays side-by-side.
"""

import json
import os
from flask import Flask, render_template, send_from_directory, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
RENDERED_DIR = os.path.join(BASE_DIR, "rendered")
DB_PATH = os.path.join(OUTPUT_DIR, "analysis_database.json")


def load_database():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    db = load_database()
    spreads = db.get("spreads", [])
    metadata = db.get("metadata", {})
    total_pages = metadata.get("total_pdf_pages", 85)

    # Build navigation data: which spreads are analyzed
    analyzed_ids = {s["id"] for s in spreads}
    nav_items = []
    for i in range(1, total_pages + 1):
        sid = f"spread_{i:03d}"
        nav_items.append({
            "id": sid,
            "pdf_page": i,
            "analyzed": sid in analyzed_ids,
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
    )


@app.route("/api/spread/<spread_id>")
def get_spread(spread_id):
    db = load_database()
    for s in db.get("spreads", []):
        if s["id"] == spread_id:
            return jsonify(s)
    return jsonify(None)


@app.route("/rendered/<filename>")
def serve_rendered(filename):
    return send_from_directory(RENDERED_DIR, filename)


if __name__ == "__main__":
    print(f"Database: {DB_PATH}")
    print(f"Rendered: {RENDERED_DIR}")
    print(f"Starting viewer at http://localhost:5001")
    app.run(host="127.0.0.1", port=5001, debug=False)
