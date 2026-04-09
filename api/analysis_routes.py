"""Blueprint: POST /v1/analyse — Free 5-min language snapshot."""

import json
from datetime import datetime, timezone

import anthropic
from flask import Blueprint, jsonify, request

from analysis_prompt import SYSTEM_PROMPT as ANALYSIS_SYSTEM, build_analysis_messages
from bot_store import save_analysis

analysis_bp = Blueprint("analysis_bp", __name__)


@analysis_bp.route("/v1/analyse", methods=["POST"])
def analyse():
    from app import claude, _limiter, _get_client_ip

    ip = _get_client_ip()
    if not _limiter.is_allowed(f"analyse:{ip}", max_requests=10, window_seconds=86400):
        return jsonify({"error": "rate_limit", "message": "Too many requests. Please try again tomorrow."}), 429

    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()
    lang = data.get("lang", "en")
    session_id = data.get("session_id", "")
    email = data.get("email")

    if len(text) < 30:
        return jsonify({"error": "Text too short — need at least 30 characters"}), 400
    if len(text) > 3000:
        text = text[:3000]

    messages = build_analysis_messages(text, lang)

    try:
        response = claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1200,
            system=ANALYSIS_SYSTEM,
            messages=messages,
        )
        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        result = json.loads(raw)
    except (json.JSONDecodeError, IndexError, KeyError) as e:
        return jsonify({"error": f"Analysis failed: {e}"}), 500
    except anthropic.APIError as e:
        return jsonify({"error": f"AI service unavailable: {e}"}), 503

    # Store for later use by bot assessment (links free → paid)
    if session_id:
        save_analysis(session_id, result, email, lang, datetime.now(timezone.utc).isoformat())

    return jsonify(result)
