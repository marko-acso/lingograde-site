"""Blueprint: Partner application route."""

import os

import requests as http_requests
from flask import Blueprint, current_app, jsonify, request

partner_bp = Blueprint("partner_bp", __name__)


@partner_bp.route("/api/partner-apply", methods=["POST"])
def partner_apply():
    from app import _limiter, _get_client_ip, _DRIP_ENABLED

    ip = _get_client_ip()
    if not _limiter.is_allowed(f"partner:{ip}", max_requests=3, window_seconds=86400):
        return jsonify({"error": "rate_limit", "message": "Too many applications. Please try again tomorrow."}), 429

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

    # Build message from extra fields not in the table schema
    msg_parts = []
    if phone:
        msg_parts.append(f"Phone: {phone}")
    if institution:
        msg_parts.append(f"Background: {institution}")
    if referral_source:
        msg_parts.append(f"Referral source: {referral_source}")
    message = "\n".join(msg_parts) or None

    # Use Supabase REST API with service_role key to bypass RLS
    sb_url = os.environ.get("SUPABASE_URL", "https://sbfjhsfvsbyjguplywfj.supabase.co")
    sb_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not sb_key:
        current_app.logger.error("partner_apply: SUPABASE_SERVICE_ROLE_KEY not set")
        return jsonify({"error": "Application could not be saved"}), 500

    try:
        resp = http_requests.post(
            f"{sb_url}/rest/v1/partner_applications",
            json={"name": name, "email": email, "country": country,
                  "languages": languages, "message": message},
            headers={
                "apikey": sb_key,
                "Authorization": f"Bearer {sb_key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            },
            timeout=10,
        )
        if resp.status_code not in (200, 201):
            current_app.logger.error(f"partner_apply Supabase error: {resp.status_code} {resp.text}")
            return jsonify({"error": "Application could not be saved"}), 500
    except Exception as e:
        current_app.logger.error(f"partner_apply error: {e}")
        return jsonify({"error": "Application could not be saved"}), 500

    # Kick off partner onboarding drip sequence
    if _DRIP_ENABLED:
        try:
            import drip_engine
            drip_engine.enqueue_partner_onboarding(
                email=email,
                first_name=first_name,
            )
        except Exception as e:
            current_app.logger.error(f"partner_apply drip error: {e}")

    return jsonify({"ok": True}), 200
