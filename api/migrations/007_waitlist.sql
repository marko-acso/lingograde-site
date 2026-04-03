-- 007_waitlist.sql
-- Waitlist table for email capture (kids page, shop, future pages).

CREATE TABLE IF NOT EXISTS waitlist (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT NOT NULL,
    source      TEXT NOT NULL DEFAULT 'general',
    created_at  TIMESTAMPTZ DEFAULT now(),
    UNIQUE (email, source)
);

CREATE INDEX IF NOT EXISTS idx_waitlist_source ON waitlist (source);

ALTER TABLE waitlist ENABLE ROW LEVEL SECURITY;

CREATE POLICY waitlist_admin_manage ON waitlist
    FOR ALL USING (
        (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
    );
