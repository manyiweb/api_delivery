import json
import os
from typing import Any

import allure

_SENSITIVE_KEYWORDS = (
    "authorization",
    "cookie",
    "loginword",
    "password",
    "secret",
    "sign",
    "token",
    "tokenid",
)
_DEFAULT_MAX_ATTACHMENT_CHARS = 8000


def _attachment_level() -> str:
    level = os.getenv("ALLURE_ATTACH_LEVEL", "summary").strip().lower()
    if level not in {"off", "summary", "full"}:
        return "summary"
    return level


def _max_attachment_chars() -> int:
    raw_value = os.getenv("ALLURE_MAX_ATTACHMENT_CHARS", "")
    if not raw_value:
        return _DEFAULT_MAX_ATTACHMENT_CHARS
    try:
        value = int(raw_value)
    except ValueError:
        return _DEFAULT_MAX_ATTACHMENT_CHARS
    return max(value, 1)


def _is_sensitive_key(key: Any) -> bool:
    normalized = str(key).replace("_", "").replace("-", "").lower()
    return any(keyword in normalized for keyword in _SENSITIVE_KEYWORDS)


def _truncate_text(value: Any) -> str:
    text = "" if value is None else str(value)
    max_chars = _max_attachment_chars()
    if len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}...<truncated>"


def _redact_and_summarize(data: Any, *, full: bool = False) -> Any:
    if isinstance(data, dict):
        return {
            key: "***" if _is_sensitive_key(key) else _redact_and_summarize(value, full=full)
            for key, value in data.items()
        }

    if isinstance(data, list):
        if full:
            return [_redact_and_summarize(item, full=full) for item in data]
        if not data:
            return []
        if all(not isinstance(item, (dict, list, tuple, set)) for item in data):
            return data[:5] + ([f"<and {len(data) - 5} more>"] if len(data) > 5 else [])
        return [f"<list len={len(data)}>"]

    if isinstance(data, tuple):
        return _redact_and_summarize(list(data), full=full)

    if isinstance(data, set):
        return _redact_and_summarize(sorted(data, key=str), full=full)

    return data


def _dump_json(data: Any, *, full: bool = False) -> str:
    payload = _redact_and_summarize(data, full=full)
    return _truncate_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


def step(title: str):
    """Return an Allure step context manager."""
    return allure.step(title)


def attach_text(name: str, value: Any) -> None:
    """Attach a value to Allure as plain text."""
    if _attachment_level() == "off":
        return
    text = "***" if _is_sensitive_key(name) else _truncate_text(value)
    allure.attach(
        text,
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )


def attach_json(name: str, data: Any, *, full: bool = False) -> None:
    """Attach JSON-like data to Allure with redaction and size control.

    By default, large nested collections are summarized so successful reports stay
    readable. Set ``full=True`` for failure diagnostics that need complete payloads.
    ``ALLURE_ATTACH_LEVEL=full`` can also force full redacted attachments globally.
    """
    level = _attachment_level()
    if level == "off":
        return
    should_attach_full = full or level == "full"
    allure.attach(
        _dump_json(data, full=should_attach_full),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )
