import pytest

from api import Invoice_api

pytestmark = pytest.mark.unit


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def test_execute_apply_invoice_returns_invoice_id_by_default(monkeypatch):
    response = FakeResponse(
        {
            "code": "200",
            "success": True,
            "data": {"invoiceId": "INV-001"},
        }
    )
    monkeypatch.setattr(Invoice_api, "safe_post", lambda *args, **kwargs: response)

    invoice_id = Invoice_api.execute_apply_invoice(
        client=object(),
        payload={"orderIds": ["order-1"]},
        token_id="token-1",
    )

    assert invoice_id == "INV-001"
