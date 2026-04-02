-- ============================================================
-- Client Memory System — LingoGrade
-- Per-student memory entries for assessors/teachers
-- ============================================================

-- ── Table ──
CREATE TABLE IF NOT EXISTS client_memories (
  id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  student_id    UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  assessor_id   UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  category      TEXT NOT NULL CHECK (category IN (
    'observation',    -- behavioral / session observation
    'preference',     -- learning style, formality, pace
    'trigger',        -- emotional triggers, sensitivities
    'progress',       -- milestone, breakthrough, regression
    'logistics',      -- scheduling, availability, timezone
    'parent_note'     -- for kids: parent communication
  )),
  tags          TEXT[] DEFAULT '{}',
  title         TEXT NOT NULL,
  body          TEXT NOT NULL,
  session_date  DATE,                       -- optional: date the observation relates to
  is_pinned     BOOLEAN DEFAULT FALSE,
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now()
);

-- ── Indexes ──
CREATE INDEX idx_memories_student    ON client_memories (student_id);
CREATE INDEX idx_memories_assessor   ON client_memories (assessor_id);
CREATE INDEX idx_memories_category   ON client_memories (student_id, category);
CREATE INDEX idx_memories_pinned     ON client_memories (student_id, is_pinned DESC, created_at DESC);

-- ── Updated-at trigger ──
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON client_memories
  FOR EACH ROW EXECUTE FUNCTION update_modified_column();

-- ── Row Level Security ──
ALTER TABLE client_memories ENABLE ROW LEVEL SECURITY;

-- Assessors can read/write their own entries
CREATE POLICY assessor_select ON client_memories
  FOR SELECT USING (auth.uid() = assessor_id);

CREATE POLICY assessor_insert ON client_memories
  FOR INSERT WITH CHECK (auth.uid() = assessor_id);

CREATE POLICY assessor_update ON client_memories
  FOR UPDATE USING (auth.uid() = assessor_id);

CREATE POLICY assessor_delete ON client_memories
  FOR DELETE USING (auth.uid() = assessor_id);

-- Admins can see everything (role stored in auth.users metadata)
CREATE POLICY admin_all ON client_memories
  FOR ALL USING (
    (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );

-- GDPR: students can read their own memories (view-only)
CREATE POLICY student_read_own ON client_memories
  FOR SELECT USING (auth.uid() = student_id);
