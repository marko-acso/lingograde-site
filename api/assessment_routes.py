"""Blueprint: Paid bot assessment routes."""

import json
import os
import uuid
from datetime import datetime, timedelta, timezone

import anthropic
import stripe
from flask import Blueprint, jsonify, request

from assessment_prompt import (
    SYSTEM_PROMPT as ASSESS_SYSTEM,
    build_start_message,
    build_turn_message,
)
from bot_store import get_analysis, get_assessment, save_assessment, update_assessment
from mini_report import generate_mini_report

assessment_bp = Blueprint("assessment_bp", __name__)


@assessment_bp.route("/v1/assess/start", methods=["POST"])
def assess_start():
    from app import claude

    data = request.get_json(force=True)
    payment_intent_id = data.get("payment_intent_id", "")
    email = (data.get("email") or "").strip()
    prior_session_id = data.get("session_id", "")
    lang = data.get("lang", "en")

    # Verify payment
    try:
        pi = stripe.PaymentIntent.retrieve(payment_intent_id)
        if pi.status != "succeeded":
            return jsonify({"error": "Payment not completed"}), 402
    except stripe.StripeError as e:
        return jsonify({"error": f"Payment verification failed: {e}"}), 400

    # Check for prior free analysis
    prior_record = get_analysis(prior_session_id) if prior_session_id else None
    prior = prior_record.get("result") if prior_record else None

    # Generate first AI message
    start_msg = build_start_message(lang, prior)
    try:
        response = claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            system=ASSESS_SYSTEM,
            messages=[start_msg],
        )
        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        first = json.loads(raw)
    except (json.JSONDecodeError, anthropic.APIError) as e:
        return jsonify({"error": f"Failed to start session: {e}"}), 500

    assess_id = str(uuid.uuid4())
    save_assessment(assess_id, {
        "stripe_session_id": payment_intent_id,
        "email": email,
        "lang": lang,
        "status": "active",
        "turns": [
            {"role": "user", "content": start_msg["content"]},
            {"role": "assistant", "content": response.content[0].text},
        ],
        "result": None,
        "phase": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })

    return jsonify({
        "assess_session_id": assess_id,
        "first_message": first.get("response", ""),
    })


@assessment_bp.route("/v1/assess/turn", methods=["POST"])
def assess_turn():
    from app import claude, REPORT_DIR, _DRIP_ENABLED

    data = request.get_json(force=True)
    assess_id = data.get("assess_session_id", "")
    message = (data.get("message") or "").strip()

    session = get_assessment(assess_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    if session["status"] != "active":
        return jsonify({"error": "Session already completed"}), 400
    # Expire sessions after 2 hours
    created = session.get("created_at", "")
    if created:
        try:
            created_dt = datetime.fromisoformat(created)
            if datetime.now(timezone.utc) - created_dt > timedelta(hours=2):
                update_assessment(assess_id, status="expired")
                return jsonify({"error": "Session expired. Please start a new assessment."}), 410
        except (ValueError, TypeError):
            pass
    if not message:
        return jsonify({"error": "Empty message"}), 400
    if len(message) > 5000:
        message = message[:5000]

    # Add student message to conversation
    turn_msg = build_turn_message(message)
    turns = session["turns"]
    turns.append({"role": "user", "content": turn_msg["content"]})

    try:
        response = claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            system=ASSESS_SYSTEM,
            messages=turns,
        )
        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        parsed = json.loads(raw)
    except (json.JSONDecodeError, anthropic.APIError) as e:
        return jsonify({"error": f"AI response failed: {e}"}), 500

    # Store assistant response
    turns.append({"role": "assistant", "content": response.content[0].text})

    bot_response = parsed.get("response", "")
    is_complete = parsed.get("complete", False)

    if is_complete:
        result = parsed.get("result", {})
        report_path = os.path.join(
            REPORT_DIR,
            f"LingoGrade_Bot_Report_{assess_id}.pdf",
        )
        generate_mini_report(result, session["lang"], session["email"], report_path)
        update_assessment(assess_id,
            status="completed", turns=turns,
            result=result,
        )

        if _DRIP_ENABLED:
            try:
                import drip_engine
                cefr = (result or {}).get("cefr_level", "")
                drip_engine.enqueue_post_assessment(
                    email=session["email"],
                    language=session["lang"],
                    cefr_level=cefr,
                    assess_id=assess_id,
                )
            except Exception:
                pass  # Drip failure must not break assessment response

        return jsonify({
            "response": bot_response,
            "complete": True,
            "result": result,
            "report_url": f"/v1/assess/report/{assess_id}",
        })

    update_assessment(assess_id, turns=turns)

    return jsonify({
        "response": bot_response,
        "complete": False,
    })


@assessment_bp.route("/v1/assess/report/<assess_id>", methods=["GET"])
def assess_report(assess_id):
    from app import REPORT_DIR

    session = get_assessment(assess_id)
    if not session:
        from flask import abort
        abort(404)
    report_path = os.path.join(REPORT_DIR, f"LingoGrade_Bot_Report_{assess_id}.pdf")
    if not os.path.exists(report_path):
        from flask import abort
        abort(404)
    from flask import send_file
    return send_file(
        report_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="LingoGrade_Bot_Report.pdf",
    )
