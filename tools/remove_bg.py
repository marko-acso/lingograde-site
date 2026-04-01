"""
remove_bg.py - Remove backgrounds from LingoGrade mascot images using remove.bg API,
then composite onto a soft radial white-to-light-blue backing.

Usage:
    python tools/remove_bg.py

Requires:
    pip install requests Pillow python-dotenv numpy

API key: set LINGOGRADE_REMOVE_BG_API_KEY in environment or in .env at project root.
Cost: 0.25 credits per image (regular size via API).
"""

import os
import sys
import math
from pathlib import Path

import requests
import numpy as np
from PIL import Image
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MASCOT_DIR = PROJECT_ROOT / "assets" / "mascot"

# Images to process (background removal + backing)
TARGET_IMAGES = [
    "marco-hero.png",
    "marco-sleeping.png",
    "marco-logo-v6.1.png",
]

# Amazon plush photos - never touch
EXCLUDED_IMAGES = {"Marco.png", "Marco2.png", "Marco3.png", "Marco4.png"}

# Backing gradient colours
CENTER_COLOR = (255, 255, 255)       # white
EDGE_COLOR   = (232, 240, 254)       # #E8F0FE  light blue

REMOVEBG_API_URL = "https://api.remove.bg/v1.0/removebg"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_api_key() -> str:
    """Load API key from env or .env file."""
    load_dotenv(PROJECT_ROOT / ".env")
    key = os.getenv("LINGOGRADE_REMOVE_BG_API_KEY")
    if not key:
        print("ERROR: LINGOGRADE_REMOVE_BG_API_KEY not found.")
        print("Set it as an environment variable or add it to .env at the project root.")
        sys.exit(1)
    return key


def remove_background(image_path: Path, api_key: str) -> bytes:
    """
    Call remove.bg API and return the PNG bytes of the cutout.
    Uses 'regular' size which costs 0.25 credits per image.
    """
    with open(image_path, "rb") as f:
        response = requests.post(
            REMOVEBG_API_URL,
            files={"image_file": f},
            data={
                "size": "regular",       # 0.25 credits
                "type": "auto",
                "format": "png",
                "channels": "rgba",
            },
            headers={"X-Api-Key": api_key},
            timeout=120,
        )

    if response.status_code != 200:
        print(f"  API error {response.status_code}: {response.text}")
        return None

    # Print credit info from headers
    credits_charged = response.headers.get("X-Credits-Charged", "?")
    credits_remaining = response.headers.get("X-Credits-Remaining", "?")
    print(f"  Credits charged: {credits_charged} | Remaining: {credits_remaining}")

    return response.content


def create_radial_gradient(width: int, height: int) -> Image.Image:
    """
    Create a radial gradient from white (center) to light blue (edges).
    Returns an RGBA image so it can be composited under the cutout.
    """
    cx, cy = width / 2.0, height / 2.0
    # Maximum distance from center to any corner
    max_dist = math.sqrt(cx * cx + cy * cy)

    # Build gradient using numpy for speed
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    distances = np.sqrt((x_coords - cx) ** 2 + (y_coords - cy) ** 2)
    # Normalise to 0..1
    t = np.clip(distances / max_dist, 0.0, 1.0)

    # Interpolate each channel
    r = (CENTER_COLOR[0] * (1 - t) + EDGE_COLOR[0] * t).astype(np.uint8)
    g = (CENTER_COLOR[1] * (1 - t) + EDGE_COLOR[1] * t).astype(np.uint8)
    b = (CENTER_COLOR[2] * (1 - t) + EDGE_COLOR[2] * t).astype(np.uint8)
    a = np.full((height, width), 255, dtype=np.uint8)

    rgba = np.stack([r, g, b, a], axis=-1)
    return Image.fromarray(rgba, "RGBA")


def composite_on_backing(cutout: Image.Image) -> Image.Image:
    """
    Place the RGBA cutout on top of the radial gradient backing.
    Canvas matches original image dimensions.
    """
    width, height = cutout.size
    backing = create_radial_gradient(width, height)
    # Paste cutout onto backing using cutout's own alpha as mask
    backing.paste(cutout, (0, 0), cutout)
    return backing


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    api_key = get_api_key()

    # Safety check: make sure we never touch excluded files
    for name in TARGET_IMAGES:
        if name in EXCLUDED_IMAGES:
            print(f"SAFETY: '{name}' is in the exclusion list. Aborting.")
            sys.exit(1)

    total_credits = 0.0

    for filename in TARGET_IMAGES:
        image_path = MASCOT_DIR / filename

        if not image_path.exists():
            print(f"SKIP: {filename} not found at {image_path}")
            continue

        print(f"\nProcessing: {filename}")
        file_size_kb = image_path.stat().st_size / 1024
        print(f"  Original size: {file_size_kb:.0f} KB")

        # Step 1: Remove background via API
        print("  Calling remove.bg API (regular size = 0.25 credits)...")
        cutout_bytes = remove_background(image_path, api_key)
        if cutout_bytes is None:
            print(f"  FAILED: Skipping {filename}")
            continue

        total_credits += 0.25

        # Step 2: Load cutout as RGBA
        from io import BytesIO
        cutout = Image.open(BytesIO(cutout_bytes)).convert("RGBA")
        print(f"  Cutout dimensions: {cutout.size[0]}x{cutout.size[1]}")

        # Step 3: Composite onto radial gradient backing
        print("  Compositing onto white-to-light-blue backing...")
        result = composite_on_backing(cutout)

        # Step 4: Save back to original path (overwrite)
        result.save(image_path, "PNG", optimize=True)
        new_size_kb = image_path.stat().st_size / 1024
        print(f"  Saved: {image_path}")
        print(f"  New size: {new_size_kb:.0f} KB")

    print(f"\n--- Done ---")
    print(f"Images processed: {len(TARGET_IMAGES)}")
    print(f"Estimated total credits used: {total_credits}")


if __name__ == "__main__":
    main()
