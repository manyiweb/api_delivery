import os
from typing import Any, Dict, Iterable, Optional

import allure
import pytest

from api.Invoice_api import mgr_apply_invoice, query_invoice_status, refresh_invoice_status
from api.order_api import pos_order_list
from conftest import access_token
from utils.logger import logger


def _iter_dicts(obj: Any) -> Iterable[Dict[str, Any]]:
    stack = [obj]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            yield current
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)


def _extract_first_order_id(resp_json: Dict[str, Any]) -> Optional[str]:
    for d in _iter_dicts(resp_json):
        if "orderId" not in d:
            continue
        value = d.get("orderId")
        if value is None:
            continue
        value_str = str(value).strip()
        if value_str:
            return value_str
    return None


def _extract_invoice_id(resp_json: Dict[str, Any]) -> Optional[str]:
    data = resp_json.get("data")
    if isinstance(data, str) and data.strip():
        return data.strip()
    if isinstance(data, dict):
        for key in ("id", "invoiceId", "invoice_id", "invoiceNo"):
            value = data.get(key)
            if value is not None and str(value).strip():
                return str(value).strip()
    if isinstance(data, list) and data:
        first = data[0]
        if isinstance(first, dict):
            for key in ("id", "invoiceId", "invoice_id", "invoiceNo"):
                value = first.get(key)
                if value is not None and str(value).strip():
                    return str(value).strip()
        if isinstance(first, str) and first.strip():
            return first.strip()
    return None


def _assert_basic_success(resp_json: Dict[str, Any]) -> None:
    if "success" in resp_json:
        assert resp_json["success"] is True
        return
    if "code" in resp_json:
        assert str(resp_json["code"]) in {"0", "200"}
        return
    if "status" in resp_json:
        assert str(resp_json["status"]) in {"0", "200", "OK", "ok"}
        return
    if "data" in resp_json:
        assert resp_json["data"] not in (None, "", [])
        return
    assert resp_json


def _resolve_order_id(client, token_id: str) -> Optional[str]:
    order_id = os.getenv("INVOICE_ORDER_ID") or os.getenv("ORDER_ID")
    if order_id:
        return order_id

    order_remark = os.getenv("INVOICE_ORDER_REMARK", "")
    list_resp = pos_order_list(
        client,
        token_id,
        order_remark=order_remark,
        page_index=1,
        page_size=20,
    )
    return _extract_first_order_id(list_resp)


@pytest.fixture(scope="class")
def invoice_context(client):
    token_id = access_token()
    order_id = _resolve_order_id(client, token_id)
    if not order_id:
        pytest.skip("未找到订单号，请设置 INVOICE_ORDER_ID 后再运行发票用例。")

    with allure.step("????"):
        apply_resp = mgr_apply_invoice(client, order_id, token_id=token_id)
        allure.attach(
            str(apply_resp),
            name="申请开票响应",
            attachment_type=allure.attachment_type.TEXT,
        )
        _assert_basic_success(apply_resp)

    invoice_id = _extract_invoice_id(apply_resp)
    if not invoice_id:
        pytest.skip("申请开票未返回发票ID。")

    return {
        "token_id": token_id,
        "order_id": order_id,
        "invoice_id": invoice_id,
        "apply_resp": apply_resp,
    }


@allure.epic("发票接口")
@allure.feature("SaaS 发票")
class TestSaasInvoice:
    @pytest.mark.critical
    @allure.story("申请开票")
    @allure.title("申请开票应返回成功响应")
    def test_apply_invoice(self, invoice_context):
        apply_resp = invoice_context["apply_resp"]
        _assert_basic_success(apply_resp)

    @pytest.mark.normal
    @allure.story("刷新发票状态")
    @allure.title("刷新发票状态应返回成功响应")
    def test_refresh_invoice_status(self, client, invoice_context):
        invoice_id = invoice_context["invoice_id"]
        token_id = invoice_context["token_id"]
        refresh_resp = refresh_invoice_status(client, invoice_id, token_id=token_id)
        allure.attach(
            str(refresh_resp),
            name="刷新发票响应",
            attachment_type=allure.attachment_type.TEXT,
        )
        _assert_basic_success(refresh_resp)

    @pytest.mark.normal
    @allure.story("查询发票状态")
    @allure.title("申请开票应返回成功响应")
    def test_query_invoice_status(self, client, invoice_context):
        invoice_id = invoice_context["invoice_id"]
        token_id = invoice_context["token_id"]
        status = query_invoice_status(client, invoice_id, token_id=token_id)
        logger.info("发票状态: %s", status)
        assert status is not None
