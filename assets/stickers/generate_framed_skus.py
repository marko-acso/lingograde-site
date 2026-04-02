"""
LingoGrade Sticker Frame Generator
Produces 15 SKUs: 5 campaigns × 3 frame colors (Blue/Gold/Grey)
Output: 960×1200 print + 640×800 web versions
"""

from PIL import Image, ImageDraw
import os

# Frame spec from memory
COLORS = {
    "blue": "#2563AB",
    "gold": "#C5960C",
    "grey": "#3A3A3A",
}

PRINT_SIZE = (960, 1200)
WEB_SIZE = (640, 800)

# At 960px width: border 24px, inner padding 18px, corner radius 48px, bleed 8px
BORDER_PX = 24
INNER_PAD = 18
CORNER_RADIUS = 48
BLEED = 8

STICKER_DIR = os.path.dirname(os.path.abspath(__file__))
MASCOT_DIR = os.path.join(os.path.dirname(STICKER_DIR), "mascot", "sliced-final")

# 5 campaigns × 3 colors = 15 SKUs
# One hero image per campaign, sourced from sliced-final or stickers dir
CAMPAIGNS = [
    ("marco-hero-standing.png", "marco_hero"),           # Marco solo
    ("gpt-mila-wave.png", "mila_wave"),                  # Mila solo
    ("marco-mila-outfit-corporate.png", "corporate_duo"),# Corporate duo
    ("marco-mila-celebrating-highfive.png", "playful_duo"),# Playful duo
    ("sticker_kids_marco_abc.png", "kids_marco_abc"),     # Kids
]
OUT_PRINT = os.path.join(STICKER_DIR, "framed_print")
OUT_WEB = os.path.join(STICKER_DIR, "framed_web")

os.makedirs(OUT_PRINT, exist_ok=True)
os.makedirs(OUT_WEB, exist_ok=True)


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rounded_rect_mask(size, radius):
    """Create a rounded rectangle mask."""
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return mask


def create_framed_sticker(base_path, color_name, color_hex, target_size):
    """
    Create a framed sticker:
    1. White background with bleed area
    2. Colored rounded-rectangle frame (border)
    3. White inner area with padding
    4. Sticker art centered inside
    """
    w, h = target_size
    scale = w / PRINT_SIZE[0]  # scale factors relative to print size
    border = int(BORDER_PX * scale)
    pad = int(INNER_PAD * scale)
    radius = int(CORNER_RADIUS * scale)
    bleed = int(BLEED * scale)

    color_rgb = hex_to_rgb(color_hex)

    # Create white canvas
    canvas = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    # Draw outer colored frame (rounded rect)
    outer_x0, outer_y0 = bleed, bleed
    outer_x1, outer_y1 = w - bleed - 1, h - bleed - 1
    draw.rounded_rectangle(
        [outer_x0, outer_y0, outer_x1, outer_y1],
        radius=radius,
        fill=color_rgb,
    )

    # Draw inner white area
    inner_x0 = outer_x0 + border
    inner_y0 = outer_y0 + border
    inner_x1 = outer_x1 - border
    inner_y1 = outer_y1 - border
    inner_radius = max(radius - border, 4)
    draw.rounded_rectangle(
        [inner_x0, inner_y0, inner_x1, inner_y1],
        radius=inner_radius,
        fill=(255, 255, 255),
    )

    # Load and resize sticker art to fit inner area with padding
    art_area_w = int(inner_x1 - inner_x0 - 2 * pad)
    art_area_h = int(inner_y1 - inner_y0 - 2 * pad)

    base = Image.open(base_path)
    if base.mode == "RGBA":
        # Composite onto white
        white_bg = Image.new("RGB", base.size, (255, 255, 255))
        white_bg.paste(base, mask=base.split()[3])
        base = white_bg
    elif base.mode != "RGB":
        base = base.convert("RGB")

    # Fit sticker into available area preserving aspect ratio
    base_ratio = base.width / base.height
    area_ratio = art_area_w / art_area_h

    if base_ratio > area_ratio:
        # Width-constrained
        new_w = art_area_w
        new_h = int(art_area_w / base_ratio)
    else:
        # Height-constrained
        new_h = art_area_h
        new_w = int(art_area_h * base_ratio)

    base_resized = base.resize((new_w, new_h), Image.LANCZOS)

    # Center in inner area
    paste_x = inner_x0 + pad + (art_area_w - new_w) // 2
    paste_y = inner_y0 + pad + (art_area_h - new_h) // 2
    canvas.paste(base_resized, (paste_x, paste_y))

    return canvas


def resolve_source(filename):
    """Find source image: check stickers dir first, then mascot/sliced-final."""
    sticker_path = os.path.join(STICKER_DIR, filename)
    if os.path.exists(sticker_path):
        return sticker_path
    mascot_path = os.path.join(MASCOT_DIR, filename)
    if os.path.exists(mascot_path):
        return mascot_path
    return None


def main():
    generated = []
    for filename, sku_prefix in CAMPAIGNS:
        base_path = resolve_source(filename)
        if not base_path:
            print(f"SKIP (not found): {filename}")
            continue

        for color_name, color_hex in COLORS.items():
            name = f"sku_{sku_prefix}_{color_name}"

            # Print version (960×1200)
            print_img = create_framed_sticker(base_path, color_name, color_hex, PRINT_SIZE)
            print_path = os.path.join(OUT_PRINT, f"{name}.png")
            print_img.save(print_path, "PNG", dpi=(300, 300))

            # Web version (640×800)
            web_img = create_framed_sticker(base_path, color_name, color_hex, WEB_SIZE)
            web_path = os.path.join(OUT_WEB, f"{name}.png")
            web_img.save(web_path, "PNG")

            generated.append(name)
            print(f"OK: {name}")

    print(f"\nGenerated {len(generated)} SKUs ({len(generated)//3} campaigns × 3 colors)")
    print(f"Print: {OUT_PRINT}")
    print(f"Web:   {OUT_WEB}")


if __name__ == "__main__":
    main()
