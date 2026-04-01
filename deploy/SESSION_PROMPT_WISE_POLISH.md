# WISE Polish Session — Post-Migration, Post-Audit

## Context

The Cal.com migration (hosted → self-hosted) is **complete**. The Marko → Marco rebrand is **complete**. A deep WISE audit was done across all 11 lenses (icons, colors, typography, spacing, language prisms). Critical fixes were applied. This session handles the **remaining polish**.

---

## Server State (verified 2026-04-01)

```
SSH: ssh -i ~/.ssh/id_ed25519_hetzner root@65.108.151.198
Cal.com: /opt/calcom (docker compose)
Nginx: /etc/nginx/sites-enabled/booking-lingograde
Backup: /etc/nginx/booking-lingograde.bak
```

- **User:** id=1, username=`marco`, name=Marco, email=marco@lingograde.com
- **9 event types** (all return 200 under `/marco/`):
  - 4: quick-assessment | 5: full-assessment | 6: deepdive-assessment
  - 7-9: alumni variants | 10: schnell-check | 11: sprachstandsanalyse | 12: re-assessment
- **Nginx:** `/` → `/marco`, `/marko` → 301 → `/marco`, `/auth` → blocked
- **Old hosted Cal.com:** Still active — user needs to delete account at cal.com/marko.check

---

## What Was Already Done (do NOT redo)

### Cal.com Migration
- 6 new event types created (5 missing + re-assessment)
- All HTML/JS/PY files updated: `cal.com/marko.check/` → `booking.lingograde.com/marco/`
- Zero references to `cal.com/marko.check` in any production file

### Marko → Marco Rebrand
- Cal.com DB: username=marco, name=Marco, email=marco@lingograde.com
- All booking URLs: `/marko/` → `/marco/` (11 HTML files + pipeline)
- All protocol files (v5.2, v5.5, v5.6, v5.7, v6.0): "Marko" → "Marco"
- All sample JSONs (12 files): `"assessor": "Marco"`
- Both lingograde_docx.py files: all text, variable names, closing maps
- Both lg_translations.py files: CLOSING dict, MARCO_NATIVE dict
- lg_send.py, homework_check.py, config.py: email from, signatures
- l_e.py, main.py, video_tip_generator.py: prompts and signatures
- Only remaining "Marko" = character name in sample_croatian_a2.json example sentences (correct)

### WISE Audit Fixes Applied
1. **ALL_CAPS → Title Case** — All BANNERS entries in both lg_translations.py (27 languages × 11 banner types)
2. **"TOP PROBLEMS" → "Top {n} Structural Focus Areas"** — renamed across all languages
3. **Orange (#E67E22) → ACCENT blue** — "medium" stability labels in both renderers + chunk_02_title.py
4. **Red (#C0392B) → ACCENT blue** — problem names in chunk_04_problems.py + both lingograde_docx.py
5. **Score card labels** — 5.5pt → 7-8pt in chunk_02_title.py
6. **Detail strip labels** — 4.5pt → 7pt in chunk_02_title.py
7. **CEFR box margins** — 10-40 twips → 60 twips in chunk_02_title.py
8. **CTA margins** — 20 twips → 80 twips in chunk_10_footer.py
9. **Homework spacing** — Pt(2) → Pt(6) in chunk_08_homework.py
10. **Owl emoji removed from payment/tip section** in lingua-pipeline/lingograde_docx.py
11. **Owl bold styling** added to pedagogical uses
12. **Reassessment price** — €69 → €139.95 in lingograde-site/pipeline/lingograde_docx.py
13. **Reassessment period** — "3 Monate" → "8 Wochen" in both renderers + 12 sample JSONs
14. **"biggest structural weakness"** → "highest-impact focus area" (12 JSONs + both .py)
15. **"break down under pressure"** → "shift under pressure" (both .py)
16. **"unstable"** → "partially stable" / "with room to stabilize" (both .py)
17. **INK_MID** (#5A5A5A) added to shared.py for WCAG AA compliance
18. **ALERT_RED** naming clarification in shared.py
19. **Formality system** expanded: bg, sr, hr, pl, ro added to is_formal() in shared.py
20. **`.upper()` fallbacks** removed from chunk_03, chunk_07, chunk_02b, chunk_08

---

## What Remains (this session's work)

### 1. Missing Bundle CTA Translations (8 languages)
**File:** `lingua-pipeline/chunks/chunk_10_footer.py`

Currently present (17): de, en, fr, es, it, ru, zh, pt, uk, bg, sr, hr, pl, ro, ar, tr, nl

Missing (8): **cs, hu, no, sv, fi, da, sq, hi**

These need bundle offer CTA text in the same Voss/Camp style as the existing translations. Find the bundle CTA section and add translations for all 8 missing languages.

### 2. Translation Cache Regeneration
**Dir:** `lingua-pipeline/translation_cache/` (96 files)

These still contain "Marko" from pre-rename. They auto-regenerate on next pipeline run, but can be force-regenerated:
```bash
cd C:/Users/RogZephyrus/lingua-pipeline
python regenerate_samples.py
```

### 3. Psycholinguistic Review of Emotional Weight
**Files:** Both `lg_translations.py` files

Key terms that carry different emotional weight across languages:
- "instabil" / "unstable" / "нестабильный" — clinical vs character judgment
- "Falsch/Richtig" (Wrong/Right) — some languages carry shame (Romanian "Greșit", Serbian "Pogrešno")
- Consider: "Common pattern" / "Refined version" instead of Wrong/Right

### 4. Test-Anxiety Calibration for Eastern European Markets
Eastern European/Russian students have 1.5-2x baseline test anxiety. The report tone is calibrated for Western markets.

Possible additions:
- Add anxiety-reduction language: "This is completely typical for your level"
- Add forgiveness valves: "Most days, aim for 5. Missed yesterday? Start fresh today."
- Add Lozanov state management: "Your brain learns best when calm and confident."

**Where:** Both lingograde_docx.py files, chunk_03_perception.py, chunk_08_homework.py, chunk_09_plan.py

### 5. Remaining Nice-to-Have WISE Improvements
From audit (saved in `~/WISE_AUDIT_FINDINGS.md`):
- Strengths section: Add subtle celebratory visual marker (Ekman/Kahneman)
- Weekly plan: Add progress indicators — "Week 1/8", "Week 2/8" (Csikszentmihalyi flow feedback)
- Homework: Add permission to adjust — "If this feels too hard/easy, let me know" (Krashen)
- Social proof: "Students who spend 15 min/day typically see B2 stability within 2 months" (Cialdini)
- Greene long-game: "This 8-week foundation opens doors to B2. Beyond that? C1." (Strategic patience)
- Reciprocity closing: "Your feedback helps strengthen these for future students" (Cialdini)

### 6. Delete Hosted Cal.com Account
**Manual step for Marko:**
1. Go to https://cal.com and log in as `marko.check`
2. Settings → General → Account → Delete Account
3. Confirm deletion

### 7. Monolithic Renderer Convergence
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

### Protocol Files
- `C:/Users/RogZephyrus/lingua-pipeline/LingoGrade_Protocol_v6.0_Master.txt` (current)
- v5.2, v5.5, v5.6, v5.7 also in lingua-pipeline/

### Sample JSONs
- `C:/Users/RogZephyrus/lingograde-site/pipeline/sample_*.json` (12 files, all updated)

### Audit Reports (reference)
- `C:/Users/RogZephyrus/WISE_AUDIT_FINDINGS.md` — original WISE audit (26 findings)
- `C:/Users/RogZephyrus/WISE_COLOR_AUDIT_REPORT.md` — color audit
- `C:/Users/RogZephyrus/lingua-pipeline/TYPOGRAPHY_AUDIT_WISE.md` — typography audit
- `C:/Users/RogZephyrus/lingua-pipeline/SPACING_AUDIT_REPORT.md` — spacing audit

---

## User Preferences (from memory)

- Use **haiku** model for all search/explore subagents
- **iida** — if in doubt, ask/advise (TOP PRIORITY)
- Never commit without explicit permission
- Terse output, no summaries unless asked
- **321 process** — audit → verify → deliver, one at a time
- All prices: EUR = USD = CHF = GBP same number, .95 ending
- "Marco" never "Marko" — brand rule
- Camp Level 5+ on all CTAs
- No emoticons in any response
