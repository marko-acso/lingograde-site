"""
Persistent storage for bot analyses and assessments.
Uses PostgreSQL via db_pool when DATABASE_URL is set,
falls back to in-memory dicts for local dev.
"""

import json
import threading
import uuid as _uuid
from datetime import datetime, timezone, timedelta

from db_pool import get_pool, get_cursor


def _is_valid_uuid(val):
    try:
        _uuid.UUID(str(val))
        return True
    except (ValueError, AttributeError):
        return False


# ── In-memory fallback (local dev without Postgres) ──
_analyses = {}
_assessments = {}
_mem_lock = threading.Lock()
_MEM_MAX_AGE = timedelta(days=7)


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
# Production schema: id (UUID), stripe_session_id, email, language,
#   paid, conversation (JSONB), report_data (JSONB), phase, status,
#   created_at, completed_at
# ═══════════════════════════════════════════════════════════════════

def save_assessment(assess_id, data):
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                """INSERT INTO bot_assessments
                   (id, stripe_session_id, email, language,
                    paid, conversation, report_data, phase, status, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    assess_id,
                    data["stripe_session_id"],
                    data["email"],
                    data["lang"],
                    data.get("paid", False),
                    json.dumps(data["turns"]),
                    json.dumps(data["result"]) if data.get("result") else None,
                    data.get("phase", 1),
                    data["status"],
                    data["created_at"],
                ),
            )
    else:
        _assessments[assess_id] = data


def get_assessment(assess_id):
    """Returns session dict with app-friendly keys, or None."""
    if not _is_valid_uuid(assess_id):
        return None
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                """SELECT id, stripe_session_id, email, language,
                          paid, conversation, report_data, phase, status,
                          created_at, completed_at
                   FROM bot_assessments WHERE id = %s""",
                (assess_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            r = dict(row)
            # Map DB columns to app-friendly keys
            r["assess_id"] = str(r.pop("id"))
            r["stripe_session_id"] = r["stripe_session_id"]
            r["lang"] = r.pop("language")
            r["turns"] = r.pop("conversation")
            r["turn_count"] = len(r["turns"]) // 2 if r["turns"] else 0
            r["result"] = r.pop("report_data")
            r["payment_confirmed"] = r.pop("paid")
            return r
    else:
        return _assessments.get(assess_id)


def update_assessment(assess_id, **fields):
    if not _is_valid_uuid(assess_id):
        return
    # Map app-level field names to DB column names
    field_map = {
        "status": "status",
        "turns": "conversation",
        "result": "report_data",
        "payment_confirmed": "paid",
        "phase": "phase",
    }
    if _has_db():
        sets = []
        vals = []
        for k, v in fields.items():
            col = field_map.get(k)
            if not col:
                continue
            sets.append(f"{col} = %s")
            if k in ("turns", "result"):
                vals.append(json.dumps(v) if v is not None else None)
            else:
                vals.append(v)
        # Auto-set completed_at when status becomes 'completed'
        if fields.get("status") == "completed":
            sets.append("completed_at = now()")
        if not sets:
            return
        vals.append(assess_id)
        with get_cursor() as cur:
            cur.execute(
                f"UPDATE bot_assessments SET {', '.join(sets)} WHERE id = %s",  # nosec B608 — keys from field_map allowlist
                vals,
            )
    else:
        session = _assessments.get(assess_id)
        if session:
            session.update(fields)


# ═══════════════════════════════════════════════════════════════════
# Free Bot Conversations (free 5-min chatbot)
# ═══════════════════════════════════════════════════════════════════

_free_bots = {}


def save_free_bot(bot_id, data):
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                """INSERT INTO free_bot_sessions
                   (bot_id, session_id, lang, status, turns, turn_count, result, ip, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    bot_id,
                    data.get("session_id", ""),
                    data["lang"],
                    data["status"],
                    json.dumps(data["turns"]),
                    data["turn_count"],
                    json.dumps(data["result"]) if data.get("result") else None,
                    data.get("ip", ""),
                    data["created_at"],
                ),
            )
    else:
        _free_bots[bot_id] = data


def get_free_bot(bot_id):
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                """SELECT bot_id, session_id, lang, status, turns, turn_count, result, ip, created_at
                   FROM free_bot_sessions WHERE bot_id = %s""",
                (bot_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None
    else:
        return _free_bots.get(bot_id)


def update_free_bot(bot_id, **fields):
    if _has_db():
        allowed = {"status", "turns", "turn_count", "result", "email"}
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
        vals.append(bot_id)
        with get_cursor() as cur:
            cur.execute(
                f"UPDATE free_bot_sessions SET {', '.join(sets)} WHERE bot_id = %s",  # nosec B608 — keys from allowed set
                vals,
            )
    else:
        session = _free_bots.get(bot_id)
        if session:
            session.update(fields)


def upsert_lead(email, lang, source, cefr=None):
    """Store a lead from free-bot or free-analysis for nurture sequence."""
    if not email or not _has_db():
        return
    with get_cursor() as cur:
        cur.execute(
            """INSERT INTO leads (email, lang, source, cefr_estimate, created_at)
               VALUES (%s, %s, %s, %s, now())
               ON CONFLICT (email) DO UPDATE
               SET lang = EXCLUDED.lang,
                   cefr_estimate = COALESCE(EXCLUDED.cefr_estimate, leads.cefr_estimate),
                   last_seen_at = now()""",
            (email.lower().strip(), lang, source, cefr),
        )


def count_free_bot_by_ip(ip, since_iso):
    """Count free bot sessions from an IP since a timestamp (rate limiting)."""
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                """SELECT COUNT(*) as cnt FROM free_bot_sessions
                   WHERE ip = %s AND created_at > %s""",
                (ip, since_iso),
            )
            return cur.fetchone()["cnt"]
    else:
        from datetime import datetime
        cutoff = datetime.fromisoformat(since_iso)
        return sum(
            1 for s in _free_bots.values()
            if s.get("ip") == ip and datetime.fromisoformat(s["created_at"]) > cutoff
        )


def find_assessment_by_payment(stripe_session_id):
    """Find assessment by Stripe session ID (for webhook)."""
    if _has_db():
        with get_cursor() as cur:
            cur.execute(
                "SELECT id FROM bot_assessments WHERE stripe_session_id = %s",
                (stripe_session_id,),
            )
            row = cur.fetchone()
            return str(row["id"]) if row else None
    else:
        for aid, session in _assessments.items():
            if session.get("stripe_session_id") == stripe_session_id:
                return aid
        return None


def cleanup_mem():
    """Remove stale in-memory sessions older than 7 days. Call periodically."""
    cutoff = (datetime.now(timezone.utc) - _MEM_MAX_AGE).isoformat()
    with _mem_lock:
        for store in (_analyses, _assessments, _free_bots):
            stale = [k for k, v in store.items()
                     if isinstance(v, dict) and v.get("created_at", "") < cutoff]
            for k in stale:
                del store[k]
