-- ============================================================
-- Student Profiles — LingoGrade
-- Lightweight lookup table for assessor-facing student names.
-- Synced from the main students table (Flask side).
-- ============================================================

CREATE TABLE IF NOT EXISTS student_profiles (
  id              UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name       TEXT NOT NULL,
  preferred_name  TEXT,
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_student_profiles_name ON student_profiles (full_name);

-- ── Updated-at trigger (reuse existing function from 001) ──
CREATE TRIGGER set_student_profiles_updated_at
  BEFORE UPDATE ON student_profiles
  FOR EACH ROW EXECUTE FUNCTION update_modified_column();

-- ── Row Level Security ──
ALTER TABLE student_profiles ENABLE ROW LEVEL SECURITY;

-- Assessors can read all student profiles (needed for student selector)
CREATE POLICY assessor_read_profiles ON student_profiles
  FOR SELECT USING (
    (auth.jwt() -> 'user_metadata' ->> 'role') IN ('assessor', 'admin')
  );

-- Admins can manage profiles
CREATE POLICY admin_manage_profiles ON student_profiles
  FOR ALL USING (
    (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );

-- Students can read their own profile
CREATE POLICY student_read_own_profile ON student_profiles
  FOR SELECT USING (auth.uid() = id);
