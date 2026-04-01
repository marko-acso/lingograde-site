# Marco Image Placement — Phase 3 Final Status

## COMPLETED THIS SESSION

### Task 2: Failed BG Removal — marco-face-wink
- Root production file already had transparency (RGBA, 34KB)
- Deleted dead non-transparent copy from sliced-images/
- All 6 HTML references correctly use transparent root file — no action needed

### Task 3: Deduplication — Coffee Swap
- Swapped `marco-coffee-morning.webp` → `marco-coffee-cozy.webp` in:
  - index.html:801 (pricing section)
  - shop.html:1288 (mug coming-soon card)
  - components/marco-gallery.html:289 (gallery slide 2)
- `marco-coffee-cozy.webp` (37KB) now the active coffee image

### Task 4: Quality Fixes — Rename Mislabeled Image
- Renamed `marco-face-serious-circle.png` → `marco-face-party-circle-v2.png` in:
  - assets/mascot/sliced-final/
  - assets/mascot/sliced-images/_bin/
- Neither file is referenced in HTML (orphaned asset)

### Task 5: PNG Cleanup
- Deleted 31 .png intermediates from sliced-images/
- 31 .webp production files remain
- Originals safe in _originals/ backup folder

### Task 6 + 8: Gitignore Update
Added to .gitignore:
```
__pycache__/
*.pyc
assets/mascot/raw-generations/
assets/mascot/sliced-images/_originals/
assets/mascot/sliced-images/_bin/
assets/mascot/Clipboard_*.png
```

### Task 7: Responsive & Favicon Fixes
- Added `?v=3` cache-buster to favicon on 8 pages:
  - dashboard.html, 404.html, terms-of-service.html, lingograde-landing.html
  - privacy-policy.html, teachers.html, scan.html, review.html
- Added mobile responsive override for corporate hero:
  - corporate.html: `.marco-img { max-width: 60vw; }` inside `@media(max-width:768px)`

---

## TODO — REMAINING WORK

### 1. DEFERRED: Two Missing Placements (needs design direction)

| Placement | Image (ready in sliced-images/) | Status |
|---|---|---|
| Horizontal banner | `marco-logo-whiteboard.webp` (26KB) | Needs: where on index.html? New section or existing? |
| About/mission page | `marco-reading-branded-logo-v1.webp` (128KB) | Needs: about.html page content + layout |

### 2. Retire Duplicate Files
Now that coffee-morning is swapped out, these can be moved to `_retired/` or deleted:
- `assets/mascot/marco-coffee-morning.webp` (36KB) — replaced by coffee-cozy
- `assets/mascot/marco-coffee-morning.png` (248KB) — PNG pair
- `assets/mascot/marco-coffee-hug.webp` (if exists) — unused variant
- `assets/mascot/marco-sleeping-branch.webp` (if exists) — v2 is the active one
- `assets/mascot/marco-sleeping.webp` (35KB) — only used in gallery, consider swap to v2
- `assets/mascot/sliced-images/marco-mila-outfit-private-casual.webp` — keep stylish, retire casual

**WARNING**: `marco-sleeping.webp` is still used in `components/marco-gallery.html:337`. Swap to `marco-sleeping-branch-v2.webp` before retiring.

### 3. Untracked Files — Decisions Needed
- `assets/mascot/GPT Images/` (26 files) — add to raw-generations or .gitignore?
- `assets/mascot/Clipboard_*.png` (2 files) — now gitignored, safe to delete
- `assets/mascot/Marco.webp`, `Marco2.webp`, `Marco4.webp` — referenced by shop.html, MUST track
- `assets/mascot/sliced-images/` — production crops, SHOULD track
- `assets/mascot/remove_bg.py`, `slice_*.py` — utility scripts, track or .gitignore?
- `deploy/*.md` (13 files) — should be tracked

### 4. Mugprint Wink Re-crop
- `marco-mugprint-wink.png` has crop artifact (feet visible at top)
- Only in sliced-final/ and _bin/ — not referenced in HTML
- Low priority — re-crop if/when this image is needed for a page

### 5. Git Commit & Track Production Assets
- Commit all changes from this session
- Track `Marco.webp`, `Marco2.webp`, `Marco4.webp` (shop.html dependencies)
- Track `assets/mascot/sliced-images/*.webp` (production crops)
- Track `deploy/*.md` session prompts

### 6. Responsive Testing (Manual)
Verify in browser at 375px / 768px / 1280px:
- [ ] Nav logo renders at 44px desktop / 32px mobile
- [ ] Favicon displays in browser tab
- [ ] Kids hero fits `.marco-sleeping` constraints (260px / 60vw)
- [ ] Corporate hero responsive at narrow screens (new 60vw cap)
- [ ] Chatbot widget bubble image renders in floating circle
- [ ] Coffee-cozy image displays correctly in all 3 placements

---

## Key Paths
- Production images: `assets/mascot/`
- Source crops: `assets/mascot/sliced-images/`
- Originals backup: `assets/mascot/sliced-images/_originals/`
- Raw GPT generations: `assets/mascot/raw-generations/`
- Website HTML: `*.html`
- Chatbot JS: `js/marco-chat.js`

## Files Modified This Session
- index.html, shop.html, corporate.html (image swaps + responsive)
- components/marco-gallery.html (coffee swap)
- dashboard.html, 404.html, terms-of-service.html, lingograde-landing.html (favicon ?v=3)
- privacy-policy.html, teachers.html, scan.html, review.html (favicon ?v=3)
- .gitignore (added 6 patterns)
- 31 PNGs deleted from sliced-images/
- 1 webp deleted from sliced-images/ (dead wink copy)
- 2 files renamed in sliced-final/ + _bin/ (serious → party)
