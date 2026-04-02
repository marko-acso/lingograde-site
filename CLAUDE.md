# LingoGrade Site — CLAUDE.md

## What this is
Static HTML marketing site + Python Flask API backend + Supabase. The public face of LingoGrade — landing pages, shop, booking, dashboard, partner portal.

## Stack
- **Frontend:** Static HTML, vanilla JS, CSS
- **Backend:** Python Flask (api/app.py)
- **Database:** Supabase (PostgreSQL)
- **Hosting:** Vercel (static) + Hetzner (API)
- **Reverse proxy:** Caddy

## Pages
index, alumni, chatbot-assessment, client-memory, corporate, dashboard, free-analysis, kids, map, partners, privacy-policy, review, scan, shop, teacher-tools, teachers, terms-of-service

## API Routes (api/)
- app.py — main Flask app
- auth.py — authentication
- dashboard_routes.py, student_routes.py — data endpoints
- bot_store.py — Marco chatbot storage
- analysis_prompt.py, assessment_prompt.py — Claude prompts
- mini_report.py — quick report generation
- db_pool.py — connection pooling

## Key Frontend JS
- marco-chat.js — Marco chatbot widget
- free-analysis.js — free analysis funnel
- client-memory.js — client-side memory
- shield.js — anti-abuse protection
- supabase-init.js — Supabase client
- i18n/lang-switcher.js — language switching

## Commands
```bash
# Local dev
python api/app.py                    # Start Flask API
caddy run --config Caddyfile.dev     # Start Caddy reverse proxy

# Deploy
vercel --prod                        # Deploy static site
```

## Business rules
- Assessment Philosophy v2 on all copy — Friend Test, Camp Level 5+, no fake scarcity
- All prices end in .95, tips round
- Marco the Owl is the only public face
- Shop follows Section X: "HOW THE SHOP SHOULD FEEL"
- Branding: navy #1A3A5C, accent blue #2563AB, upsell green #27AE60
