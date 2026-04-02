"""
Mini-report PDF generator for bot assessments.
Uses WeasyPrint to convert an HTML template to PDF.
"""

import os
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)


# CEFR level → color mapping
CEFR_COLORS = {
    "A1": "#27AE60", "A1.1": "#27AE60", "A1.2": "#27AE60",
    "A2": "#2ECC71", "A2.1": "#2ECC71", "A2.2": "#2ECC71",
    "B1": "#2563AB", "B1.1": "#2563AB", "B1.2": "#2563AB",
    "B2": "#1A3A5C", "B2.1": "#1A3A5C", "B2.2": "#1A3A5C",
    "C1": "#8E44AD", "C1.1": "#8E44AD", "C1.2": "#8E44AD",
    "C2": "#C0392B", "C2.1": "#C0392B", "C2.2": "#C0392B",
}


def get_cefr_color(level):
    """Get brand color for CEFR level badge."""
    base = level.split(".")[0].split("-")[0] if level else "B1"
    return CEFR_COLORS.get(base, "#2563AB")


def generate_mini_report(result, lang, email, output_path):
    """
    Generate a 2-page PDF mini-report from bot assessment results.

    Args:
        result: dict with keys: cefr_active, cefr_passive, confidence_pct,
                perception, strengths, core_insight, problems, corrections,
                solutions, marco_summary
        lang: student's language code
        email: student's email
        output_path: where to save the PDF
    """
    try:
        from weasyprint import HTML
    except ImportError:
        raise RuntimeError(
            "WeasyPrint is not installed — cannot generate PDF report. "
            "Install it with: pip install weasyprint"
        )

    template = jinja_env.get_template("mini_report.html")

    html_content = template.render(
        cefr_active=result.get("cefr_active", "?"),
        cefr_passive=result.get("cefr_passive", "?"),
        cefr_color=get_cefr_color(result.get("cefr_active", "B1")),
        confidence_pct=result.get("confidence_pct", 0),
        perception=result.get("perception", ""),
        strengths=result.get("strengths", []),
        core_insight=result.get("core_insight", ""),
        problems=result.get("problems", []),
        corrections=result.get("corrections", []),
        solutions=result.get("solutions", []),
        marco_summary=result.get("marco_summary", ""),
        email=email,
        date=datetime.now(timezone.utc).strftime("%d %B %Y"),
        year=datetime.now(timezone.utc).year,
    )

    HTML(string=html_content).write_pdf(output_path)
