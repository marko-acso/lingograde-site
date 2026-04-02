-- 001_student_dashboard.sql
-- Student dashboard: students, assessments, homework
-- Supabase-compatible: UUID PKs, timestamptz, ready for RLS

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ── Students ──
CREATE TABLE IF NOT EXISTS students (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT UNIQUE NOT NULL,
    full_name       TEXT,
    preferred_name  TEXT,
    formality_preference TEXT DEFAULT 'informal' CHECK (formality_preference IN ('informal', 'formal')),
    country_of_residence TEXT,
    display_country TEXT,
    password_hash   TEXT,                          -- bcrypt; nullable until OAuth replaces it
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_students_email ON students (email);

-- ── Assessments ──
CREATE TABLE IF NOT EXISTS assessments (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id  UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    date        DATE NOT NULL DEFAULT CURRENT_DATE,
    language    TEXT NOT NULL,
    cefr_level  TEXT NOT NULL CHECK (cefr_level IN ('A1','A2','B1','B2','C1','C2')),
    pdf_path    TEXT,                              -- server path to generated PDF
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_assessments_student ON assessments (student_id);

-- ── Homework ──
CREATE TABLE IF NOT EXISTS homework (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    assessment_id   UUID REFERENCES assessments(id) ON DELETE SET NULL,
    title           TEXT NOT NULL,
    type            TEXT NOT NULL CHECK (type IN ('A','B','C','D','E')),
    status          TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','submitted','reviewed')),
    deadline        TIMESTAMPTZ NOT NULL,          -- typically created_at + 48h
    submitted_at    TIMESTAMPTZ,
    file_path       TEXT,                          -- server path to uploaded file
    feedback        TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_homework_student ON homework (student_id);
CREATE INDEX IF NOT EXISTS idx_homework_assessment ON homework (assessment_id);

-- ── Updated_at trigger ──
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_students_updated ON students;
CREATE TRIGGER trg_students_updated
    BEFORE UPDATE ON students
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ── RLS (enable when migrating to Supabase) ──
-- ALTER TABLE students ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE homework ENABLE ROW LEVEL SECURITY;
--
-- CREATE POLICY students_own ON students FOR ALL USING (id = auth.uid());
-- CREATE POLICY assessments_own ON assessments FOR SELECT USING (student_id = auth.uid());
-- CREATE POLICY homework_own_read ON homework FOR SELECT USING (student_id = auth.uid());
-- CREATE POLICY homework_own_upload ON homework FOR UPDATE
--     USING (student_id = auth.uid())
--     WITH CHECK (status = 'submitted');
