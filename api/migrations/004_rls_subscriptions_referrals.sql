-- 004_rls_subscriptions_referrals.sql
-- Enable RLS on core tables + add subscriptions, referrals, partner earnings, drip log

-- ══════════════════════════════════════════════════
-- 1. Enable RLS on existing tables (from 001)
-- ══════════════════════════════════════════════════

ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE homework ENABLE ROW LEVEL SECURITY;
ALTER TABLE sticker_verifications ENABLE ROW LEVEL SECURITY;

-- Students: own row only
CREATE POLICY students_own ON students
    FOR ALL USING (id = auth.uid());

-- Assessments: student reads own, assessors read all
CREATE POLICY assessments_student_read ON assessments
    FOR SELECT USING (student_id = auth.uid());

CREATE POLICY assessments_assessor_read ON assessments
    FOR SELECT USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') IN ('assessor', 'admin')
    );

CREATE POLICY assessments_admin_write ON assessments
    FOR ALL USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') IN ('assessor', 'admin')
    );

-- Homework: student reads + submits own, assessors manage all
CREATE POLICY homework_student_read ON homework
    FOR SELECT USING (student_id = auth.uid());

CREATE POLICY homework_student_submit ON homework
    FOR UPDATE USING (student_id = auth.uid())
    WITH CHECK (status = 'submitted');

CREATE POLICY homework_assessor_manage ON homework
    FOR ALL USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') IN ('assessor', 'admin')
    );

-- Sticker verifications: student reads own, admin manages all
CREATE POLICY sticker_student_read ON sticker_verifications
    FOR SELECT USING (student_id = auth.uid());

CREATE POLICY sticker_student_submit ON sticker_verifications
    FOR INSERT WITH CHECK (student_id = auth.uid());

CREATE POLICY sticker_admin_manage ON sticker_verifications
    FOR ALL USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
    );

-- ══════════════════════════════════════════════════
-- 2. Subscriptions
-- ══════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS subscriptions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id          UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    tier                TEXT NOT NULL CHECK (tier IN ('weekly', 'complete')),
    status              TEXT NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active', 'paused', 'cancelled', 'expired')),
    stripe_subscription_id TEXT UNIQUE,
    currency            TEXT NOT NULL DEFAULT 'eur',
    amount_cents        INTEGER NOT NULL,
    billing_interval    TEXT NOT NULL DEFAULT 'month' CHECK (billing_interval IN ('week', 'month')),
    assessor_id         UUID,                           -- assigned assessor
    first_session_date  DATE,
    next_session_date   DATE,
    session_time        TIME,
    reassessment_date   DATE,                           -- 8 weeks from start (Complete only)
    started_at          TIMESTAMPTZ DEFAULT now(),
    cancelled_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ DEFAULT now(),
    updated_at          TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_subscriptions_student ON subscriptions (student_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions (status);
CREATE INDEX IF NOT EXISTS idx_subscriptions_stripe ON subscriptions (stripe_subscription_id);

ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY subscriptions_student_read ON subscriptions
    FOR SELECT USING (student_id = auth.uid());

CREATE POLICY subscriptions_admin_manage ON subscriptions
    FOR ALL USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') IN ('assessor', 'admin')
    );

-- ══════════════════════════════════════════════════
-- 3. Referrals (partner + sticker tracking)
-- ══════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS referrals (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    referred_email  TEXT NOT NULL,
    source          TEXT NOT NULL DEFAULT 'link'
                    CHECK (source IN ('link', 'sticker', 'manual')),
    sticker_uuid    TEXT,                               -- if source = sticker
    assessment_id   UUID REFERENCES assessments(id) ON DELETE SET NULL,
    status          TEXT NOT NULL DEFAULT 'clicked'
                    CHECK (status IN ('clicked', 'booked', 'completed', 'credited')),
    credited_amount_cents INTEGER,
    credited_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_referrals_partner ON referrals (partner_id);
CREATE INDEX IF NOT EXISTS idx_referrals_status ON referrals (status);
CREATE INDEX IF NOT EXISTS idx_referrals_sticker ON referrals (sticker_uuid);

ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;

-- Partners see own referrals
CREATE POLICY referrals_partner_read ON referrals
    FOR SELECT USING (partner_id = auth.uid());

CREATE POLICY referrals_admin_manage ON referrals
    FOR ALL USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
    );

-- ══════════════════════════════════════════════════
-- 4. Partner earnings + payouts
-- ══════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS partner_earnings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    referral_id     UUID REFERENCES referrals(id) ON DELETE SET NULL,
    type            TEXT NOT NULL CHECK (type IN ('referral_credit', 'sticker_credit', 'tip', 'payout')),
    amount_cents    INTEGER NOT NULL,
    currency        TEXT NOT NULL DEFAULT 'eur',
    description     TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_partner_earnings_partner ON partner_earnings (partner_id);

-- Running balance view (SECURITY INVOKER so RLS on partner_earnings is enforced)
CREATE OR REPLACE VIEW partner_balance
    WITH (security_invoker = true) AS
SELECT
    partner_id,
    SUM(CASE WHEN type != 'payout' THEN amount_cents ELSE 0 END) AS earned_cents,
    SUM(CASE WHEN type = 'payout' THEN ABS(amount_cents) ELSE 0 END) AS paid_out_cents,
    SUM(CASE WHEN type != 'payout' THEN amount_cents ELSE -ABS(amount_cents) END) AS balance_cents,
    COUNT(DISTINCT referral_id) FILTER (WHERE type = 'referral_credit') AS total_referrals
FROM partner_earnings
GROUP BY partner_id;

ALTER TABLE partner_earnings ENABLE ROW LEVEL SECURITY;

CREATE POLICY partner_earnings_own_read ON partner_earnings
    FOR SELECT USING (partner_id = auth.uid());

CREATE POLICY partner_earnings_admin_manage ON partner_earnings
    FOR ALL USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
    );

-- ══════════════════════════════════════════════════
-- 5. Drip email log (audit trail)
-- ══════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS drip_email_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    sequence        TEXT NOT NULL,                       -- 'post_assessment', 'partner_onboarding', 'subscriber_welcome'
    day             INTEGER NOT NULL,                    -- 0, 1, 3, 5, 7, 30, 56
    template        TEXT NOT NULL,                       -- template identifier
    status          TEXT NOT NULL DEFAULT 'sent'
                    CHECK (status IN ('sent', 'suppressed', 'bounced', 'opened', 'clicked')),
    suppression_reason TEXT,                             -- why it was suppressed, if applicable
    sent_at         TIMESTAMPTZ DEFAULT now(),
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_drip_log_student ON drip_email_log (student_id);
CREATE INDEX IF NOT EXISTS idx_drip_log_sequence ON drip_email_log (sequence, day);

ALTER TABLE drip_email_log ENABLE ROW LEVEL SECURITY;

-- Only admin/system can read/write drip logs
CREATE POLICY drip_log_admin ON drip_email_log
    FOR ALL USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
    );

-- ══════════════════════════════════════════════════
-- 6. Updated-at triggers for new tables
-- ══════════════════════════════════════════════════

CREATE TRIGGER trg_subscriptions_updated
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ══════════════════════════════════════════════════
-- 7. Unique constraint on sticker_uuid
-- ══════════════════════════════════════════════════

ALTER TABLE sticker_verifications
    ADD CONSTRAINT uq_sticker_uuid UNIQUE (sticker_uuid);
