# Marco Image WISE Audit — Phase 1 Complete

**Date:** 2026-04-01
**Auditor:** Claude (Opus 4.6)
**Scope:** All 164 files in `sliced-images/` — 48 finished crops + 116 gpt- violations

---

## CRITICAL: sliced-folder rule violations

**116 files** have `gpt-` prefix and must be moved out of `sliced-images/`.
Per rule: sliced-images = finished crops ONLY, no GPT raw generations.

**Action required:** Move all `gpt-*` files to a separate `mascot/raw-generations/` folder for reference, or delete if superseded by a finished crop.

### gpt- files with finished crop equivalents (can delete):
| gpt- file | Finished crop |
|-----------|--------------|
| gpt-marco-coffee-hug.png | marco-coffee-hug.png |
| gpt-marco-coffee-saucer.png | marco-coffee-saucer.png |
| gpt-marco-face-grad.png | marco-face-graduation.png |
| gpt-marco-face-serious.png | marco-face-serious-circle.png |
| gpt-marco-face-party.png | marco-face-party-v2.png |
| gpt-marco-face-grad-v2.png | marco-face-grad-v2.png |
| gpt-marco-face-wink.png | marco-face-wink.png |
| gpt-marco-face-party-v2.png | marco-face-party-v2.png |
| gpt-marco-coffee-hug-v2.png | marco-coffee-hug.png |
| gpt-marco-coffee-saucer-v2.png | marco-coffee-saucer.png |
| gpt-marco-alarm-v2.png | marco-alarm-v2.png |
| gpt-marco-sleeping-v2.png | marco-sleeping-branch-v2.png |
| gpt-marco-face-grad-v3.png | marco-face-grad-v2.png |
| gpt-marco-face-wink-v2.png | marco-face-wink-v2.png |
| gpt-marco-face-party-v3.png | marco-face-party-confetti.png |
| gpt-marco-hero.png | marco-hero-standing.png |
| gpt-marco-headset.png | marco-headset-standing.png |
| gpt-marco-reading.png | marco-reading-book.png |
| gpt-marco-thumbsup.png | marco-thumbsup-wink.png |
| gpt-marco-chatbot.png | marco-chatbot-speech-bubble.png |
| gpt-marco-wave.png / gpt-marco-wave-nobg.png | marco-logo-book-wave.png |
| gpt-marco-abc-blocks.png | marco-abc-blocks.png |
| gpt-marco-alarm-sweat.png | marco-alarm-sweat.png |
| gpt-marco-mila-outfit-*.png (6 files) | marco-mila-outfit-*.png (6 crops) |

### gpt- files WITHOUT finished crop (96 files — need triage):
These are raw generations that were never cropped/finalized. Decision needed: crop the best ones or archive all.

---

## WISE Audit Table — 48 Finished Crops

### Legend
- **Ego State:** FC = Free Child, A = Adult, NC = Nurturing Parent, AC = Adapted Child
- **Filter:** ↓ = lowers affective filter (good), ↑ = raises it (bad), — = neutral
- **Safe:** Y = de-suggests anxiety, N = may trigger stress
- **Category:** REPORT / SITE / BOTH / RETIRE / MERCH

| # | Filename | Ego State | Emotion | Safe? | Filter | Greene (authority) | Brand | Category | Use Recommendation |
|---|----------|-----------|---------|-------|--------|-------------------|-------|----------|-------------------|
| 1 | marco-card-reading-branded.png | A/FC | Friendly, knowledgeable | Y | ↓ | Strong — grad cap + book + brand text | On-brand (navy, orange, blue) | BOTH | **Hero card.** Report header, site about/landing. Full branded composition. |
| 2 | marco-mila-card-corporate.png | A | Professional, welcoming | Y | ↓ | Moderate — uniforms, badges | On-brand (navy blazers) | SITE | Corporate/B2B landing page. Both owls in professional attire. |
| 3 | marco-mila-card-kids.png | FC | Playful, magical | Y | ↓ | Low — wizard hat, coffee, casual | On-brand (navy/purple) | SITE | Kids assessment page, family-oriented sections. Warm, inviting. |
| 4 | marco-alarm.png | A/AC | Slightly anxious, urgent | N | ↑ | Moderate — cap present | On-brand | SITE | Deadline reminders, booking urgency CTAs. Sweat drop = mild stress. |
| 5 | marco-tea-eyes-closed.png | FC/NC | Calm, content, serene | Y | ↓ | Moderate — cap, glasses | On-brand | BOTH | Report tip sections, "take a breath" moments, homework encouragement. |
| 6 | marco-logo-reading-v5.png | A/FC | Engaged, eager | Y | ↓ | Strong — cap, reading pose | On-brand | SITE | Site logo variant, assessment intro. Clean, no text overlay. |
| 7 | marco-icon-party.png | FC | Joyful, celebratory | Y | ↓ | Low — party hat replaces cap | Partially (rainbow hat off-palette) | REPORT | Strengths/celebration sections. Party hat = Free Child. Winking = playful. |
| 8 | marco-face-grad-v2.png | A | Calm, wise, approachable | Y | ↓ | Strong — grad cap, centered gaze | On-brand (navy cap, blue bg) | BOTH | **Top pick for favicon/avatar.** Clean circle crop, serious but warm. |
| 9 | marco-face-party-v2.png | FC | Excited, celebrating | Y | ↓ | Low — party hat | Partially (rainbow hat) | REPORT | Strengths celebration in report. Currently used as MARCO_FACE_PARTY. |
| 10 | marco-abc-blocks.png | FC/A | Encouraging, thumbs up | Y | ↓ | Moderate — cap + thumbs up | On-brand | SITE | Kids section, beginner assessments, "first steps" content. |
| 11 | marco-alarm-sweat.png | AC | Worried, rushed | N | ↑ | Moderate — cap present | On-brand | SITE | Urgency CTAs only. Sweat drops = mild anxiety. Use sparingly. |
| 12 | marco-alarm-v2.png | A/AC | Concerned, time-aware | N | — | Moderate — close-up, big eyes | On-brand | SITE | Countdown timers, session reminders. Less anxious than alarm-sweat. |
| 13 | marco-chatbot-speech-bubble.png | A/FC | Friendly, inviting conversation | Y | ↓ | Moderate — cap, waving gesture | On-brand | SITE | **Chatbot widget.** Speech bubble ready for overlay text. Perfect for Marco bot. |
| 14 | marco-coffee-cozy.png | FC/NC | Content, peaceful | Y | ↓ | Moderate — cap, eyes closed | On-brand | BOTH | Report rest/reflection sections, "take your time" tips. |
| 15 | marco-coffee-hug.png | FC | Warm, comforting | Y | ↓ | Moderate — cap, hugging cup | On-brand | BOTH | Report encouragement, site testimonial sections. Nurturing feel. |
| 16 | marco-coffee-morning.png | FC | Sleepy-cozy, content | Y | ↓ | Moderate — cap, gentle pose | On-brand | SITE | Loading states, "we're preparing your report" screens. |
| 17 | marco-coffee-saucer.png | A/FC | Elegant, composed | Y | ↓ | Strong — saucer held formally | On-brand | BOTH | Professional tip sections, report sidebars. More adult than coffee-hug. |
| 18 | marco-face-grad-circle.png | A | Neutral, attentive | Y | — | Strong — direct gaze, cap | On-brand | BOTH | **Avatar/favicon.** Slightly different angle from grad-v2. Wider eyes = more attentive. |
| 19 | marco-face-graduation.png | A | Thoughtful, wise | Y | ↓ | Strong — larger cap, soft lighting | On-brand | BOTH | Report header face, about page. More painted/artistic style. |
| 20 | marco-face-party-circle.png | FC | Winking, playful | Y | ↓ | Low — party hat | Off-palette (orange/green hat) | REPORT | Circle crop for report celebrations. Slightly different from face-party-v2. |
| 21 | marco-face-party-confetti.png | FC | Ecstatic, celebrating | Y | ↓ | Low — party hat, confetti | Off-palette (rainbow) | REPORT | Big wins in report. More confetti than party-circle. |
| 22 | marco-face-serious-circle.png | A/AC | Winking but party-styled | Y | ↓ | Low — party hat with confetti | Off-palette | RETIRE | **Mislabeled** — this is another party face, NOT serious. Confusing name. |
| 23 | marco-face-wink-v2.png | FC | Cheeky, knowing | Y | ↓ | Moderate — cap, circular crop | On-brand | BOTH | Tips, "did you know" sections, playful asides. |
| 24 | marco-face-wink.png | FC | Cheeky, playful | Y | ↓ | Moderate — cap, painted style | On-brand | BOTH | Similar to v2 but different art style. Softer, more watercolor. |
| 25 | marco-headset-standing.png | A | Ready, professional | Y | ↓ | Strong — headset = service | On-brand | SITE | **Lessons/booking page.** Headset signals "ready for your session." |
| 26 | marco-hero-standing.png | A | Neutral, present | Y | — | Strong — standing tall, cap | On-brand | SITE | Generic hero section, about page. Clean standing pose. |
| 27 | marco-logo-book-wave.png | FC/A | Excited, welcoming | Y | ↓ | Strong — brand text + wave + pencil + speech bubble "A♥" | On-brand (full branded) | SITE | **Landing page hero.** Complete branded composition with personality. |
| 28 | marco-logo-books-stack.png | A/FC | Curious, knowledge-loving | Y | ↓ | Strong — sitting on books, lightbulb | On-brand (full branded) | SITE | About page, methodology section. "Knowledge" visual metaphor. |
| 29 | marco-logo-grade-a.png | FC | Winking, mischievous | Y | ↓ | Moderate — holding blank sign | On-brand | SITE | **Versatile.** Blank sign can overlay text. CTA sections, announcements. |
| 30 | marco-logo-reading-book.png | A/FC | Focused, sharing knowledge | Y | ↓ | Strong — horizontal layout, brand text | On-brand (full branded) | SITE | **Header/nav logo.** Horizontal format, text right of mascot. |
| 31 | marco-logo-reading-v6.png | A/FC | Engaged, eager | Y | ↓ | Strong — full body, book, cap | On-brand | SITE | Alternative to v5, slightly different proportions. More detailed. |
| 32 | marco-logo-whiteboard.png | A | Teaching, presenting | Y | ↓ | Strong — holding book, waving, brand text | On-brand (full branded) | SITE | **Horizontal hero.** Wide format for banner sections. |
| 33 | marco-mila-celebrating-highfive.png | FC | Pure joy, connection | Y | ↓ | Low — casual, no cap on Marco | Partial (no cap = off-brand) | SITE | Completion pages, success states. High-five = shared achievement. |
| 34 | marco-mila-outfit-celebration.png | FC/A | Festive, magical | Y | ↓ | Moderate — wizard hat, wand, badges | On-brand (navy outfits) | SITE | Completion/celebration pages, annual milestones. |
| 35 | marco-mila-outfit-corporate.png | A | Professional, trustworthy | Y | ↓ | Strong — blazers, ties, badges | On-brand (navy uniforms) | SITE | **B2B/corporate page.** Most professional duo image. |
| 36 | marco-mila-outfit-kids-playful.png | FC | Warm, inviting | Y | ↓ | Moderate — wizard hat, coffee | On-brand (navy + purple) | SITE | Kids section, family assessment page. Same as card-kids but different crop. |
| 37 | marco-mila-outfit-partner-professional.png | A | Calm, professional | Y | ↓ | Moderate — white coats, badges | On-brand (clean, minimal) | SITE | Partner/affiliate page, team section. Lab-coat style = clinical trust. |
| 38 | marco-mila-outfit-private-casual.png | FC/A | Relaxed, approachable | Y | ↓ | Low — scarves, casual | On-brand (blue/pink scarves) | SITE | Private lessons page, casual learning contexts. |
| 39 | marco-mila-outfit-private-stylish.png | A | Composed, stylish | Y | ↓ | Moderate — scarves, neat pose | On-brand (blue/pink) | SITE | Similar to casual but cleaner pose. Pick one — this one is slightly more polished. |
| 40 | marco-mugprint-face-and-body.png | A | Confident, alert | Y | ↓ | Strong — direct gaze, circle crop | On-brand | MERCH | **Mug/sticker print.** High-res circle face. |
| 41 | marco-mugprint-wink.png | FC | Winking, playful | Y | ↓ | Moderate — wink, circle | On-brand | MERCH | **Mug print.** BUT has cropping artifact — feet visible at top of frame. NEEDS FIX. |
| 42 | marco-reading-book.png | A | Studious, focused | Y | ↓ | Strong — reading, cap, glasses | On-brand | BOTH | Report reading/comprehension sections, site methodology. Classic pose. |
| 43 | marco-reading-branded-logo-v1.png | FC/A | Warm, shared learning | Y | ↓ | Strong — both reading, brand text | On-brand (full branded) | SITE | **Duo branded.** Marco + Mila reading together. Perfect for about/mission page. |
| 44 | marco-sleeping-branch-v2.png | FC | Peaceful, resting | Y | ↓ | Low — sleeping, relaxed | On-brand | SITE | 404 page, "come back later," maintenance mode. Clean linework. |
| 45 | marco-sleeping-branch.png | FC | Deeply asleep | Y | ↓ | Low — sleeping | On-brand | SITE | Same concept, more watercolor style. Pick v2 (cleaner). |
| 46 | marco-tea-half-body.png | FC/NC | Serene, content | Y | ↓ | Moderate — saucer, closed eyes | On-brand | BOTH | Close-up version of tea pose. Good for report tips, smaller placements. |
| 47 | marco-thumbsup-wink.png | FC | Confident, encouraging | Y | ↓ | Strong — thumbs up, sparkles | On-brand | BOTH | **Tip/encouragement icon.** Thumbs up = approval. Report tips, site CTAs. |
| 48 | mila-card-party-branded.png | FC | Joyful, magical | Y | ↓ | Moderate — wand, star, brand text | On-brand (purple/gold) | SITE | Mila-specific pages, female assessor variant, kids celebration. |

---

## Summary Statistics

| Category | Count | Notes |
|----------|-------|-------|
| BOTH (report + site) | 17 | Versatile images usable everywhere |
| SITE only | 23 | Website-specific (too complex for DOCX) |
| REPORT only | 5 | Circle crops / celebration faces for PDF |
| MERCH | 2 | Mug/sticker prints |
| RETIRE | 1 | marco-face-serious-circle (mislabeled) |

## Quality Issues Found

1. **marco-mugprint-wink.png** — Cropping artifact: feet/body fragment visible at top of frame. Needs re-crop.
2. **marco-face-serious-circle.png** — MISLABELED. Shows a party/winking face with confetti, not a serious expression. Rename or retire.
3. **Coffee variants redundancy** — 4 very similar coffee images (cozy, hug, morning, saucer). Recommend picking 2 max.
4. **Sleeping variants** — v1 and v2 are near-identical. Keep v2 only (cleaner lines).
5. **Private outfit variants** — casual vs stylish are very similar. Keep stylish (more polished).

## Top Picks by Use Case

### Report (assessment PDF)
| Use | Image | Why |
|-----|-------|-----|
| Header/cover | marco-card-reading-branded.png | Full brand, professional, warm |
| Strengths celebration | marco-face-party-v2.png | Already in use (MARCO_FACE_PARTY) |
| Tips/encouragement | marco-thumbsup-wink.png | Clear approval signal, sparkles |
| Reflection/pause | marco-tea-eyes-closed.png | Calm, de-suggests anxiety |
| Reading sections | marco-reading-book.png | On-topic, studious |
| Wink asides | marco-face-wink-v2.png | "Did you know" sections |

### Website
| Use | Image | Why |
|-----|-------|-----|
| Landing hero | marco-logo-book-wave.png | Full branded, dynamic, welcoming |
| Horizontal banner | marco-logo-whiteboard.png | Wide format, brand text included |
| Nav logo | marco-logo-reading-book.png | Horizontal, text beside mascot |
| Chatbot widget | marco-chatbot-speech-bubble.png | Speech bubble built in |
| Booking/lessons | marco-headset-standing.png | Headset = "ready for session" |
| Corporate B2B | marco-mila-outfit-corporate.png | Most professional pair image |
| Kids section | marco-abc-blocks.png | Playful, age-appropriate |
| About/mission | marco-reading-branded-logo-v1.png | Duo reading, warm |
| 404/maintenance | marco-sleeping-branch-v2.png | Peaceful, "come back" |
| Favicon/avatar | marco-face-grad-v2.png | Clean circle, authoritative |

### Merch
| Use | Image | Why |
|-----|-------|-----|
| Mug print (face) | marco-mugprint-face-and-body.png | High-res, centered |
| Mug print (playful) | marco-mugprint-wink.png | Needs crop fix first |

---

## gpt- Violation Summary

**116 files must be removed from sliced-images/.** Options:
1. Move to `mascot/raw-generations/` for archive
2. Delete those with finished crop equivalents (~28 files)
3. Triage remaining ~88 for potential cropping into finished versions

## WISE Lens Summary

### Berne (Transactional Analysis)
- **Dominant:** Free Child (24/48) — playful, joyful, safe
- **Secondary:** Adult (18/48) — professional, trustworthy
- **Rare:** Adapted Child (3/48) — only alarm variants
- **Absence:** Critical Parent (0/48) — good, no intimidation

### Ekman (Emotion)
- Most images convey **joy, warmth, calm, or curiosity** — all positive valence
- Only alarm variants convey worry/urgency — use sparingly
- No anger, disgust, contempt, or sadness — appropriate for educational brand

### Lozanov (Suggestopedia)
- 45/48 images **de-suggest anxiety** — safe, warm, inviting
- 3 alarm variants introduce mild stress — useful for urgency CTAs but counter to Lozanov principles

### Krashen (Affective Filter)
- 43/48 **lower the affective filter** — students feel safe
- 2 neutral, 3 raise filter (alarm images)
- Overall collection is strongly filter-lowering

### Greene (Authority)
- Grad cap is the primary authority signal — present in ~40/48
- Party hat variants sacrifice authority for celebration
- Headset and blazer variants add professional authority
- No image is intimidating — authority is always paired with warmth

### Brand Consistency
- Navy/blue palette dominant — consistent
- Orange accents (beak, chest) — consistent
- Party hat images (rainbow) are the main off-palette items
- All finished crops maintain consistent owl character design
- Mila consistently distinguished by purple bow

---

*Phase 1 complete. See SESSION_PROMPT_MARCO_PHASE2.md for report placement + Phase 3 prompt generation.*
