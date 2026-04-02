-- 002_bot_sessions.sql
-- Persistent storage for free bot analyses and paid chatbot assessments.
-- Replaces in-memory dicts in app.py.

-- ── Free 5-min analyses ──
CREATE TABLE IF NOT EXISTS bot_analyses (
    session_id      TEXT PRIMARY KEY,
    email           TEXT,
    lang            TEXT NOT NULL DEFAULT 'en',
    result          JSONB NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_bot_analyses_email ON bot_analyses (email);

-- ── Paid chatbot assessment sessions ──
CREATE TABLE IF NOT EXISTS bot_assessments (
    assess_id           TEXT PRIMARY KEY,
    payment_intent_id   TEXT NOT NULL,
    email               TEXT NOT NULL,
    session_id          TEXT,                          -- links to bot_analyses
    lang                TEXT NOT NULL DEFAULT 'en',
    status              TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'complete')),
    turns               JSONB NOT NULL DEFAULT '[]'::jsonb,
    turn_count          INTEGER NOT NULL DEFAULT 0,
    result              JSONB,
    report_path         TEXT,
    payment_confirmed   BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_bot_assessments_email ON bot_assessments (email);
CREATE INDEX IF NOT EXISTS idx_bot_assessments_payment ON bot_assessments (payment_intent_id);
