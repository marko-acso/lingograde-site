-- Partner applications submitted via partners.html / teachers.html
CREATE TABLE IF NOT EXISTS partner_applications (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    phone           TEXT,
    institution     TEXT,
    country         TEXT,
    languages       TEXT,
    referral_source TEXT,
    applied_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_partner_applications_email ON partner_applications (email);
