# Cal.com Migration: Hosted → Self-Hosted (Complete)

## Context

LingoGrade has a self-hosted Cal.com instance at `booking.lingograde.com` on Hetzner
(65.108.151.198). It's running via Docker, proxied through nginx with SSL (Certbot).

Currently, the site has a MIX of booking links:
- 8 links across HTML files point to `booking.lingograde.com/marko` (just fixed this session)
- 8 links still point to `cal.com/marko.check/...` (hosted Cal.com — needs migration)

The goal: **everything on self-hosted**, then delete the hosted Cal.com account entirely.

---

## Server Access

```
SSH: ssh -i ~/.ssh/id_ed25519_hetzner root@65.108.151.198
Cal.com Docker: /opt/calcom (docker compose)
Nginx configs: /etc/nginx/sites-enabled/
```

## Current Self-Hosted Cal.com State

- **User:** id=1, username=`marko`, email=info@lingograde.com, name=Marko Markovic
- **Existing event types (3):**
  - id=4: Quick Assessment (slug: quick-assessment, 15 min)
  - id=5: Full Assessment (slug: full-assessment, 25 min)
  - id=6: DeepDive Assessment (slug: deepdive-assessment, 45 min)
- **Database:** PostgreSQL 16 (calcom-db container, user: calcom, db: calcom)
- **Integrations configured:** Stripe, Resend (email), Daily.co (video)

## What Needs to Be Created (5 new event types)

### Alumni Assessment Types (3)

These are the SAME assessments but at alumni discount prices, for returning students.

1. **Quick Assessment — Alumni**
   - slug: `quick-assessment-alumni`
   - duration: 15 min
   - price: EUR 71.95 (alumni 20% discount from 89.95)

2. **Full Assessment — Alumni**
   - slug: `full-assessment-alumni`
   - duration: 25 min
   - price: EUR 103.95 (alumni discount from 129.95)

3. **DeepDive Assessment — Alumni**
   - slug: `deepdive-assessment-alumni`
   - duration: 45 min
   - price: EUR 199.95 (alumni discount from 249.95)

### German Landing Page Types (2)

These are German-language versions of existing assessments for the German landing page.

4. **Schnell-Check** (= Quick Assessment in German)
   - slug: `schnell-check`
   - duration: 15 min
   - price: EUR 89.95 (same as Quick Assessment)

5. **Sprachstandsanalyse** (= Full Assessment in German)
   - slug: `sprachstandsanalyse`
   - duration: 25 min
   - price: EUR 129.95 (same as Full Assessment)

### How to Create

**Option A (preferred): Via Cal.com admin UI**
1. Log in at https://booking.lingograde.com (currently /auth is blocked by nginx — you'll need to temporarily allow it)
2. To temporarily allow admin access:
   ```bash
   ssh -i ~/.ssh/id_ed25519_hetzner root@65.108.151.198
   # Comment out the /auth redirect block in nginx config
   sed -i 's|location /auth {|#location /auth {|; s|return 301 https://booking.lingograde.com/marko;|#return 301 https://booking.lingograde.com/marko;|' /etc/nginx/sites-enabled/booking-lingograde
   # BUT the sed above is fragile — better to manually edit:
   nano /etc/nginx/sites-enabled/booking-lingograde
   # Comment out the location /auth block (lines with "location /auth" and its "return 301" and closing "}")
   nginx -t && systemctl reload nginx
   ```
3. Go to https://booking.lingograde.com/auth/login
4. Create each event type with the correct slug, duration, and price
5. Re-enable the /auth block after:
   ```bash
   # Uncomment the /auth block
   nano /etc/nginx/sites-enabled/booking-lingograde
   nginx -t && systemctl reload nginx
   ```

**Option B: Via database SQL (faster but riskier)**
```bash
ssh -i ~/.ssh/id_ed25519_hetzner root@65.108.151.198
cd /opt/calcom
docker compose exec -T calcom-db psql -U calcom -d calcom
```

Then run SQL to create event types. You'll need to match the schema of existing event types (copy from id=4,5,6 as templates). Key columns: title, slug, length, userId, hidden, metadata, locations, etc.

**IMPORTANT:** After creating via SQL, restart the Cal.com container:
```bash
docker compose restart calcom
```

## Links to Update in Site Files (after event types exist)

These are in `C:/Users/RogZephyrus/lingograde-site/`:

| File | Current Link | New Link |
|------|-------------|----------|
| alumni.html:143 | `cal.com/marko.check/deepdive-assessment-alumni` | `booking.lingograde.com/marko/deepdive-assessment-alumni` |
| alumni.html:164 | `cal.com/marko.check/full-assessment-alumni` | `booking.lingograde.com/marko/full-assessment-alumni` |
| alumni.html:184 | `cal.com/marko.check/quick-assessment-alumni` | `booking.lingograde.com/marko/quick-assessment-alumni` |
| index.html:691 | `cal.com/marko.check/deepdive-assessment` | `booking.lingograde.com/marko/deepdive-assessment` |
| index.html:707 | `cal.com/marko.check/full-assessment` | `booking.lingograde.com/marko/full-assessment` |
| index.html:724 | `cal.com/marko.check/quick-assessment` | `booking.lingograde.com/marko/quick-assessment` |
| lingograde-landing.html:331 | `cal.com/marko.check/schnell-check` | `booking.lingograde.com/marko/schnell-check` |
| lingograde-landing.html:348 | `cal.com/marko.check/sprachstandsanalyse` | `booking.lingograde.com/marko/sprachstandsanalyse` |

Also update any Cal.com references in:
- `lingograde-site/js/marco-chat.js` (line 857: has cal.com/marko.check booking link)
- `lingograde-site/pipeline/lingograde_docx.py` (line 189: generates cal.com URLs in reports)

## Verification Checklist

After all changes, verify each URL returns 200:
```bash
SERVER="root@65.108.151.198"
SSH_KEY="~/.ssh/id_ed25519_hetzner"
for slug in quick-assessment full-assessment deepdive-assessment quick-assessment-alumni full-assessment-alumni deepdive-assessment-alumni schnell-check sprachstandsanalyse; do
  CODE=$(ssh -i $SSH_KEY $SERVER "curl -sI http://127.0.0.1:3001/marko/$slug" | head -1)
  echo "$slug: $CODE"
done
```

All should return `HTTP/1.1 200 OK`.

## After Everything Works

1. **Delete hosted Cal.com account:**
   - Go to https://cal.com/marko.check
   - Settings → Account → Delete Account
   - This removes all hosted event types

2. **Verify no remaining references to cal.com/marko.check:**
   ```bash
   grep -r "cal.com/marko" ~/lingograde-site/ --include="*.html" --include="*.js" --include="*.py"
   ```
   Should return zero results.

3. **Re-block /auth on self-hosted** (if not already):
   - Ensure nginx /auth redirect is active

## Mascot Images on Cal.com Event Types

There's a SQL script to set Marco mascot images on event types:
`lingograde-site/deploy/calcom_set_mascot_images.sql`

Run it after creating all event types to set the correct owl images.

## Nginx Config State

Current `/etc/nginx/sites-enabled/booking-lingograde` has:
- Root `/` → redirect to `/marko`
- `/auth` → redirect to `/marko` (blocks login)
- Security headers: X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, HSTS
- SSL via Certbot
- Backup at `/etc/nginx/booking-lingograde.bak`

## User Preferences (from memory)

- Use **haiku** model for all search/explore subagents
- **iida** — if in doubt, ask/advise
- Never commit without explicit permission
- Terse output, no summaries unless asked
- **321 process** — audit → verify → deliver, one at a time
- All prices: EUR = USD = CHF = GBP same number, .95 ending
