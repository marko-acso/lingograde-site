# Marco Image Placement — Phase 3: Website

## Prior
- Phase 1: WISE audit complete (`MARCO_IMAGE_WISE_AUDIT_PHASE1.md`) — 48 finished crops audited across 11 lenses
- Phase 2: Report placement complete + verified
  - Typst PDF pipeline (master_v16): 4 owl placements in banner tables (problems, solutions, engine, plan)
  - Approach: owl integrated as 3rd column in banner `table()` — NO floating overlays, NO `place()`, zero text overlap
  - DOCX pipeline: `add_floating_image()` in shared.py exists but broken in LibreOffice (wp:anchor rendering issues). Not production-ready. Typst is the active pipeline.
  - Title/score section: skipped (no banner to attach to, area too tight)
  - Lesson learned: `place()` in Typst overlays on top of text with no wrapping. Always integrate images into layout (table columns, grid cells).

## Goal
Map winning images to website pages in lingograde-site (Astro).

## Placement Map (from Phase 1 audit)

| Page/Section | Image | WISE Rationale |
|---|---|---|
| Landing hero | marco-logo-book-wave.png | Full branded, dynamic, FC/A |
| Horizontal banner | marco-logo-whiteboard.png | Wide format, brand text |
| Nav logo | marco-logo-reading-book.png | Horizontal, text beside mascot |
| Chatbot widget | marco-chatbot-speech-bubble.png | Speech bubble built in |
| Booking/lessons | marco-headset-standing.png | Headset = "ready for session" |
| Corporate B2B | marco-mila-outfit-corporate.png | Most professional pair |
| Kids section | marco-abc-blocks.png | Playful, age-appropriate |
| About/mission | marco-reading-branded-logo-v1.png | Duo reading, warm |
| 404/maintenance | marco-sleeping-branch-v2.png | Peaceful, "come back" |
| Favicon/avatar | marco-face-grad-v2.png | Clean circle, authoritative |
| Shop/merch | marco-mugprint-face-and-body.png | High-res circle face |

## Steps
1. Grep lingograde-site/src/ for existing mascot/owl/marco image references
2. Map current usage to replacement images from audit
3. Add new placements using Astro `<Image>` or `<Picture>` components
4. Verify responsive display at mobile/tablet/desktop
5. Present for approval (321 rule)

## gpt- file cleanup
Move 116 gpt-prefixed files out of sliced-images/:
```bash
mkdir -p C:/Users/RogZephyrus/lingograde-site/assets/mascot/raw-generations
mv C:/Users/RogZephyrus/lingograde-site/assets/mascot/sliced-images/gpt-* C:/Users/RogZephyrus/lingograde-site/assets/mascot/raw-generations/
```

## Deduplication (from Phase 1 audit)
- Coffee: keep coffee-cozy + coffee-saucer, retire coffee-hug + coffee-morning
- Sleeping: keep sleeping-branch-v2, retire sleeping-branch
- Private outfits: keep private-stylish, retire private-casual

## Quality fixes
- marco-mugprint-wink.png — crop artifact (feet at top), re-crop before use
- marco-face-serious-circle.png — mislabeled (party face), rename to marco-face-party-circle-v2.png

## Key Paths
- Images: C:/Users/RogZephyrus/lingograde-site/assets/mascot/sliced-images/
- Website src: C:/Users/RogZephyrus/lingograde-site/src/
- Components: check for existing Image/Picture component patterns

## Report pipeline reference (for consistency)
- Typst master: C:/Users/RogZephyrus/lingua-pipeline/typst/master_v16/
- Typst assets: C:/Users/RogZephyrus/lingua-pipeline/typst/assets/
- Compile: `C:/Users/RogZephyrus/typst.exe compile main.typ --root ../.. --input data=data.json output.pdf`
- Banner owl pattern: 3rd column in banner table, `columns: (1fr, 1fr, 1.4cm)`, image width 1.2cm

## Critical rules
- Icons must NEVER overlap text (feedback_no_icon_text_overlap.md)
- Tip amounts always 20/10/5 descending (feedback_tip_descending_order.md)
- sliced-images = finished crops ONLY, no gpt- raw generations
- See CLAUDE.md + memory. iida, 321, no commit without approval.
