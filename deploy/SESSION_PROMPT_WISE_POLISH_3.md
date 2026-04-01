# WISE Polish Session 3 — Falsch/Richtig Softening + Marco Declension Cleanup

## Context

Sessions 1-2 complete. Cal.com migration, Marco rebrand, WISE audit, bundle translations, psycholinguistic softening ("im Aufbau"), anxiety-reduction micro-messages, MARCO_FACE_PARTY, social proof/Greene/reciprocity all done. Translation cache cleaned (Marko → Marco).

This session handles two remaining items from Session 2 review:
1. Falsch/Richtig → Inkorrekt/Korrekt across all languages
2. Croatian/Serbian declension cleanup — "Marco" stays undeclined everywhere

---

## What Was Already Done (do NOT redo)

### Session 1 (2026-04-01)
- 20 WISE audit fixes (caps, colors, typography, spacing, formality, language)
- pl CTA formality fix, tr CTA tense fix
- 8 missing bundle translations (cs, hu, no, sv, fi, da, sq, hi)

### Session 2 (2026-04-01)
25. **"instabil" → "im Aufbau"/"Developing"** — 6 files updated (both lg_translations.py, shared.py, both lingograde_docx.py, context_builder.py)
26. **Homework forgiveness valve** — _HW_REASSURANCE + formal variants added to chunk_08_homework.py (24 languages)
27. **Plan reassurance** — _PLAN_REASSURANCE added to chunk_09_plan.py ("Your brain learns best when calm and confident", 24 languages)
28. **MARCO_FACE_PARTY** — deployed in chunk_03_perception.py strengths section (floating image, right margin)
29. **Social proof + Greene long-game + Reciprocity** — 3 bilingual WISE rows added to chunk_10_footer.py before professional closing
30. **Translation cache** — "Marko" → "Marco" across all 95 JSON files in lingua-pipeline/translation_cache/

---

## What Remains (this session's work)

### 1. Falsch/Richtig → Inkorrekt/Korrekt

**Rationale (WISE):** "Falsch" = "false/wrong" — character judgment, Critical Parent ego state (Berne). "Inkorrekt" = observational, Adult ego state. Same information, zero shame load. Latin root cognate across Romance + Germanic + Slavic languages.

**Where labels appear:**

#### Primary (chunks renderer)
- `C:/Users/RogZephyrus/lingua-pipeline/chunks/chunk_08_homework.py`
  - Search for "Falsch" and "Richtig" — these are used as labels in HW B (error correction pairs)
  - Replace all "Falsch:"/"Wrong:" labels with "Inkorrekt:"/"Incorrect:" equivalents
  - Replace all "Richtig:"/"Right:"/"Correct:" labels with "Korrekt:"/"Correct:" equivalents
  - Check both informal AND formal translation dicts

#### Legacy (monolithic renderers)
- `C:/Users/RogZephyrus/lingua-pipeline/lingograde_docx.py`
- `C:/Users/RogZephyrus/lingograde-site/pipeline/lingograde_docx.py`
  - Same Falsch/Richtig labels — sync changes

#### Translation tables
- `C:/Users/RogZephyrus/lingua-pipeline/lg_translations.py`
- `C:/Users/RogZephyrus/lingograde-site/pipeline/lg_translations.py`
  - Check if Falsch/Richtig appears as translatable terms

**Target translations (all 24 languages):**

| Language | "Inkorrekt:" | "Korrekt:" |
|----------|-------------|------------|
| de | Inkorrekt: | Korrekt: |
| en | Incorrect: | Correct: |
| fr | Incorrect : | Correct : |
| es | Incorrecto: | Correcto: |
| it | Scorretto: | Corretto: |
| ru | Некорректно: | Корректно: |
| uk | Некоректно: | Коректно: |
| bg | Некоректно: | Коректно: |
| sr | Некоректно: | Коректно: |
| hr | Neispravno: | Ispravno: |
| pl | Niepoprawnie: | Poprawnie: |
| pt | Incorreto: | Correto: |
| ro | Incorect: | Corect: |
| ar | غير صحيح: | صحيح: |
| zh | 不正确： | 正确： |
| tr | Yanlış: | Doğru: |
| sq | Pasaktë: | Saktë: |
| hu | Helytelen: | Helyes: |
| cs | Nesprávně: | Správně: |
| no | Feil: | Riktig: |
| sv | Felaktigt: | Korrekt: |
| fi | Virheellinen: | Oikein: |
| da | Forkert: | Korrekt: |
| nl | Onjuist: | Juist: |
| hi | गलत: | सही: |

**Note:** Some languages (tr, no, fi, hi) don't have clean Latin-root cognates — use the closest neutral/observational equivalent rather than forcing a calque. The table above reflects this.

**WISE lenses:** Berne (Adult ego state, avoid Critical Parent shame), Lozanov (de-suggestion), Krashen (lower affective filter)

### 2. Marco Declension Cleanup

**Rule:** "Marco" stays undeclined in ALL languages. It is a brand name, not a native word. Standard practice for foreign brand names in Croatian/Serbian/other declining languages.

**Where to fix:**
- `C:/Users/RogZephyrus/lingua-pipeline/translation_cache/*.json` — 95 files
  - Search for "Marcom" (Croatian instrumental of Marco — was changed from "Markom" in Session 2)
  - Replace with "Marco" (undeclined)
  - Also search for any other declined forms: "Marca" (genitive), "Marcu" (dative), "Marce" (vocative)
  - Replace ALL declined forms with "Marco"

- Check all `.py` files in both pipelines for any hardcoded declined forms of Marco

**WISE rationale:** Brand consistency (Greene Law 4: say less than necessary — one name, one form, everywhere). The slight grammatical foreignness reinforces that Marco is a distinct character, not a generic Croatian name.

---

## Key File Locations

### Report Pipeline (primary — chunks)
- `C:/Users/RogZephyrus/lingua-pipeline/chunks/shared.py` — colors, fonts, formality, helpers
- `C:/Users/RogZephyrus/lingua-pipeline/chunks/chunk_08_homework.py` — homework with Falsch/Richtig labels
- `C:/Users/RogZephyrus/lingua-pipeline/lg_translations.py` — ALL translations

### Report Pipeline (legacy — monolithic)
- `C:/Users/RogZephyrus/lingograde-site/pipeline/lingograde_docx.py`
- `C:/Users/RogZephyrus/lingua-pipeline/lingograde_docx.py`
- `C:/Users/RogZephyrus/lingograde-site/pipeline/lg_translations.py`

### Translation Cache
- `C:/Users/RogZephyrus/lingua-pipeline/translation_cache/` — 95 JSON files

---

## Verification Checklist

After all changes:
- [ ] `grep -r "Falsch" lingua-pipeline/chunks/` returns 0 results
- [ ] `grep -r "Richtig" lingua-pipeline/chunks/` returns 0 results (except in comments explaining the change)
- [ ] `grep -r "Marcom\|Marca\b\|Marcu\b\|Marce\b" lingua-pipeline/translation_cache/` returns 0 results
- [ ] `python -m chunks.test_chunk 8` passes (HW B renders correctly with new labels)
- [ ] `python -m chunks.test_chunk all` passes (full report renders)

---

## User Preferences (from memory)

- Use **sonnet** model for agents, **haiku** for pure search/grep only
- **iida** — if in doubt, ask/advise (TOP PRIORITY)
- Never commit without explicit permission
- Terse output, no summaries unless asked
- **321 process** — audit → verify → deliver, one at a time
- "Marco" never "Marko" — brand rule
- Camp Level 5+ on all CTAs
- No emoticons in any response
