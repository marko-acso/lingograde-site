# Mascot Image Slicing — Status Report

## Current State (2026-04-01)

### `assets/mascot/sliced-images/` — ~164 files
All individually cropped with 50px safe space, white backgrounds, named correctly.

**Naming:**
- `marco-{pose}.png` — Marco (graduation cap + glasses) from root originals
- `gpt-marco-{pose}.png` — Marco from GPT grids
- `gpt-mila-{pose}.png` — Mila (purple bow) from GPT grids
- `gpt-marco-mila-{scene}.png` — Both characters together (ONLY if both present)
- `marco-mila-outfit-{type}.png` — 6 outfit pair variants
- `marco-face-{expr}.png` / `marco-logo-{variant}.png` — Faces / branding

### `assets/mascot/GPT Images/` — 24 PNG source files + 2 prompt docs
All original GPT grid sheets archived for future re-processing.

### `assets/mascot/` (root) — 33 files
31 single-image PNGs (originals) + 2 GIFs (marco-tip.gif, marco-Tip-v6.1.gif)

## Processing Method (Phase 4)
1. **Generous crop** from source grid (overflow beyond cell boundaries)
2. **Connected-component white-out** (scipy ndimage) — find main character blob, paint disconnected fragments white
3. **Auto-trim** with 30px safety margin (WHITE_THRESH=225)
4. **50px padding** added to all final images

## Known Issues
- `gpt-mila-telescope`, `gpt-mila-ballet` — baked-in illustrated backgrounds from GPT (need regeneration with white bg)
- Some `gpt-mila-*` adventure scenes (ninja, chef, balloon, multilingual) have partial scene backgrounds
- `marco-alarm-v2` — bust shot only (source grid cell was close-up, full-body version is `marco-alarm-sweat.png`)

## What's Left
1. **Near-duplicate review** — ~164 images likely reducible to ~100-120 unique usable assets
2. **Resolution standardization** — sizes range from ~250px to ~1000px, normalize for web
3. **WebP conversion** — for smaller file sizes
4. **Background consistency** — some have white RGB, some have transparency RGBA
5. **Regenerate problem images** — telescope, ballet need white-bg GPT regeneration
6. **GIF handling** — 2 animated GIFs skipped
7. **Consolidate naming** — some poses exist as both `marco-` and `gpt-marco-` variants
