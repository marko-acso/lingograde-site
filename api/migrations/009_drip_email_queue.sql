-- 009_drip_email_queue.sql
-- Extends drip_email_log for scheduling: adds pending/failed statuses,
-- scheduled_for timestamp, email column, metadata JSONB, resend_id tracking.

BEGIN;

ALTER TABLE drip_email_log
  ADD COLUMN IF NOT EXISTS scheduled_for TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS email TEXT,
  ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS resend_id TEXT;

ALTER TABLE drip_email_log
  DROP CONSTRAINT IF EXISTS drip_email_log_status_check;

ALTER TABLE drip_email_log
  ADD CONSTRAINT drip_email_log_status_check
  CHECK (status IN ('pending', 'sent', 'suppressed', 'bounced', 'opened', 'clicked', 'failed'));

ALTER TABLE drip_email_log
  ALTER COLUMN status SET DEFAULT 'pending',
  ALTER COLUMN sent_at DROP DEFAULT;

CREATE INDEX IF NOT EXISTS idx_drip_log_pending
  ON drip_email_log (scheduled_for, status)
  WHERE status = 'pending';

CREATE INDEX IF NOT EXISTS idx_drip_log_suppress_check
  ON drip_email_log (student_id, sequence, day);

COMMENT ON TABLE drip_email_log IS
  'Dual-purpose: queue (status=pending) and audit log (status=sent/suppressed/etc). Worker polls WHERE status=pending AND scheduled_for <= now().';

COMMENT ON COLUMN drip_email_log.scheduled_for IS
  'When the email should be sent. Worker sends when scheduled_for <= now().';

COMMENT ON COLUMN drip_email_log.metadata IS
  'Template variables stored at enqueue time: first_name, cefr_level, language, assessor_name, specific_pattern, discounted_price, full_price, currency, booking_link, dashboard_link, referral_link, etc.';

COMMIT;
