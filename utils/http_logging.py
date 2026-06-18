"""HTTP 请求/响应日志工具。"""

import json
from typing import Any, Dict

import httpx

from utils.logger import logger

_MAX_LOG_CHARS = 4000


def _truncate(text: str) -> str:
    if len(text) <= _MAX_LOG_CHARS:
        return text
    return f"{text[:_MAX_LOG_CHARS]}...<truncated>"


def _format_json(data: Any) -> str:
    return _truncate(json.dumps(data, ensure_ascii=False, default=str))


def _body_as_json(request: httpx.Request) -> Any:
    if not request.content:
        return None
    try:
        return json.loads(request.content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return f"<{len(request.content)} bytes non-json body>"


def _response_as_json(response: httpx.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return _truncate(response.text)


def _log_request(request: httpx.Request) -> None:
    body = _body_as_json(request)
    if body is None:
        logger.info("HTTP request: %s %s", request.method, request.url)
        return
    logger.info("HTTP request: %s %s body=%s", request.method, request.url, _format_json(body))


def _log_response(response: httpx.Response) -> None:
    request = response.request
    logger.info(
        "HTTP response: %s %s -> %s body=%s",
        request.method,
        request.url,
        response.status_code,
        _format_json(_response_as_json(response)),
    )


def create_logged_client(**kwargs: Dict[str, Any]) -> httpx.Client:
    """创建带请求/响应日志的 httpx.Client。"""
    event_hooks = dict(kwargs.pop("event_hooks", {}) or {})
    event_hooks.setdefault("request", [])
    event_hooks.setdefault("response", [])
    event_hooks["request"] = [*event_hooks["request"], _log_request]
    event_hooks["response"] = [*event_hooks["response"], _log_response]
    return httpx.Client(event_hooks=event_hooks, **kwargs)
