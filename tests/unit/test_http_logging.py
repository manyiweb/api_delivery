import logging

import httpx
import pytest

from utils.http_logging import create_logged_client, redact_data

pytestmark = pytest.mark.unit


def test_redact_data_masks_sensitive_fields():
    payload = {
        "mobile": "13800138000",
        "loginWord": "plain-or-md5-password",
        "nested": {
            "tokenId": "token-value",
            "sign": "signature",
        },
    }

    assert redact_data(payload) == {
        "mobile": "13800138000",
        "loginWord": "***",
        "nested": {
            "tokenId": "***",
            "sign": "***",
        },
    }


def test_logged_client_logs_request_and_response_with_redaction(caplog):
    def handler(request):
        return httpx.Response(
            200,
            json={"code": "200", "data": {"tokenId": "secret-token"}, "msg": "ok"},
        )

    transport = httpx.MockTransport(handler)
    caplog.set_level(logging.INFO, logger="api_delivery")

    with create_logged_client(
        base_url="http://example.test/api",
        transport=transport,
        timeout=1,
    ) as client:
        client.post(
            "/login?debug=1",
            json={"mobile": "13800138000", "loginWord": "plain-or-md5-password"},
        )

    log_text = caplog.text
    assert "HTTP request: POST http://example.test/api/login?debug=1" in log_text
    assert '"mobile": "13800138000"' in log_text
    assert '"loginWord": "***"' in log_text
    assert "plain-or-md5-password" not in log_text
    assert "HTTP response: POST http://example.test/api/login?debug=1 -> 200" in log_text
    assert '"tokenId": "***"' in log_text
    assert "secret-token" not in log_text
