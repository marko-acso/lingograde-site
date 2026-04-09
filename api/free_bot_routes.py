"""Blueprint: Free 5-min conversation bot routes."""

import json
import uuid
from datetime import datetime, timedelta, timezone

import anthropic
from flask import Blueprint, jsonify, request

from bot_store import (
    count_free_bot_by_ip,
    get_analysis,
    get_free_bot,
    save_free_bot,
    update_free_bot,
)
from free_bot_prompt import (
    SYSTEM_PROMPT as FREE_BOT_SYSTEM,
    build_start_message as free_bot_start_message,
    build_turn_message as free_bot_turn_message,
)

free_bot_bp = Blueprint("free_bot_bp", __name__)

FREE_BOT_MAX_TURNS = 8
FREE_BOT_RATE_LIMIT = 3  # per IP per 24h


@free_bot_bp.route("/v1/free-bot/start", methods=["POST"])
def free_bot_start():
    from app import claude

    data = request.get_json(force=True)
    lang = data.get("lang", "en")
    session_id = data.get("session_id", "")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0].strip()

    # Rate limit by IP
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    if count_free_bot_by_ip(ip, cutoff) >= FREE_BOT_RATE_LIMIT:
        return jsonify({"error": "rate_limit", "message": "You have reached today's limit. Come back tomorrow."}), 429

    # Check for prior free analysis
    prior_record = get_analysis(session_id) if session_id else None
    prior = prior_record.get("result") if prior_record else None

    start_msg = free_bot_start_message(lang, prior)
    try:
        response = claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            system=FREE_BOT_SYSTEM,
            messages=[start_msg],
        )
        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        first = json.loads(raw)
    except (json.JSONDecodeError, anthropic.APIError) as e:
        return jsonify({"error": f"Failed to start conversation: {e}"}), 500

    bot_id = "fb_" + uuid.uuid4().hex[:16]
    save_free_bot(bot_id, {
        "session_id": session_id,
        "lang": lang,
        "status": "active",
        "turns": [
            {"role": "user", "content": start_msg["content"]},
            {"role": "assistant", "content": response.content[0].text},
        ],
        "turn_count": 1,
        "result": None,
        "ip": ip,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })

    return jsonify({
        "bot_id": bot_id,
        "first_message": first.get("response", ""),
    })


@free_bot_bp.route("/v1/free-bot/turn", methods=["POST"])
def free_bot_turn():
    from app import claude

    data = request.get_json(force=True)
    bot_id = data.get("bot_id", "")
    message = (data.get("message") or "").strip()

    session = get_free_bot(bot_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    if session["status"] != "active":
        return jsonify({"error": "Conversation already completed"}), 400
    if not message:
        return jsonify({"error": "Empty message"}), 400
    if len(message) > 2000:
        message = message[:2000]

    turns = session["turns"]
    turn_msg = free_bot_turn_message(message)
    turns.append({"role": "user", "content": turn_msg["content"]})
    turn_count = session["turn_count"] + 1

    # Force completion after max turns
    force_complete = turn_count >= FREE_BOT_MAX_TURNS
    extra_instruction = ""
    if force_complete:
        extra_instruction = "\n\n[SYSTEM: This is the final turn. You MUST set complete: true and include the full result object now.]"

    messages = turns[:]
    if extra_instruction:
        messages[-1] = {"role": "user", "content": messages[-1]["content"] + extra_instruction}

    try:
        response = claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600 if force_complete else 300,
            system=FREE_BOT_SYSTEM,
            messages=messages,
        )
        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        parsed = json.loads(raw)
    except (json.JSONDecodeError, anthropic.APIError) as e:
        return jsonify({"error": f"AI response failed: {e}"}), 500

    turns.append({"role": "assistant", "content": response.content[0].text})

    bot_response = parsed.get("response", "")
    is_complete = parsed.get("complete", False)

    if is_complete or force_complete:
        result = parsed.get("result", {})
        update_free_bot(bot_id, status="complete", turns=turns, turn_count=turn_count, result=result)
        return jsonify({
            "response": bot_response,
            "complete": True,
            "result": result,
        })

    update_free_bot(bot_id, turns=turns, turn_count=turn_count)
    return jsonify({
        "response": bot_response,
        "complete": False,
        "turn": turn_count,
        "max_turns": FREE_BOT_MAX_TURNS,
    })


@free_bot_bp.route("/v1/free-bot/email", methods=["POST"])
def free_bot_email():
    data = request.get_json(force=True)
    bot_id = data.get("bot_id", "")
    email = (data.get("email") or "").strip()

    if not bot_id:
        return jsonify({"error": "bot_id required"}), 400
    if not email or "@" not in email:
        return jsonify({"error": "Valid email required"}), 400

    session = get_free_bot(bot_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    update_free_bot(bot_id, email=email)
    return jsonify({"status": "ok"})


@free_bot_bp.route("/v1/free-bot/complete/<bot_id>", methods=["GET"])
def free_bot_complete(bot_id):
    session = get_free_bot(bot_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    if session["status"] != "complete":
        return jsonify({
            "complete": False,
            "status": session["status"],
            "turn_count": session["turn_count"],
            "max_turns": FREE_BOT_MAX_TURNS,
        })

    return jsonify({
        "complete": True,
        "result": session["result"],
        "lang": session["lang"],
    })
