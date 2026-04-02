"""
LingoGrade Bot API — Free analysis + Paid chatbot assessment.
Flask microservice, deployed behind Caddy at api.lingograde.com.
"""

import json
import os
import uuid
from datetime import datetime, timezone

import anthropic
import stripe
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request, send_file
from flask_cors import CORS

from analysis_prompt import SYSTEM_PROMPT as ANALYSIS_SYSTEM, build_analysis_messages
from assessment_prompt import (
    SYSTEM_PROMPT as ASSESS_SYSTEM,
    build_start_message,
    build_turn_message,
)
from mini_report import generate_mini_report
from bot_store import (
    save_analysis, get_analysis,
    save_assessment, get_assessment, update_assessment,
    find_assessment_by_payment,
)

load_dotenv()

# ── Database + student dashboard ──
from db_pool import init_pool
from student_routes import student_bp

app = Flask(__name__)
CORS(
    app,
    origins=[
        os.environ.get("CORS_ORIGIN", "https://www.lingograde.com"),
        "https://www.lingograde.com",
    ],
    supports_credentials=True,
)

# Init DB pool + register student dashboard blueprint
init_pool(app)
app.register_blueprint(student_bp)

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
REPORT_DIR = os.environ.get("REPORT_DIR", "/tmp/lingograde-reports")
os.makedirs(REPORT_DIR, exist_ok=True)

claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── Storage via bot_store (Postgres when DATABASE_URL is set, else in-memory) ──


# ═══════════════════════════════════════════════════════════════════
# Endpoint 1: POST /v1/analyse — Free 5-min language snapshot
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/analyse", methods=["POST"])
def analyse():
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


# ═══════════════════════════════════════════════════════════════════
# Endpoint 2: POST /v1/payment/intent — Create Stripe PaymentIntent
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/payment/intent", methods=["POST"])
def create_payment_intent():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip()
    session_id = data.get("session_id", "")
    package = data.get("package", "bot-assessment")

    if not email or "@" not in email:
        return jsonify({"error": "Valid email required"}), 400

    if package != "bot-assessment":
        return jsonify({"error": "Unknown package"}), 400

    try:
        intent = stripe.PaymentIntent.create(
            amount=4995,  # EUR 49.95
            currency="eur",
            receipt_email=email,
            metadata={"session_id": session_id, "package": package},
            description="LingoGrade Chatbot Assessment",
        )
    except stripe.StripeError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"client_secret": intent.client_secret})


# ═══════════════════════════════════════════════════════════════════
# Endpoint 3: POST /v1/assess/start — Begin bot assessment session
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/assess/start", methods=["POST"])
def assess_start():
    data = request.get_json(force=True)
    payment_intent_id = data.get("payment_intent_id", "")
    email = (data.get("email") or "").strip()
    session_id = data.get("session_id", "")
    lang = data.get("lang", "en")

    # Verify payment
    try:
        pi = stripe.PaymentIntent.retrieve(payment_intent_id)
        if pi.status != "succeeded":
            return jsonify({"error": "Payment not completed"}), 402
    except stripe.StripeError as e:
        return jsonify({"error": f"Payment verification failed: {e}"}), 400

    # Check for prior free analysis
    prior_record = get_analysis(session_id) if session_id else None
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

    assess_id = "as_" + uuid.uuid4().hex[:16]
    save_assessment(assess_id, {
        "payment_intent_id": payment_intent_id,
        "email": email,
        "session_id": session_id,
        "lang": lang,
        "status": "active",
        "turns": [
            {"role": "user", "content": start_msg["content"]},
            {"role": "assistant", "content": response.content[0].text},
        ],
        "turn_count": 1,
        "result": None,
        "report_path": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })

    return jsonify({
        "assess_session_id": assess_id,
        "first_message": first.get("response", ""),
    })


# ═══════════════════════════════════════════════════════════════════
# Endpoint 4: POST /v1/assess/turn — Send a message in assessment
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/assess/turn", methods=["POST"])
def assess_turn():
    data = request.get_json(force=True)
    assess_id = data.get("assess_session_id", "")
    message = (data.get("message") or "").strip()

    session = get_assessment(assess_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    if session["status"] != "active":
        return jsonify({"error": "Session already completed"}), 400
    if not message:
        return jsonify({"error": "Empty message"}), 400

    # Add student message to conversation
    turn_msg = build_turn_message(message)
    turns = session["turns"]
    turns.append({"role": "user", "content": turn_msg["content"]})
    turn_count = session["turn_count"] + 1

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
            status="complete", turns=turns, turn_count=turn_count,
            result=result, report_path=report_path,
        )

        return jsonify({
            "response": bot_response,
            "complete": True,
            "result": result,
            "report_url": f"/v1/assess/report/{assess_id}",
        })

    update_assessment(assess_id, turns=turns, turn_count=turn_count)

    return jsonify({
        "response": bot_response,
        "complete": False,
    })


# ═══════════════════════════════════════════════════════════════════
# Endpoint 5: GET /v1/assess/report/<id> — Download mini-report PDF
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/assess/report/<assess_id>", methods=["GET"])
def assess_report(assess_id):
    session = get_assessment(assess_id)
    if not session:
        abort(404)
    if not session.get("report_path") or not os.path.exists(session["report_path"]):
        abort(404)
    return send_file(
        session["report_path"],
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"LingoGrade_Bot_Report.pdf",
    )


# ═══════════════════════════════════════════════════════════════════
# Endpoint 6: POST /v1/stripe/webhook — Stripe event handler
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/stripe/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig = request.headers.get("Stripe-Signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except (stripe.SignatureVerificationError, ValueError):
        abort(400)

    if event["type"] == "payment_intent.succeeded":
        pi = event["data"]["object"]
        matched_id = find_assessment_by_payment(pi["id"])
        if matched_id:
            update_assessment(matched_id, payment_confirmed=True)

    return jsonify({"status": "ok"})


# ═══════════════════════════════════════════════════════════════════
# Endpoint 7: GET /v1/config — Public frontend config
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/config", methods=["GET"])
def frontend_config():
    pk = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
    if not pk:
        return jsonify({"error": "Stripe not configured"}), 503
    return jsonify({"stripe_pk": pk})


# ═══════════════════════════════════════════════════════════════════
# Health check
# ═══════════════════════════════════════════════════════════════════

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "lingograde-bot-api"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
