from types import SimpleNamespace

import pytest

from assertions.pay_assert import assert_pay_success

pytestmark = pytest.mark.unit


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload


def test_assert_pay_success_accepts_standard_success_response():
    resp = FakeResponse({"code": "200", "success": True, "data": {"orderId": "order-1"}})

    payload = assert_pay_success(resp, "现金支付", order_id="order-1")

    assert payload["code"] == "200"


def test_assert_pay_success_accepts_legacy_success_without_success_flag():
    resp = FakeResponse({"ResultInt": 0, "ResultString": "OK", "DataLine": []})

    payload = assert_pay_success(resp, "购物卡支付")

    assert payload["ResultInt"] == 0


def test_assert_pay_success_rejects_failed_business_code():
    resp = FakeResponse({"code": "500", "success": False, "msg": "支付失败"})

    with pytest.raises(AssertionError, match="支付失败"):
        assert_pay_success(resp, "现金支付")


def test_assert_pay_success_rejects_missing_order_id_when_expected():
    resp = FakeResponse({"code": "200", "success": True, "data": {"orderId": "other"}})

    with pytest.raises(AssertionError, match="订单号不一致"):
        assert_pay_success(resp, "现金支付", order_id="order-1")


def test_assert_pay_success_accepts_plain_namespace_response():
    resp = SimpleNamespace(status_code=200, json=lambda: {"code": 200, "success": True})

    assert_pay_success(resp, "现金支付")
