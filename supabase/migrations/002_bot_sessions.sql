-- Bot analysis results (free 5-min snapshots)
CREATE TABLE IF NOT EXISTS bot_analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT NOT NULL,
  email TEXT,
  input_text TEXT NOT NULL,
  lang TEXT NOT NULL DEFAULT 'en',
  result JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_bot_analyses_session ON bot_analyses (session_id);
CREATE INDEX idx_bot_analyses_email ON bot_analyses (email) WHERE email IS NOT NULL;
CREATE INDEX idx_bot_analyses_created ON bot_analyses (created_at DESC);

-- Bot assessment sessions (EUR 49.95 paid tier)
CREATE TABLE IF NOT EXISTS bot_assessments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  assess_session_id TEXT NOT NULL UNIQUE,
  payment_intent_id TEXT NOT NULL UNIQUE,
  session_id TEXT NOT NULL,
  email TEXT NOT NULL,
  lang TEXT NOT NULL DEFAULT 'en',
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'complete', 'expired')),
  turns JSONB DEFAULT '[]'::jsonb,
  turn_count INTEGER DEFAULT 0,
  result JSONB,
  report_url TEXT,
  payment_confirmed BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now(),
  completed_at TIMESTAMPTZ
);

CREATE INDEX idx_bot_assessments_session ON bot_assessments (session_id);
CREATE INDEX idx_bot_assessments_email ON bot_assessments (email);
CREATE INDEX idx_bot_assessments_status ON bot_assessments (status);
CREATE INDEX idx_bot_assessments_created ON bot_assessments (created_at DESC);

-- RLS policies
ALTER TABLE bot_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE bot_assessments ENABLE ROW LEVEL SECURITY;

-- Service role can do everything (API backend uses service key)
CREATE POLICY bot_analyses_service ON bot_analyses
  FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY bot_assessments_service ON bot_assessments
  FOR ALL USING (true) WITH CHECK (true);
