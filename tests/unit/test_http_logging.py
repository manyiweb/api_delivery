import logging

import httpx
import pytest

from utils.http_logging import create_logged_client

pytestmark = pytest.mark.unit


def test_logged_client_logs_request_and_response_payload(caplog):
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
    assert '"loginWord": "plain-or-md5-password"' in log_text
    assert "HTTP response: POST http://example.test/api/login?debug=1 -> 200" in log_text
    assert '"tokenId": "secret-token"' in log_text
