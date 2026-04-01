# Marco Image Placement — Phase 3 Remaining Work

## Prior (completed this session)
- Phase 3 website placement: 9 of 11 mascot images swapped across all HTML pages
- Background removal: 31/32 images processed via remove.bg API, converted to webp
- 87 gpt-prefixed files moved from sliced-images/ to raw-generations/
- Code audit: 7 fixes applied (onerror loops, og:image, fetch error handling, alt text, accessibility, lazy loading)
- Committed and pushed: `5602cf5` on main

## WHAT WAS DONE (do NOT redo)
- Nav logo → `marco-logo-reading-book.webp` (all 12 pages)
- Favicon → `marco-face-grad-v2.webp` (13 pages)
- Index hero → `marco-logo-book-wave.webp`
- Index headset step → `marco-headset-standing.webp`
- Corporate hero → `marco-mila-outfit-corporate.webp`
- Kids hero → `marco-abc-blocks.webp`
- 404 page → `marco-sleeping-branch-v2.webp`
- Shop hero → `marco-mugprint-face-and-body.webp`
- Chatbot widget → `marco-chatbot-speech-bubble.webp`
- onerror fallbacks fixed (now fall back to marco-logo-v6.1.webp)
- og:image meta tags fixed (now use og-logo-v2.png)
- Lazy loading added to 37 below-fold images
- Review avatar picker converted to accessible buttons
- Kids waitlist fetch error handling fixed
- Shop mug alert() replaced with inline feedback

---

## REMAINING WORK — ORDERED BY PRIORITY

### 1. TWO MISSING PLACEMENTS (pages don't exist yet)

| Placement | Image (ready in sliced-images/) | Action |
|---|---|---|
| Horizontal banner | `marco-logo-whiteboard.webp` | Build a banner component or section on index.html |
| About/mission page | `marco-reading-branded-logo-v1.webp` | Create about.html with mission content |

Decision needed: build these pages/sections, or defer?

### 2. FAILED BG REMOVAL — marco-face-wink.webp
- remove.bg returned "Could not identify foreground" (tight face crop)
- Original in `sliced-images/_originals/marco-face-wink.webp`
- Used on: shop.html (save badge, flashcard section), partners.html (how-it-works), index.html (FAQ)
- Options: manual bg removal in Photoshop/GIMP, or accept as-is (may already have transparent bg)

### 3. DEDUPLICATION (from Phase 1 audit)
Retire duplicate variants — move to `_retired/` or delete:
- Coffee: keep `marco-coffee-cozy.webp` + `marco-coffee-saucer.webp`, retire `marco-coffee-hug.webp` + `marco-coffee-morning.webp`
- Sleeping: keep `marco-sleeping-branch-v2.webp`, retire `marco-sleeping-branch.webp`
- Private outfits: keep `marco-mila-outfit-private-stylish.webp`, retire `marco-mila-outfit-private-casual.webp`

**WARNING**: `marco-coffee-morning.webp` is actively used on index.html and shop.html. Must swap before retiring:
- index.html line ~733: availability section → replace with `marco-coffee-cozy.webp`
- shop.html line ~1288: mug section → replace with `marco-coffee-cozy.webp`

### 4. QUALITY FIXES (from Phase 1 audit)
- `marco-mugprint-wink.png` — has crop artifact (feet visible at top). Re-crop before using anywhere.
- `marco-face-serious-circle.png` — mislabeled (actually party face). Rename to `marco-face-party-circle-v2.png`.

### 5. PNG CLEANUP IN sliced-images/
After bg removal, both .png and .webp versions exist for 31 images. The .webp versions are the production files. Options:
- Delete the .png intermediates (originals safe in `_originals/`)
- Or move .png files to a `_png-exports/` subfolder

### 6. UNTRACKED FILES AUDIT
Large number of untracked files remain in the repo. Review and decide:
- `assets/mascot/GPT Images/` — 26 new Apr 1 images (not tracked). Add to raw-generations or .gitignore?
- `assets/mascot/Clipboard_*.png` — clipboard dumps. Delete or archive?
- `assets/mascot/Marco.webp`, `Marco2.webp`, etc. — plush product photos. These ARE referenced by shop.html. Should be tracked.
- `assets/mascot/sliced-images/` — the whole folder is untracked. Contains production crops. Should be tracked.
- `assets/mascot/raw-generations/` — 87 gpt files. Large. Consider .gitignore.
- `assets/mascot/remove_bg.py`, `slice_*.py` — utility scripts. Track or .gitignore?
- `deploy/*.md` — session prompts. Track the new ones.
- `pipeline/__pycache__/` — should be .gitignored

### 7. RESPONSIVE VERIFICATION
Phase 3 Step 4 was not completed: verify all new image placements display correctly at:
- Mobile (375px)
- Tablet (768px)
- Desktop (1280px+)

Key things to check:
- New nav logo (`marco-logo-reading-book.webp`) renders at correct 44x44 / 32px mobile
- New favicon (`marco-face-grad-v2.webp`) displays in browser tab
- Kids hero (`marco-abc-blocks.webp`) fits the `.marco-sleeping` class constraints (260px max)
- Corporate hero (`marco-mila-outfit-corporate.webp`) — duo image may need wider container
- Chatbot widget bubble image renders in the floating circle

### 8. .GITIGNORE ADDITIONS
Create or update `.gitignore` to exclude:
```
__pycache__/
assets/mascot/raw-generations/
assets/mascot/sliced-images/_originals/
assets/mascot/sliced-images/_bin/
assets/mascot/Clipboard_*.png
*.pyc
```

---

## Key Paths
- Production images: `C:/Users/RogZephyrus/lingograde-site/assets/mascot/`
- Source crops: `C:/Users/RogZephyrus/lingograde-site/assets/mascot/sliced-images/`
- Originals backup: `C:/Users/RogZephyrus/lingograde-site/assets/mascot/sliced-images/_originals/`
- Raw GPT generations: `C:/Users/RogZephyrus/lingograde-site/assets/mascot/raw-generations/`
- Website HTML: `C:/Users/RogZephyrus/lingograde-site/*.html`
- Chatbot JS: `C:/Users/RogZephyrus/lingograde-site/js/marco-chat.js`

## Critical Rules
- Icons must NEVER overlap text (feedback_no_icon_text_overlap.md)
- sliced-images = finished crops ONLY
- IIDA: if in doubt, ask
- 321: audit → verify → deliver
- No commit without approval
