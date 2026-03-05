"""
Generate AI-distorted face images for spread_033 of The Model is the Massage.

Uses a local SDXL checkpoint (JuggernautXL) with two techniques to produce
faces that are structurally coherent but perceptually uncanny:

1. LOW STEP-COUNT: Generate with very few denoising steps (5-12 out of 50).
   The face doesn't fully converge — features are suggested but unresolved.

2. IMG2IMG RE-NOISING: Generate a clean face, then add noise back and partially
   re-denoise with altered prompt/guidance. Creates interpolation artifacts.

Both techniques produce valid VAE-decodable outputs (unlike raw intermediate
latent capture which produces black images with SDXL).

Requires: torch, diffusers, accelerate, Pillow
GPU: NVIDIA RTX 5090 (32GB VRAM)
"""

import os
import gc
import json
import torch
import numpy as np
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from datetime import datetime, timezone

# Paths
CHECKPOINT = r"C:\Users\attic\Documents\Comfy_Workspace\ComfyUI-Full\ComfyUI\models\checkpoints\juggernautXL_ragnarokBy.safetensors"
VAE_PATH = r"C:\Users\attic\Documents\Comfy_Workspace\ComfyUI-Full\ComfyUI\models\vae\SDXL\sdxl_vae.safetensors"
OUTPUT_DIR = Path(r"C:\Users\attic\Documents\ClaudeCode\MassageRevisited\mcluhan-analysis\docs\images")

# Generation parameters
WIDTH = 1024
HEIGHT = 1024
SEED_BASE = 42

# Prompts
FACE_PROMPTS = [
    # 0: Classic portrait
    "extreme close-up portrait of a human face, frontal view, dramatic chiaroscuro lighting, "
    "deep shadows, high contrast, studio photography, sharp features, intense gaze, "
    "black and white, monochrome, fine art portrait, 8k, highly detailed",

    # 1: Face from shadow
    "human face emerging from deep shadow, half-illuminated, dramatic side lighting, "
    "one eye visible, features dissolving into darkness, high contrast black and white, "
    "cinematic portrait, film noir, fine art photography, 8k",

    # 2: Distorted/reflected
    "portrait of a human face seen through curved glass, slightly distorted reflection, "
    "warped features, elongated face, dramatic black and white, high contrast, "
    "fine art photography, surreal portrait, unsettling beauty, 8k",

    # 3: Ethereal/abstract
    "ethereal human face, flowing organic forms, features melting and reforming, "
    "surreal portrait, dramatic chiaroscuro, deep blacks and bright highlights, "
    "black and white, monochrome, fine art, dreamlike quality, 8k",
]

NEGATIVE_PROMPT = (
    "text, watermark, logo, signature, low quality, blurry, cartoon, anime, "
    "illustration, painting, drawing, horror, gore, grotesque, ugly, deformed hands, "
    "extra fingers, glitch art, digital artifacts, pixelated, color, colorful"
)


def load_pipelines():
    """Load SDXL txt2img and img2img pipelines from local checkpoint."""
    from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline, AutoencoderKL

    print(f"Loading VAE from {os.path.basename(VAE_PATH)}...")
    vae = AutoencoderKL.from_single_file(VAE_PATH, torch_dtype=torch.float16)

    print(f"Loading txt2img pipeline from {os.path.basename(CHECKPOINT)}...")
    txt2img = StableDiffusionXLPipeline.from_single_file(
        CHECKPOINT, vae=vae, torch_dtype=torch.float16, use_safetensors=True,
    )
    txt2img.to("cuda")

    print("Creating img2img pipeline (shared components)...")
    img2img = StableDiffusionXLImg2ImgPipeline(
        vae=txt2img.vae,
        text_encoder=txt2img.text_encoder,
        text_encoder_2=txt2img.text_encoder_2,
        tokenizer=txt2img.tokenizer,
        tokenizer_2=txt2img.tokenizer_2,
        unet=txt2img.unet,
        scheduler=txt2img.scheduler,
    )
    img2img.to("cuda")

    return txt2img, img2img


def apply_bw_treatment(img, contrast=1.8, brightness=1.1):
    """Convert to high-contrast black and white."""
    gray = img.convert("L")
    gray = ImageEnhance.Contrast(gray).enhance(contrast)
    gray = ImageEnhance.Brightness(gray).enhance(brightness)
    gray = gray.filter(ImageFilter.SHARPEN)
    return gray.convert("RGB")


def upscale_for_print(img, target_w=2400, target_h=1600):
    """Upscale and crop to print-ready dimensions."""
    w, h = img.size
    scale = max(target_w / w, target_h / h)
    img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    new_w, new_h = img.size
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def save_option(img, idx, desc, params, all_options):
    """Apply B&W treatment, upscale, save, and record metadata."""
    contrast = params.get("contrast", 1.8)
    brightness = params.get("brightness", 1.1)

    processed = apply_bw_treatment(img, contrast=contrast, brightness=brightness)
    processed = upscale_for_print(processed)

    filename = f"spread_033_v2_opt_{idx}.jpg"
    filepath = OUTPUT_DIR / filename
    processed.save(filepath, "JPEG", quality=95)
    size_kb = filepath.stat().st_size / 1024

    print(f"  [{idx}] {filename} ({size_kb:.0f}KB) — {desc}")

    all_options.append({
        "file": filename,
        "source": "generated_local",
        "model": "juggernautXL_ragnarokBy (SDXL)",
        "prompt": params["prompt"],
        "license": "open_model",
        "size_kb": round(size_kb, 1),
        "_generation_params": {
            "checkpoint": "juggernautXL_ragnarokBy.safetensors",
            "vae": "sdxl_vae.safetensors",
            "technique": params["technique"],
            "steps": params["steps"],
            "cfg_scale": params["cfg"],
            "seed": params["seed"],
            "strength": params.get("strength"),
            "bw_contrast": contrast,
            "resolution": f"{WIDTH}x{HEIGHT} -> 2400x1600",
        },
    })
    return idx + 1


def main():
    print("=" * 60)
    print("Spread 033 Image Generation — AI-Distorted Faces (v2)")
    print("=" * 60)
    print()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    txt2img, img2img = load_pipelines()
    print("Pipelines loaded.\n")

    all_options = []
    idx = 0

    # ----------------------------------------------------------------
    # TECHNIQUE 1: Low step-count generation
    # The face doesn't fully converge, creating uncanny half-formed features
    # ----------------------------------------------------------------
    print("--- Technique 1: Low Step-Count Generation ---")
    low_step_configs = [
        # (prompt_idx, steps, cfg, seed, contrast, description)
        (0, 6, 7.0, 42, 2.0, "close-up, 6 steps — very abstract"),
        (0, 10, 7.0, 42, 1.8, "close-up, 10 steps — half-formed"),
        (0, 14, 7.0, 42, 1.8, "close-up, 14 steps — emerging"),
        (1, 8, 7.0, 49, 2.0, "shadow face, 8 steps — abstract"),
        (1, 12, 7.0, 49, 1.8, "shadow face, 12 steps — half-formed"),
        (2, 8, 7.0, 55, 2.0, "curved glass, 8 steps — abstract"),
        (2, 12, 7.0, 55, 1.8, "curved glass, 12 steps — half-formed"),
        (3, 10, 7.0, 63, 2.0, "ethereal, 10 steps — abstract"),
    ]

    for prompt_idx, steps, cfg, seed, contrast, desc in low_step_configs:
        prompt = FACE_PROMPTS[prompt_idx]
        gen = torch.Generator("cuda").manual_seed(seed)

        print(f"\n  Generating: {desc}...")
        result = txt2img(
            prompt=prompt,
            negative_prompt=NEGATIVE_PROMPT,
            width=WIDTH, height=HEIGHT,
            num_inference_steps=steps,
            guidance_scale=cfg,
            generator=gen,
        )

        idx = save_option(result.images[0], idx, desc, {
            "prompt": prompt, "technique": "low_step_count",
            "steps": steps, "cfg": cfg, "seed": seed,
            "contrast": contrast, "brightness": 1.0,
        }, all_options)

    # ----------------------------------------------------------------
    # TECHNIQUE 2: img2img re-noising
    # Generate a clean face, then add noise and partially re-denoise
    # with different prompt or high strength -> interpolation artifacts
    # ----------------------------------------------------------------
    print("\n\n--- Technique 2: img2img Re-Noising ---")

    # First generate 2 clean reference faces
    ref_faces = []
    for pi, seed in [(0, 42), (2, 55)]:
        gen = torch.Generator("cuda").manual_seed(seed)
        print(f"\n  Generating reference face (prompt {pi}, seed {seed})...")
        result = txt2img(
            prompt=FACE_PROMPTS[pi],
            negative_prompt=NEGATIVE_PROMPT,
            width=WIDTH, height=HEIGHT,
            num_inference_steps=50,
            guidance_scale=7.0,
            generator=gen,
        )
        ref_faces.append(result.images[0])

    # Now re-noise them with different strengths and prompts
    renoise_configs = [
        # (ref_idx, strength, prompt_idx, cfg, seed, contrast, desc)
        (0, 0.75, 3, 8.0, 100, 1.8, "portrait -> ethereal, strength 0.75"),
        (0, 0.85, 3, 8.0, 101, 2.0, "portrait -> ethereal, strength 0.85"),
        (0, 0.65, 2, 7.0, 102, 1.8, "portrait -> curved glass, strength 0.65"),
        (1, 0.75, 3, 8.0, 103, 1.8, "curved -> ethereal, strength 0.75"),
        (1, 0.85, 0, 8.0, 104, 2.0, "curved -> portrait, strength 0.85"),
        (0, 0.90, 1, 9.0, 105, 2.2, "portrait -> shadow, strength 0.90 (high distortion)"),
    ]

    for ref_idx, strength, prompt_idx, cfg, seed, contrast, desc in renoise_configs:
        gen = torch.Generator("cuda").manual_seed(seed)
        prompt = FACE_PROMPTS[prompt_idx]

        print(f"\n  Re-noising: {desc}...")
        result = img2img(
            prompt=prompt,
            negative_prompt=NEGATIVE_PROMPT,
            image=ref_faces[ref_idx],
            strength=strength,
            num_inference_steps=50,
            guidance_scale=cfg,
            generator=gen,
        )

        idx = save_option(result.images[0], idx, f"img2img: {desc}", {
            "prompt": prompt, "technique": "img2img_renoise",
            "steps": 50, "cfg": cfg, "seed": seed,
            "strength": strength, "contrast": contrast, "brightness": 1.0,
        }, all_options)

    # ----------------------------------------------------------------
    # TECHNIQUE 3: Extreme CFG (guidance scale)
    # Very high CFG creates over-saturated, almost hallucinatory faces
    # ----------------------------------------------------------------
    print("\n\n--- Technique 3: Extreme CFG ---")
    extreme_cfgs = [
        (0, 12, 20.0, 42, 2.0, "close-up, CFG 20 — over-guided"),
        (3, 12, 25.0, 63, 2.2, "ethereal, CFG 25 — hallucinatory"),
    ]

    for prompt_idx, steps, cfg, seed, contrast, desc in extreme_cfgs:
        prompt = FACE_PROMPTS[prompt_idx]
        gen = torch.Generator("cuda").manual_seed(seed)

        print(f"\n  Generating: {desc}...")
        result = txt2img(
            prompt=prompt,
            negative_prompt=NEGATIVE_PROMPT,
            width=WIDTH, height=HEIGHT,
            num_inference_steps=steps,
            guidance_scale=cfg,
            generator=gen,
        )

        idx = save_option(result.images[0], idx, desc, {
            "prompt": prompt, "technique": "extreme_cfg",
            "steps": steps, "cfg": cfg, "seed": seed,
            "contrast": contrast, "brightness": 0.95,
        }, all_options)

    # ----------------------------------------------------------------
    # Also save the 2 clean reference faces as options (useful as
    # comparison and they may work well with different treatments)
    # ----------------------------------------------------------------
    print("\n\n--- Clean References (high-contrast B&W) ---")
    for i, (face, pi) in enumerate(zip(ref_faces, [0, 2])):
        desc = f"clean reference, prompt {pi}"
        idx = save_option(face, idx, desc, {
            "prompt": FACE_PROMPTS[pi], "technique": "full_generation",
            "steps": 50, "cfg": 7.0, "seed": [42, 55][i],
            "contrast": 1.8, "brightness": 1.1,
        }, all_options)

    # Write manifest
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_options": len(all_options),
        "techniques": ["low_step_count", "img2img_renoise", "extreme_cfg", "full_generation"],
        "options": all_options,
    }
    manifest_path = OUTPUT_DIR.parent / "data" / "spread_033_generated_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Generated {len(all_options)} images for spread_033")
    print(f"Manifest: {manifest_path}")
    print(f"{'=' * 60}")

    return all_options


if __name__ == "__main__":
    main()
