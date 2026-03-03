"""
gemini_tools.py — Google Gemini API client for image description
and analysis of "The Medium is the Massage" spreads.

Supports model fallback chain:
  1. gemini-3.1-pro-preview  (best quality, newest)
  2. gemini-2.5-pro          (thinking model, very capable)
  3. gemini-2.5-flash         (fast, reliable fallback)

Requires:
  pip install google-genai python-dotenv

API key: Set GEMINI_API_KEY environment variable or add to source/.env
"""

import json
import os
import time
from pathlib import Path

from google import genai
from google.genai import types

# ── Configuration ──

BASE_DIR = Path(__file__).parent.parent
SOURCE_DIR = Path(__file__).parent
CONTEXT_DOCS_DIR = BASE_DIR / "ContextDocs"
OUTPUT_DIR = BASE_DIR / "output" / "gemini_extractions"
RENDERED_DIR = BASE_DIR / "rendered"

# Model fallback chain: try in order until one works
MODEL_CHAIN = [
    "gemini-3.1-pro-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
]

# Models that require thinking mode
THINKING_MODELS = {"gemini-2.5-pro"}
THINKING_BUDGET = 8192  # tokens for thinking

# Default model (can be overridden by set_model())
GEMINI_MODEL = "gemini-2.5-pro"  # Default to 2.5-pro (reliable + high quality)


def set_model(model_name: str):
    """Override the default model."""
    global GEMINI_MODEL
    GEMINI_MODEL = model_name
    print(f"  Model set to: {model_name}")


def _load_api_key():
    """Load API key from environment or .env file."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    env_path = SOURCE_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip("'\"")

    raise EnvironmentError(
        "GEMINI_API_KEY not found. Set it as an environment variable "
        "or add it to source/.env (format: GEMINI_API_KEY=your_key_here)"
    )


def get_client():
    """Get a configured Gemini client."""
    key = _load_api_key()
    return genai.Client(api_key=key)


# ── Context Document Loading ──

def load_methodology() -> str:
    """Load the Phase B methodology document."""
    path = SOURCE_DIR / "phase_b_methodology_v2.md"
    return path.read_text(encoding="utf-8")


def load_schema() -> str:
    """Load the analysis schema v1.2."""
    path = SOURCE_DIR / "analysis_schema_v1.2.json"
    return path.read_text(encoding="utf-8")


def load_sample_entries() -> str:
    """Load gold-standard sample entries."""
    samples = []
    for name in ["sample_entry_spread_011.json", "sample_entry_spread_008.json"]:
        path = SOURCE_DIR / name
        if path.exists():
            samples.append(f"=== {name} ===\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(samples)


def load_framework() -> str:
    """Load the intellectual framework document."""
    path = CONTEXT_DOCS_DIR / "framework_v3.md"
    return path.read_text(encoding="utf-8")


def load_theorist_reference() -> str:
    """Load theorist reference profiles."""
    path = CONTEXT_DOCS_DIR / "theorist_reference.md"
    return path.read_text(encoding="utf-8")


def load_visual_description_context() -> str:
    """Load context for visual description pass (Phase 2).
    Includes methodology, schema, and sample entries."""
    parts = [
        "# ANALYSIS METHODOLOGY\n\n" + load_methodology(),
        "\n\n# ANALYSIS SCHEMA (v1.2)\n\n" + load_schema(),
        "\n\n# GOLD-STANDARD SAMPLE ENTRIES\n\n" + load_sample_entries(),
    ]
    return "\n".join(parts)


def load_full_analysis_context() -> str:
    """Load full context for analysis pass (Phase 3).
    Includes everything from Phase 2 plus framework and theorist docs."""
    parts = [
        "# ANALYSIS METHODOLOGY\n\n" + load_methodology(),
        "\n\n# ANALYSIS SCHEMA (v1.2)\n\n" + load_schema(),
        "\n\n# GOLD-STANDARD SAMPLE ENTRIES\n\n" + load_sample_entries(),
        "\n\n# INTELLECTUAL FRAMEWORK\n\n" + load_framework(),
        "\n\n# THEORIST REFERENCE PROFILES\n\n" + load_theorist_reference(),
    ]
    return "\n".join(parts)


# ── Core API Functions ──

def _build_contents(image_path: str | None, prompt: str) -> list:
    """Build contents list from optional image + prompt."""
    contents = []
    if image_path:
        img_path = Path(image_path)
        image_bytes = img_path.read_bytes()
        suffix = img_path.suffix.lower()
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
        mime_type = mime_map.get(suffix, "image/png")
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
    contents.append(prompt)
    return contents


def _make_config(
    model: str,
    temperature: float,
    max_output_tokens: int,
    system_prompt: str | None = None,
    json_mode: bool = False,
) -> types.GenerateContentConfig:
    """Build a GenerateContentConfig, adding thinking config for thinking models."""
    kwargs = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }
    if system_prompt:
        kwargs["system_instruction"] = system_prompt
    if json_mode:
        kwargs["response_mime_type"] = "application/json"
    if model in THINKING_MODELS:
        kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=THINKING_BUDGET)
    return types.GenerateContentConfig(**kwargs)


def _call_with_retry(
    client,
    model: str,
    contents: list,
    config: types.GenerateContentConfig,
    max_retries: int = 5,
    initial_delay: float = 2.0,
):
    """Call Gemini API with exponential backoff retry on transient errors."""
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )
            return response
        except Exception as e:
            error_str = str(e)
            # Retry on 503 (high demand), 429 (rate limit), 500 (server error)
            if any(code in error_str for code in ["503", "429", "500", "UNAVAILABLE", "RESOURCE_EXHAUSTED"]):
                if attempt < max_retries - 1:
                    print(f"    [Retry {attempt+1}/{max_retries}] {error_str[:80]}... waiting {delay:.0f}s")
                    time.sleep(delay)
                    delay *= 2  # exponential backoff
                    continue
            raise  # Non-retryable error or max retries exceeded


def _call_with_fallback(
    client,
    contents: list,
    temperature: float = 0.2,
    max_output_tokens: int = 16384,
    system_prompt: str | None = None,
    json_mode: bool = False,
    primary_model: str | None = None,
):
    """Try primary model, then fall through MODEL_CHAIN on 503 errors."""
    models_to_try = [primary_model or GEMINI_MODEL]
    # Add fallbacks from the chain that aren't already the primary
    for m in MODEL_CHAIN:
        if m not in models_to_try:
            models_to_try.append(m)

    last_error = None
    for model in models_to_try:
        config = _make_config(model, temperature, max_output_tokens, system_prompt, json_mode)
        try:
            response = _call_with_retry(client, model, contents, config, max_retries=3, initial_delay=2.0)
            return response, model
        except Exception as e:
            last_error = e
            error_str = str(e)
            if any(code in error_str for code in ["503", "UNAVAILABLE"]):
                print(f"    [{model}] 503 — trying next model...")
                continue
            raise  # Non-retryable error

    # All models exhausted
    raise last_error


def gemini_chat(
    image_path: str | None,
    prompt: str,
    system_prompt: str | None = None,
    temperature: float = 0.2,
    max_output_tokens: int = 16384,
) -> str:
    """Send a prompt (optionally with an image) to Gemini and get a text response.

    Args:
        image_path: Path to image file, or None for text-only
        prompt: The user prompt
        system_prompt: Optional system instruction
        temperature: Sampling temperature (default 0.2 for factual)
        max_output_tokens: Maximum response length
    Returns:
        Response text string
    """
    client = get_client()
    contents = _build_contents(image_path, prompt)

    response, model_used = _call_with_fallback(
        client, contents,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_prompt=system_prompt,
        json_mode=False,
    )
    return response.text


def gemini_json(
    image_path: str | None,
    prompt: str,
    system_prompt: str | None = None,
    temperature: float = 0.2,
    max_output_tokens: int = 16384,
) -> dict:
    """Send a prompt to Gemini and get a parsed JSON response.

    Args:
        image_path: Path to image file, or None for text-only
        prompt: The user prompt (should request JSON output)
        system_prompt: Optional system instruction
        temperature: Sampling temperature
        max_output_tokens: Maximum response length
    Returns:
        Tuple of (parsed JSON dict, model name used)
    """
    client = get_client()
    contents = _build_contents(image_path, prompt)

    response, model_used = _call_with_fallback(
        client, contents,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_prompt=system_prompt,
        json_mode=True,
    )

    # Parse JSON from response
    text = response.text.strip()
    # Handle potential markdown code block wrapping
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    result = json.loads(text)
    # If result is an array, wrap it in a dict
    if isinstance(result, list):
        result = {"_array_response": result}
    # Attach model metadata
    result["_model_used"] = model_used
    return result


# ── Utility Functions ──

def get_spread_image_path(spread_num: int) -> str:
    """Get the path to a spread's rendered PNG image."""
    return str(RENDERED_DIR / f"spread_{spread_num:03d}.png")


def get_cached_result(spread_num: int, suffix: str) -> dict | None:
    """Check if a cached result exists for this spread/suffix combo."""
    path = OUTPUT_DIR / f"spread_{spread_num:03d}_{suffix}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def save_result(spread_num: int, suffix: str, data: dict):
    """Save a result to the cache directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"spread_{spread_num:03d}_{suffix}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)


def load_database() -> dict:
    """Load the analysis database."""
    db_path = BASE_DIR / "output" / "analysis_database.json"
    return json.loads(db_path.read_text(encoding="utf-8"))


def get_spread_text(db: dict, spread_num: int) -> dict:
    """Extract text fields from the database for a specific spread."""
    sid = f"spread_{spread_num:03d}"
    for s in db["spreads"]:
        if s["id"] == sid:
            return {
                "body_text": s.get("text", {}).get("body_text", ""),
                "display_text": s.get("text", {}).get("display_text", ""),
                "captions": s.get("text", {}).get("captions", []),
                "quotations": s.get("quotations", []),
            }
    return {"body_text": "", "display_text": "", "captions": [], "quotations": []}


# ── Quick Test ──

if __name__ == "__main__":
    print("Testing Gemini API connection...")
    print(f"  Default model: {GEMINI_MODEL}")
    print(f"  Fallback chain: {' >> '.join(MODEL_CHAIN)}")
    print()

    # Test text
    try:
        result = gemini_chat(None, "Reply with exactly one word: WORKING")
        print(f"  Text response: {result.strip()}")
        print("  [PASS] Text API working")
    except Exception as e:
        print(f"  [FAIL] Text: {e}")

    # Test image + JSON with spread_050
    img = get_spread_image_path(50)
    if Path(img).exists():
        print()
        try:
            result = gemini_json(
                img,
                'What body part is shown in the large photograph? Reply as JSON: {"body_part": "...", "details": "..."}',
                temperature=0.1,
            )
            model = result.pop("_model_used", "unknown")
            print(f"  Image+JSON response ({model}): {json.dumps(result)}")
            if "foot" in json.dumps(result).lower():
                print("  [PASS] Correctly identifies foot (Qwen3 says 'hand')")
            else:
                print("  [WARN] Unexpected identification")
        except Exception as e:
            print(f"  [FAIL] Image+JSON: {e}")
    else:
        print(f"  [SKIP] No image at {img}")
