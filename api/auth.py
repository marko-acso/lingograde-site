"""
Session-cookie auth for the student dashboard.
Uses itsdangerous (bundled with Flask) to sign a cookie containing the student UUID.
Will be replaced by OAuth (Google + Apple) in a future phase.
"""

import functools
import os

from flask import abort, g, request
from itsdangerous import BadSignature, TimestampSigner

_SECRET = os.environ.get("SESSION_SECRET", os.environ.get("FLASK_SECRET_KEY", "dev-insecure-key"))
_COOKIE = "lg_session"
_MAX_AGE = 60 * 60 * 24 * 30  # 30 days


def _signer():
    return TimestampSigner(_SECRET)


def create_session_cookie(student_id: str) -> dict:
    """Return cookie params dict. Caller sets it on the response."""
    token = _signer().sign(student_id).decode()
    return {
        "key": _COOKIE,
        "value": token,
        "max_age": _MAX_AGE,
        "httponly": True,
        "secure": True,
        "samesite": "None",
        "path": "/",
    }


def read_session() -> str | None:
    """Return student_id from cookie, or None if invalid/missing."""
    raw = request.cookies.get(_COOKIE)
    if not raw:
        return None
    try:
        return _signer().unsign(raw, max_age=_MAX_AGE).decode()
    except BadSignature:
        return None


def require_auth(fn):
    """Decorator: 401 if no valid session cookie."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        student_id = read_session()
        if not student_id:
            abort(401)
        g.student_id = student_id
        return fn(*args, **kwargs)
    return wrapper
