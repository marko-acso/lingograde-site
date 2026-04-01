# Mascot Images — Next Session

## Status

All mascot slicing work is **complete**. No remaining tasks.

## Key rules (reference)
- 2-step: crop first, cover leftovers with white second
- SAFETY margin >= 30px, WHITE_THRESH = 225
- 50px safe space padding on all sides
- sliced-images = finished crops only, no raw GPT generations
- Originals kept in `sliced-images-png-backup/`
- Full history: `assets/mascot/MASCOT_SLICING_STATUS.md`

## Notes
- 35 root `.png` files in `assets/mascot/` kept intentionally — 6 OG/Twitter/JSON-LD references still point to absolute PNG URLs. Revisit when crawler support for WebP improves.
