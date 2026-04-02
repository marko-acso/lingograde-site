"""
Persistent storage for bot analyses and assessments.
Uses PostgreSQL via db_pool when DATABASE_URL is set,
falls back to in-memory dicts for local dev.
"""

import json

from db_pool import get_pool, get_cursor


# ── In-memory fallback (local dev without Postgres) ──
_analyses = {}
_assessments = {}


def _has_db():
    return get_pool() is not None


# ═══════════════════════════════════════════════════════════════════
# Bot Analyses (free 5-min snapshot)
# ═══════════════════════════════════════════════════════════════════

def save_analysis(session_id, result, email, lang, created_at):
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                """INSERT INTO bot_analyses (session_id, email, lang, result, created_at)
                   VALUES (%s, %s, %s, %s, %s)
                   ON CONFLICT (session_id) DO UPDATE
                   SET result = EXCLUDED.result, email = EXCLUDED.email""",
                (session_id, email, lang, json.dumps(result), created_at),
            )
    else:
        _analyses[session_id] = {
            "result": result, "email": email, "lang": lang, "created_at": created_at,
        }


def get_analysis(session_id):
    """Returns dict with 'result' key, or None."""
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                "SELECT result, email, lang FROM bot_analyses WHERE session_id = %s",
                (session_id,),
            )
            row = cur.fetchone()
            if row:
                return {"result": row["result"], "email": row["email"], "lang": row["lang"]}
            return None
    else:
        return _analyses.get(session_id)


# ═══════════════════════════════════════════════════════════════════
# Bot Assessments (paid chatbot sessions)
# ═══════════════════════════════════════════════════════════════════

def save_assessment(assess_id, data):
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                """INSERT INTO bot_assessments
                   (assess_id, payment_intent_id, email, session_id, lang,
                    status, turns, turn_count, result, report_path, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    assess_id,
                    data["payment_intent_id"],
                    data["email"],
                    data.get("session_id", ""),
                    data["lang"],
                    data["status"],
                    json.dumps(data["turns"]),
                    data["turn_count"],
                    json.dumps(data["result"]) if data.get("result") else None,
                    data.get("report_path"),
                    data["created_at"],
                ),
            )
    else:
        _assessments[assess_id] = data


def get_assessment(assess_id):
    """Returns full session dict, or None."""
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                """SELECT assess_id, payment_intent_id, email, session_id, lang,
                          status, turns, turn_count, result, report_path,
                          payment_confirmed, created_at
                   FROM bot_assessments WHERE assess_id = %s""",
                (assess_id,),
            )
            row = cur.fetchone()
            if row:
                return dict(row)
            return None
    else:
        return _assessments.get(assess_id)


def update_assessment(assess_id, **fields):
    if _has_db():
        allowed = {
            "status", "turns", "turn_count", "result", "report_path", "payment_confirmed",
        }
        sets = []
        vals = []
        for k, v in fields.items():
            if k not in allowed:
                continue
            sets.append(f"{k} = %s")
            if k in ("turns", "result"):
                vals.append(json.dumps(v) if v is not None else None)
            else:
                vals.append(v)
        if not sets:
            return
        vals.append(assess_id)
        with get_cursor() as cur:
            cur.execute(
                f"UPDATE bot_assessments SET {', '.join(sets)} WHERE assess_id = %s",
                vals,
            )
    else:
        session = _assessments.get(assess_id)
        if session:
            session.update(fields)


def find_assessment_by_payment(payment_intent_id):
    """Find assessment by Stripe PaymentIntent ID (for webhook)."""
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                "SELECT assess_id FROM bot_assessments WHERE payment_intent_id = %s",
                (payment_intent_id,),
            )
            row = cur.fetchone()
            return row["assess_id"] if row else None
    else:
        for aid, session in _assessments.items():
            if session.get("payment_intent_id") == payment_intent_id:
                return aid
        return None
