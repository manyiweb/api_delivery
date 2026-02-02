import copy
from typing import Any, Dict, Optional

import httpx

from api.base import safe_post
from conftest import access_token
from utils.file_loader import get_data_file_path, load_yaml_data
from utils.logger import logger

APPLY_INVOICE_ENDPOINT = "/hr/retail/invoice/batchApply"
INVOICE_DETAIL_ENDPOINT = "/hr/retail/invoice/detail"
INVOICE_REFRESH_ENDPOINT = "/hr/retail/invoice/refreshInvoiceStatus"


def _load_invoice_payload() -> Dict[str, Any]:
    raw_data = load_yaml_data(get_data_file_path("invoice_data.yaml")) or {}
    if not isinstance(raw_data, dict):
        raise ValueError("data/invoice_data.yaml 缺少或无效")
    return copy.deepcopy(raw_data)


def build_apply_invoice_payload(
    order_id: str,
    token_id: str,
    *,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = _load_invoice_payload()
    order_amount_list = payload.get("orderAmountList")
    if not isinstance(order_amount_list, list) or not order_amount_list:
        raise ValueError("invoice_data.yaml 缺少 orderAmountList 配置")

    order_amount_list[0]["orderId"] = order_id
    payload["orderIds"] = [order_id]
    payload["tokenId"] = token_id

    if extra:
        payload.update(extra)

    return payload


def mgr_apply_invoice(
    client: httpx.Client,
    order_id: str,
    *,
    token_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    token_id = token_id or access_token()
    payload = build_apply_invoice_payload(order_id, token_id, extra=extra)

    resp = safe_post(
        client,
        APPLY_INVOICE_ENDPOINT,
        json=payload,
        headers={"Authorization": f"Bearer {token_id}"},
    )
    return resp.json()


def query_invoice_status(
    client: httpx.Client,
    invoice_id: str,
    *,
    token_id: Optional[str] = None,
) -> Optional[Any]:
    token_id = token_id or access_token()
    resp = safe_post(
        client,
        INVOICE_DETAIL_ENDPOINT,
        json={"id": invoice_id, "token": token_id},
        headers={"Authorization": f"Bearer {token_id}"},
    )
    data = resp.json().get("data") or {}
    if not data:
        logger.warning("Invoice detail 返回空数据: invoice_id=%s", invoice_id)
    return data.get("status")


def refresh_invoice_status(
    client: httpx.Client,
    invoice_id: str,
    *,
    token_id: Optional[str] = None,
) -> Dict[str, Any]:
    token_id = token_id or access_token()
    resp = safe_post(
        client,
        INVOICE_REFRESH_ENDPOINT,
        json={"id": invoice_id, "token": token_id},
        headers={"Authorization": f"Bearer {token_id}"},
    )
    return resp.json()
