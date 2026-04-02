# LingoGrade — Next Session Prompt

## COMPLETED — Tier 1: Quick Fixes (Apr 1)
- 1A. chunk_04 pl/pt/ro translations added
- 1B. Logo v5 deleted, remove_bg.py updated to v6.1
- 1C. 16 unused pipeline assets deleted
- 1D. mila-hero.png — needs art generation (fallback safe)

## COMPLETED — Tier 4: Merch & Physical (Apr 1)
- ~~Sticker frame 15 SKUs~~ — 3-swatch color picker (Blue/Gold/Grey) below carousel, syncs bracket overlays, 5 campaigns x 3 colors
- ~~Branded accessories~~ — 3-card grid (Cap, Bracelet, Enamel Pin), Coming Soon + waitlist, JSON-LD PreOrder, tablet 2-col fix
- ~~Geolocation sticker map~~ — Leaflet + CARTO dark tiles, 28 cities, circle markers, stat bar, responsive

---

## COMPLETED — Tier 2: Report Camp Tone Fixes (Apr 1)
- 2A. HW CTA urgency → "Would you like professional feedback?" (13 inf + 6 formal)
- 2B. Reassess guilt → "Ready to book your next session?" (2x21 inf + 2x6 formal)
- 2C. Tip obligation → "Would you like to leave a tip for Marco?" (24 inf + 6 formal)
- 2D. Prescriptive reassessment → "8-week reassessment cycle" (21 langs)
- 2E. HW submit command → "You can submit your homework at..." (24 inf + 7 formal)
- 2F. chunk_08 register fix — ru/uk/bg/sr/hr informal CTAs were using formal conjugations (Apr 1)

---

## COMPLETED — Tier 3: Git Commits (Apr 1)
- 3A. lingua-track: 3 commits (MFA+client notes, LetterHighlighter+SQL, Suspense boundaries)
- 3B. lingograde-flashcards: 1 commit (anti-export protection + Lozanov language)

---

## COMPLETED — Tier 4A: Teachers Page WISE (Apr 1)
- CEFR credibility box (Council of Europe strip with Goethe/Cambridge/telc/DELF badges)
- Sharper exclusivity (3 partners per city, specific cap language)
- Starter kit split (partner materials + equipment recommendations as separate sections)
- Flow-state proof (student testimonial about conversation-like assessment experience)
- FAQ Voss labels (accusation audit header + 6 category labels: Level Concern, Trust, Money, Price, Credibility, Risk)
- Loss-frame CTA (Kahneman: "Every month without diagnostics is a month students plateau on guesswork")

## COMPLETED — Tier 4B: Partners Page WISE (Apr 1)
- Silent partner option ("Share once, earn forever" passive path + secondary CTA)
- Monetizing trust FAQ (Voss labeling + doctor/specialist reframe)
- Identity hero ("You are the person people trust when they need to learn a language")
- Calibrated calculator (interactive slider 1-20, contextual descriptions, 10+ highlight)
- Removed pulse animation on submit button (Camp violation)
- Milestone cards (First Share → First Referral → 10 Referrals → Established Partner)
- Micro-commitments ("Who are the 3 people..." pre-form nudge)

## COMPLETED — Tier 4C: Shop Page WISE (Apr 1)
- **4C-A. AIDA Core:** Trust strip in hero (500+/4.8/12/127), FAQ/Objections section (6 Voss accusation audit items: Value Concern, Trust, Money, Price, Risk, Commitment), final "Ready?" 3-path guided CTA (free link / Marco EUR 24.95 / Complete Package EUR 299.95) with safety valve
- **4C-B. Copy/Safety Valves:** Mega bundle "Massive savings" → "One decision", removed vague "Available while stock lasts" scarcity, added mega bundle safety valve ("Not the right time? No problem"), free sticker imperatives → observational, "Wear the brand. Own the identity." → "The things that make it yours", Chinese bundle "立即购买" (Buy Now) → "查看详情" (See Details)
- **4C-C. Visual Cleanup:** Removed bracketPulse animation on carousel (Camp violation — no pulsing animations on products, matching partners page precedent)
- **4C-D. Guided Funnel:** 3-column final CTA section with ascending commitment (free dashboard / Meet Marco / Complete Package), MOST CHOSEN badge on middle tier, bottom safety valve
- **4C-E. Shop Polish (Apr 2):** Consolidated hero paragraphs (3→2, merged duplicate "invisible QR" copy), added BYAF safety valves to 4 missing CTAs (Sticker Pack, Free Sticker Opt-In, Need More Stickers, Assessor), merged 2 duplicate FAQ/Accusation Audit sections into 1 (9 items: Trust, Money, Credibility, Level Concern, Risk, Price, Commitment, Payout), removed duplicate "locked pricing" message

---

## COMPLETED — Tier 5: Content Creation (Apr 2)
- **5A. Camp Protocol** — Full assessor training supplement (10 sections): Camp pillars, BYAF compliance, self-selection upsells, CTA Level 5 optimization, fake scarcity policy, session scripts, report-as-Camp-document, 9 common violations with fixes, self-assessment checklist
- **5B. Drip Email System** — Complete 5-day Camp+Voss sequence: Day 0 (no sell) → Day 1 (HW 20%) → Day 3 (Reassess 15%) → Day 5 (2xHW 10%) → Day 7 (0% Camp pure) → Day 10 (silence) → Day 30 (value) → Week 8 (reassessment). 24-language matrix, segmentation (6 segments), discount ladder, personalisation variables, automation rules, suppression logic, anti-patterns, technical specs

---

## COMPLETED — Google OAuth (Apr 2)
- New GCP project `lingograde-492105`, OAuth client created
- Supabase auth config updated via CLI (client ID + secret pushed to `sbfjhsfvsbyjguplywfj`)
- Redirect URI (`supabase.co/auth/v1/callback`) + JS origin (`app.lingograde.com`) configured
- Consent screen published (Testing → In Production), basic scopes only (email/profile/openid)
- Branding set: logo, privacy-policy.html, terms-of-service.html, developer contacts

---

## STILL PENDING
- **mila-hero.png** — Needs generation (same style as marco-hero.png). Fallback works.
- **Apple OAuth:** Needs Apple Developer Program ($99/yr) — skipped for now
