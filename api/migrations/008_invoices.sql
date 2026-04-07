-- 008: Invoices table for auto-invoicing
-- Sequential numbering, PDF storage path, linked to Stripe sessions

CREATE TABLE IF NOT EXISTS invoices (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_number  INTEGER NOT NULL UNIQUE,
    issued_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    due_at          TIMESTAMPTZ NOT NULL DEFAULT (now() + interval '14 days'),

    -- Customer
    customer_name   TEXT,
    customer_email  TEXT NOT NULL,

    -- Line items stored as JSONB array: [{description, quantity, unit_price_cents, total_cents}]
    line_items      JSONB NOT NULL DEFAULT '[]',

    -- Amounts (all in cents)
    subtotal_cents  INTEGER NOT NULL,
    vat_rate        NUMERIC(5,2) NOT NULL DEFAULT 20.00,
    vat_cents       INTEGER NOT NULL,
    total_cents     INTEGER NOT NULL,
    currency        TEXT NOT NULL DEFAULT 'eur',

    -- BGN conversion (fixed peg 1.95583)
    total_bgn_cents INTEGER NOT NULL,

    -- Stripe reference
    stripe_session_id   TEXT,
    stripe_payment_intent_id TEXT,
    product_type    TEXT,

    -- Storage
    pdf_path        TEXT,

    -- Metadata
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Sequence for invoice numbering (starting after current 22)
CREATE SEQUENCE IF NOT EXISTS invoice_number_seq START WITH 23;

-- Index for lookups
CREATE INDEX IF NOT EXISTS idx_invoices_email ON invoices (customer_email);
CREATE INDEX IF NOT EXISTS idx_invoices_stripe ON invoices (stripe_session_id);
