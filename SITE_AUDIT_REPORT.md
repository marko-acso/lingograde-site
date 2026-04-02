# LingoGrade.com — Full Site Audit Report
**Date:** 2026-04-02 | **Process:** 321 (3 audit → 2 cross-check → consolidated)
**Raw findings:** 114 | **After dedup + false positive removal:** 78 unique verified issues

---

## FIXES COMPLETED (2026-04-02)

| # | Fix | Files Changed |
|---|-----|---------------|
| 1 | Cookie consent banner — GA gated behind explicit Accept | `js/cookie-consent.js` (new), all 13 HTML pages |
| 2 | ToS contradictions — 24h→48h cancellation, €29→€29.95 homework | `terms-of-service.html` |
| 3 | Corporate schema — Enterprise €49.95, Team 5-14, Dept 15-49 | `corporate.html` |
| 4 | Waitlist forms — actual API submission + localStorage fallback | `shop.html` |
| 5a | Vercel 307→301 — permanent redirect via Vercel API | Vercel dashboard (API call) |
| 5b | cleanUrls + security headers + .html extension redirects | `vercel.json` (new), `sitemap.xml` |
| 6 | Waitlist API endpoint + Supabase migration | `lingua-track/app/api/waitlist/route.ts` (new), `lingua-track/supabase/create-waitlist.sql` (new) |
| 7 | teachers.html #join anchor | Already correct — false positive |
| 8 | Image width/height (15 images) + LCP preload + gstatic preconnect | `index.html` |
| 9 | kids.html noindex + schema on alumni/partners/teachers | `kids.html`, `alumni.html`, `partners.html`, `teachers.html` |
| 10 | Accessibility — skip link, aria-expanded, H4→H3, logo alt | `index.html` |
| 11 | **C1: Canonical URL mismatch blocking Google indexing** — all canonical/OG/schema URLs had `.html` extensions but `cleanUrls: true` 301-redirects `.html` away, so every canonical pointed to a redirect. Stripped `.html` from canonicals, OG URLs, and schema JSON-LD across all 13 pages. Fixed `robots.txt` disallow to clean URL. **Manual step required:** verify `www.lingograde.com` in Google Search Console + submit sitemap + request indexing. | 11 HTML files, `robots.txt` |

---

## FALSE POSITIVES REMOVED (11)

These were flagged by audit agents but confirmed wrong by live verification:

1. ~~Missing OG/Twitter tags~~ → All pages have full OG tags
2. ~~Missing canonical URLs~~ → Present on all pages
3. ~~No sitemap.xml~~ → Exists with 11 URLs
4. ~~Corporate meta desc 16 chars~~ → Actually 150 chars
5. ~~Alumni H1 missing space~~ → `<br>` tag, renders correctly
6. ~~No favicon~~ → Accessible via redirect
7. ~~Booking mixes German/English~~ → English only
8. ~~Logo alt text missing~~ → `alt="Marco"` present
9. ~~How It Works images no alt~~ → All have descriptive alts
10. ~~Kids page no urgency~~ → Social proof copy exists
11. ~~Corporate pricing order reversed~~ → Standard volume discount layout

---

## REMAINING ISSUES — NOT YET FIXED

### CRITICAL (still open)

| ID | Issue | Category |
|----|-------|----------|
| C1 | ~~**Site not indexed by Google**~~ — FIXED (see #11 above). Manual: GSC verify + submit sitemap | SEO |
| C2 | **No OAuth or sign-up on app.lingograde.com/login** | CONVERSION |
| C3 | **Bot Assessment CTA is JS-only** — no fallback if script fails | CONVERSION |
| C4 | **dashboard.html publicly accessible** — no auth gate | SECURITY |

### HIGH (still open)

| ID | Issue | Category |
|----|-------|----------|
| H1 | **Trustpilot widget is "review collector" not "star display"** — zero social proof visible | CONVERSION |
| H2 | **No money-back guarantee** copy anywhere on pricing | CONVERSION |
| H3 | **"28 languages" (bot) vs "12 languages" (assessments)** — unexplained gap | CONVERSION |
| H4 | **Booking subdomain has no back-link** to lingograde.com | UX |
| H5 | **Shop "Meet Marco" → direct Stripe** with no product page | UX |
| H6 | **Partner commission rate never disclosed** — "shared upon approval" | CONVERSION |
| H7 | **No scarcity/urgency signals** on pricing section | CONVERSION |
| H8 | **Corporate "Request a Quote" → #contact** far below fold | CONVERSION |
| H9 | **Privacy Policy has no child data provisions** despite kids product ages 6-14 | LEGAL |
| H10 | **ToS §8 blanket consent clause** conflicts with GDPR Art. 7 | LEGAL |
| H11 | **Privacy Policy doesn't name Google Analytics** by name | LEGAL |
| H12 | **Voss calibrated question repeated twice** on homepage — dilutes technique | COPY |
| H13 | **Testimonials lack specificity** — no photos, dates, or verifiable links | CONVERSION |
| H14 | **Shop liability disclaimer** in sales copy flow — reads as threat | COPY |
| H15 | **Teachers H1 "Now prove it"** — combative tone | COPY |

### MEDIUM (still open)

| ID | Issue | Category |
|----|-------|----------|
| M1 | `twitter:title` / `twitter:description` missing on all pages | SEO |
| M2 | No `og:locale` declared | SEO |
| M3 | kids.html in sitemap at priority 0.7 (should be 0.3 or removed) | SEO |
| M4 | No `hreflang` tags despite 25+ language markets | SEO |
| M5 | `sameAs` array in Organization schema is empty | SEO |
| M6 | 16 H2 tags on homepage — keyword signal dilution | SEO |
| M7 | Currency detection timezone-only — inaccurate for travelers | TECHNICAL |
| M8 | Leaflet.js loaded from unpkg CDN (no SLA, GDPR) | TECHNICAL |
| M9 | ToS/Privacy use Arial font instead of DM Sans | BRAND |
| M10 | "personalised" vs "personalized" mixed spelling | BRAND |
| M11 | "Glitches" terminology only on homepage, not sitewide | BRAND |
| M12 | Block D/E rendered out of order (C→E→D) | BRAND |
| M13 | Pricing "MOST CHOSEN" badge has no social proof number | CONVERSION |
| M14 | Subscription "Complete Program" €249.95/week — lessons not specified | CONVERSION |
| M15 | No testimonial with corporate voice on corporate page | CONVERSION |
| M16 | "3x faster progress" claim in FAQ — no citation | LEGAL |
| M17 | No Right to Withdraw notice for digital services (EU Consumer Rights) | LEGAL |
| M18 | Nav logo alt "LingoGrade - Home" (fixed) but subpages may still have old alt | ACCESSIBILITY |
| M19 | CEFR bar colour contrast may fail WCAG AA | ACCESSIBILITY |
| M20 | Pricing badges "MOST CHOSEN"/"MOST THOROUGH" are CSS pseudo-elements (not screen-reader accessible) | ACCESSIBILITY |
| M21 | No `<noscript>` fallback for shield.js and marco-chat.js | TECHNICAL |
| M22 | `marco-reading.webp` has no cache-busting `?v=3` query string | TECHNICAL |

### LOW (still open)

| ID | Issue | Category |
|----|-------|----------|
| L1 | No `apple-touch-icon.png` (iOS bookmarks) | TECHNICAL |
| L2 | No `manifest.json` (Web App Manifest) | TECHNICAL |
| L3 | `og:type` is `website` on all pages including service/product pages | SEO |
| L4 | Sitemap missing `<lastmod>` dates | SEO |
| L5 | Direct Stripe buy link exposed in HTML (no redirect wrapper) | TECHNICAL |
| L6 | All CSS is per-page inline — no shared stylesheet caching | PERFORMANCE |
| L7 | 160+ elements with long inline `style` attributes | PERFORMANCE |
| L8 | Trustpilot widget uses protocol-relative URL `//widget.trustpilot.com` | TECHNICAL |
| L9 | Alumni page title "Welcome Back — LingoGrade" — no keywords | SEO |
| L10 | kids.html H1 "Marco is getting ready for the little ones" — no keyword signal | SEO |
| L11 | "bespoke" is UK-market jargon, unclear to non-native speakers | COPY |
| L12 | Corporate footer links differ from main footer | UX |

---

## AUDIT METHODOLOGY

- **3 parallel audit agents**: UX/UI, SEO/Technical, Copy/Conversion
- **2 cross-check agents**: Live verification (HTTP fetches) + deduplication/categorization
- **False positive rate**: 11 of 114 raw findings (9.6%) were incorrect
- **Contradictions resolved**: 5 (OG tags, canonical, sitemap, cancellation policy, homework price)
- **New issues surfaced by cross-check**: 2 (ToS §4 contradiction, ToS §12 price mismatch)
