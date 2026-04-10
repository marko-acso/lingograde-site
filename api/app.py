"""
LingoGrade Bot API — Free analysis + Paid chatbot assessment.
Flask microservice, deployed behind Caddy at api.lingograde.com.
"""

import logging
import os
import threading
import time
import uuid
from collections import defaultdict

import anthropic
import stripe
from dotenv import load_dotenv
from flask import Flask, abort, g, jsonify, request
from flask_cors import CORS

from bot_store import cleanup_mem as _bot_store_cleanup

load_dotenv()

# ── Structured logging with JSON format ──
class _JsonFormatter(logging.Formatter):
    def format(self, record):
        import json
        from flask import has_request_context
        log = {
            "ts": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if has_request_context():
            log["request_id"] = getattr(g, "request_id", "-")
        if record.exc_info and record.exc_info[0]:
            log["exception"] = self.formatException(record.exc_info)
        return json.dumps(log)

_handler = logging.StreamHandler()
_handler.setFormatter(_JsonFormatter())
logging.root.handlers = [_handler]
logging.root.setLevel(logging.INFO)

# ── Database + student dashboard ──
from db_pool import init_pool  # noqa: E402
from student_routes import student_bp  # noqa: E402
from dashboard_routes import dashboard_bp  # noqa: E402

try:
    import drip_engine  # noqa: F401
    _DRIP_ENABLED = True
except Exception:
    _DRIP_ENABLED = False

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
app.register_blueprint(dashboard_bp)

# ── Simple in-memory rate limiter ──
class _RateLimiter:
    """Token-bucket rate limiter keyed by IP. Thread-safe."""
    def __init__(self):
        self._buckets = defaultdict(list)  # key -> [timestamp, ...]
        self._lock = threading.Lock()

    def is_allowed(self, key, max_requests, window_seconds):
        now = time.time()
        cutoff = now - window_seconds
        with self._lock:
            bucket = self._buckets[key]
            # Prune old entries
            self._buckets[key] = [t for t in bucket if t > cutoff]
            if len(self._buckets[key]) >= max_requests:
                return False
            self._buckets[key].append(now)
            return True

    def cleanup(self, max_age=86400):
        """Remove stale keys older than max_age seconds."""
        now = time.time()
        cutoff = now - max_age
        with self._lock:
            stale = [k for k, v in self._buckets.items() if not v or v[-1] < cutoff]
            for k in stale:
                del self._buckets[k]

_limiter = _RateLimiter()

def _get_client_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0].strip()

_ALLOWED_ORIGINS = {
    "https://www.lingograde.com",
    "https://app.lingograde.com",
    os.environ.get("CORS_ORIGIN", "https://www.lingograde.com"),
}

@app.before_request
def _assign_request_id():
    """Attach a unique request ID for log correlation."""
    g.request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex[:12])

@app.after_request
def _log_request(response):
    app.logger.info(
        "%s %s %s", request.method, request.path, response.status_code,
    )
    response.headers["X-Request-ID"] = getattr(g, "request_id", "-")
    return response

@app.before_request
def _csrf_origin_check():
    """Block state-changing requests from unknown origins (CSRF protection)."""
    if request.method in ("GET", "HEAD", "OPTIONS"):
        return
    # Stripe webhooks use Stripe-Signature, not Origin
    if request.path.startswith("/v1/webhook"):
        return
    origin = request.headers.get("Origin", "")
    if origin and origin not in _ALLOWED_ORIGINS:
        abort(403, description="Origin not allowed")

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
REPORT_DIR = os.environ.get("REPORT_DIR", "/tmp/lingograde-reports")  # nosec B108
os.makedirs(REPORT_DIR, exist_ok=True)

claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# ── Register route blueprints ──
from analysis_routes import analysis_bp  # noqa: E402
from free_bot_routes import free_bot_bp  # noqa: E402
from assessment_routes import assessment_bp  # noqa: E402
from checkout_routes import checkout_bp  # noqa: E402
from webhook_routes import webhook_bp  # noqa: E402
from sticker_routes import sticker_bp  # noqa: E402
from partner_routes import partner_bp  # noqa: E402

app.register_blueprint(analysis_bp)
app.register_blueprint(free_bot_bp)
app.register_blueprint(assessment_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(webhook_bp)
app.register_blueprint(sticker_bp)
app.register_blueprint(partner_bp)


# ═══════════════════════════════════════════════════════════════════
# Endpoint: GET /v1/config — Public frontend config
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
    # Piggyback periodic cleanup on health checks
    _limiter.cleanup()
    _bot_store_cleanup()
    return jsonify({"status": "ok", "service": "lingograde-bot-api"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=os.environ.get("FLASK_DEBUG", "").lower() == "true")
