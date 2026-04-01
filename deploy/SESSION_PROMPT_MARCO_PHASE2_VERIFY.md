# Marco Image Phase 2 — Verify Report Rendering + Phase 3 Prompt

## Prior
- Phase 1: WISE audit complete (`MARCO_IMAGE_WISE_AUDIT_PHASE1.md`)
- Phase 2 code changes complete (this session verifies them):
  - 7 image swaps in `lingua-pipeline/assets/` (WISE-audited versions)
  - 1 new asset: `marco-face-grad.png`
  - 3 new constants in `shared.py`: `MARCO_FACE_GRAD`, `MARCO_TEA`, `MARCO_FACE_WINK`
  - Removed duplicate `MARCO_WAVING` + `MARCO_COFFEE_CUP` definitions in `shared.py`
  - 5 new floating image placements in chunks 02, 04, 06, 07, 09

## Goal

1. Generate a test report and verify all image placements render correctly
2. Fix any layout issues (table breaks, overlap, sizing)
3. Update Phase 1 audit doc with final status
4. Create Phase 3 session prompt for website placement

## Step 1 — Test Report Generation

Run the test harness to generate a full report:
```bash
cd C:/Users/RogZephyrus/lingua-pipeline
python -m chunks.test_chunk all
```

If that fails, try with a sample JSON:
```bash
python lingograde_docx.py samples/sample_de_en.json
```

Open the output DOCX and verify each placement:

### Verification Checklist

- [ ] **chunk_01 (header):** Logo still renders correctly after swap
- [ ] **chunk_02 (title):** MARCO_FACE_GRAD appears after score cards, right side, ~1.6cm, no table break
- [ ] **chunk_03 (perception):** MARCO_FACE_PARTY still renders (now uses swapped face-party-v2.png)
- [ ] **chunk_04 (problems):** MARCO_TEA appears after problems banner, calming presence, no overlap with problem rows
- [ ] **chunk_06 (solutions):** MARCO_FACE_WINK appears after solutions banner, playful, no overlap
- [ ] **chunk_07 (engine):** MARCO_READING appears after engine banner, studious pose, no overlap
- [ ] **chunk_08 (homework):** Booking icon still renders correctly
- [ ] **chunk_09 (plan):** MARCO_COFFEE_CUP appears after weekly plan banner, composed, no overlap with week rows
- [ ] **chunk_10 (footer):** All tip box images still render (thumbsup, waving, coffee — note: thumbsup and coffee now use swapped versions)
- [ ] **QR codes:** marco-face-wink embedded in QR still works (swapped to v2)

### Common Issues to Watch For

1. **Image too large** — if it overlaps content, reduce `width_cm` (try 1.3 or 1.2)
2. **Image clips into next section** — adjust `y_offset_cm` (try -0.5 or 0.0)
3. **postprocess_anchors.py conflicts** — the postprocessor matches images by width (EMU). New placements use different widths than existing rules, so they should NOT be matched. Verify by checking `ANCHOR_RULES` cx_cm ranges don't overlap with 1.5/1.6cm.
4. **Swapped images different dimensions** — PIL auto-calculates aspect ratio, but verify no distortion

### Anchor Rule Conflict Check

Current `postprocess_anchors.py` rules match these width ranges:
- Header logo: 2.80-2.96 cm
- Homework tip owl: 1.70-1.78 cm
- Homework CTA owl: 1.90-2.00 cm
- Booking CTA owl: 2.28-2.36 cm
- Tip section owl: 1.74-1.90 cm

New placements use 1.5 cm and 1.6 cm — **1.6 cm is OUTSIDE all ranges** (good), but **check if 1.5 cm accidentally falls into any range** (it shouldn't, closest is 1.70-1.78).

## Step 2 — Fix Any Issues

If any placement breaks layout:
1. Adjust `width_cm`, `x_offset_cm`, `y_offset_cm` in the specific chunk file
2. Re-generate and re-verify
3. Document final parameters

## Step 3 — Update Phase 1 Audit

Update `MARCO_IMAGE_WISE_AUDIT_PHASE1.md`:
- Mark swaps as complete
- Mark 5 new placements as complete
- Note any parameter adjustments made during verification

## Step 4 — Create Phase 3 Session Prompt

Create `SESSION_PROMPT_MARCO_PHASE3.md` with this structure:

```markdown
# Marco Image Placement — Phase 3: Website

## Prior
- Phase 1: WISE audit complete (MARCO_IMAGE_WISE_AUDIT_PHASE1.md)
- Phase 2: Report placement complete + verified

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
3. Add new placements using Astro <Image> or <Picture> components
4. Verify responsive display at mobile/tablet/desktop
5. Present for approval (321 rule)

## Also handle: gpt- file cleanup
Move 116 gpt-prefixed files out of sliced-images/:
```bash
mkdir -p lingograde-site/assets/mascot/raw-generations
mv lingograde-site/assets/mascot/sliced-images/gpt-* lingograde-site/assets/mascot/raw-generations/
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

## Rules: See CLAUDE.md + memory. iida, 321, no commit without approval.
```

Adapt based on any findings from Phase 2 verification — add image sizing lessons, component patterns, or layout constraints discovered during DOCX testing.

## Key Paths

- Pipeline: `C:/Users/RogZephyrus/lingua-pipeline/`
- Chunks: `C:/Users/RogZephyrus/lingua-pipeline/chunks/`
- Assets: `C:/Users/RogZephyrus/lingua-pipeline/assets/`
- Test: `python -m chunks.test_chunk all`
- Postprocess: `C:/Users/RogZephyrus/lingua-pipeline/chunks/postprocess_anchors.py`

## Rules: See CLAUDE.md + memory. iida, 321, no commit without approval.
