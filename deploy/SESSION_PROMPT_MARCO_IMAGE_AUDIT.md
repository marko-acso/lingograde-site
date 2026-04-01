# Marco Image WISE Audit + Placement

## Prior: WISE Polish Sessions 1-3 complete. See git log.

## Goal

Audit all 98 images in `C:/Users/RogZephyrus/lingograde-site/assets/mascot/sliced-images/` through the 11 WISE lenses, then apply placement decisions to (A) the assessment report and (B) the website.

## Phase 1 — WISE Audit (this session)

Open and analyze every image. For each, score:

- **Berne:** Free Child / Adult / Adapted Child / Critical Parent — which ego state does it evoke?
- **Ekman:** What emotion does the face/body convey? Congruent with intended use?
- **Lozanov:** Does it de-suggest anxiety? Does it feel safe?
- **Krashen:** Would it lower or raise the affective filter?
- **Greene:** Does it project authority without intimidation (Law 4)?
- **Brand:** Is it on-brand (navy/blue palette, consistent style, no uncanny valley)?

Output a table: `filename | ego state | emotion | safe? | filter effect | use recommendation`

Categorize each image into:
- **REPORT** — suitable for assessment PDF (which chunk?)
- **SITE** — suitable for website (which page/section?)
- **BOTH** — works in both contexts
- **RETIRE** — off-brand, wrong emotion, duplicate of a better version

Flag any `gpt-` prefixed files that shouldn't be in sliced-images (per sliced-folder rule: finished crops only).

## Phase 2 — Report Placement (next session)

Map winning images to report chunks. Current image usage:
- `chunk_03_perception.py` — MARCO_FACE_PARTY (strengths section)
- Other chunks — check for existing image refs

Key constraint: DOCX images must be small, float-compatible, and not break table layouts.

## Phase 3 — Website Placement (next session)

Map winning images to site pages. Check current usage:
- `C:/Users/RogZephyrus/lingograde-site/` — Astro components, shop pages, landing pages

## Key Paths

- Images: `C:/Users/RogZephyrus/lingograde-site/assets/mascot/sliced-images/`
- Report chunks: `C:/Users/RogZephyrus/lingua-pipeline/chunks/chunk_01_header.py` through `chunk_10_footer.py`
- Website: `C:/Users/RogZephyrus/lingograde-site/src/`

## Verification

- [ ] All 98 images reviewed and categorized
- [ ] gpt- prefix files flagged
- [ ] Placement map for report (chunk + position)
- [ ] Placement map for site (page + section)

## Rules: See CLAUDE.md + memory. iida, 321, no commit without approval.
