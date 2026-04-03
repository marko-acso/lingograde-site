# Pre-Deploy Status — Session 22

**Date:** 2026-04-02

## Server Audit Results

| Component | Status | Details |
|-----------|--------|---------|
| Web server | Nginx 1.24.0 (NOT Caddy) | Handles api + booking subdomains |
| Pipeline API (FastAPI) | Running | Port 8000, systemd service, 8+ days uptime |
| Cal.com (Docker) | Running | Port 3001, healthy |
| Flask API (bot/dashboard) | NOT running | Code at /opt/lingograde-site/api/, no systemd, no .env, no process |
| PostgreSQL (standalone) | NOT running | Only Cal.com Docker Postgres exists |
| Supabase DB | Provisioned | Project sbfjhsfvsbyjguplywfj, EU-North, Postgres 17.6 |
| app.lingograde.com | NOT configured | No Nginx block, no SSL cert |

## Supabase Migrations (from Session 15)

| Migration | Status |
|-----------|--------|
| 001_student_dashboard.sql | Applied |
| 002_bot_sessions.sql | Skipped (existing schema) |
| 003_sticker_verifications.sql | Applied |
| 004_rls_subscriptions_referrals.sql | Applied |

All tables, RLS policies (16), triggers, and views are live on Supabase.

## What Exists

- Supabase pooler URL: `aws-1-eu-north-1.pooler.supabase.com:5432/postgres`
- SSL cert: `prod-ca-2021.crt` (valid until 2031)
- Flask API code deployed to `/opt/lingograde-site/api/`
- Nginx running with configs for `api.lingograde.com` and `booking.lingograde.com`

## What's Missing (execution order)

| # | Task | Depends on | Estimated risk |
|---|------|-----------|----------------|
| 1 | Create `/opt/lingograde-site/api/.env` | Supabase password, Stripe keys, Anthropic key | Low — file creation |
| 2 | Install psycopg2-binary in Python env | pip access | Low |
| 3 | Create systemd service for Flask/Gunicorn on port 5050 | .env file | Medium — new service |
| 4 | Create Nginx config for app.lingograde.com + SSL cert | DNS pointing to server | Medium — public endpoint |
| 5 | Create `/var/data/lingograde/homework/` directory | N/A | Low — mkdir |
| 6 | Sync latest dashboard_routes.py from local to server | N/A | Low — file copy |
| 7 | Test RLS policies with real JWT tokens | Running API + DB | Verification only |
| 8 | Smoke-test all API endpoints | Everything above | Verification only |

## WISE Decision: Supabase over local Postgres

- Thaler: zero setup friction — already provisioned
- Camp: no lock-in, can migrate anytime
- Csikszentmihalyi: get to endpoint testing faster
- Krashen: right next step (i+1), not overreach

## Key Architecture Note

The repo contains `deploy/Caddyfile.prod` but the server runs **Nginx**, not Caddy.
All reverse proxy config must be done in Nginx format at `/etc/nginx/sites-available/`.

## Blockers Before Proceeding

1. **Supabase DB password** — needed for DATABASE_URL in .env
2. **DNS for app.lingograde.com** — must point to 65.108.151.198 before SSL cert
3. **Stripe + Anthropic API keys** — needed for .env (may already be in password manager)
