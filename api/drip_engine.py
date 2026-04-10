"""
drip_engine.py — LingoGrade drip email engine
Enqueues sequences into drip_email_queue and sends via Resend.
"""

import json
import logging
import os
import uuid
from datetime import datetime, timedelta, timezone

import requests as http_requests

import drip_templates
from db_pool import get_cursor
from pricing import HOMEWORK_CHECK, REASSESSMENT, DOUBLE_HOMEWORK

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Resend config
# ---------------------------------------------------------------------------

RESEND_API_URL = "https://api.resend.com/emails"
FROM_ASSESSOR = "Marco | LingoGrade <marco@lingograde.com>"
FROM_LINGOGRADE = "LingoGrade <hello@lingograde.com>"

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")

# ---------------------------------------------------------------------------
# Template dispatch
# ---------------------------------------------------------------------------

TEMPLATE_DISPATCH = {
    "post_assessment_day1": drip_templates.post_assessment_day1,
    "post_assessment_day3": drip_templates.post_assessment_day3,
    "post_assessment_day5": drip_templates.post_assessment_day5,
    "post_assessment_day7": drip_templates.post_assessment_day7,
    "post_assessment_day30": drip_templates.post_assessment_day30,
    "post_assessment_day56": drip_templates.post_assessment_day56,
    "partner_onboarding_day0": drip_templates.partner_onboarding_day0,
    "partner_onboarding_day3": drip_templates.partner_onboarding_day3,
    "partner_onboarding_day7": drip_templates.partner_onboarding_day7,
    "subscriber_welcome_day0": drip_templates.subscriber_welcome_day0,
    "subscriber_post_session": drip_templates.subscriber_post_session,
}

# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------


def get_student_by_email(email: str) -> dict | None:
    """Look up student by email. Returns {id, full_name, preferred_name, is_child, parent_email} or None."""
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT id, full_name, preferred_name, is_child, parent_email
                FROM students
                WHERE email = %s
                LIMIT 1
                """,
                (email,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            return dict(row)
    except Exception as e:
        logger.warning(f"get_student_by_email failed for {email}: {e}")
        return None


def get_first_name(student: dict | None, email: str) -> str:
    """Extract first name from student record. Falls back to email prefix if no student found."""
    if student:
        # preferred_name takes priority, then first word of full_name
        name = student.get("preferred_name") or student.get("full_name") or ""
        name = name.strip()
        if name:
            return name.split()[0]
    # Fallback: use the part of the email before the @
    return email.split("@")[0]


def is_suppressed(student_id: str, sequence: str, day: int) -> bool:
    """Check if this email was already sent or suppressed for this student/sequence/day."""
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT 1 FROM drip_email_queue
                WHERE student_id = %s
                  AND sequence = %s
                  AND day = %s
                  AND status IN ('sent', 'suppressed')
                LIMIT 1
                """,
                (student_id, sequence, day),
            )
            return cur.fetchone() is not None
    except Exception as e:
        logger.warning(f"is_suppressed check failed: {e}")
        return False


def suppress_remaining(student_id: str, sequence: str, reason: str):
    """Mark all pending emails in a sequence as suppressed for this student."""
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE drip_email_queue
                SET status = 'suppressed',
                    suppression_reason = %s
                WHERE student_id = %s
                  AND sequence = %s
                  AND status = 'pending'
                """,
                (reason, student_id, sequence),
            )
            logger.info(
                f"Suppressed remaining {sequence} emails for student {student_id}: {reason}"
            )
    except Exception as e:
        logger.error(f"suppress_remaining failed for student {student_id} / {sequence}: {e}")


# ---------------------------------------------------------------------------
# Enqueue helpers
# ---------------------------------------------------------------------------


def _insert_drip(
    *,
    student_id: str | None,
    email: str,
    sequence: str,
    day: int,
    template: str,
    scheduled_for: datetime,
    metadata: dict,
):
    """Insert a single row into drip_email_queue. Idempotent — skips if already exists."""
    log_id = str(uuid.uuid4())
    with get_cursor() as cur:
        # Idempotency: skip if any row exists for this student/sequence/day (any status)
        if student_id:
            cur.execute(
                """SELECT 1 FROM drip_email_queue
                   WHERE student_id = %s AND sequence = %s AND day = %s LIMIT 1""",
                (student_id, sequence, day),
            )
            if cur.fetchone():
                logger.info(f"Idempotent skip: {template} for student {student_id} already enqueued")
                return None

        cur.execute(
            """
            INSERT INTO drip_email_queue
              (id, student_id, email, sequence, day, template, status, scheduled_for, metadata)
            VALUES
              (%s, %s, %s, %s, %s, %s, 'pending', %s, %s)
            """,
            (
                log_id,
                student_id,
                email,
                sequence,
                day,
                template,
                scheduled_for,
                json.dumps(metadata),
            ),
        )
    return log_id


def enqueue_post_assessment(
    email: str,
    language: str,
    cefr_level: str,
    assess_id: str,
    specific_pattern: str = None,
):
    """
    Enqueue post-assessment drip sequence Days 1, 3, 5, 7, 30, 56.

    Day 0 is already handled by the existing report delivery.
    Schedules:
    - Day 1: now + 24 hours
    - Day 3: now + 72 hours
    - Day 5: now + 120 hours
    - Day 7: now + 168 hours
    - Day 30: now + 30 days
    - Day 56: now + 56 days

    Pricing (hardcoded per business rules):
    - Day 1: HW discounted=23.95, full=29.95
    - Day 3: Reassessment discounted=118.95, full=139.95
    - Day 5: Double HW discounted=53.95, full=59.90

    If student is a child (is_child=True), skip all Day 1-7 emails.
    """
    now = datetime.now(timezone.utc)
    sequence = "post_assessment"

    student = get_student_by_email(email)
    first_name = get_first_name(student, email)
    student_id = student["id"] if student else None

    # Kids segment — skip Day 1-7, parents not yet implemented
    is_child = student.get("is_child", False) if student else False

    # Resolve language display name
    language_display = drip_templates.LANGUAGE_NAMES.get(language.lower(), language)

    # Assessor name is always Marco
    assessor_name = "Marco"

    # Default specific_pattern fallback
    if not specific_pattern:
        specific_pattern = f"a key pattern at {cefr_level}"

    # Booking link for Day 56
    booking_link = "https://www.lingograde.com/shop#reassessment"

    # Define all days with schedule offsets
    schedule = [
        (1, now + timedelta(hours=24)),
        (3, now + timedelta(hours=72)),
        (5, now + timedelta(hours=120)),
        (7, now + timedelta(hours=168)),
        (30, now + timedelta(days=30)),
        (56, now + timedelta(days=56)),
    ]

    for day, scheduled_for in schedule:
        # Skip Day 1-7 for children
        if is_child and day <= 7:
            continue

        # Skip if already sent or suppressed (idempotency)
        if student_id and is_suppressed(student_id, sequence, day):
            logger.info(f"Skipping {sequence} day {day} for {email} — already sent/suppressed")
            continue

        template_name = f"post_assessment_day{day}"

        # Build metadata for this day's template
        if day == 1:
            metadata = {
                "first_name": first_name,
                "cefr_level": cefr_level,
                "specific_pattern": specific_pattern,
                "discounted_price": HOMEWORK_CHECK["discounted"],
                "full_price": HOMEWORK_CHECK["full"],
                "currency": HOMEWORK_CHECK["currency"],
                "assessor_name": assessor_name,
                "language": language_display,
            }
        elif day == 3:
            metadata = {
                "first_name": first_name,
                "language": language_display,
                "discounted_price": REASSESSMENT["discounted"],
                "full_price": REASSESSMENT["full"],
                "currency": REASSESSMENT["currency"],
                "assessor_name": assessor_name,
            }
        elif day == 5:
            metadata = {
                "first_name": first_name,
                "discounted_price": DOUBLE_HOMEWORK["discounted"],
                "full_price": DOUBLE_HOMEWORK["full"],
                "currency": DOUBLE_HOMEWORK["currency"],
                "assessor_name": assessor_name,
            }
        elif day == 7:
            metadata = {
                "first_name": first_name,
                "assessor_name": assessor_name,
            }
        elif day == 30:
            metadata = {
                "first_name": first_name,
                "language": language,  # pass code for LANGUAGE_INSIGHTS lookup
            }
        elif day == 56:
            metadata = {
                "first_name": first_name,
                "language": language_display,
                "one_specific_finding": specific_pattern,
                "booking_link": booking_link,
                "assessor_name": assessor_name,
            }

        try:
            log_id = _insert_drip(
                student_id=student_id,
                email=email,
                sequence=sequence,
                day=day,
                template=template_name,
                scheduled_for=scheduled_for,
                metadata=metadata,
            )
            logger.info(
                f"Enqueued {template_name} for {email} at {scheduled_for.isoformat()} (id={log_id})"
            )
        except Exception as e:
            logger.error(f"Failed to enqueue {template_name} for {email}: {e}")


def enqueue_partner_onboarding(
    email: str,
    first_name: str,
    student_id: str = None,
    dashboard_link: str = "https://www.lingograde.com/dashboard",
    partner_manager_name: str = "Marco",
):
    """
    Enqueue partner onboarding sequence: Day 0 (immediate), Day 3, Day 7.
    """
    now = datetime.now(timezone.utc)
    sequence = "partner_onboarding"

    # Referral link derived from dashboard (placeholder — real link stored in partner record)
    referral_link = dashboard_link  # caller should pass a real referral link via dashboard_link

    schedule = [
        (0, "partner_onboarding_day0", now),
        (3, "partner_onboarding_day3", now + timedelta(days=3)),
        (7, "partner_onboarding_day7", now + timedelta(days=7)),
    ]

    for day, template_name, scheduled_for in schedule:
        if student_id and is_suppressed(student_id, sequence, day):
            logger.info(f"Skipping {sequence} day {day} for {email} — already sent/suppressed")
            continue

        if day == 0:
            metadata = {
                "first_name": first_name,
                "dashboard_link": dashboard_link,
                "partner_manager_name": partner_manager_name,
            }
        elif day == 3:
            metadata = {
                "first_name": first_name,
                "referral_link": referral_link,
                "partner_manager_name": partner_manager_name,
            }
        elif day == 7:
            metadata = {
                "first_name": first_name,
                "referral_link": referral_link,
                "partner_manager_name": partner_manager_name,
                "has_stickers": True,
            }

        try:
            log_id = _insert_drip(
                student_id=student_id,
                email=email,
                sequence=sequence,
                day=day,
                template=template_name,
                scheduled_for=scheduled_for,
                metadata=metadata,
            )
            logger.info(
                f"Enqueued {template_name} for {email} at {scheduled_for.isoformat()} (id={log_id})"
            )
        except Exception as e:
            logger.error(f"Failed to enqueue {template_name} for {email}: {e}")


def enqueue_subscriber_welcome(
    email: str,
    student_id: str,
    subscription_tier: str,
    first_session_date: str,
    first_session_time: str,
    assessor_name: str,
    homework_included: bool = True,
    reassessment_date: str = None,
):
    """
    Enqueue subscriber welcome sequence: Day 0 (immediate).
    Also suppresses any pending post_assessment sequence for this student
    (subscriber already bought — no need for upsell drip).
    """
    now = datetime.now(timezone.utc)
    sequence = "subscriber_welcome"

    student = get_student_by_email(email)
    first_name = get_first_name(student, email)

    # Suppress post_assessment drip — subscriber has already converted
    if student_id:
        suppress_remaining(student_id, "post_assessment", "converted_to_subscriber")

    dashboard_link = "https://www.lingograde.com/dashboard"

    metadata = {
        "first_name": first_name,
        "subscription_tier": subscription_tier,
        "first_session_date": first_session_date,
        "first_session_time": first_session_time,
        "assessor_name": assessor_name,
        "dashboard_link": dashboard_link,
        "homework_included": homework_included,
        "reassessment_date": reassessment_date,
    }

    try:
        log_id = _insert_drip(
            student_id=student_id,
            email=email,
            sequence=sequence,
            day=0,
            template="subscriber_welcome_day0",
            scheduled_for=now,
            metadata=metadata,
        )
        logger.info(
            f"Enqueued subscriber_welcome_day0 for {email} at {now.isoformat()} (id={log_id})"
        )
    except Exception as e:
        logger.error(f"Failed to enqueue subscriber_welcome_day0 for {email}: {e}")


# ---------------------------------------------------------------------------
# Send
# ---------------------------------------------------------------------------


def send_email(log_id: str) -> bool:
    """
    Send a single drip_email_queue row via Resend.
    - Fetches the row
    - Calls the appropriate template function with metadata
    - POSTs to Resend API
    - Updates status to 'sent' + sets sent_at + stores resend_id
    - On failure: sets status to 'failed'
    - Returns True on success
    """
    # Fetch the log row
    try:
        with get_cursor() as cur:
            cur.execute(
                "SELECT * FROM drip_email_queue WHERE id = %s",
                (log_id,),
            )
            row = cur.fetchone()
    except Exception as e:
        logger.error(f"send_email: DB fetch failed for {log_id}: {e}")
        return False

    if row is None:
        logger.error(f"send_email: log row not found: {log_id}")
        return False

    row = dict(row)
    template_name = row["template"]
    metadata = row.get("metadata") or {}

    # Resolve template function
    template_fn = TEMPLATE_DISPATCH.get(template_name)
    if template_fn is None:
        logger.error(f"send_email: unknown template '{template_name}' for log {log_id}")
        _mark_failed(log_id, "unknown_template")
        return False

    # Render the template
    try:
        rendered = template_fn(**metadata)
    except Exception as e:
        logger.error(f"send_email: template render failed for {log_id} ({template_name}): {e}")
        _mark_failed(log_id, f"render_error: {e}")
        return False

    # Day 30 sends from LingoGrade, all others from the assessor
    from_addr = FROM_LINGOGRADE if row.get("day") == 30 else FROM_ASSESSOR

    # Send via Resend
    payload = {
        "from": from_addr,
        "to": [row["email"]],
        "subject": rendered["subject"],
        "html": rendered["html"],
        "text": rendered.get("text", ""),
    }

    try:
        resp = http_requests.post(
            RESEND_API_URL,
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=15,
        )
        resp.raise_for_status()
        resend_id = resp.json().get("id", "")
    except Exception as e:
        logger.error(f"send_email: Resend request failed for {log_id}: {e}")
        _mark_failed(log_id, f"resend_error: {e}")
        return False

    # Mark sent
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE drip_email_queue
                SET status = 'sent',
                    sent_at = now(),
                    resend_id = %s
                WHERE id = %s
                """,
                (resend_id, log_id),
            )
        logger.info(
            f"send_email: sent {template_name} to {row['email']} (log={log_id}, resend={resend_id})"
        )
        return True
    except Exception as e:
        logger.error(f"send_email: DB update after send failed for {log_id}: {e}")
        return False


def _mark_failed(log_id: str, reason: str):
    """Set a log row to 'failed' and record the reason in suppression_reason."""
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE drip_email_queue
                SET status = 'failed',
                    suppression_reason = %s
                WHERE id = %s
                """,
                (reason, log_id),
            )
    except Exception as e:
        logger.error(f"_mark_failed: could not update log {log_id}: {e}")
