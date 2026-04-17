"""Blueprint: Stripe checkout/payment routes."""

import os

import stripe
from flask import Blueprint, jsonify, request

from db_pool import get_cursor
from pricing import (
    BOT_ASSESSMENT_CENTS, KIDS_PACKAGES, MEGA_BUNDLE_CENTS,
    ACCESSORY_CATALOG, ALLOWED_CURRENCIES,
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
