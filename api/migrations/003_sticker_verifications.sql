-- 003_sticker_verifications.sql
-- Sticker verification system: selfie uploads, geo-verification, map data
-- Supports 7-layer anti-abuse + geo map + partner credit system

CREATE TABLE IF NOT EXISTS sticker_verifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    sticker_uuid    TEXT UNIQUE NOT NULL,              -- burned on scan, one selfie per QR
    latitude        DOUBLE PRECISION NOT NULL,
    longitude       DOUBLE PRECISION NOT NULL,
    city            TEXT,
    country         TEXT,
    selfie_path     TEXT NOT NULL,                     -- server path to uploaded image
    status          TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'verified', 'rejected')),
    submitted_at    TIMESTAMPTZ DEFAULT now(),
    verified_at     TIMESTAMPTZ,                       -- set after 48h review
    rejection_reason TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_sticker_student ON sticker_verifications (student_id);
CREATE INDEX IF NOT EXISTS idx_sticker_status ON sticker_verifications (status);
CREATE INDEX IF NOT EXISTS idx_sticker_geo ON sticker_verifications (latitude, longitude);

-- Accessory orders (for Stripe Checkout tracking)
CREATE TABLE IF NOT EXISTS accessory_orders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT NOT NULL,
    product         TEXT NOT NULL CHECK (product IN ('cap', 'bracelet', 'pin')),
    amount_cents    INTEGER NOT NULL,
    currency        TEXT NOT NULL DEFAULT 'eur',
    stripe_session_id TEXT UNIQUE,
    status          TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'paid', 'shipped', 'delivered')),
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_accessory_email ON accessory_orders (email);
