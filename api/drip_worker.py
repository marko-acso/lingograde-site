"""
drip_worker.py — LingoGrade drip email worker daemon
Run as: python drip_worker.py
Systemd service: lingograde-drip.service

Polls drip_email_queue every 60 seconds for due emails (status='pending' AND scheduled_for <= now()).
Respects the 48-hour minimum gap between emails (per spec: max 1 email per 48 hours across all sequences).
Sends via Resend. Logs to stdout.
"""

import logging
import os
import signal
import time
from datetime import datetime, timedelta, timezone

from db_pool import init_pool, get_cursor
import drip_engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("drip_worker")

running = True

POLL_INTERVAL = 60  # seconds
BATCH_SIZE = 50
GAP_HOURS = 48
MAX_RETRIES = 3


def handle_signal(sig, frame):
    global running
    logger.info("Shutdown signal received")
    running = False


signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)


def _last_sent_at(student_id: str) -> datetime | None:
    """Return the sent_at timestamp of the most recent sent email for this student across all sequences."""
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT sent_at
                FROM drip_email_queue
                WHERE student_id = %s
                  AND status = 'sent'
                ORDER BY sent_at DESC
                LIMIT 1
                """,
                (student_id,),
            )
            row = cur.fetchone()
            if row and row["sent_at"]:
                sent_at = row["sent_at"]
                # Ensure timezone-aware
                if sent_at.tzinfo is None:
                    sent_at = sent_at.replace(tzinfo=timezone.utc)
                return sent_at
            return None
    except Exception as e:
        logger.warning(f"_last_sent_at query failed for student {student_id}: {e}")
        return None


def _within_gap(student_id: str | None, day: int) -> bool:
    """
    Return True if the student received an email within the last 48 hours
    and this email is NOT exempt (day=0 transactional emails are exempt).
    """
    # Day 0 of any sequence is transactional — exempt from the gap rule
    if day == 0:
        return False

    # If there is no student_id, we cannot check the gap — allow sending
    if not student_id:
        return False

    last = _last_sent_at(student_id)
    if last is None:
        return False

    now = datetime.now(timezone.utc)
    return (now - last) < timedelta(hours=GAP_HOURS)


def _handle_failure(log_id: str, template: str, email: str):
    """Increment retry count; move to dead_letter after MAX_RETRIES."""
    try:
        with get_cursor() as cur:
            cur.execute(
                "SELECT COALESCE((metadata->>'retry_count')::int, 0) AS retries FROM drip_email_queue WHERE id = %s",
                (log_id,),
            )
            row = cur.fetchone()
            retries = (row["retries"] if row else 0) + 1

            if retries >= MAX_RETRIES:
                cur.execute(
                    """UPDATE drip_email_queue
                       SET status = 'dead_letter',
                           metadata = jsonb_set(COALESCE(metadata, '{}'::jsonb), '{retry_count}', %s::jsonb)
                       WHERE id = %s""",
                    (str(retries), log_id),
                )
                logger.error(f"DLQ: {template} to {email} (log={log_id}) after {retries} retries")
            else:
                # Exponential backoff: 5min, 25min, 125min
                backoff_minutes = 5 ** retries
                cur.execute(
                    """UPDATE drip_email_queue
                       SET status = 'pending',
                           scheduled_for = now() + make_interval(mins => %s),
                           metadata = jsonb_set(COALESCE(metadata, '{}'::jsonb), '{retry_count}', %s::jsonb)
                       WHERE id = %s""",
                    (backoff_minutes, str(retries), log_id),
                )
                logger.warning(
                    f"Retry {retries}/{MAX_RETRIES} for {template} to {email} (log={log_id}), backoff {backoff_minutes}m"
                )
    except Exception as e:
        logger.error(f"_handle_failure error for {log_id}: {e}")


def process_due_emails():
    """Fetch and send all due pending emails, respecting the 48-hour gap rule."""
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT id, student_id, email, template, sequence, day, scheduled_for
                FROM drip_email_queue
                WHERE status = 'pending'
                  AND scheduled_for <= now()
                ORDER BY scheduled_for ASC
                LIMIT %s
                """,
                (BATCH_SIZE,),
            )
            rows = cur.fetchall()
    except Exception as e:
        logger.error(f"process_due_emails: DB query failed: {e}")
        return

    if not rows:
        return

    logger.info(f"Processing {len(rows)} due email(s)")

    for row in rows:
        row = dict(row)
        log_id = row["id"]
        student_id = row.get("student_id")
        day = row.get("day", -1)
        template = row.get("template", "")
        email = row.get("email", "")

        # 48-hour gap check (transactional day=0 emails are exempt)
        if _within_gap(student_id, day):
            logger.info(
                f"Skipping {log_id} ({template} → {email}) — within 48-hour gap for student {student_id}"
            )
            continue

        try:
            success = drip_engine.send_email(log_id)
            if success:
                logger.info(f"Sent {template} to {email} (log={log_id})")
            else:
                _handle_failure(log_id, template, email)
        except Exception as e:
            logger.error(f"Unexpected error sending {log_id}: {e}")
            _handle_failure(log_id, template, email)


if __name__ == "__main__":
    logger.info("LingoGrade drip worker starting")

    # Initialise DB pool (no Flask app — standalone process)
    init_pool()

    while running:
        try:
            process_due_emails()
        except Exception as e:
            logger.error(f"Worker loop error: {e}")
        time.sleep(POLL_INTERVAL)

    logger.info("LingoGrade drip worker stopped")
