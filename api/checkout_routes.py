"""Blueprint: Stripe checkout/payment routes."""

import os
import re
import secrets

import stripe
from flask import Blueprint, jsonify, request

from db_pool import get_cursor
from pricing import (
    BOT_ASSESSMENT_CENTS, KIDS_PACKAGES, MEGA_BUNDLE_CENTS,
    ACCESSORY_CATALOG, ALLOWED_CURRENCIES,
    EXPRESS_HIRING_AUDIT,
    CORPORATE_ASSESSMENT,
)

checkout_bp = Blueprint("checkout_bp", __name__)


@checkout_bp.route("/v1/payment/intent", methods=["POST"])
def create_payment_intent():
    from app import _limiter, _get_client_ip

    ip = _get_client_ip()
    if not _limiter.is_allowed(f"payment:{ip}", max_requests=10, window_seconds=3600):
        return jsonify({"error": "rate_limit", "message": "Too many payment attempts. Please try again later."}), 429

    data = request.get_json(force=True)
    email = (data.get("email") or "").strip()
    session_id = data.get("session_id", "")
    package = data.get("package", "bot-assessment")
    ga_client_id = (data.get("ga_client_id") or "").strip()

    if not email or "@" not in email:
        return jsonify({"error": "Valid email required"}), 400

    if package != "bot-assessment":
        return jsonify({"error": "Unknown package"}), 400

    try:
        intent = stripe.PaymentIntent.create(
            amount=BOT_ASSESSMENT_CENTS,
            currency="eur",
            receipt_email=email,
            metadata={
                "session_id": session_id,
                "package": package,
                "ga_client_id": ga_client_id,
            },
            description="LingoGrade Chatbot Assessment",
        )
    except stripe.StripeError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"client_secret": intent.client_secret})


@checkout_bp.route("/v1/checkout/accessory", methods=["POST"])
def checkout_accessory():
    from app import _limiter, _get_client_ip

    ip = _get_client_ip()
    if not _limiter.is_allowed(f"checkout:{ip}", max_requests=15, window_seconds=3600):
        return jsonify({"error": "rate_limit", "message": "Too many checkout attempts. Please try again later."}), 429

    data = request.get_json(force=True)
    email = (data.get("email") or "").strip()
    product = (data.get("product") or "").strip().lower()
    ga_client_id = (data.get("ga_client_id") or "").strip()

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
            metadata={
                "product_type": "accessory",
                "product": product,
                "ga_client_id": ga_client_id,
            },
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


@checkout_bp.route("/v1/checkout/kids", methods=["POST"])
def checkout_kids():
    from app import _limiter, _get_client_ip

    ip = _get_client_ip()
    if not _limiter.is_allowed(f"checkout:{ip}", max_requests=15, window_seconds=3600):
        return jsonify({"error": "rate_limit", "message": "Too many checkout attempts. Please try again later."}), 429

    data = request.get_json(force=True)
    parent_email = (data.get("parent_email") or "").strip()
    child_name = (data.get("child_name") or "").strip()
    age_group = (data.get("age_group") or "").strip()
    package = (data.get("package") or "").strip().lower()
    currency = (data.get("currency") or "eur").strip().lower()
    guardian_name = (data.get("guardian_name") or "").strip()
    ga_client_id = (data.get("ga_client_id") or "").strip()

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
                "ga_client_id": ga_client_id,
            },
            consent_collection={"terms_of_service": "required"},
        )
    except stripe.StripeError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"checkout_url": session.url, "session_id": session.id})


@checkout_bp.route("/v1/checkout/mega-bundle", methods=["POST"])
def checkout_mega_bundle():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip()
    currency = (data.get("currency") or "eur").strip().lower()
    ga_client_id = (data.get("ga_client_id") or "").strip()

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
                    "unit_amount": MEGA_BUNDLE_CENTS,
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
                "ga_client_id": ga_client_id,
            },
            consent_collection={"terms_of_service": "required"},
        )
    except stripe.StripeError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"checkout_url": session.url, "session_id": session.id})


_VALID_CEFR = {"A1", "A2", "B1", "B2", "C1", "C2"}
_VALID_AUDIT_LANGS = {"de", "en", "fr", "it", "es", "bg", "ru"}


@checkout_bp.route("/v1/checkout/express-hiring-audit", methods=["POST"])
def checkout_express_hiring_audit():
    """
    Express Hiring Audit — B2B product where an employer pays for an
    independent CEFR audit of a candidate they intend to hire.

    Flow starts here: employer intake + Stripe payment. On successful
    payment, the stripe webhook creates a consent token and emails the
    candidate a consent link. No session is scheduled until the candidate
    has given explicit GDPR-compliant consent.
    """
    from app import _limiter, _get_client_ip

    ip = _get_client_ip()
    if not _limiter.is_allowed(f"checkout:{ip}", max_requests=10, window_seconds=3600):
        return jsonify({"error": "rate_limit", "message": "Too many checkout attempts. Please try again later."}), 429

    data = request.get_json(force=True) or {}
    employer_company = (data.get("employer_company") or "").strip()
    employer_email = (data.get("employer_email") or "").strip().lower()
    candidate_name = (data.get("candidate_name") or "").strip()
    candidate_email = (data.get("candidate_email") or "").strip().lower()
    target_level = (data.get("target_level") or "").strip().upper()
    language = (data.get("language") or "").strip().lower()
    currency = (data.get("currency") or "eur").strip().lower()
    ga_client_id = (data.get("ga_client_id") or "").strip()

    email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    if not employer_company or len(employer_company) > 200:
        return jsonify({"error": "Employer company required"}), 400
    if not email_re.match(employer_email):
        return jsonify({"error": "Valid employer email required"}), 400
    if not candidate_name or len(candidate_name) > 200:
        return jsonify({"error": "Candidate name required"}), 400
    if not email_re.match(candidate_email):
        return jsonify({"error": "Valid candidate email required"}), 400
    if candidate_email == employer_email:
        return jsonify({"error": "Candidate and employer email must differ"}), 400
    if target_level not in _VALID_CEFR:
        return jsonify({"error": f"target_level must be one of {sorted(_VALID_CEFR)}"}), 400
    if language not in _VALID_AUDIT_LANGS:
        return jsonify({"error": f"language must be one of {sorted(_VALID_AUDIT_LANGS)}"}), 400
    if currency not in ALLOWED_CURRENCIES:
        currency = "eur"

    amount = EXPRESS_HIRING_AUDIT["amounts"][currency]
    consent_token = secrets.token_urlsafe(32)
    origin = os.environ.get("CORS_ORIGIN", "https://www.lingograde.com")

    # Persist pending audit row BEFORE creating the Stripe session — if
    # Stripe fails we still have a record; if DB fails we abort cleanly.
    audit_id = None
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO hiring_audits (
                    employer_company, employer_email, employer_ip,
                    candidate_name, candidate_email,
                    target_level, language,
                    currency, amount_paid_cents,
                    consent_token, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending_consent')
                RETURNING id
                """,
                (
                    employer_company, employer_email, ip,
                    candidate_name, candidate_email,
                    target_level, language,
                    currency, amount,
                    consent_token,
                ),
            )
            row = cur.fetchone()
            audit_id = row["id"] if row else None
    except Exception as e:
        return jsonify({"error": "Could not create audit record", "detail": str(e)}), 500

    if not audit_id:
        return jsonify({"error": "Could not create audit record"}), 500

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": currency,
                    "unit_amount": amount,
                    "product_data": {
                        "name": EXPRESS_HIRING_AUDIT["name"],
                        "description": EXPRESS_HIRING_AUDIT["description"],
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            customer_email=employer_email,
            success_url=f"{origin}/express-hiring-audit/pending?audit={audit_id}",
            cancel_url=f"{origin}/express-hiring-audit?cancelled=1",
            metadata={
                "product_type": "express_hiring_audit",
                "audit_id": str(audit_id),
                "employer_company": employer_company,
                "employer_email": employer_email,
                "candidate_email": candidate_email,
                "candidate_name": candidate_name,
                "target_level": target_level,
                "language": language,
                "ga_client_id": ga_client_id,
            },
            consent_collection={"terms_of_service": "required"},
        )
    except stripe.StripeError as e:
        try:
            with get_cursor() as cur:
                cur.execute(
                    "UPDATE hiring_audits SET status = 'expired' WHERE id = %s",
                    (audit_id,),
                )
        except Exception:
            pass
        return jsonify({"error": str(e)}), 400

    try:
        with get_cursor() as cur:
            cur.execute(
                "UPDATE hiring_audits SET stripe_session_id = %s WHERE id = %s",
                (session.id, audit_id),
            )
    except Exception:
        pass  # non-fatal; webhook falls back to metadata.audit_id

    return jsonify({
        "checkout_url": session.url,
        "session_id": session.id,
        "audit_id": str(audit_id),
    })


_VALID_CORP_LANGS = {
    "de", "en", "fr", "it", "es", "pt", "ru", "sr", "hr", "ro", "pl", "bg",
}


@checkout_bp.route("/v1/checkout/corporate", methods=["POST"])
def checkout_corporate():
    """
    Corporate Assessment — volume-tier purchase (Team / Department / Enterprise).
    Buyer pays per candidate; candidate invitations are handled post-payment by
    the assessment coordinator. Enterprise orders above 200 seats fall through
    to the contact form (return 400 with guidance).
    """
    from app import _limiter, _get_client_ip

    ip = _get_client_ip()
    if not _limiter.is_allowed(f"checkout:{ip}", max_requests=10, window_seconds=3600):
        return jsonify({"error": "rate_limit", "message": "Too many checkout attempts. Please try again later."}), 429

    data = request.get_json(force=True) or {}
    tier = (data.get("tier") or "").strip().lower()
    try:
        seat_count = int(data.get("seat_count") or 0)
    except (TypeError, ValueError):
        return jsonify({"error": "seat_count must be an integer"}), 400
    company_name = (data.get("company_name") or "").strip()
    buyer_email = (data.get("buyer_email") or "").strip().lower()
    buyer_name = (data.get("buyer_name") or "").strip()
    language = (data.get("language") or "").strip().lower()
    currency = (data.get("currency") or "eur").strip().lower()
    ga_client_id = (data.get("ga_client_id") or "").strip()

    email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    if tier not in CORPORATE_ASSESSMENT:
        return jsonify({"error": "tier must be one of team, department, enterprise"}), 400
    tier_cfg = CORPORATE_ASSESSMENT[tier]
    if seat_count < tier_cfg["min_seats"] or seat_count > tier_cfg["max_seats"]:
        return jsonify({
            "error": "seat_count out of tier bounds",
            "tier": tier,
            "allowed_range": [tier_cfg["min_seats"], tier_cfg["max_seats"]],
        }), 400
    if not company_name or len(company_name) > 200:
        return jsonify({"error": "Company name required"}), 400
    if not email_re.match(buyer_email):
        return jsonify({"error": "Valid buyer email required"}), 400
    if buyer_name and len(buyer_name) > 200:
        return jsonify({"error": "Buyer name too long"}), 400
    if language and language not in _VALID_CORP_LANGS:
        return jsonify({"error": f"language must be one of {sorted(_VALID_CORP_LANGS)}"}), 400
    if currency not in ALLOWED_CURRENCIES:
        currency = "eur"

    unit_amount = tier_cfg["unit_cents"]
    total_amount = unit_amount * seat_count
    origin = os.environ.get("CORS_ORIGIN", "https://www.lingograde.com")

    order_id = None
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO corporate_orders (
                    tier, seat_count, language,
                    buyer_email, buyer_name, company_name, buyer_ip,
                    currency, unit_amount_cents, total_amount_cents,
                    status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending_payment')
                RETURNING id
                """,
                (
                    tier, seat_count, (language or None),
                    buyer_email, (buyer_name or None), company_name, ip,
                    currency, unit_amount, total_amount,
                ),
            )
            row = cur.fetchone()
            order_id = row["id"] if row else None
    except Exception as e:
        return jsonify({"error": "Could not create order record", "detail": str(e)}), 500

    if not order_id:
        return jsonify({"error": "Could not create order record"}), 500

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": currency,
                    "unit_amount": unit_amount,
                    "product_data": {
                        "name": tier_cfg["name"],
                        "description": tier_cfg["description"],
                    },
                },
                "quantity": seat_count,
            }],
            mode="payment",
            customer_email=buyer_email,
            success_url=f"{origin}/corporate-success?order={order_id}",
            cancel_url=f"{origin}/corporate?purchase=cancelled",
            metadata={
                "product_type": "corporate_assessment",
                "order_id": str(order_id),
                "tier": tier,
                "seat_count": str(seat_count),
                "company_name": company_name,
                "buyer_email": buyer_email,
                "buyer_name": buyer_name,
                "language": language,
                "ga_client_id": ga_client_id,
            },
            consent_collection={"terms_of_service": "required"},
        )
    except stripe.StripeError as e:
        try:
            with get_cursor() as cur:
                cur.execute(
                    "UPDATE corporate_orders SET status = 'expired' WHERE id = %s",
                    (order_id,),
                )
        except Exception:
            pass
        return jsonify({"error": str(e)}), 400

    try:
        with get_cursor() as cur:
            cur.execute(
                "UPDATE corporate_orders SET stripe_session_id = %s WHERE id = %s",
                (session.id, order_id),
            )
    except Exception:
        pass

    return jsonify({
        "checkout_url": session.url,
        "session_id": session.id,
        "order_id": str(order_id),
    })
