CREATE TABLE pack_purchases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    student_id UUID REFERENCES students(id),
    pack_type TEXT NOT NULL DEFAULT 'mega_bundle',
    stripe_session_id TEXT UNIQUE,
    amount_cents INTEGER NOT NULL,
    currency TEXT NOT NULL DEFAULT 'eur',
    assessment_status TEXT NOT NULL DEFAULT 'not_booked'
        CHECK (assessment_status IN ('not_booked','booked','completed')),
    reassessment_status TEXT NOT NULL DEFAULT 'locked'
        CHECK (reassessment_status IN ('locked','not_booked','booked','completed')),
    reassessment_eligible_date DATE,
    purchased_at TIMESTAMPTZ DEFAULT now(),
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_pack_purchases_email ON pack_purchases(email);
CREATE INDEX idx_pack_purchases_student ON pack_purchases(student_id);
