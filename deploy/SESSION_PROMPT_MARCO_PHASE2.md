# Marco Image Placement — Phase 2: Assessment Report

## Prior: Phase 1 WISE audit complete. See `MARCO_IMAGE_WISE_AUDIT_PHASE1.md`.

## Goal

Map the winning images from the WISE audit to specific report chunks, implement the placements, and verify they render correctly in DOCX output.

## Context

The assessment report is built by `lingua-pipeline/chunks/chunk_01_header.py` through `chunk_10_footer.py`, assembled into DOCX. Images must be small, float-compatible, and must NOT break table layouts (see feedback: no-float rule — images should be anchored, not floating if they risk table disruption).

### Current image usage in report chunks:
- `chunk_03_perception.py` — uses `MARCO_FACE_PARTY` (strengths section)
- `postprocess_anchors.py` — references "Homework tip owl", "Homework CTA owl", "Booking CTA owl (large)", "Tip section owl (thumbsup/waving/coffee)"
- Check all other chunks for existing image references before adding new ones

### Image source path:
```
C:/Users/RogZephyrus/lingograde-site/assets/mascot/sliced-images/
```

## Placement Map (from Phase 1 audit)

Apply these placements — verify each one renders in DOCX before moving to the next:

| Chunk | Section | Image | WISE Rationale |
|-------|---------|-------|----------------|
| chunk_01_header.py | Report cover/header | marco-card-reading-branded.png | A/FC, strong authority + warmth, full brand |
| chunk_03_perception.py | Strengths celebration | marco-face-party-v2.png | FC, already in use — KEEP |
| chunk_08_homework.py | Homework tips | marco-thumbsup-wink.png | FC, approval signal, lowers filter |
| chunk_08_homework.py | Homework CTA | marco-chatbot-speech-bubble.png | A/FC, invites conversation |
| Tip sections (any chunk) | Encouragement tips | marco-tea-eyes-closed.png | FC/NC, calm, de-suggests anxiety |
| Tip sections (any chunk) | "Did you know" | marco-face-wink-v2.png | FC, playful aside |
| Reading/comprehension sections | Content reference | marco-reading-book.png | A, studious, on-topic |
| chunk_10_footer.py | Booking CTA | marco-headset-standing.png | A, headset = "ready for session" |

## Steps

1. **Read** each chunk file to understand current image integration patterns
2. **Check** `postprocess_anchors.py` for the image constant definitions (MARCO_FACE_PARTY, etc.)
3. **Map** new images to the same constant/path pattern
4. **Implement** placements one chunk at a time
5. **Verify** each placement doesn't break table layouts
6. Do NOT commit — present changes for approval (321 rule)

## Key Constraints

- DOCX images must be anchored, not floating (no-float rule)
- Keep images small (max ~1.5 inches wide in report context)
- Circle-crop faces work best in narrow columns
- Full-body images only in header/footer where space allows
- Test with a sample report generation if possible

## Quality Issues to Fix During This Phase

1. **marco-mugprint-wink.png** — crop artifact (feet at top). Re-crop if this image is selected for report use.
2. **marco-face-serious-circle.png** — mislabeled (it's a party face). Rename to `marco-face-party-circle-v2.png` or retire.

## Verification

- [ ] All chunk files read and understood
- [ ] Image constants defined in shared module
- [ ] Each placement implemented and tested
- [ ] No table layout breakage
- [ ] Changes presented for approval (not committed)

## End-of-Session Task: Generate Phase 3 Prompt

**Before closing this session, create `SESSION_PROMPT_MARCO_PHASE3.md`** with the following structure:

```markdown
# Marco Image Placement — Phase 3: Website

## Prior
- Phase 1: WISE audit complete (MARCO_IMAGE_WISE_AUDIT_PHASE1.md)
- Phase 2: Report placement complete (this session)

## Goal
Map winning images to website pages in lingograde-site (Astro).

## Placement Map (from Phase 1 audit)
[Copy the SITE category placements from Phase 1 audit]

## Steps
1. Grep lingograde-site/src/ for existing mascot/image references
2. Identify all pages that currently use or should use Marco/Mila images
3. Map images to components, checking responsive sizing
4. Implement using Astro <Image> or <Picture> components
5. Verify responsive display at mobile/tablet/desktop
6. Present for approval (321 rule)

## Also handle:
- gpt- file cleanup (move 116 files out of sliced-images/)
- Retire marco-face-serious-circle.png
- Deduplicate coffee variants (keep cozy + saucer, retire hug + morning)
- Deduplicate sleeping variants (keep v2, retire v1)
- Deduplicate private outfit variants (keep stylish, retire casual)
```

Adapt the Phase 3 prompt based on what you learned during Phase 2 implementation — add any image sizing discoveries, path patterns, or component conventions you encountered.

## Rules: See CLAUDE.md + memory. iida, 321, no commit without approval.
