-- 006_kids_profiles.sql
-- Kids support: child fields on students, parental consent tracking,
-- widen CEFR constraint to include Pre-A1, add kids booking metadata.

-- ══════════════════════════════════════════════════
-- 1. Add kids columns to students
-- ══════════════════════════════════════════════════

ALTER TABLE students
    ADD COLUMN IF NOT EXISTS is_child          BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS date_of_birth     DATE,
    ADD COLUMN IF NOT EXISTS age_group         TEXT CHECK (age_group IN ('6-8', '9-11', '12-14', '15-17')),
    ADD COLUMN IF NOT EXISTS parent_email      TEXT,
    ADD COLUMN IF NOT EXISTS guardian_name     TEXT,
    ADD COLUMN IF NOT EXISTS parental_consent_at TIMESTAMPTZ;

-- Parent email index for lookups (e.g. "show me all my kids")
CREATE INDEX IF NOT EXISTS idx_students_parent_email ON students (parent_email)
    WHERE parent_email IS NOT NULL;

-- ══════════════════════════════════════════════════
-- 2. Widen CEFR constraint to include Pre-A1
-- ══════════════════════════════════════════════════

-- Drop old constraint (named after the column in 001)
ALTER TABLE assessments
    DROP CONSTRAINT IF EXISTS assessments_cefr_level_check;

ALTER TABLE assessments
    ADD CONSTRAINT assessments_cefr_level_check
    CHECK (cefr_level IN ('Pre-A1', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'));

-- ══════════════════════════════════════════════════
-- 3. Add package_type to assessments for kids vs adult
-- ══════════════════════════════════════════════════

ALTER TABLE assessments
    ADD COLUMN IF NOT EXISTS package_type TEXT DEFAULT 'adult'
    CHECK (package_type IN ('adult', 'kids'));

-- ══════════════════════════════════════════════════
-- 4. Parental consent log (audit trail)
-- ══════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS parental_consents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    parent_email    TEXT NOT NULL,
    guardian_name   TEXT NOT NULL,
    consent_method  TEXT NOT NULL DEFAULT 'checkbox'
                    CHECK (consent_method IN ('checkbox', 'email_confirm', 'signed_form')),
    ip_address      TEXT,
    consented_at    TIMESTAMPTZ DEFAULT now(),
    revoked_at      TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_parental_consents_student ON parental_consents (student_id);

ALTER TABLE parental_consents ENABLE ROW LEVEL SECURITY;

-- Parent reads own consents (matched by parent_email in JWT)
CREATE POLICY consents_admin_manage ON parental_consents
    FOR ALL USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
    );

-- ══════════════════════════════════════════════════
-- 5. Check constraint: children must have parental consent
-- ══════════════════════════════════════════════════

ALTER TABLE students
    ADD CONSTRAINT chk_child_needs_consent
    CHECK (
        is_child = FALSE
        OR (parent_email IS NOT NULL AND parental_consent_at IS NOT NULL)
    );

-- ══════════════════════════════════════════════════
-- 6. Kids bookings (Stripe checkout tracking)
-- ══════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS kids_bookings (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_email        TEXT NOT NULL,
    child_name          TEXT NOT NULL,
    age_group           TEXT NOT NULL CHECK (age_group IN ('6-8', '9-11', '12-14', '15-17')),
    package             TEXT NOT NULL CHECK (package IN ('quick', 'full', 'deep-dive')),
    guardian_name       TEXT,
    stripe_session_id   TEXT UNIQUE,
    amount_cents        INTEGER NOT NULL,
    currency            TEXT NOT NULL DEFAULT 'eur',
    status              TEXT NOT NULL DEFAULT 'paid'
                        CHECK (status IN ('paid', 'scheduled', 'completed', 'cancelled', 'refunded')),
    student_id          UUID REFERENCES students(id) ON DELETE SET NULL,
    assessment_id       UUID REFERENCES assessments(id) ON DELETE SET NULL,
    scheduled_at        TIMESTAMPTZ,
    completed_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_kids_bookings_parent ON kids_bookings (parent_email);
CREATE INDEX IF NOT EXISTS idx_kids_bookings_status ON kids_bookings (status);

ALTER TABLE kids_bookings ENABLE ROW LEVEL SECURITY;

CREATE POLICY kids_bookings_admin_manage ON kids_bookings
    FOR ALL USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
    );
