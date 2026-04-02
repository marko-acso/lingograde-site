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
from flask import Flask, abort, g, jsonify, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

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
from db_pool import init_pool, get_cursor
from student_routes import student_bp
from auth import require_auth

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
                """SELECT latitude, longitude, city, country, COUNT(*) as count
                   FROM sticker_verifications
                   WHERE status = 'verified'
                   GROUP BY latitude, longitude, city, country
                   ORDER BY count DESC"""
            )
            rows = cur.fetchall()

            cur.execute(
                """SELECT COUNT(*) as total,
                          COUNT(DISTINCT country) as countries,
                          COUNT(DISTINCT city) as cities
                   FROM sticker_verifications
                   WHERE status = 'verified'"""
            )
            stats = cur.fetchone()

        placements = [
            {"lat": r["latitude"], "lng": r["longitude"],
             "city": r["city"] or "Unknown", "count": r["count"]}
            for r in rows
        ]
        return jsonify({
            "placements": placements,
            "stats": {
                "total": stats["total"],
                "countries": stats["countries"],
                "cities": stats["cities"],
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
                """SELECT COUNT(*) as cnt FROM sticker_verifications
                   WHERE student_id = %s::uuid
                   AND submitted_at > now() - interval '24 hours'""",
                (student_id,),
            )
            if cur.fetchone()["cnt"] >= 3:
                return jsonify({"error": "You have reached today's limit. Try again tomorrow."}), 429

            # GPS uniqueness: max 3 stickers within 50m radius per account
            cur.execute(
                """SELECT COUNT(*) as cnt FROM sticker_verifications
                   WHERE student_id = %s::uuid
                   AND earth_distance(
                       ll_to_earth(latitude, longitude),
                       ll_to_earth(%s, %s)
                   ) < 50""",
                (student_id, lat, lng),
            )
            nearby = cur.fetchone()["cnt"]
    except Exception:
        nearby = 0  # If earthdistance not installed, skip geo check

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
            cur.execute(
                """INSERT INTO sticker_verifications
                   (student_id, sticker_uuid, latitude, longitude, city, country, selfie_path)
                   VALUES (%s::uuid, %s, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (student_id, sticker_uuid, lat, lng, city, country, save_path),
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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
