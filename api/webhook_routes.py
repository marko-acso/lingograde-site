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
