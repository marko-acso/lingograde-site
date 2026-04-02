-- 005_free_bot_sessions.sql
-- Persistent storage for free 5-min bot conversations (Marco chatbot funnel).

CREATE TABLE IF NOT EXISTS free_bot_sessions (
    bot_id          TEXT PRIMARY KEY,
    session_id      TEXT DEFAULT '',
    lang            TEXT NOT NULL DEFAULT 'en',
    status          TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'complete')),
    turns           JSONB NOT NULL DEFAULT '[]'::jsonb,
    turn_count      INTEGER NOT NULL DEFAULT 0,
    result          JSONB,
    email           TEXT,
    ip              TEXT DEFAULT '',
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_free_bot_ip ON free_bot_sessions (ip, created_at);
CREATE INDEX IF NOT EXISTS idx_free_bot_email ON free_bot_sessions (email);
