# WISE Polish Session 2 — Psycholinguistic & Tone Calibration

## Context

Cal.com migration, Marco rebrand, WISE audit, and bundle translations are **all complete**. This session handles the deeper psycholinguistic and tone work remaining from the WISE audit.

---

## Server State (verified 2026-04-01)

```
SSH: ssh -i ~/.ssh/id_ed25519_hetzner root@65.108.151.198
Cal.com: /opt/calcom (docker compose)
Nginx: /etc/nginx/sites-enabled/booking-lingograde
```

- **Self-hosted Cal.com:** All 9 event types live under `/marco/`
- **Old hosted Cal.com:** Event types deactivated, account kept (may need later)

---

## What Was Already Done (do NOT redo)

### Previous Sessions (migration, rebrand, audit)
- Cal.com migration: hosted → self-hosted, all URLs updated
- Marko → Marco rebrand: DB, all files, all protocols, all samples
- 20 WISE audit fixes applied (caps, colors, typography, spacing, formality, language)
- See `SESSION_PROMPT_WISE_POLISH.md` for full list

### This Round (Session 1 — 2026-04-01)
21. **pl CTA formality fix** — informal `czułbyś` → formal `wydałoby się Państwu` in chunk_10_footer.py
22. **tr CTA tense fix** — past `hissettirdi mi?` → conditional `gelir miydi?` in chunk_10_footer.py
23. **8 missing bundle translations added** — cs, hu, no, sv, fi, da, sq, hi across all 3 bundle dicts (BADGE, CONTENT, CTA) in chunk_10_footer.py
24. **Hosted Cal.com decision** — event types deactivated, account kept

---

## What Remains (this session's work)

### 1. Psycholinguistic Review of Emotional Weight
**Files:** Both `lg_translations.py` files

Key terms that carry different emotional weight across languages:
- "instabil" / "unstable" / "нестабильный" — clinical vs character judgment
- "Falsch/Richtig" (Wrong/Right) — some languages carry shame (Romanian "Greșit", Serbian "Pogrešno")
- Consider: "Common pattern" / "Refined version" instead of Wrong/Right

**WISE lenses:** Berne (avoid Critical Parent shame triggers), Lozanov (de-suggestion), Krashen (affective filter), Ekman (emotional leakage in word choice)

### 2. Test-Anxiety Calibration for Eastern European Markets
Eastern European/Russian students have 1.5-2x baseline test anxiety. The report tone is calibrated for Western markets.

Possible additions:
- Anxiety-reduction language: "This is completely typical for your level"
- Forgiveness valves: "Most days, aim for 5. Missed yesterday? Start fresh today."
- Lozanov state management: "Your brain learns best when calm and confident."

**Where:** Both lingograde_docx.py files, chunk_03_perception.py, chunk_08_homework.py, chunk_09_plan.py

**WISE lenses:** Krashen (affective filter), Lozanov (suggestopedia), Berne (Free Child activation), Csikszentmihalyi (flow channel)

### 3. Remaining Nice-to-Have WISE Improvements
From audit (saved in `~/WISE_AUDIT_FINDINGS.md`):
- Strengths section: Add subtle celebratory visual marker (Ekman/Kahneman)
- Weekly plan: Add progress indicators — "Week 1/8", "Week 2/8" (Csikszentmihalyi flow feedback)
- Homework: Add permission to adjust — "If this feels too hard/easy, let me know" (Krashen)
- Social proof: "Students who spend 15 min/day typically see B2 stability within 2 months" (Cialdini)
- Greene long-game: "This 8-week foundation opens doors to B2. Beyond that? C1." (Strategic patience)
- Reciprocity closing: "Your feedback helps strengthen these for future students" (Cialdini)

### 4. Translation Cache Regeneration
**Dir:** `lingua-pipeline/translation_cache/` (96 files)

Still contain "Marko" from pre-rename. Force-regenerate:
```bash
cd C:/Users/RogZephyrus/lingua-pipeline
python regenerate_samples.py
```

### 5. Monolithic Renderer Convergence
The chunks renderer (lingua-pipeline/chunks/) and monolithic renderer (lingograde_docx.py) have diverged on some styling. Long-term: deprecate monolithic. Short-term: keep in sync.

---

## Key File Locations

### Report Pipeline (primary — chunks)
- `C:/Users/RogZephyrus/lingua-pipeline/chunks/shared.py` — colors, fonts, formality, helpers
- `C:/Users/RogZephyrus/lingua-pipeline/chunks/chunk_01_header.py` through `chunk_10_footer.py`
- `C:/Users/RogZephyrus/lingua-pipeline/lg_translations.py` — ALL translations

### Report Pipeline (legacy — monolithic)
- `C:/Users/RogZephyrus/lingograde-site/pipeline/lingograde_docx.py`
- `C:/Users/RogZephyrus/lingua-pipeline/lingograde_docx.py`
- `C:/Users/RogZephyrus/lingograde-site/pipeline/lg_translations.py`

### Audit Reports (reference)
- `C:/Users/RogZephyrus/WISE_AUDIT_FINDINGS.md` — original WISE audit (26 findings)
- `C:/Users/RogZephyrus/WISE_COLOR_AUDIT_REPORT.md` — color audit
- `C:/Users/RogZephyrus/lingua-pipeline/TYPOGRAPHY_AUDIT_WISE.md` — typography audit
- `C:/Users/RogZephyrus/lingua-pipeline/SPACING_AUDIT_REPORT.md` — spacing audit

---

## User Preferences (from memory)

- Use **sonnet** model for agents, **haiku** for pure search/grep only
- **iida** — if in doubt, ask/advise (TOP PRIORITY)
- Never commit without explicit permission
- Terse output, no summaries unless asked
- **321 process** — audit → verify → deliver, one at a time
- All prices: EUR = USD = CHF = GBP same number, .95 ending
- "Marco" never "Marko" — brand rule
- Camp Level 5+ on all CTAs
- No emoticons in any response
