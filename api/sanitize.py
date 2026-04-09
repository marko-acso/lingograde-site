"""
sanitize.py — Shared input sanitization for all Claude prompt builders.
Defends against prompt injection by stripping dangerous patterns from user text
before it reaches the system/user message boundary.
"""

import re

# Tags that could impersonate system/assistant message boundaries
_BOUNDARY_TAG_RE = re.compile(
    r"<\/?(?:system|assistant|human|user|instructions?|prompt|tool_use|tool_result|function_call|function_response)\b[^>]*>",
    re.IGNORECASE,
)

# Unicode control characters (except normal whitespace: \t \n \r \x20)
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")

# Excessive newlines (more than 3 consecutive)
_EXCESSIVE_NEWLINES_RE = re.compile(r"\n{4,}")

# Max lengths
MAX_MESSAGE_LEN = 5000
MAX_LANG_LEN = 20
MAX_FIELD_LEN = 500


def sanitize_text(text: str, max_len: int = MAX_MESSAGE_LEN) -> str:
    """Sanitize user-provided text before inserting into a Claude prompt.

    - Strips XML-like boundary tags that could trick the model
    - Removes unicode control characters
    - Collapses excessive newlines
    - Enforces max length
    """
    if not isinstance(text, str):
        return ""
    text = text[:max_len]
    text = _BOUNDARY_TAG_RE.sub("", text)
    text = _CONTROL_CHAR_RE.sub("", text)
    text = _EXCESSIVE_NEWLINES_RE.sub("\n\n\n", text)
    return text.strip()


def sanitize_lang(lang: str) -> str:
    """Sanitize a language code. Only allows alphanumeric, hyphens, underscores."""
    if not isinstance(lang, str):
        return "en"
    # Strip to safe chars only
    safe = re.sub(r"[^a-zA-Z0-9_\-]", "", lang)
    return safe[:MAX_LANG_LEN] or "en"


def sanitize_field(value: str, max_len: int = MAX_FIELD_LEN) -> str:
    """Sanitize a short field value (e.g., CEFR estimate from prior analysis)."""
    if not isinstance(value, str):
        return ""
    value = value[:max_len]
    value = _BOUNDARY_TAG_RE.sub("", value)
    value = _CONTROL_CHAR_RE.sub("", value)
    return value.strip()


def sanitize_list(items: list, max_items: int = 10, max_len: int = MAX_FIELD_LEN) -> list:
    """Sanitize a list of string values (e.g., focus_areas from prior analysis)."""
    if not isinstance(items, list):
        return []
    return [sanitize_field(str(item), max_len) for item in items[:max_items] if item]
