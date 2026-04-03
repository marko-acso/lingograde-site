# Pre-Deploy Verification — Session 15

**Date:** 2026-04-02

## Migrations Executed

| Migration | Status | Notes |
|-----------|--------|-------|
| 001_student_dashboard.sql | ✅ Applied | students, assessments, homework tables + update_updated_at() trigger |
| 002_bot_sessions.sql | ⏭ Skipped | bot_assessments already exists with different schema; not required for 004 |
| 003_sticker_verifications.sql | ✅ Applied | sticker_verifications + accessory_orders tables |
| 004_rls_subscriptions_referrals.sql | ✅ Applied | RLS policies, subscriptions, referrals, partner_earnings, drip_email_log |

## Tables Created/Updated

- `subscriptions` — Weekly/Complete tier tracking with Stripe, assessor, scheduling
- `referrals` — Partner referral tracking (link/sticker/manual source)
- `partner_earnings` — Earnings ledger (referral_credit, sticker_credit, tip, payout)
- `partner_balance` — View with `security_invoker = true` (RLS-enforced)
- `drip_email_log` — Audit trail for all email sequences
- `homework` — From migration 001 (was missing)
- `sticker_verifications` — From migration 003 (was missing)

## RLS Policies Deployed (16 from migration 004)

| Table | Policy | Access |
|-------|--------|--------|
| students | students_own | Own row only |
| assessments | assessments_student_read | Student reads own |
| assessments | assessments_assessor_read | Assessor/admin read all |
| assessments | assessments_admin_write | Assessor/admin full write |
| homework | homework_student_read | Student reads own |
| homework | homework_student_submit | Student updates own (status=submitted only) |
| homework | homework_assessor_manage | Assessor/admin full access |
| sticker_verifications | sticker_student_read | Student reads own |
| sticker_verifications | sticker_student_submit | Student inserts own |
| sticker_verifications | sticker_admin_manage | Admin full access |
| subscriptions | subscriptions_student_read | Student reads own |
| subscriptions | subscriptions_admin_manage | Assessor/admin full access |
| referrals | referrals_partner_read | Partner reads own |
| referrals | referrals_admin_manage | Admin full access |
| partner_earnings | partner_earnings_own_read | Partner reads own |
| partner_earnings | partner_earnings_admin_manage | Admin full access |
| drip_email_log | drip_log_admin | Admin only |

## Code Fixes Applied (7 issues)

### Migration (004_rls_subscriptions_referrals.sql)

1. **CRITICAL** — Renamed `interval` → `billing_interval` (reserved word in PostgreSQL)
2. **MEDIUM** — Added `security_invoker = true` on `partner_balance` view
3. **LOW** — Added `UNIQUE(sticker_uuid)` constraint on sticker_verifications

### API (dashboard_routes.py)

4. **MEDIUM** — Fixed `file.filename` null crash → `secure_filename(file.filename or "")`
5. **MEDIUM** — Merged sticker verify into single transaction + orphan selfie cleanup
6. **LOW** — Masked `referred_email` with `_mask_email()` (privacy)
7. **LOW** — Added `LIMIT 100` on referrals and stickers queries
8. *(cascading)* — Updated subscription query to use `billing_interval` column name

## Drip Email Review (§13–15)

| Section | Lozanov | Berne A-to-A | Camp/BYAF | Upsell-free |
|---------|---------|--------------|-----------|-------------|
| §13 Partner Onboarding | ✅ | ✅ | ✅ | ✅ |
| §14 Subscriber Welcome | ✅ | ✅ | ✅ | ✅ |
| §15 Homework Delivery | ✅ | ✅ | ✅ | ✅ |

No tone violations found. All compliant.

## Supabase Connection Notes

- **Project ref:** sbfjhsfvsbyjguplywfj
- **Region:** North EU (Stockholm)
- **Direct host:** db.sbfjhsfvsbyjguplywfj.supabase.co (IPv6 only — no IPv4)
- **Pooler:** aws-0-eu-central-1.pooler.supabase.com:6543
- **SSL cert:** `prod-ca-2021.crt` (valid until 2031-04-26) — use for `sslmode=verify-full` on Hetzner
- **CLI linked:** `supabase link --project-ref sbfjhsfvsbyjguplywfj` (run from lingograde-site/)

## Remaining Pre-Deploy Steps

- [ ] Test RLS policies with real JWT tokens (anon/student/assessor/admin roles)
- [ ] Smoke-test API endpoints against live DB
- [ ] Deploy updated `dashboard_routes.py` to server
