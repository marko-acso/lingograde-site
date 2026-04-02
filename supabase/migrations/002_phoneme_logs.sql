-- ============================================================
-- Phoneme Logs — LingoGrade
-- Teacher-logged pronunciation observations during live lessons.
-- Feeds FSRS flashcard generation and longitudinal tracking.
-- ============================================================

-- ── Table ──
CREATE TABLE IF NOT EXISTS phoneme_logs (
  id                UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  student_id        UUID        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  assessor_id       UUID        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  session_id        UUID,                        -- nullable: groups logs from one session
  session_date      DATE        NOT NULL DEFAULT CURRENT_DATE,
  assessed_language TEXT        NOT NULL,         -- e.g. 'de', 'en', 'fr'
  word              TEXT        NOT NULL,         -- the word being spoken
  phoneme           TEXT        NOT NULL,         -- specific phoneme marked, e.g. 'th', 'r', 'ü'
  phoneme_family    TEXT CHECK (phoneme_family IN (
    'plosives',       -- b, p, d, t, g, k
    'fricatives',     -- f, v, s, z, sh, zh, th
    'nasals',         -- m, n, ng
    'approximants',   -- l, r, w, y
    'vowels',         -- monophthong vowel sounds
    'diphthongs'      -- gliding vowel sounds
  )),
  position          TEXT CHECK (position IN (
    'initial',        -- beginning of word
    'medial',         -- middle of word
    'final'           -- end of word
  )),
  severity          TEXT        NOT NULL DEFAULT 'developing' CHECK (severity IN (
    'developing',     -- needs more practice (Lozanov-friendly, replaces "error")
    'focus'           -- active priority for this student
  )),
  notes             TEXT,                        -- optional teacher observation
  created_at        TIMESTAMPTZ DEFAULT now()
);

-- ── Indexes ──
CREATE INDEX idx_phoneme_logs_student_lang  ON phoneme_logs (student_id, assessed_language);
CREATE INDEX idx_phoneme_logs_session       ON phoneme_logs (session_id);
CREATE INDEX idx_phoneme_logs_family        ON phoneme_logs (phoneme_family);

-- ── Row Level Security ──
ALTER TABLE phoneme_logs ENABLE ROW LEVEL SECURITY;

-- Assessors can read/write their own entries
CREATE POLICY assessor_select ON phoneme_logs
  FOR SELECT USING (auth.uid() = assessor_id);

CREATE POLICY assessor_insert ON phoneme_logs
  FOR INSERT WITH CHECK (auth.uid() = assessor_id);

CREATE POLICY assessor_update ON phoneme_logs
  FOR UPDATE USING (auth.uid() = assessor_id);

CREATE POLICY assessor_delete ON phoneme_logs
  FOR DELETE USING (auth.uid() = assessor_id);

-- Admins can see everything (role stored in auth.users metadata)
CREATE POLICY admin_all ON phoneme_logs
  FOR ALL USING (
    (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );

-- GDPR: students can read their own logs (view-only)
CREATE POLICY student_read_own ON phoneme_logs
  FOR SELECT USING (auth.uid() = student_id);

-- ── Helper View: phoneme_summary ──
-- Aggregates per student + language + phoneme.
-- Powers the pronunciation heat map and FSRS flashcard generation.
CREATE OR REPLACE VIEW phoneme_summary AS
SELECT
  student_id,
  assessed_language,
  phoneme,
  phoneme_family,
  COUNT(*)                                          AS log_count,
  MAX(created_at)                                   AS last_logged_at,
  -- Latest severity: use the most recent row's severity
  (
    SELECT pl2.severity
    FROM   phoneme_logs pl2
    WHERE  pl2.student_id        = pl.student_id
      AND  pl2.assessed_language = pl.assessed_language
      AND  pl2.phoneme           = pl.phoneme
    ORDER  BY pl2.created_at DESC
    LIMIT  1
  )                                                 AS latest_severity
FROM phoneme_logs pl
GROUP BY
  student_id,
  assessed_language,
  phoneme,
  phoneme_family;
