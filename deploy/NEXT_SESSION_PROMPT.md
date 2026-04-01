# Next Session — LingoGrade Site Fixes

## COMPLETED

### Priority 1 (commit 7e632a6)
1. **Chinese tip amounts** — CNY tips now use lucky numbers: ¥88/¥18/¥8 (mapped from EUR 20/10/5)
2. **Footer inconsistency** — review.html and scan.html footers now have full nav links (Languages, Pricing, Teachers, Partners)
3. **`lingograde-landing.html` orphan** — deleted (zero incoming links, missing analytics/Trustpilot/schema)

### Priority 2 (commit fa5c212)
4. **corporate.html:97 duplicate color** — removed `color:var(--ink)` leaving only `color:white`
5. **review.html clipboard fallback** — added `document.execCommand('copy')` fallback for older browsers
6. **404.html footer conflict** — unified `.footer-minimal` bg from `#1C1C1C` to `#1A3A5C`
7. **WCAG contrast** — `--ink-soft` bumped from `#B0B0B0` to `#C8C8C8`, all hardcoded `#B0B0B0` in shop.html replaced with `var(--ink-soft)`

---

### Priority 3 (this session)
8. **Favicon path consistency** — standardized all 13 pages to absolute `/assets/...` paths
9. **Canonical URL** — added `<link rel="canonical">` to 404.html

---

### Priority 4 (this session)
10. **Two Marco placements** — images found in `sliced-images/`, copied to `assets/mascot/`, placed in `index.html`:
    - Horizontal banner (`marco-logo-whiteboard.webp`) — between FAQ and Meet Marco Plush sections
    - "Language is personal" philosophy section (`marco-reading-branded-logo-v1.webp`) — between Corporate Teaser and Review Submission

## TODO — REMAINING

### Housekeeping
11. **All items complete** — no remaining blockers

---

## ADVICE

- **Don't touch marco-chat.js** without testing the full chat flow — it's a complex IIFE with session state, language detection, and sales funnel logic.
- **Shop.html is 2100+ lines.** Consider splitting CSS into a separate file before it becomes unmanageable.
- **The `.mc-fab` fix should be tested** — click "Start Free Analysis with Marco" and "Start Bot Assessment" buttons on index.html to verify the chat widget opens.
