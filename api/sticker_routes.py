"""Blueprint: Sticker map + verification routes."""

import math
import os
import uuid

from flask import Blueprint, g, jsonify, request

from auth import require_auth
from db_pool import get_cursor

sticker_bp = Blueprint("sticker_bp", __name__)

STICKER_UPLOAD_DIR = os.environ.get("STICKER_UPLOAD_DIR", "/var/data/lingograde/stickers")
ALLOWED_IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}
MAX_SELFIE_SIZE = 10 * 1024 * 1024  # 10 MB


@sticker_bp.route("/v1/stickers/map", methods=["GET"])
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


@sticker_bp.route("/v1/stickers/verify", methods=["POST"])
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

    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180) or math.isnan(lat) or math.isnan(lng):
        return jsonify({"error": "Coordinates out of range"}), 400

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
