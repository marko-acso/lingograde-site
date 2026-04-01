# Marco Image Placement — Phase 4 Status

## COMPLETED THIS SESSION

### 1. Fix 404 Page — Missing Image + Footer Overlap
- All paths made absolute (`/assets/...`, `/index.html`, etc.) so they resolve from any URL depth (e.g. `/partner/onboarding`)
- Fixed footer overlap: added `flex-direction: column` to body, footer now spans full width below content
- Fixed: favicon, Home, Shop, Privacy, Terms links all absolute

### 2. Fix Navbar Logo Spacing — "LingoGr A de" → "LingoGrAde"
- Root cause: `.brand-logo` uses `display: inline-flex; gap: 8px` — text nodes around `<span class="brand-a">A</span>` became separate flex items
- Fix: wrapped text in a single `<span>` so gap only applies between logo image and text
- Applied to **8 pages**: index.html, shop.html, kids.html, partners.html, dashboard.html, lingograde-landing.html, corporate.html, teachers.html

### 3. Fix Mug Card Coffee Image — Grey BG on Dark Theme
- Added `border-radius: 16px` to coffee image in shop.html mug card
- Later replaced with bg-removed transparent version

### 4. Fix Flashcard Section — Bad Crop/Blend
- Swapped `marco-face-wink.webp` (circular close-up, ugly on dark) → `marco-reading.webp` (full-body Marco with book, fits flashcard theme)
- Added `border-radius: 16px`, `max-width: 220px`

### 5. Retire Duplicate Files + Gallery Swap
- Swapped `marco-sleeping.webp` → `marco-sleeping-branch-v2.webp` in `components/marco-gallery.html:337`
- Moved to `_retired/`: marco-coffee-morning.webp, marco-coffee-morning.png, marco-sleeping.webp, marco-sleeping.png
- Moved broken crops to `_retired/`: marco-mugprint.png (broken composite), gpt-mila-dancing.png (headless)
- Added `assets/mascot/_retired/` to .gitignore

### 6. Gitignore + Untracked Cleanup
Added to .gitignore:
```
assets/mascot/GPT Images/
assets/mascot/sliced-images-png-backup/
assets/mascot/_retired/
assets/mascot/*.py
assets/mascot/contact-sheets/
```
- Deleted 2 clipboard PNGs (already gitignored)

### 7. Background Removal Audit + Re-export
Audited all mascot face/icon images for bad remove.bg work.

**Re-exported with proper bg removal (6 files):**
- `marco-reading.png` → `.webp` (47KB) — clean
- `marco-coffee-cozy.png` → `.webp` (46KB) — clean
- `marco-face-party.png` → `.webp` (49KB) — clean, decorative circle kept
- `marco-mugprint-face-and-body.png` → `.webp` (35KB) — clean, decorative circle kept
- `marco-logo-v5.png` → `.webp` (31KB) — clean, decorative circle kept
- `marco-logo-v6.1.png` → `.webp` (15KB) — cropped from 816x1056 → 312x263, then converted

**Not re-exported (minor, optional):**
- `marco-face-wink.png` — forehead disc slightly thinned (minor)

---

## TODO — REMAINING WORK

### 1. DEFERRED: Two Missing Placements (needs design direction)
| Placement | Image | Status |
|---|---|---|
| Horizontal banner | `marco-logo-whiteboard.webp` (26KB) | Needs: where on index.html? |
| About/mission page | `marco-reading-branded-logo-v1.webp` (128KB) | Needs: about.html content + layout |

### 2. Untracked Files — Decisions Needed
- `assets/mascot/Marco.webp`, `Marco2.webp`, `Marco4.webp` — referenced by shop.html, MUST track
- `assets/mascot/sliced-images/*.webp` — production crops, SHOULD track
- `deploy/*.md` (14 files) — should be tracked

### 3. Mugprint Wink Re-crop
- `sliced-final/marco-mugprint-wink.png` has crop artifact (feet at top)
- Not referenced in HTML — low priority

### 4. Git Commit & Track Production Assets
- Commit all changes from Phase 3 + Phase 4
- Track Marco shop images, sliced-images, deploy docs

### 5. Responsive Testing (Manual)
Verify in browser at 375px / 768px / 1280px:
- [ ] Navbar logo renders "LingoGrAde" (no spacing) on all pages
- [ ] 404 page: Marco image loads, footer below content (test at /partner/onboarding)
- [ ] Coffee-cozy transparent on dark mug card
- [ ] Flashcard section: marco-reading renders clean on dark bg
- [ ] Mugprint-face-and-body transparent in shop hero

---

## Files Modified This Session
- 404.html (absolute paths, flex-direction fix, footer width)
- shop.html (navbar wrap, coffee border-radius, flashcard image swap)
- index.html, kids.html, partners.html, dashboard.html, lingograde-landing.html, corporate.html, teachers.html (navbar wrap fix)
- components/marco-gallery.html (sleeping → sleeping-branch-v2)
- .gitignore (added 5 patterns)
- 6 PNGs re-exported with bg removal → 6 webps converted
- 4 files moved to _retired/
- 2 clipboard PNGs deleted
