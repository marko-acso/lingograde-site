"""Blueprint: Stripe webhook + invoice endpoints."""

import os
import uuid
from datetime import datetime, timedelta, timezone

import requests as http_requests
import stripe
from flask import Blueprint, abort, g, jsonify, request, send_file

from auth import require_auth
from bot_store import find_assessment_by_payment, update_assessment
from db_pool import get_cursor
from invoice_generator import generate_invoice, get_invoice_pdf, get_invoices_by_email

webhook_bp = Blueprint("webhook_bp", __name__)


def _send_ga4_purchase(transaction_id, value_cents, currency, items, client_id=None):
    """Fire GA4 purchase event via Measurement Protocol (server-side)."""
    measurement_id = os.environ.get("GA4_MEASUREMENT_ID", "")
    api_secret = os.environ.get("GA4_API_SECRET", "")
    if not measurement_id or not api_secret or not value_cents:
        return
    try:
        http_requests.post(
            "https://www.google-analytics.com/mp/collect",
            params={"measurement_id": measurement_id, "api_secret": api_secret},
            timeout=5,
            json={
                "client_id": client_id or str(uuid.uuid4()),
                "non_personalized_ads": False,
                "events": [{
                    "name": "purchase",
                    "params": {
                        "transaction_id": transaction_id,
                        "value": round(value_cents / 100, 2),
                        "currency": (currency or "EUR").upper(),
                        "items": items,
                    },
                }],
            },
        )
    except Exception:
        pass  # Analytics must never break webhook response


def _render_consent_email(
    candidate_name: str,
    employer_company: str,
    employer_email: str,
    target_level: str,
    audit_language: str,
    consent_url: str,
) -> str:
    """
    Bilingual DE+EN consent-request email for the Express Hiring Audit.
    The candidate is the GDPR data subject; this message is their lawful-basis
    capture under Art. 6(1)(a) — explicit, informed, specific, revocable.
    """
    lang_label_de = {
        "de": "Deutsch", "en": "Englisch", "fr": "Französisch",
        "it": "Italienisch", "es": "Spanisch", "bg": "Bulgarisch", "ru": "Russisch",
    }.get(audit_language, audit_language.upper())
    lang_label_en = {
        "de": "German", "en": "English", "fr": "French",
        "it": "Italian", "es": "Spanish", "bg": "Bulgarian", "ru": "Russian",
    }.get(audit_language, audit_language.upper())

    return f"""
    <div style="font-family: Inter, Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #1A3A5C;">
      <p style="font-size: 13px; color: #6b7280; margin-bottom: 24px;">Deutsch unten · English below</p>

      <h2 style="font-size: 20px; margin: 0 0 12px;">Einladung zur CEFR-Prüfung</h2>
      <p>Hallo {candidate_name},</p>
      <p><strong>{employer_company}</strong> hat bei LingoGrade eine unabhängige CEFR-Sprachprüfung ({lang_label_de}, Zielniveau <strong>{target_level}</strong>) angefragt — als Teil des Einstellungsprozesses.</p>
      <p>Diese Prüfung findet nur statt, wenn Sie ausdrücklich zustimmen. Sie entscheiden.</p>

      <h3 style="font-size: 15px; margin: 24px 0 8px;">Was verarbeitet wird</h3>
      <ul style="line-height: 1.7;">
        <li>Ein 25-minütiges Gespräch mit einem LingoGrade-Prüfer (Audio-Aufnahme)</li>
        <li>Analyse Ihrer sprachlichen Leistung nach CEFR-Methodik</li>
        <li>Schriftlicher Audit-Bericht, signiert vom Prüfer</li>
      </ul>

      <h3 style="font-size: 15px; margin: 24px 0 8px;">Wer den Bericht erhält</h3>
      <ul style="line-height: 1.7;">
        <li>Sie persönlich (an diese E-Mail-Adresse)</li>
        <li>{employer_company} ({employer_email})</li>
      </ul>

      <h3 style="font-size: 15px; margin: 24px 0 8px;">Aufbewahrung & Ihre Rechte</h3>
      <ul style="line-height: 1.7;">
        <li>Speicherung bei LingoGrade: 180 Tage nach Lieferung, dann Löschung</li>
        <li>Recht auf Widerruf vor der Sitzung — jederzeit möglich</li>
        <li>Recht auf Auskunft, Berichtigung, Löschung gemäß DSGVO</li>
        <li>Nach Zustellung an den Arbeitgeber wird dieser unabhängiger Verantwortlicher</li>
      </ul>

      <p style="margin: 28px 0;">
        <a href="{consent_url}"
           style="background: #1A3A5C; color: #fff; padding: 14px 22px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: 600;">
          Zustimmen & Termin wählen
        </a>
      </p>

      <p style="color: #6b7280; font-size: 13px;">Wenn Sie nicht zustimmen möchten, müssen Sie nichts tun. Der Arbeitgeber wird benachrichtigt und erhält die Zahlung zurück.</p>

      <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 40px 0;">

      <h2 style="font-size: 20px; margin: 0 0 12px;">Invitation to a CEFR Audit</h2>
      <p>Hello {candidate_name},</p>
      <p><strong>{employer_company}</strong> has requested an independent LingoGrade CEFR audit ({lang_label_en}, target level <strong>{target_level}</strong>) as part of your hiring process.</p>
      <p>This audit only happens if you consent. The decision is yours.</p>

      <h3 style="font-size: 15px; margin: 24px 0 8px;">What we process</h3>
      <ul style="line-height: 1.7;">
        <li>A 25-minute conversation with a LingoGrade assessor (audio recording)</li>
        <li>Analysis of your language performance against the CEFR framework</li>
        <li>A written audit report signed by the assessor</li>
      </ul>

      <h3 style="font-size: 15px; margin: 24px 0 8px;">Who receives the report</h3>
      <ul style="line-height: 1.7;">
        <li>You personally (to this email address)</li>
        <li>{employer_company} ({employer_email})</li>
      </ul>

      <h3 style="font-size: 15px; margin: 24px 0 8px;">Retention & your rights</h3>
      <ul style="line-height: 1.7;">
        <li>LingoGrade stores data for 180 days after delivery, then deletes</li>
        <li>Right to withdraw before the session — at any time</li>
        <li>Right to access, correct, delete under GDPR</li>
        <li>After delivery to the employer, they become an independent controller</li>
      </ul>

      <p style="margin: 28px 0;">
        <a href="{consent_url}"
           style="background: #1A3A5C; color: #fff; padding: 14px 22px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: 600;">
          Consent & Pick a time
        </a>
      </p>

      <p style="color: #6b7280; font-size: 13px;">If you don't want to consent, do nothing. The employer will be informed and receive a refund.</p>

      <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 40px 0;">
      <p style="color: #9ca3af; font-size: 12px;">LingoGrade · hello@lingograde.com · <a href="https://www.lingograde.com/privacy-policy" style="color: #6b7280;">Privacy Policy</a></p>
    </div>
    """.strip()


@webhook_bp.route("/v1/stripe/webhook", methods=["POST"])
def stripe_webhook():
    from app import _DRIP_ENABLED

    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
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

        _send_ga4_purchase(
            transaction_id=pi["id"],
            value_cents=pi.get("amount", 0),
            currency=pi.get("currency", "eur"),
            items=[{
                "item_id": "bot_assessment",
                "item_name": "LingoGrade Chatbot Assessment",
                "price": round(pi.get("amount", 0) / 100, 2),
                "quantity": 1,
            }],
            client_id=pi.get("metadata", {}).get("ga_client_id"),
        )

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
                            timeout=30,
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

        elif meta.get("product_type") == "express_hiring_audit":
            audit_id = meta.get("audit_id")
            pi_id = cs.get("payment_intent")
            candidate_email = meta.get("candidate_email", "")
            candidate_name = meta.get("candidate_name", "")
            employer_company = meta.get("employer_company", "")
            employer_email = meta.get("employer_email", "")
            target_level = meta.get("target_level", "")
            audit_language = meta.get("language", "de")

            consent_token = None
            if audit_id:
                try:
                    with get_cursor() as cur:
                        cur.execute(
                            """UPDATE hiring_audits
                               SET stripe_payment_intent_id = %s,
                                   stripe_session_id = %s
                               WHERE id = %s::uuid
                               RETURNING consent_token""",
                            (pi_id, cs["id"], audit_id),
                        )
                        row = cur.fetchone()
                        if row:
                            consent_token = row["consent_token"]
                except Exception:
                    pass  # Stripe is source of truth

            # Send candidate the consent request email. The candidate is the
            # GDPR data subject — they must give explicit consent before any
            # session or data-sharing occurs.
            if candidate_email and consent_token:
                consent_url = f"https://app.lingograde.com/hiring-audit/consent/{consent_token}"
                try:
                    resend_key = os.environ.get("RESEND_API_KEY")
                    if resend_key:
                        subject_de = f"Einladung zur CEFR-Prüfung — {employer_company}"
                        subject_en = f"Invitation to a CEFR Audit — {employer_company}"
                        http_requests.post(
                            "https://api.resend.com/emails",
                            headers={"Authorization": f"Bearer {resend_key}"},
                            timeout=30,
                            json={
                                "from": "LingoGrade <hello@lingograde.com>",
                                "to": [candidate_email],
                                "bcc": ["marco@lingograde.com"],
                                "reply_to": "marco@lingograde.com",
                                "subject": f"{subject_de} / {subject_en}",
                                "html": _render_consent_email(
                                    candidate_name=candidate_name,
                                    employer_company=employer_company,
                                    employer_email=employer_email,
                                    target_level=target_level,
                                    audit_language=audit_language,
                                    consent_url=consent_url,
                                ),
                            },
                        )
                except Exception:
                    pass  # Email failure must not break webhook

        elif meta.get("product_type") == "corporate_assessment":
            order_id = meta.get("order_id")
            pi_id = cs.get("payment_intent")
            buyer_email = meta.get("buyer_email", "")
            buyer_name = meta.get("buyer_name", "") or buyer_email.split("@")[0]
            company_name = meta.get("company_name", "")
            tier = meta.get("tier", "")
            seat_count = meta.get("seat_count", "")
            language = meta.get("language", "")

            if order_id:
                try:
                    with get_cursor() as cur:
                        cur.execute(
                            """UPDATE corporate_orders
                               SET stripe_payment_id = %s,
                                   status = 'paid',
                                   paid_at = NOW()
                               WHERE id = %s""",
                            (pi_id, int(order_id)),
                        )
                except Exception:
                    pass

            # Welcome email to the buyer with next steps (share candidate list).
            # BCC Marco so a human sees the order immediately and can reach out.
            if buyer_email:
                try:
                    resend_key = os.environ.get("RESEND_API_KEY")
                    if resend_key:
                        tier_label = {
                            "team": "Team", "department": "Department", "enterprise": "Enterprise",
                        }.get(tier, tier.title())
                        html = (
                            f"<p>Dear {buyer_name},</p>"
                            f"<p>Thank you for your LingoGrade {tier_label} Assessment order for <strong>{company_name}</strong>. "
                            f"Your payment for <strong>{seat_count} candidate seat(s)</strong> has been received and your order is confirmed.</p>"
                            f"<p><strong>Next step — share your candidate list.</strong> Simply reply to this email with:</p>"
                            f"<ul>"
                            f"<li>Full name and email of each candidate ({seat_count} total)</li>"
                            f"<li>Target language"
                            + (f" (you indicated <strong>{language.upper()}</strong>)" if language else "")
                            + "</li>"
                            f"<li>Any scheduling window you prefer (optional — default is within 5 business days)</li>"
                            f"</ul>"
                            f"<p>Your assessment coordinator will then send a scheduling link to each candidate and deliver the CEFR reports within one hour of each session. "
                            f"You will receive a Team Summary once all assessments are complete.</p>"
                            f"<p>If you have any questions, just reply to this email.</p>"
                            f"<p>Kind regards,<br>The LingoGrade Team<br>"
                            f"<a href=\"https://lingograde.com/corporate\">lingograde.com/corporate</a></p>"
                        )
                        http_requests.post(
                            "https://api.resend.com/emails",
                            headers={"Authorization": f"Bearer {resend_key}"},
                            timeout=30,
                            json={
                                "from": "LingoGrade <corporate@lingograde.com>",
                                "to": [buyer_email],
                                "bcc": ["marco@lingograde.com"],
                                "reply_to": "corporate@lingograde.com",
                                "subject": f"Order confirmed — LingoGrade {tier_label} Assessment for {company_name}",
                                "html": html,
                            },
                        )
                except Exception:
                    pass

        elif meta.get("product_type") == "subscription":
            customer_email = cs.get("customer_email") or cs.get("customer_details", {}).get("email", "")
            if customer_email and _DRIP_ENABLED:
                try:
                    import drip_engine
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
                    "express_hiring_audit": f"Express Hiring Audit — {meta.get('language', 'de').upper()} {meta.get('target_level', '')}".strip(),
                    "corporate_assessment": f"LingoGrade {meta.get('tier', 'corporate').title()} Assessment — {meta.get('company_name', '')} ({meta.get('seat_count', '1')} seats)".strip(),
                }
                desc = descriptions.get(product_type, f"LingoGrade — {product_type}")

                # For corporate_assessment, invoice line is per-seat x quantity.
                if product_type == "corporate_assessment":
                    try:
                        seat_count = int(meta.get("seat_count") or 1)
                    except (TypeError, ValueError):
                        seat_count = 1
                    unit_price_cents = amount // seat_count if seat_count > 0 else amount
                    invoice_line_items = [{
                        "description": desc,
                        "quantity": seat_count,
                        "unit_price_cents": unit_price_cents,
                    }]
                else:
                    invoice_line_items = [{
                        "description": desc,
                        "quantity": 1,
                        "unit_price_cents": amount,
                    }]

                generate_invoice(
                    customer_email=customer_email,
                    customer_name=customer_name,
                    line_items=invoice_line_items,
                    total_cents=amount,
                    currency=currency,
                    stripe_session_id=cs["id"],
                    product_type=product_type,
                )
        except Exception:
            pass  # Invoice failure must not break webhook

        # GA4 purchase tracking (server-side Measurement Protocol)
        try:
            amount = cs.get("amount_total", 0)
            currency = (cs.get("currency") or "eur").upper()
            product_type = meta.get("product_type", "unknown")
            item_names = {
                "kids_assessment": f"Kids Assessment — {meta.get('package', 'standard').title()}",
                "homework": f"Homework Check — Type {meta.get('homework_type', 'A')}",
                "mega_bundle": "LingoGrade Mega Bundle",
                "accessory": f"LingoGrade {meta.get('product', 'item').title()}",
                "subscription": f"LingoGrade Subscription — {meta.get('tier', 'weekly').title()}",
                "express_hiring_audit": f"Express Hiring Audit — {meta.get('language', 'de').upper()} {meta.get('target_level', '')}".strip(),
                "corporate_assessment": f"Corporate Assessment — {meta.get('tier', 'team').title()}",
            }
            item_name = item_names.get(product_type, f"LingoGrade — {product_type}")
            item_id = meta.get("product") or meta.get("package") or meta.get("tier") or product_type
            if product_type == "corporate_assessment":
                try:
                    ga_quantity = int(meta.get("seat_count") or 1)
                except (TypeError, ValueError):
                    ga_quantity = 1
                unit_price = round((amount / ga_quantity) / 100, 2) if (amount and ga_quantity > 0) else 0
            else:
                ga_quantity = 1
                unit_price = round(amount / 100, 2) if amount else 0
            _send_ga4_purchase(
                transaction_id=cs["id"],
                value_cents=amount,
                currency=currency,
                items=[{
                    "item_id": item_id,
                    "item_name": item_name,
                    "item_category": product_type,
                    "price": unit_price,
                    "quantity": ga_quantity,
                }],
                client_id=meta.get("ga_client_id"),
            )
        except Exception:
            pass

    return jsonify({"status": "ok"})


# ═══════════════════════════════════════════════════════════════════
# Invoice endpoints
# ═══════════════════════════════════════════════════════════════════

@webhook_bp.route("/v1/invoice/<invoice_id>/pdf", methods=["GET"])
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


@webhook_bp.route("/v1/invoices", methods=["GET"])
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
