"""
LingoGrade Sticker Framer — 5 campaigns × 3 colors = 15 SKUs
Outputs print (960×1200) and web (640×800) versions = 30 total assets.

Frame spec:
  - Border: 8px @ 320px → 24px @ 960px print, 16px @ 640px web
  - Rounded corners: 18px @ 320px → 54px @ 960px, 36px @ 640px
  - Inner padding: 6px @ 320px → 18px @ 960px, 12px @ 640px
  - Outer bleed: 3px @ 320px → 9px @ 960px, 6px @ 640px
  - Colors: Blue #2563AB, Gold #C5960C, Grey #3A3A3A
"""

from PIL import Image, ImageDraw
from pathlib import Path

# === CONFIG ===

COLORS = {
    "blue": (0x25, 0x63, 0xAB),
    "gold": (0xC5, 0x96, 0x0C),
    "grey": (0x3A, 0x3A, 0x3A),
}

SIZES = {
    "print": {"canvas": (960, 1200), "border": 24, "radius": 54, "padding": 18, "bleed": 9},
    "web":   {"canvas": (640, 800),  "border": 16, "radius": 36, "padding": 12, "bleed": 6},
}

STICKERS_DIR = Path(__file__).parent
MASCOT_DIR = STICKERS_DIR.parent / "mascot"
OUTPUT_DIR = STICKERS_DIR / "framed"

# 5 campaigns → source images
CAMPAIGNS = {
    "marco":      MASCOT_DIR / "sliced-final" / "gpt-marco-coffee-thumbsup.png",
    "mila":       MASCOT_DIR / "sliced-images-png-backup" / "mila-card-party-branded.png",
    "duo":        MASCOT_DIR / "marco-mila-celebrating.png",
    "kids_marco": STICKERS_DIR / "sticker_kids_marco_backpack_v2.png",
    "kids_mila":  STICKERS_DIR / "sticker_kids_mila_wand.png",
}


def round_rect_mask(size, radius):
    """Create a rounded rectangle mask."""
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return mask


def fit_image(img, max_w, max_h):
    """Resize image to fit within max_w × max_h, preserving aspect ratio."""
    ratio = min(max_w / img.width, max_h / img.height)
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)
    return img.resize((new_w, new_h), Image.LANCZOS)


def create_framed_sticker(source_path, color_name, color_rgb, size_name, specs):
    """Create a single framed sticker variant."""
    canvas_w, canvas_h = specs["canvas"]
    border = specs["border"]
    radius = specs["radius"]
    padding = specs["padding"]
    bleed = specs["bleed"]

    # Load source
    src = Image.open(source_path).convert("RGBA")

    # Inner area for the image (inside border + padding)
    inner_x = border + padding
    inner_y = border + padding
    inner_w = canvas_w - 2 * inner_x
    inner_h = canvas_h - 2 * inner_y

    # Fit source image into inner area
    fitted = fit_image(src, inner_w, inner_h)

    # Create canvas with transparency
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # Draw the frame (outer rounded rect)
    outer_mask = round_rect_mask((canvas_w, canvas_h), radius)
    frame_layer = Image.new("RGBA", (canvas_w, canvas_h), color_rgb + (255,))
    canvas.paste(frame_layer, mask=outer_mask)

    # Cut out the inner area (transparent padding gap + image area)
    inner_rect_x = border
    inner_rect_y = border
    inner_rect_w = canvas_w - 2 * border
    inner_rect_h = canvas_h - 2 * border
    inner_radius = max(radius - border, 4)

    # Create inner cutout on a temp mask
    inner_mask = Image.new("L", (canvas_w, canvas_h), 0)
    inner_draw = ImageDraw.Draw(inner_mask)
    inner_draw.rounded_rectangle(
        [inner_rect_x, inner_rect_y,
         inner_rect_x + inner_rect_w - 1, inner_rect_y + inner_rect_h - 1],
        radius=inner_radius, fill=255
    )

    # White background inside the frame
    white_layer = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 255))
    canvas.paste(white_layer, mask=inner_mask)

    # Center the fitted image in the inner area
    paste_x = inner_x + (inner_w - fitted.width) // 2
    paste_y = inner_y + (inner_h - fitted.height) // 2
    canvas.paste(fitted, (paste_x, paste_y), fitted)

    # Apply overall rounded rect shape (clip everything outside)
    final_mask = round_rect_mask((canvas_w, canvas_h), radius)
    result = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    result.paste(canvas, mask=final_mask)

    return result


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    print_dir = OUTPUT_DIR / "print"
    web_dir = OUTPUT_DIR / "web"
    print_dir.mkdir(exist_ok=True)
    web_dir.mkdir(exist_ok=True)

    generated = 0

    for campaign, source_path in CAMPAIGNS.items():
        if not source_path.exists():
            print(f"  SKIP {campaign}: source not found at {source_path}")
            continue

        for color_name, color_rgb in COLORS.items():
            for size_name, specs in SIZES.items():
                out_dir = print_dir if size_name == "print" else web_dir
                filename = f"sticker_{campaign}_{color_name}_{specs['canvas'][0]}x{specs['canvas'][1]}.png"
                out_path = out_dir / filename

                result = create_framed_sticker(source_path, color_name, color_rgb, size_name, specs)
                result.save(out_path, "PNG", optimize=True)
                generated += 1
                print(f"  OK  {size_name}/{filename}")

    print(f"\nDone: {generated} assets generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
