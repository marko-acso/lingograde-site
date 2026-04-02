"""
Student dashboard API — Blueprint mounted at /api/student.
Endpoints match the contract in dashboard.html exactly.
"""

import os
import uuid
from datetime import datetime, timezone

from flask import Blueprint, g, jsonify, request
from werkzeug.utils import secure_filename

from auth import require_auth
from db_pool import get_cursor

student_bp = Blueprint("student", __name__, url_prefix="/api/student")

UPLOAD_DIR = os.environ.get("HOMEWORK_UPLOAD_DIR", "/var/data/lingograde/homework")
ALLOWED_EXT = {"pdf", "docx", "doc", "jpg", "jpeg", "png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
PDF_BASE_URL = os.environ.get("PDF_BASE_URL", "https://app.lingograde.com/reports")


def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# ═══════════════════════════════════════════════════════════════════
# GET /api/student/profile
# ═══════════════════════════════════════════════════════════════════

@student_bp.route("/profile", methods=["GET"])
@require_auth
def get_profile():
    with get_cursor() as cur:
        cur.execute(
            """SELECT id, email, full_name, preferred_name,
                      formality_preference, country_of_residence,
                      display_country
               FROM students WHERE id = %s""",
            (g.student_id,),
        )
        row = cur.fetchone()

    if not row:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(row))


# ═══════════════════════════════════════════════════════════════════
# PATCH /api/student/profile
# ═══════════════════════════════════════════════════════════════════

_PATCHABLE = {"preferred_name", "formality_preference", "display_country"}

@student_bp.route("/profile", methods=["PATCH"])
@require_auth
def patch_profile():
    data = request.get_json(force=True)
    updates = {k: v for k, v in data.items() if k in _PATCHABLE and v is not None}

    if not updates:
        return jsonify({"error": "Nothing to update"}), 400

    # Validate formality if provided
    if "formality_preference" in updates and updates["formality_preference"] not in ("informal", "formal"):
        return jsonify({"error": "formality_preference must be 'informal' or 'formal'"}), 400

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    values = list(updates.values()) + [g.student_id]

    with get_cursor() as cur:
        cur.execute(
            f"UPDATE students SET {set_clause} WHERE id = %s",
            values,
        )

    return jsonify({"ok": True})


# ═══════════════════════════════════════════════════════════════════
# GET /api/student/assessments
# ═══════════════════════════════════════════════════════════════════

@student_bp.route("/assessments", methods=["GET"])
@require_auth
def get_assessments():
    with get_cursor() as cur:
        cur.execute(
            """SELECT id, date, language, cefr_level, pdf_path
               FROM assessments
               WHERE student_id = %s
               ORDER BY date DESC""",
            (g.student_id,),
        )
        rows = cur.fetchall()

    assessments = []
    for r in rows:
        assessments.append({
            "id": str(r["id"]),
            "date": r["date"].isoformat(),
            "language": r["language"],
            "cefr_level": r["cefr_level"],
            "pdf_url": f"{PDF_BASE_URL}/{r['pdf_path']}" if r["pdf_path"] else None,
        })

    return jsonify({"assessments": assessments})


# ═══════════════════════════════════════════════════════════════════
# GET /api/student/homework
# ═══════════════════════════════════════════════════════════════════

@student_bp.route("/homework", methods=["GET"])
@require_auth
def get_homework():
    with get_cursor() as cur:
        cur.execute(
            """SELECT id, title, type, status, deadline,
                      submitted_at, feedback
               FROM homework
               WHERE student_id = %s
               ORDER BY created_at DESC""",
            (g.student_id,),
        )
        rows = cur.fetchall()

    homework = []
    for r in rows:
        homework.append({
            "id": str(r["id"]),
            "title": r["title"],
            "type": r["type"],
            "status": r["status"],
            "deadline": r["deadline"].isoformat() if r["deadline"] else None,
            "submitted_at": r["submitted_at"].isoformat() if r["submitted_at"] else None,
            "feedback": r["feedback"],
        })

    return jsonify({"homework": homework})


# ═══════════════════════════════════════════════════════════════════
# POST /api/student/homework/upload
# ═══════════════════════════════════════════════════════════════════

@student_bp.route("/homework/upload", methods=["POST"])
@require_auth
def upload_homework():
    file = request.files.get("file")
    homework_id = request.form.get("homework_id", "").strip()

    if not file or not homework_id:
        return jsonify({"error": "file and homework_id required"}), 400

    if not _allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Read into memory to check size (avoids saving oversized files)
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > MAX_FILE_SIZE:
        return jsonify({"error": "File exceeds 10 MB limit"}), 400

    # Verify homework belongs to this student and is pending
    with get_cursor() as cur:
        cur.execute(
            "SELECT id, status FROM homework WHERE id = %s AND student_id = %s",
            (homework_id, g.student_id),
        )
        hw = cur.fetchone()

    if not hw:
        return jsonify({"error": "Homework not found"}), 404
    if hw["status"] != "pending":
        return jsonify({"error": "Homework already submitted"}), 400

    # Save file
    ext = file.filename.rsplit(".", 1)[1].lower()
    safe_name = f"{homework_id}_{uuid.uuid4().hex[:8]}.{ext}"
    student_dir = os.path.join(UPLOAD_DIR, g.student_id)
    os.makedirs(student_dir, exist_ok=True)
    save_path = os.path.join(student_dir, safe_name)
    file.save(save_path)

    # Update homework record
    now = datetime.now(timezone.utc)
    with get_cursor() as cur:
        cur.execute(
            """UPDATE homework
               SET status = 'submitted', submitted_at = %s, file_path = %s
               WHERE id = %s AND student_id = %s""",
            (now, save_path, homework_id, g.student_id),
        )

    return jsonify({"success": True})
