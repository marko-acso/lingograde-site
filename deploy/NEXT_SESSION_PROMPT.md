# Next Session — LingoGrade Site Fixes

## COMPLETED THIS SESSION

### Image Swaps
- Flashcard section: `marco-reading.webp` → `gpt-marco-studying-desk.webp` (35KB, RGBA) on both **index.html:922** and **shop.html:1516**
- `marco-face-wink.webp` replaced with blue-circle bg-removed version (30KB, RGBA)
- `marco-hero.webp` re-exported with transparency preserved (42KB, RGBA — was RGB)

### Bug Fixes
- **shop.html sticker map overlap** — map stats (127/14/38) were bleeding into Kids section. Fixed with `position:relative;z-index:1;overflow:hidden` on sticker-map section
- **index.html `.mc-fab` selector** — two onclick handlers referenced `.mc-fab` but the chat widget creates `#marco-fab`. Fixed both to `#marco-fab`

---

## TODO — REMAINING FROM FULL AUDIT

### Priority 1 — Fix Now
1. **Chinese tip amounts (88/18/8)** — not implemented. If targeting CN market, add CNY variant with lucky numbers to shop.html tip section
2. **Footer inconsistency** — review.html and scan.html have stripped-down footers (missing Language/Pricing/Teachers links). Standardize with other pages
3. **`lingograde-landing.html` orphan** — full duplicate of index.html, not linked anywhere. Delete or redirect

### Priority 2 — Should Fix
4. **corporate.html:97 duplicate color** — `color:var(--ink)` then `color:white` on `.btn-secondary`. Remove first declaration
5. **review.html:164 clipboard fallback** — `navigator.clipboard` has no fallback for older browsers. Add `document.execCommand('copy')` fallback
6. **404.html:34,48 conflicting footer styles** — two footer backgrounds defined (`.footer-minimal #1C1C1C` vs inline `#1A3A5C`). Pick one
7. **WCAG contrast** — `#B0B0B0` text on dark backgrounds fails AA (3.16:1 ratio). Lighten to `#C8C8C8` or use `var(--ink-soft)` consistently

### Priority 3 — Nice to Have
8. **Favicon path consistency** — 404.html uses absolute `/assets/...`, all others use relative `assets/...`. Standardize to absolute on all pages for deep-path safety
9. **Canonical URL missing** on 404.html
10. **Two missing Marco placements** (from Phase 4):
    - Horizontal banner: `marco-logo-whiteboard.webp` — needs placement decision
    - About/mission page: `marco-reading-branded-logo-v1.webp` — needs about.html content

### Priority 4 — Track Assets
11. **Untracked files** — `Marco.webp`, `Marco2.webp`, `Marco4.webp` referenced by shop.html, `sliced-images/*.webp` production crops, `deploy/*.md` docs — all need `git add`
12. **Git commit** — all Phase 3 + Phase 4 + this session's changes uncommitted

---

## ADVICE

- **Commit before next changes.** There are 4+ sessions of uncommitted work. One bad operation could lose everything. Do `git add` on production assets + HTML changes, then commit.
- **Don't touch marco-chat.js** without testing the full chat flow — it's a complex IIFE with session state, language detection, and sales funnel logic.
- **Shop.html is 2100+ lines.** Consider splitting CSS into a separate file before it becomes unmanageable.
- **The `.mc-fab` fix should be tested** — click "Start Free Analysis with Marco" and "Start Bot Assessment" buttons on index.html to verify the chat widget opens.
- **Session is getting heavy on context.** Start fresh for the next batch of fixes.
