# LingoGrade — Next Session Prompt

## COMPLETED — Full Site Audit & Fixes (Apr 8)

### Security (Done)
- Session secret validation (crashes in prod if weak/missing)
- SameSite cookie changed from "None" to "Lax"
- CSRF origin check via @app.before_request
- Flask debug mode now env-controlled (no longer hardcoded True)
- CSP header added to vercel.json (matches Caddyfile.prod)
- Rate limiting on 5 public POST endpoints (analyse, payment/intent, checkout/accessory, checkout/kids, partner-apply)
- Coordinate validation (lat/lng range + NaN check) on sticker verify
- secure_filename() now actually used on homework uploads
- Bot store in-memory TTL cleanup (7-day expiry)

### SEO (Done)
- Sitemap fixed: /reviews → /review
- Title tags shortened: teachers (51ch), programs (51ch), alumni (53ch)
- Meta descriptions trimmed: chatbot-assessment, free-bot, partners, programs, teachers
- og:url fixed on terms-of-service and privacy-policy (removed .html extension)

### Frontend (Done)
- memory-widget.js: try/catch on fetchMemories() and auth session check
- site.css: navy color typo #1B3A5C → #1A3A5C
- site.css: keyboard :focus-visible states for all interactive elements

### Assets (Done)
- marco-alarm.webp copied from sliced-images/ to assets/mascot/ (fixed broken refs)

---

## TODO — High Priority

### 1. Prompt Injection Hardening (~1h)
- `api/analysis_prompt.py:48` — user text interpolated directly into Claude prompt
- `api/app.py:410` — student messages passed to Claude without sanitization
- `api/assessment_prompt.py:86` — lang parameter not validated against ISO 639-1 whitelist
- Fix: treat user text as data-only (separate role), validate lang against whitelist, strip control chars

### 2. Drip Worker Dead-Letter Queue (~1h)
- `api/drip_worker.py:130` — failed emails marked 'failed' and never retried
- If Resend is temporarily down, those emails are lost forever
- Fix: exponential backoff + retry queue (max 3 retries over 24h)

### 3. CI/CD Pipeline (~2h)
- No GitHub Actions, no automated tests, no security scanning
- Need: Python lint (flake8), security scan (bandit), HTML validation
- Auto-deploy static to Vercel on push to main
- Consider: API deploy via SSH action to Hetzner

### 4. Backup Strategy (~30m)
- No documented backup for Supabase, Cal.com Docker volume, generated reports in /tmp
- Enable Supabase automated backups (verify in dashboard)
- Document disaster recovery procedure (RTO/RPO)

---

## TODO — Medium Priority

### 5. Assessment Session Expiry (~15m)
- `api/app.py:401` — old assessment IDs accessible forever
- Add created_at check + 24-hour expiry

### 6. Drip Enqueue Idempotency (~30m)
- `api/drip_engine.py:134` — no duplicate check before insert
- Fix: UNIQUE constraint on (email, sequence, day) or upsert

### 7. Refactor app.py (~2h)
- 1,200+ lines, should split into route modules
- Suggested: assessment_routes.py, checkout_routes.py, sticker_routes.py

### 8. Price Constants Module (~1h)
- Prices hardcoded in app.py, drip_templates.py, HTML pages
- Create prices.py single source of truth

### 9. Structured Logging + Request IDs (~1h)
- Mixed app.logger, logging.getLogger(), no JSON logs
- Add python-json-logger + request_id via @app.before_request

### 10. DB Pool Timeouts (~15m)
- `api/db_pool.py:24-28` — no connect_timeout or statement_timeout
- Fix: add connect_timeout=5, statement_timeout=30000 to DSN

### 11. Invoice Exchange Rate (~15m)
- `api/invoice_generator.py:18` — hardcoded EUR_TO_BGN
- Move to config or fetch daily from ECB

### 12. i18n Hardcoded Strings (~2h)
- Nav items, shop product names, pricing tier labels bypass translations.json
- Extract to i18n keys

### 13. Footer Text Contrast (~10m)
- `site.css:26,50,57` — rgba(255,255,255,0.4/0.5/0.6) on navy fails WCAG AA
- Bump to 0.7+ minimum

---

## TODO — Low Priority

- Missing ARIA labels on interactive elements (buttons, modals, close icons)
- No OpenAPI/Swagger docs for API
- Missing semantic HTML (<main>, <header>, <footer>) on all pages
- PWA manifest.json: add maskable icon + purpose field
- Assessment Philosophy v2 ("Friend Test", "Camp Level 5+") not in marketing copy
- CLAUDE.md pages list missing: free-bot, homework, programs
- Multiple H1 tags on chatbot-assessment.html and free-bot.html

---

## STILL PENDING (from before)
- **mila-hero.png** — Needs generation (same style as marco-hero.png). Fallback works.
- **Apple OAuth:** Needs Apple Developer Program ($99/yr) — skipped for now
