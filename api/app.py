"""
LingoGrade Bot API — Free analysis + Paid chatbot assessment.
Flask microservice, deployed behind Caddy at api.lingograde.com.
"""

import json
import os
import uuid
from datetime import datetime, timezone

import anthropic
import requests as http_requests
import stripe
from dotenv import load_dotenv
from flask import Flask, abort, g, jsonify, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from analysis_prompt import SYSTEM_PROMPT as ANALYSIS_SYSTEM, build_analysis_messages
from assessment_prompt import (
    SYSTEM_PROMPT as ASSESS_SYSTEM,
    build_start_message,
    build_turn_message,
)
from free_bot_prompt import (
    SYSTEM_PROMPT as FREE_BOT_SYSTEM,
    build_start_message as free_bot_start_message,
    build_turn_message as free_bot_turn_message,
)
from mini_report import generate_mini_report
from invoice_generator import generate_invoice, get_invoice_pdf, get_invoices_by_email
from bot_store import (
    save_analysis, get_analysis,
    save_assessment, get_assessment, update_assessment,
    find_assessment_by_payment,
    save_free_bot, get_free_bot, update_free_bot, count_free_bot_by_ip,
    upsert_lead,
)

load_dotenv()

# ── Database + student dashboard ──
from db_pool import init_pool, get_cursor
from student_routes import student_bp
from dashboard_routes import dashboard_bp
from auth import require_auth

try:
    import drip_engine
    _DRIP_ENABLED = True
except Exception:
    _DRIP_ENABLED = False

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
app.register_blueprint(dashboard_bp)

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
# Endpoint 2a: POST /v1/free-bot/start — Begin free 5-min conversation
# ═══════════════════════════════════════════════════════════════════

FREE_BOT_MAX_TURNS = 8
FREE_BOT_RATE_LIMIT = 3  # per IP per 24h

@app.route("/v1/free-bot/start", methods=["POST"])
def free_bot_start():
    data = request.get_json(force=True)
    lang = data.get("lang", "en")
    session_id = data.get("session_id", "")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0].strip()

    # Rate limit by IP
    from datetime import timedelta
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


# ═══════════════════════════════════════════════════════════════════
# Endpoint 2b: POST /v1/free-bot/turn — Send a message in free conversation
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/free-bot/turn", methods=["POST"])
def free_bot_turn():
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


# ═══════════════════════════════════════════════════════════════════
# Endpoint 2c: POST /v1/free-bot/email — Attach email to free bot session
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/free-bot/email", methods=["POST"])
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

    # Store as lead for nurture sequence
    lang = session.get("lang", "")
    cefr = None
    result = session.get("result")
    if isinstance(result, dict):
        cefr = result.get("cefr")
    elif isinstance(result, str):
        try:
            cefr = json.loads(result).get("cefr")
        except (json.JSONDecodeError, AttributeError):
            pass
    upsert_lead(email, lang, "free-bot", cefr)

    return jsonify({"status": "ok"})


# ═══════════════════════════════════════════════════════════════════
# Endpoint 2d: GET /v1/free-bot/complete/<bot_id> — Retrieve completed result
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/free-bot/complete/<bot_id>", methods=["GET"])
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


# ═══════════════════════════════════════════════════════════════════
# Endpoint 3: POST /v1/payment/intent — Create Stripe PaymentIntent
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


# ═══════════════════════════════════════════════════════════════════
# Endpoint 5: GET /v1/assess/report/<id> — Download mini-report PDF
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/assess/report/<assess_id>", methods=["GET"])
def assess_report(assess_id):
    session = get_assessment(assess_id)
    if not session:
        abort(404)
    report_path = os.path.join(REPORT_DIR, f"LingoGrade_Bot_Report_{assess_id}.pdf")
    if not os.path.exists(report_path):
        abort(404)
    return send_file(
        report_path,
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

        # Generate invoice for direct PaymentIntent payments
        try:
            customer_email = (pi.get("receipt_email")
                              or pi.get("metadata", {}).get("email", ""))
            if customer_email and pi.get("amount"):
                generate_invoice(
                    customer_email=customer_email,
                    customer_name=pi.get("metadata", {}).get("customer_name"),
                    line_items=[{
                        "description": "LingoGrade Bot Assessment",
                        "quantity": 1,
                        "unit_price_cents": pi["amount"],
                    }],
                    total_cents=pi["amount"],
                    currency=(pi.get("currency") or "eur").upper(),
                    stripe_payment_intent_id=pi["id"],
                    product_type="bot_assessment",
                )
        except Exception:
            pass  # Invoice failure must not break webhook

    elif event["type"] == "checkout.session.completed":
        cs = event["data"]["object"]
        meta = cs.get("metadata", {})

        if meta.get("product_type") == "kids_assessment":
            # Record kids booking in DB
            try:
                with get_cursor() as cur:
                    cur.execute(
                        """INSERT INTO kids_bookings
                           (parent_email, child_name, age_group, package,
                            guardian_name, stripe_session_id, amount_cents, currency)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            meta.get("parent_email"),
                            meta.get("child_name"),
                            meta.get("age_group"),
                            meta.get("package"),
                            meta.get("guardian_name"),
                            cs["id"],
                            cs.get("amount_total", 0),
                            cs.get("currency", "eur"),
                        ),
                    )
            except Exception:
                pass  # Stripe is source of truth; DB is supplementary

        elif meta.get("product_type") == "homework":
            # Create homework record for the student after payment
            customer_email = cs.get("customer_email") or cs.get("customer_details", {}).get("email", "")
            hw_type = meta.get("homework_type", "A")
            if customer_email:
                try:
                    from datetime import timedelta
                    deadline = datetime.now(timezone.utc) + timedelta(days=14)
                    with get_cursor() as cur:
                        # Find student by email
                        cur.execute("SELECT id FROM students WHERE email = %s", (customer_email,))
                        student = cur.fetchone()
                        if student:
                            cur.execute(
                                """INSERT INTO homework
                                   (id, student_id, title, type, status, deadline)
                                   VALUES (%s, %s, %s, %s, 'pending', %s)""",
                                (
                                    str(uuid.uuid4()),
                                    student["id"],
                                    "Homework Check",
                                    hw_type,
                                    deadline,
                                ),
                            )
                except Exception:
                    pass  # Stripe is source of truth

        elif meta.get("product_type") == "mega_bundle":
            customer_email = cs.get("customer_email") or cs.get("customer_details", {}).get("email", "")
            if customer_email:
                try:
                    with get_cursor() as cur:
                        # Link to student if exists
                        cur.execute("SELECT id FROM students WHERE email = %s", (customer_email,))
                        student = cur.fetchone()
                        student_id = student["id"] if student else None

                        cur.execute(
                            """INSERT INTO pack_purchases
                               (email, student_id, pack_type, stripe_session_id,
                                amount_cents, currency, reassessment_eligible_date)
                               VALUES (%s, %s, 'mega_bundle', %s, %s, %s,
                                       now() + interval '8 weeks')""",
                            (
                                customer_email,
                                student_id,
                                cs["id"],
                                cs.get("amount_total", 29995),
                                cs.get("currency", "eur"),
                            ),
                        )
                except Exception:
                    pass  # Stripe is source of truth

                # Send confirmation email via Resend
                try:
                    resend_key = os.environ.get("RESEND_API_KEY")
                    if resend_key:
                        http_requests.post(
                            "https://api.resend.com/emails",
                            headers={"Authorization": f"Bearer {resend_key}"},
                            json={
                                "from": "LingoGrade <hello@lingograde.com>",
                                "to": [customer_email],
                                "bcc": ["marco@lingograde.com"],
                                "subject": "Your LingoGrade Mega Bundle is ready! / Vaš LingoGrade paket je spreman!",
                                "html": (
                                    "<h2>Your LingoGrade Pack is ready!</h2>"
                                    "<p>Thank you for your purchase. Your Mega Bundle includes:</p>"
                                    "<ul>"
                                    "<li>Full language assessment (55 min)</li>"
                                    "<li>8 weeks of personalised 15-minute lessons</li>"
                                    "<li>Reassessment after 8 weeks</li>"
                                    "</ul>"
                                    "<p><strong>Next step:</strong> Book your assessment in your student dashboard.</p>"
                                    "<p><a href='https://www.lingograde.com/dashboard'>Open Dashboard</a></p>"
                                    "<hr>"
                                    "<h2>Vaš LingoGrade paket je spreman!</h2>"
                                    "<p>Hvala na kupovini. Vaš Mega Bundle uključuje:</p>"
                                    "<ul>"
                                    "<li>Potpuna jezička procjena (55 min)</li>"
                                    "<li>8 sedmica personaliziranih lekcija od 15 minuta</li>"
                                    "<li>Ponovna procjena nakon 8 sedmica</li>"
                                    "</ul>"
                                    "<p><strong>Sljedeći korak:</strong> Zakažite procjenu u svom studentskom dashboardu.</p>"
                                    "<p><a href='https://www.lingograde.com/dashboard'>Otvorite Dashboard</a></p>"
                                ),
                            },
                        )
                except Exception:
                    pass  # Email failure should not block webhook response

        elif meta.get("product_type") == "subscription":
            customer_email = cs.get("customer_email") or cs.get("customer_details", {}).get("email", "")
            if customer_email and _DRIP_ENABLED:
                try:
                    with get_cursor() as cur:
                        cur.execute("SELECT id FROM students WHERE email = %s", (customer_email,))
                        student = cur.fetchone()
                    if student:
                        sub_meta = cs.get("metadata", {})
                        drip_engine.enqueue_subscriber_welcome(
                            email=customer_email,
                            student_id=str(student["id"]),
                            subscription_tier=sub_meta.get("tier", "weekly"),
                            first_session_date=sub_meta.get("first_session_date", "TBD"),
                            first_session_time=sub_meta.get("first_session_time", "TBD"),
                            assessor_name="Marco",
                            homework_included=True,
                        )
                except Exception:
                    pass  # Drip failure must not break webhook

        else:
            matched_id = find_assessment_by_payment(cs["id"])
            if matched_id:
                update_assessment(matched_id, payment_confirmed=True)

        # ── Auto-invoice for ALL checkout sessions ──
        try:
            customer_email = (cs.get("customer_email")
                              or cs.get("customer_details", {}).get("email", ""))
            customer_name = cs.get("customer_details", {}).get("name")
            amount = cs.get("amount_total", 0)
            currency = (cs.get("currency") or "eur").upper()
            product_type = meta.get("product_type", "unknown")

            if customer_email and amount:
                # Build description from product type
                descriptions = {
                    "kids_assessment": f"Kids Assessment — {meta.get('package', 'standard').title()}",
                    "homework": f"Homework Check — Type {meta.get('homework_type', 'A')}",
                    "mega_bundle": "LingoGrade Mega Bundle",
                    "accessory": f"LingoGrade {meta.get('product', 'item').title()}",
                }
                desc = descriptions.get(product_type, f"LingoGrade — {product_type}")

                generate_invoice(
                    customer_email=customer_email,
                    customer_name=customer_name,
                    line_items=[{
                        "description": desc,
                        "quantity": 1,
                        "unit_price_cents": amount,
                    }],
                    total_cents=amount,
                    currency=currency,
                    stripe_session_id=cs["id"],
                    product_type=product_type,
                )
        except Exception:
            pass  # Invoice failure must not break webhook

    return jsonify({"status": "ok"})


# ═══════════════════════════════════════════════════════════════════
# Invoice endpoints
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/invoice/<invoice_id>/pdf", methods=["GET"])
@require_auth
def download_invoice(invoice_id):
    pdf_path = get_invoice_pdf(invoice_id)
    if not pdf_path or not os.path.isfile(pdf_path):
        return jsonify({"error": "Invoice not found"}), 404
    return send_file(
        pdf_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=os.path.basename(pdf_path),
    )


@app.route("/v1/invoices", methods=["GET"])
@require_auth
def list_invoices():
    student_id = g.student_id
    try:
        with get_cursor() as cur:
            cur.execute("SELECT email FROM students WHERE id = %s::uuid", (student_id,))
            row = cur.fetchone()
            if not row:
                return jsonify([])
            email = row["email"]
    except Exception:
        return jsonify([])

    invoices = get_invoices_by_email(email)
    return jsonify([
        {
            "id": str(inv["id"]),
            "number": f"{inv['invoice_number']:010d}",
            "date": inv["issued_at"].isoformat(),
            "total": inv["total_cents"] / 100,
            "currency": inv["currency"],
            "product": inv["product_type"],
        }
        for inv in invoices
    ])


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


# ═══════════════════════════════════════════════════════════════════
# Endpoint 8: POST /v1/checkout/accessory — Stripe Checkout for merch
# ═══════════════════════════════════════════════════════════════════

ACCESSORY_CATALOG = {
    "cap": {
        "name": "LingoGrade Cap",
        "description": "Embroidered Marco logo on navy cotton twill. Adjustable strap.",
        "amount": 2995,  # EUR 29.95
    },
    "bracelet": {
        "name": "Marco Bracelet",
        "description": "Woven fabric bracelet with Marco silhouette clasp. LingoGrade blue with gold accent thread.",
        "amount": 1495,  # EUR 14.95
    },
    "pin": {
        "name": "Marco Enamel Pin",
        "description": "Hard enamel pin of Marco with mortarboard. Gold-plated metal. Butterfly clutch backing.",
        "amount": 1295,  # EUR 12.95
    },
}


@app.route("/v1/checkout/accessory", methods=["POST"])
def checkout_accessory():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip()
    product = (data.get("product") or "").strip().lower()

    if not email or "@" not in email:
        return jsonify({"error": "Valid email required"}), 400

    if product not in ACCESSORY_CATALOG:
        return jsonify({"error": f"Unknown product. Choose: {', '.join(ACCESSORY_CATALOG)}"}), 400

    item = ACCESSORY_CATALOG[product]
    origin = os.environ.get("CORS_ORIGIN", "https://www.lingograde.com")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "unit_amount": item["amount"],
                    "product_data": {
                        "name": item["name"],
                        "description": item["description"],
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            customer_email=email,
            success_url=f"{origin}/shop?purchase=success&product={product}",
            cancel_url=f"{origin}/shop?purchase=cancelled",
            metadata={"product_type": "accessory", "product": product},
        )
    except stripe.StripeError as e:
        return jsonify({"error": str(e)}), 400

    # Track order in DB (best-effort)
    try:
        with get_cursor() as cur:
            cur.execute(
                """INSERT INTO accessory_orders (email, product, amount_cents, stripe_session_id)
                   VALUES (%s, %s, %s, %s)""",
                (email, product, item["amount"], session.id),
            )
    except Exception:
        pass  # DB optional; Stripe is source of truth

    return jsonify({"checkout_url": session.url, "session_id": session.id})


# ═══════════════════════════════════════════════════════════════════
# Endpoint 9: GET /v1/stickers/map — Public sticker placement map data
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/stickers/map", methods=["GET"])
def sticker_map():
    try:
        with get_cursor() as cur:
            cur.execute(
                """SELECT lat, lng, location_label, COUNT(*) as count
                   FROM sticker_placements
                   WHERE status = 'verified'
                   GROUP BY lat, lng, location_label
                   ORDER BY count DESC"""
            )
            rows = cur.fetchall()

            cur.execute(
                """SELECT COUNT(*) as total,
                          COUNT(DISTINCT location_label) as locations
                   FROM sticker_placements
                   WHERE status = 'verified'"""
            )
            stats = cur.fetchone()

        placements = [
            {"lat": r["lat"], "lng": r["lng"],
             "city": r["location_label"] or "Unknown", "count": r["count"]}
            for r in rows
        ]
        return jsonify({
            "placements": placements,
            "stats": {
                "total": stats["total"],
                "countries": stats["locations"],
                "cities": stats["locations"],
            },
        })
    except Exception:
        # DB not available — return empty so frontend uses fallback
        return jsonify({"placements": [], "stats": {"total": 0, "countries": 0, "cities": 0}})


# ═══════════════════════════════════════════════════════════════════
# Endpoint 10: POST /v1/stickers/verify — Submit sticker selfie
# ═══════════════════════════════════════════════════════════════════

STICKER_UPLOAD_DIR = os.environ.get("STICKER_UPLOAD_DIR", "/var/data/lingograde/stickers")
ALLOWED_IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}
MAX_SELFIE_SIZE = 10 * 1024 * 1024  # 10 MB


@app.route("/v1/stickers/verify", methods=["POST"])
@require_auth
def sticker_verify():
    student_id = g.student_id

    sticker_uuid = (request.form.get("sticker_uuid") or "").strip()
    lat = request.form.get("latitude")
    lng = request.form.get("longitude")
    city = request.form.get("city", "")
    country = request.form.get("country", "")

    if not sticker_uuid:
        return jsonify({"error": "Sticker QR code required"}), 400
    if not lat or not lng:
        return jsonify({"error": "Location required — please enable GPS"}), 400

    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return jsonify({"error": "Invalid coordinates"}), 400

    # Velocity throttle: max 3/day per student
    try:
        with get_cursor() as cur:
            cur.execute(
                """SELECT COUNT(*) as cnt FROM sticker_placements
                   WHERE student_id = %s::uuid
                   AND submitted_at > now() - interval '24 hours'""",
                (student_id,),
            )
            if cur.fetchone()["cnt"] >= 3:
                return jsonify({"error": "You have reached today's limit. Try again tomorrow."}), 429

            # GPS uniqueness: max 3 within 50m — Haversine in Python
            cur.execute(
                """SELECT lat, lng FROM sticker_placements
                   WHERE student_id = %s::uuid""",
                (student_id,),
            )
            import math
            def _hav(la1, lo1, la2, lo2):
                R = 6371000
                rl1, rl2 = math.radians(la1), math.radians(la2)
                dl, dg = math.radians(la2 - la1), math.radians(lo2 - lo1)
                a = math.sin(dl/2)**2 + math.cos(rl1)*math.cos(rl2)*math.sin(dg/2)**2
                return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            nearby = sum(1 for p in cur.fetchall() if _hav(lat, lng, p["lat"], p["lng"]) < 50)
    except Exception:
        nearby = 0

    if nearby >= 3:
        return jsonify({"error": "Too many stickers in this area. Spread them around."}), 400

    # File upload
    selfie = request.files.get("selfie")
    if not selfie:
        return jsonify({"error": "Selfie image required"}), 400

    ext = os.path.splitext(selfie.filename or "")[1].lower()
    if ext not in ALLOWED_IMG_EXT:
        return jsonify({"error": f"Allowed formats: {', '.join(ALLOWED_IMG_EXT)}"}), 400

    selfie.seek(0, 2)
    if selfie.tell() > MAX_SELFIE_SIZE:
        return jsonify({"error": "Image too large (max 10 MB)"}), 400
    selfie.seek(0)

    # Save file
    safe_name = f"{uuid.uuid4().hex[:12]}{ext}"
    student_dir = os.path.join(STICKER_UPLOAD_DIR, student_id)
    os.makedirs(student_dir, exist_ok=True)
    save_path = os.path.join(student_dir, safe_name)
    selfie.save(save_path)

    # Create verification record (pending 48h review)
    try:
        with get_cursor() as cur:
            location_label = ", ".join(filter(None, [city, country])) or None
            cur.execute(
                """INSERT INTO sticker_placements
                   (student_id, sticker_uuid, lat, lng, location_label, selfie_path)
                   VALUES (%s::uuid, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (student_id, sticker_uuid, lat, lng, location_label, save_path),
            )
            verification_id = str(cur.fetchone()["id"])
    except Exception as e:
        if "unique" in str(e).lower():
            return jsonify({"error": "This sticker has already been claimed"}), 409
        return jsonify({"error": "Verification submission failed"}), 500

    return jsonify({
        "verification_id": verification_id,
        "status": "pending",
        "message": "Your selfie is being reviewed. You will be notified within 48 hours.",
    }), 201


# ═══════════════════════════════════════════════════════════════════
# Endpoint 11: POST /v1/checkout/kids — Stripe Checkout for kids assessment
# ═══════════════════════════════════════════════════════════════════

KIDS_PACKAGES = {
    "quick": {
        "name": "Kids Quick Check",
        "description": "15-minute assessment for ages 6-17. Pre-A1 to B2. Visual report with parent summary.",
        "amounts": {"eur": 8995, "usd": 8995, "gbp": 8995, "chf": 8995},
    },
    "full": {
        "name": "Kids Full Picture",
        "description": "25-minute assessment for ages 6-17. Pre-A1 to B2. Full report with parent guide + homework.",
        "amounts": {"eur": 12995, "usd": 12995, "gbp": 12995, "chf": 12995},
    },
    "deep-dive": {
        "name": "Kids Deep Dive",
        "description": "40-minute assessment (15+25 with break) for ages 6-17. Comprehensive report + parent consultation.",
        "amounts": {"eur": 24995, "usd": 24995, "gbp": 24995, "chf": 24995},
    },
}

ALLOWED_CURRENCIES = {"eur", "usd", "gbp", "chf"}


@app.route("/v1/checkout/kids", methods=["POST"])
def checkout_kids():
    data = request.get_json(force=True)
    parent_email = (data.get("parent_email") or "").strip()
    child_name = (data.get("child_name") or "").strip()
    age_group = (data.get("age_group") or "").strip()
    package = (data.get("package") or "").strip().lower()
    currency = (data.get("currency") or "eur").strip().lower()
    guardian_name = (data.get("guardian_name") or "").strip()

    if not parent_email or "@" not in parent_email:
        return jsonify({"error": "Valid parent email required"}), 400
    if not child_name:
        return jsonify({"error": "Child's name required"}), 400
    if age_group not in ("6-8", "9-11", "12-14", "15-17"):
        return jsonify({"error": "age_group must be 6-8, 9-11, 12-14, or 15-17"}), 400
    if package not in KIDS_PACKAGES:
        return jsonify({"error": f"Unknown package. Choose: {', '.join(KIDS_PACKAGES)}"}), 400
    if currency not in ALLOWED_CURRENCIES:
        currency = "eur"

    pkg = KIDS_PACKAGES[package]
    amount = pkg["amounts"][currency]
    origin = os.environ.get("CORS_ORIGIN", "https://www.lingograde.com")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": currency,
                    "unit_amount": amount,
                    "product_data": {
                        "name": pkg["name"],
                        "description": pkg["description"],
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            customer_email=parent_email,
            success_url=f"{origin}/kids?purchase=success&package={package}",
            cancel_url=f"{origin}/kids?purchase=cancelled",
            metadata={
                "product_type": "kids_assessment",
                "package": package,
                "child_name": child_name,
                "age_group": age_group,
                "guardian_name": guardian_name,
                "parent_email": parent_email,
            },
            consent_collection={"terms_of_service": "required"},
        )
    except stripe.StripeError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"checkout_url": session.url, "session_id": session.id})


# ═══════════════════════════════════════════════════════════════════
# Endpoint: POST /v1/checkout/mega-bundle — Mega Bundle checkout
# ═══════════════════════════════════════════════════════════════════

@app.route("/v1/checkout/mega-bundle", methods=["POST"])
def checkout_mega_bundle():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip()
    currency = (data.get("currency") or "eur").strip().lower()

    if not email or "@" not in email:
        return jsonify({"error": "Valid email required"}), 400
    if currency not in ALLOWED_CURRENCIES:
        currency = "eur"

    origin = os.environ.get("CORS_ORIGIN", "https://www.lingograde.com")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": currency,
                    "unit_amount": 29995,
                    "product_data": {
                        "name": "LingoGrade Mega Bundle",
                        "description": "Full assessment + 8 weeks of 15-min lessons + reassessment. Everything included.",
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            customer_email=email,
            success_url=f"{origin}/shop?purchase=success&product=mega-bundle",
            cancel_url=f"{origin}/shop?purchase=cancelled",
            metadata={
                "product_type": "mega_bundle",
                "email": email,
            },
            consent_collection={"terms_of_service": "required"},
        )
    except stripe.StripeError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"checkout_url": session.url, "session_id": session.id})


# ═══════════════════════════════════════════════════════════════════
# Endpoint: POST /api/partner-apply — Partner application
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/partner-apply", methods=["POST"])
def partner_apply():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    phone = (data.get("phone") or "").strip()
    institution = (data.get("institution") or "").strip()
    country = (data.get("country") or "").strip()
    languages = (data.get("languages") or "").strip()
    referral_source = (data.get("referral_source") or "").strip()

    if not name or not email or "@" not in email:
        return jsonify({"error": "Name and valid email required"}), 400

    first_name = name.split()[0] if name else ""

    try:
        with get_cursor() as cur:
            cur.execute(
                """INSERT INTO partner_applications
                   (name, email, phone, institution, country, languages, referral_source)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (email) DO UPDATE SET
                       name = EXCLUDED.name,
                       phone = EXCLUDED.phone,
                       institution = EXCLUDED.institution,
                       country = EXCLUDED.country,
                       languages = EXCLUDED.languages,
                       referral_source = EXCLUDED.referral_source,
                       applied_at = NOW()
                   RETURNING id""",
                (name, email, phone, institution, country, languages, referral_source),
            )
            row = cur.fetchone()
            app_id = row[0] if row else None
    except Exception as e:
        app.logger.error(f"partner_apply DB error: {e}")
        return jsonify({"error": "Application could not be saved"}), 500

    # Kick off partner onboarding drip sequence
    if _DRIP_ENABLED:
        try:
            drip_engine.enqueue_partner_onboarding(
                email=email,
                first_name=first_name,
            )
        except Exception as e:
            app.logger.error(f"partner_apply drip error: {e}")

    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
