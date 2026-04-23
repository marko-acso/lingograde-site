-- Corporate assessment orders (Team / Department / Enterprise tiers)
-- Buyer pays via Stripe; candidate invitations handled post-payment.

CREATE TABLE IF NOT EXISTS corporate_orders (
    id                  SERIAL PRIMARY KEY,
    tier                TEXT NOT NULL CHECK (tier IN ('team','department','enterprise')),
    seat_count          INTEGER NOT NULL CHECK (seat_count > 0),
    language            TEXT,
    buyer_email         TEXT NOT NULL,
    buyer_name          TEXT,
    company_name        TEXT NOT NULL,
    buyer_ip            TEXT,
    currency            TEXT NOT NULL DEFAULT 'eur',
    unit_amount_cents   INTEGER NOT NULL,
    total_amount_cents  INTEGER NOT NULL,
    stripe_session_id   TEXT,
    stripe_payment_id   TEXT,
    status              TEXT NOT NULL DEFAULT 'pending_payment',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    paid_at             TIMESTAMPTZ,
    notes               TEXT
);

CREATE INDEX IF NOT EXISTS idx_corporate_orders_buyer_email ON corporate_orders (buyer_email);
CREATE INDEX IF NOT EXISTS idx_corporate_orders_status ON corporate_orders (status);
CREATE INDEX IF NOT EXISTS idx_corporate_orders_stripe_session ON corporate_orders (stripe_session_id);
