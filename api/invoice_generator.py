"""
Auto-invoicing for LingoGrade.
Generates bilingual BG/EN PDF invoices matching Fattura Acso format.
Triggered by Stripe webhook on successful payment.
"""

import base64
import io
import os
from datetime import datetime, timedelta, timezone

import requests as http_requests
from weasyprint import HTML

from db_pool import get_cursor

# ── Constants ──
# Fixed by law (Bulgarian National Bank Act, Art. 29): 1 EUR = 1.95583 BGN.
# This is NOT a market rate — it's a legally mandated fixed peg.
# Review date: if Bulgaria adopts the euro, remove BGN conversion entirely.
# Next review: 2027-01-01 (current accession target is 2026).
EUR_TO_BGN = float(os.environ.get("EUR_TO_BGN_RATE", "1.95583"))
INVOICE_DIR = os.environ.get("INVOICE_DIR", "/var/data/lingograde/invoices")

COMPANY = {
    "name_en": "Acso Consulting LTD",
    "name_bg": "Аксо Консултинг ЕООД",
    "address": "ul. Okolovrasten pat 251, 621 vh.1 et.3",
    "city": "BG-1715 Sofia",
    "eik": "201054736",
}


def _next_invoice_number():
    """Get next sequential invoice number from DB sequence."""
    with get_cursor() as cur:
        cur.execute("SELECT nextval('invoice_number_seq') AS num")
        return cur.fetchone()["num"]


def _format_number(num):
    """Format invoice number as 10-digit zero-padded string."""
    return f"{num:010d}"


def _cents_to_eur(cents):
    return cents / 100


def _cents_to_bgn(cents):
    return (cents / 100) * EUR_TO_BGN


def _fmt_money(amount, currency="EUR"):
    return f"{amount:,.2f} {currency}"


def generate_invoice(
    customer_email,
    customer_name,
    line_items,
    total_cents,
    currency,
    stripe_session_id=None,
    stripe_payment_intent_id=None,
    product_type=None,
):
    """
    Generate an invoice PDF and store it.

    line_items: list of dicts with keys: description, quantity, unit_price_cents
    total_cents: total amount charged by Stripe (cents)
    currency: 'eur', 'usd', etc.

    Returns dict with invoice_number, pdf_path, invoice_id.
    """
    invoice_number = _next_invoice_number()
    now = datetime.now(timezone.utc)
    due = now + timedelta(days=14)

    # No VAT — not VAT registered
    subtotal_cents = total_cents
    vat_cents = 0

    total_bgn_cents = round(total_cents * EUR_TO_BGN)

    # Enrich line items with totals
    enriched_items = []
    for item in line_items:
        qty = item.get("quantity", 1)
        unit = item.get("unit_price_cents", 0)
        enriched_items.append({
            "description": item["description"],
            "quantity": qty,
            "unit_price_cents": unit,
            "total_cents": qty * unit,
        })

    # Generate PDF
    pdf_bytes = _render_pdf(
        invoice_number=invoice_number,
        issued=now,
        due=due,
        customer_name=customer_name or customer_email,
        customer_email=customer_email,
        line_items=enriched_items,
        total_cents=total_cents,
        total_bgn_cents=total_bgn_cents,
        currency=currency.upper(),
    )

    # Save PDF to filesystem
    os.makedirs(INVOICE_DIR, exist_ok=True)
    filename = f"invoice_{_format_number(invoice_number)}.pdf"
    pdf_path = os.path.join(INVOICE_DIR, filename)
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    # Store in DB
    import json
    with get_cursor() as cur:
        cur.execute(
            """INSERT INTO invoices
               (invoice_number, issued_at, due_at, customer_name, customer_email,
                line_items, subtotal_cents, vat_rate, vat_cents, total_cents,
                currency, total_bgn_cents, stripe_session_id,
                stripe_payment_intent_id, product_type, pdf_path)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                invoice_number, now, due, customer_name, customer_email,
                json.dumps(enriched_items), subtotal_cents, 0, 0,
                total_cents, currency, total_bgn_cents, stripe_session_id,
                stripe_payment_intent_id, product_type, pdf_path,
            ),
        )
        invoice_id = str(cur.fetchone()["id"])

    # Email invoice
    _email_invoice(customer_email, invoice_number, pdf_bytes, filename)

    return {
        "invoice_id": invoice_id,
        "invoice_number": _format_number(invoice_number),
        "pdf_path": pdf_path,
    }


def _render_pdf(
    invoice_number, issued, due, customer_name, customer_email,
    line_items, total_cents, total_bgn_cents, currency,
):
    """Render invoice HTML and convert to PDF via WeasyPrint."""
    rows_html = ""
    for item in line_items:
        unit_bgn = _cents_to_bgn(item['unit_price_cents'])
        total_bgn_item = _cents_to_bgn(item['total_cents'])
        rows_html += f"""
        <tr>
            <td style="text-align:center">{item['quantity']}</td>
            <td>{item['description']}</td>
            <td style="text-align:right">{_fmt_money(_cents_to_eur(item['unit_price_cents']), currency)}<br>
                <span class="bgn-sub">{_fmt_money(unit_bgn, 'BGN')}</span></td>
            <td style="text-align:right">{_fmt_money(_cents_to_eur(item['total_cents']), currency)}<br>
                <span class="bgn-sub">{_fmt_money(total_bgn_item, 'BGN')}</span></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page {{ size: A4; margin: 20mm; }}
    body {{ font-family: Arial, Helvetica, sans-serif; font-size: 10pt; color: #1a1a1a; }}
    .header {{ display: flex; justify-content: space-between; margin-bottom: 30px; }}
    .company {{ }}
    .company h2 {{ margin: 0; font-size: 14pt; color: #1A3A5C; }}
    .company p {{ margin: 2px 0; font-size: 9pt; color: #555; }}
    .invoice-title {{ text-align: right; }}
    .invoice-title h1 {{ margin: 0; font-size: 22pt; color: #1A3A5C; }}
    .invoice-title .subtitle {{ font-size: 10pt; color: #888; }}
    .meta-grid {{ display: flex; justify-content: space-between; margin-bottom: 25px; }}
    .meta-block {{ }}
    .meta-block h3 {{ margin: 0 0 5px 0; font-size: 9pt; text-transform: uppercase;
                       letter-spacing: 1px; color: #888; }}
    .meta-block p {{ margin: 2px 0; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; }}
    thead th {{ background: #1A3A5C; color: white; padding: 8px 10px; text-align: left;
                font-size: 9pt; text-transform: uppercase; letter-spacing: 0.5px; }}
    tbody td {{ padding: 8px 10px; border-bottom: 1px solid #e0e0e0; }}
    .bgn-sub {{ font-size: 8pt; color: #888; }}
    .totals {{ width: 60%; margin-left: auto; }}
    .totals td {{ padding: 5px 10px; }}
    .totals .label {{ text-align: right; color: #555; }}
    .totals .value {{ text-align: right; font-weight: bold; }}
    .totals .grand {{ font-size: 13pt; color: #1A3A5C; border-top: 2px solid #1A3A5C; }}
    .no-vat {{ font-size: 9pt; color: #555; margin-bottom: 20px; text-align: right; }}
    .footer {{ margin-top: 40px; padding-top: 15px; border-top: 1px solid #ddd;
               font-size: 8pt; color: #888; }}
    .footer .bilingual {{ display: flex; gap: 40px; }}
    .footer .col {{ flex: 1; }}
</style>
</head>
<body>

<div class="header">
    <div class="company">
        <h2>{COMPANY['name_en']}</h2>
        <p>{COMPANY['name_bg']}</p>
        <p>{COMPANY['address']}</p>
        <p>{COMPANY['city']}</p>
        <p>ЕИК / UIC: {COMPANY['eik']}</p>
    </div>
    <div class="invoice-title">
        <h1>INVOICE</h1>
        <p class="subtitle">ФАКТУРА</p>
    </div>
</div>

<div class="meta-grid">
    <div class="meta-block">
        <h3>Bill To / Получател</h3>
        <p><strong>{customer_name}</strong></p>
        <p>{customer_email}</p>
    </div>
    <div class="meta-block" style="text-align:right">
        <h3>Invoice Details / Данни за фактурата</h3>
        <p><strong>№:</strong> {_format_number(invoice_number)}</p>
        <p><strong>Date / Дата:</strong> {issued.strftime('%d.%m.%Y')}</p>
        <p><strong>Due / Срок:</strong> {due.strftime('%d.%m.%Y')}</p>
    </div>
</div>

<table>
    <thead>
        <tr>
            <th style="width:8%; text-align:center">Qty</th>
            <th>Description / Описание</th>
            <th style="width:20%; text-align:right">Unit Price / Ед. цена</th>
            <th style="width:20%; text-align:right">Total / Сума</th>
        </tr>
    </thead>
    <tbody>
        {rows_html}
    </tbody>
</table>

<p class="no-vat">Not VAT registered / Нерегистриран по ДДС</p>

<table class="totals">
    <tr>
        <td class="label grand">Total / Общо:</td>
        <td class="value grand">{_fmt_money(_cents_to_eur(total_cents), currency)}</td>
    </tr>
    <tr>
        <td class="label">Равностойност в лева / BGN equivalent<br>
            <span style="font-size:8pt">(1 EUR = 1.95583 BGN)</span></td>
        <td class="value">{_fmt_money(_cents_to_eur(total_bgn_cents), 'BGN')}</td>
    </tr>
</table>

<div class="footer">
    <div class="bilingual">
        <div class="col">
            <p><strong>Payment method:</strong> Card payment via Stripe</p>
            <p><strong>Status:</strong> Paid</p>
            <p>Thank you for choosing LingoGrade.</p>
        </div>
        <div class="col">
            <p><strong>Начин на плащане:</strong> Картово плащане чрез Stripe</p>
            <p><strong>Статус:</strong> Платено</p>
            <p>Благодарим ви, че избрахте LingoGrade.</p>
        </div>
    </div>
</div>

</body>
</html>"""

    pdf = HTML(string=html).write_pdf()
    return pdf


def _email_invoice(customer_email, invoice_number, pdf_bytes, filename):
    """Send invoice PDF via Resend."""
    resend_key = os.environ.get("RESEND_API_KEY")
    if not resend_key:
        return

    pdf_b64 = base64.b64encode(pdf_bytes).decode("ascii")
    formatted_num = _format_number(invoice_number)

    try:
        http_requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {resend_key}"},
            timeout=30,
            json={
                "from": "LingoGrade <hello@lingograde.com>",
                "to": [customer_email],
                "bcc": ["marco@lingograde.com", "info@lingograde.com"],
                "subject": f"Invoice {formatted_num} / Фактура {formatted_num} — LingoGrade",
                "html": (
                    f"<p>Please find your invoice <strong>{formatted_num}</strong> attached.</p>"
                    f"<p>Приложена е вашата фактура <strong>{formatted_num}</strong>.</p>"
                    "<hr>"
                    "<p style='color:#888; font-size:12px'>LingoGrade — Acso Consulting LTD</p>"
                ),
                "attachments": [
                    {
                        "filename": filename,
                        "content": pdf_b64,
                        "type": "application/pdf",
                    }
                ],
            },
        )
    except Exception:
        pass  # Email failure should not break the webhook


def get_invoice_pdf(invoice_id):
    """Retrieve invoice PDF path by invoice UUID."""
    with get_cursor() as cur:
        cur.execute("SELECT pdf_path FROM invoices WHERE id = %s::uuid", (invoice_id,))
        row = cur.fetchone()
        return row["pdf_path"] if row else None


def get_invoices_by_email(email):
    """List all invoices for a customer email."""
    with get_cursor() as cur:
        cur.execute(
            """SELECT id, invoice_number, issued_at, total_cents, currency, product_type
               FROM invoices WHERE customer_email = %s ORDER BY invoice_number DESC""",
            (email,),
        )
        return cur.fetchall()
