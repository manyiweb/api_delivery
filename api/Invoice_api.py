import copy
import time
from typing import Any, Dict, Optional

import httpx

from api.base import safe_post
from conftest import access_token
from utils.file_loader import get_data_file_path, load_yaml_data
from utils.logger import logger

APPLY_INVOICE_ENDPOINT = "/hr/retail/invoice/batchApply"
INVOICE_DETAIL_ENDPOINT = "/hr/retail/invoice/detail"
INVOICE_REFRESH_ENDPOINT = "/hr/retail/invoice/refreshInvoiceStatus"
RED_PUNCH_ENDPOINT = "/hr/retail/invoice/redPunch"



def _load_invoice_payload() -> Dict[str, Any]:
    raw_data = load_yaml_data(get_data_file_path("invoice_data.yaml")) or {}
    if not isinstance(raw_data, dict):
        raise ValueError("data/invoice_data.yaml 缺少或无效")
    return copy.deepcopy(raw_data)

# 构建开票请求payload
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


# 品牌端开票
def mgr_apply_invoice(
        client: httpx.Client,
        order_id: str,
        *,
        token_id: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
) -> str:
    token_id = token_id
    payload = build_apply_invoice_payload(order_id, token_id, extra=extra)

    resp = safe_post(
        client,
        APPLY_INVOICE_ENDPOINT,
        json=payload,
        headers={"Authorization": f"Bearer {token_id}"},
    )
    logger.info("开票接口响应: %s", resp.json())
    invoice_id = resp.json()["data"]["invoiceId"]
    if invoice_id is None:
        raise ValueError("开票号为空")
    logger.info("开票号: invoice_id=%s", invoice_id)
    return invoice_id


# 查询开票状态
def query_invoice_status(
        client: httpx.Client,
        invoice_id: str,
        *,
        token_id: Optional[str] = None,
) -> Optional[Any]:
    token_id = token_id
    max_attempts = 5
    last_status: Optional[str] = None
    last_response: Optional[Dict[str, Any]] = None

    for attempt in range(1, max_attempts + 1):
        resp = safe_post(
            client,
            INVOICE_DETAIL_ENDPOINT,
            json={"id": invoice_id, "token": token_id},
            headers={"Authorization": f"Bearer {token_id}"},
        )
        response_json = resp.json()
        last_response = response_json if isinstance(response_json, dict) else None
        logger.info("Invoice detail response (%s/%s): %s", attempt, max_attempts, response_json)

        data = last_response.get("data") if isinstance(last_response, dict) else None
        last_status = data.get("status") if isinstance(data, dict) else None

        logger.info("Invoice status=%s", last_status)
        if last_status == "INVOICED":
            return last_status

        if attempt < max_attempts:
            time.sleep(2)

    raise RuntimeError(
        f"Invoice status not INVOICED after {max_attempts} attempts: "
        f"invoice_id={invoice_id}, status={last_status}, response={last_response}"
    )


def refresh_invoice_status(
        client: httpx.Client,
        invoice_id: str,
        *,
        token_id: Optional[str] = None,
) -> Dict[str, Any]:
    token_id = token_id
    resp = safe_post(
        client,
        INVOICE_REFRESH_ENDPOINT,
        json={"id": invoice_id, "token": token_id},
        headers={"Authorization": f"Bearer {token_id}"},
    )
    logger.info("发票状态刷新接口响应: %s", resp.json())
    return resp.json()


# 红冲
def red_punch_invoice(
        client: httpx.Client,
        invoice_id: str,
        *,
        token_id: Optional[str] = None
) -> Dict[str, Any]:
    token_id = token_id
    resp = safe_post(
        client,
        RED_PUNCH_ENDPOINT,
        json={"id": invoice_id, "tokenId": token_id},
        headers={"Authorization": f"Bearer {token_id}"},
    )
    logger.info("红冲接口响应: %s", resp.json())
    return resp.json()

