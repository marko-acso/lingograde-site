"""
Extended dashboard API — Blueprint mounted at /api/dashboard.
Covers subscriptions, referrals, partner earnings, sticker read endpoints.
Sticker verification POST lives in app.py (/v1/stickers/verify) with full anti-abuse.
"""

from flask import Blueprint, g, jsonify, request

from auth import require_auth
from db_pool import get_cursor


def _mask_email(email: str) -> str:
    """m***@gmail.com"""
    local, _, domain = email.partition("@")
    if not domain or len(local) < 2:
        return "***@" + (domain or "***")
    return local[0] + "***@" + domain

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


# ═══════════════════════════════════════════════════════════════════
# GET /api/dashboard/subscription
# ═══════════════════════════════════════════════════════════════════

@dashboard_bp.route("/subscription", methods=["GET"])
@require_auth
def get_subscription():
    with get_cursor() as cur:
        cur.execute(
            """SELECT id, tier, status, currency, amount_cents, billing_interval,
                      first_session_date, next_session_date, session_time,
                      reassessment_date, started_at, cancelled_at
               FROM subscriptions
               WHERE student_id = %s AND status = 'active'
               ORDER BY started_at DESC LIMIT 1""",
            (g.student_id,),
        )
        row = cur.fetchone()

    if not row:
        return jsonify({"subscription": None})

    return jsonify({"subscription": {
        "id": str(row["id"]),
        "tier": row["tier"],
        "status": row["status"],
        "currency": row["currency"],
        "amount_cents": row["amount_cents"],
        "interval": row["billing_interval"],
        "first_session_date": row["first_session_date"].isoformat() if row["first_session_date"] else None,
        "next_session_date": row["next_session_date"].isoformat() if row["next_session_date"] else None,
        "session_time": row["session_time"].isoformat() if row["session_time"] else None,
        "reassessment_date": row["reassessment_date"].isoformat() if row["reassessment_date"] else None,
        "started_at": row["started_at"].isoformat() if row["started_at"] else None,
    }})


# ═══════════════════════════════════════════════════════════════════
# GET /api/dashboard/referrals
# ═══════════════════════════════════════════════════════════════════

@dashboard_bp.route("/referrals", methods=["GET"])
@require_auth
def get_referrals():
    with get_cursor() as cur:
        cur.execute(
            """SELECT id, referred_email, source, status,
                      credited_amount_cents, credited_at, created_at
               FROM referrals
               WHERE partner_id = %s
               ORDER BY created_at DESC
               LIMIT 100""",
            (g.student_id,),
        )
        rows = cur.fetchall()

    referrals = []
    for r in rows:
        referrals.append({
            "id": str(r["id"]),
            "referred_email": _mask_email(r["referred_email"]),
            "source": r["source"],
            "status": r["status"],
            "credited_amount_cents": r["credited_amount_cents"],
            "credited_at": r["credited_at"].isoformat() if r["credited_at"] else None,
            "created_at": r["created_at"].isoformat(),
        })

    return jsonify({"referrals": referrals})


# ═══════════════════════════════════════════════════════════════════
# GET /api/dashboard/earnings
# ═══════════════════════════════════════════════════════════════════

@dashboard_bp.route("/earnings", methods=["GET"])
@require_auth
def get_earnings():
    with get_cursor() as cur:
        # Balance summary
        cur.execute(
            """SELECT
                   COALESCE(SUM(CASE WHEN type != 'payout' THEN amount_cents ELSE 0 END), 0) AS earned_cents,
                   COALESCE(SUM(CASE WHEN type = 'payout' THEN ABS(amount_cents) ELSE 0 END), 0) AS paid_out_cents
               FROM partner_earnings
               WHERE partner_id = %s""",
            (g.student_id,),
        )
        summary = cur.fetchone()

        # Recent transactions
        cur.execute(
            """SELECT id, type, amount_cents, currency, description, created_at
               FROM partner_earnings
               WHERE partner_id = %s
               ORDER BY created_at DESC
               LIMIT 50""",
            (g.student_id,),
        )
        rows = cur.fetchall()

    earned = summary["earned_cents"]
    paid = summary["paid_out_cents"]

    transactions = []
    for r in rows:
        transactions.append({
            "id": str(r["id"]),
            "type": r["type"],
            "amount_cents": r["amount_cents"],
            "currency": r["currency"],
            "description": r["description"],
            "created_at": r["created_at"].isoformat(),
        })

    return jsonify({
        "earned_cents": earned,
        "paid_out_cents": paid,
        "balance_cents": earned - paid,
        "transactions": transactions,
    })


# ═══════════════════════════════════════════════════════════════════
# GET /api/dashboard/stickers
# ═══════════════════════════════════════════════════════════════════

@dashboard_bp.route("/stickers", methods=["GET"])
@require_auth
def get_stickers():
    with get_cursor() as cur:
        cur.execute(
            """SELECT id, sticker_uuid, city, country, status,
                      submitted_at, verified_at
               FROM sticker_verifications
               WHERE student_id = %s
               ORDER BY submitted_at DESC
               LIMIT 100""",
            (g.student_id,),
        )
        rows = cur.fetchall()

    stickers = []
    for r in rows:
        stickers.append({
            "id": str(r["id"]),
            "sticker_uuid": r["sticker_uuid"],
            "city": r["city"],
            "country": r["country"],
            "status": r["status"],
            "submitted_at": r["submitted_at"].isoformat() if r["submitted_at"] else None,
            "verified_at": r["verified_at"].isoformat() if r["verified_at"] else None,
        })

    return jsonify({"stickers": stickers})


# POST /api/dashboard/stickers/verify — REMOVED
# Use POST /v1/stickers/verify instead (has full 7-layer anti-abuse protection)
