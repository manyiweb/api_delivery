import copy
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import httpx

from api.base import safe_post
from conftest import access_token
from utils.file_loader import (
    get_data_file_path,
    load_yaml_data,
)
from utils.logger import logger

APPLY_INVOICE_ENDPOINT = "/hr/retail/invoice/batchApply"
INVOICE_DETAIL_ENDPOINT = "/hr/retail/invoice/detail"
INVOICE_REFRESH_ENDPOINT = "/hr/retail/invoice/refreshInvoiceStatus"
RED_PUNCH_ENDPOINT = "/hr/retail/invoice/redPunch"


# 加载开票请求参数


def _load_invoice_payload(section: str = "orderInvoice") -> Dict[str, Any]:
    """加载开票请求参数

    Args:
        section: YAML 中的配置段名称，默认为 "orderInvoice"（基于订单开票）
               无订单开票时使用 "noneorderInvoice"
    """
    raw_data = load_yaml_data(get_data_file_path("invoice_data.yaml")) or {}
    if not isinstance(raw_data, dict):
        raise ValueError("data/invoice_data.yaml 缺少或无效")

    payload = raw_data.get(section)
    if not isinstance(payload, dict):
        raise ValueError(f"data/invoice_data.yaml 缺少 {section} 配置")

    return copy.deepcopy(payload)


# 构建单独开票请求参数


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


# 构建合并开票请求参数


def build_merge_invoice_payload(
        order_ids: List[str],
        token_id: str,
        *,
        amount_list: Optional[List[Any]] = None,
        extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = _load_invoice_payload()
    if not order_ids:
        raise ValueError("合并开票订单为空")

    payload["orderIds"] = list(order_ids)
    payload["tokenId"] = token_id

    order_amount_list = payload.get("orderAmountList")
    if not isinstance(order_amount_list, list) or not order_amount_list:
        raise ValueError("invoice_data.yaml 缺少 orderAmountList 配置")

    template = order_amount_list[0]
    default_amount = template.get("currentInvoiceAmount")

    if amount_list is not None and len(amount_list) != len(order_ids):
        raise ValueError("合并开票订单数量与金额数量不一致")

    merged_amount_list: List[Dict[str, Any]] = []
    for idx, order_id in enumerate(order_ids):
        item = template.copy()
        item["orderId"] = order_id
        if amount_list is not None:
            item["currentInvoiceAmount"] = amount_list[idx]
        else:
            item["currentInvoiceAmount"] = default_amount
        merged_amount_list.append(item)

    payload["orderAmountList"] = merged_amount_list
    # 合并开票设置 billingType 为 1
    payload["billingType"] = 1

    if extra:
        payload.update(extra)

    return payload


# 构建订单号为空请求参数


def build_empty_order_id_payload(token_id: str) -> Dict[str, Any]:
    """构建 orderAmountList 中 orderId 为空的 payload，用于测试空指针异常"""
    payload = _load_invoice_payload()
    payload["tokenId"] = token_id
    payload["orderIds"] = [""]

    order_amount_list = payload.get("orderAmountList")
    if not isinstance(order_amount_list, list) or not order_amount_list:
        raise ValueError("invoice_data.yaml 缺少 orderAmountList 配置")

    # 将 orderAmountList 中的 orderId 设为空字符串
    for item in order_amount_list:
        item["orderId"] = ""

    payload["orderAmountList"] = order_amount_list
    return payload


# 构建无订单开票请求参数


def build_none_order_invoice_payload(
        token_id: str,
        *,
        extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """构建无订单开票请求参数，使用 invoice_data.yaml 中的 noneorderInvoice 配置"""
    payload = _load_invoice_payload(section="noneorderInvoice")
    payload["tokenId"] = token_id

    if extra:
        payload.update(extra)

    return payload


# 解析开票接口响应


def _parse_apply_invoice_response(resp: httpx.Response) -> Tuple[str, Dict[str, Any]]:
    response_json = resp.json()
    if not isinstance(response_json, dict):
        raise ValueError("开票接口响应不是字典")
    logger.info("开票接口响应: %s", response_json)
    data = response_json.get("data")
    if not isinstance(data, dict):
        raise ValueError("开票接口响应缺少data")
    invoice_id = data.get("invoiceId")
    if not invoice_id:
        raise ValueError("开票号为空")
    logger.info("开票号: invoice_id=%s", invoice_id)
    return str(invoice_id), response_json


# 执行开票请求（传入已构建的 payload）


def execute_apply_invoice(
        client: httpx.Client,
        payload: Dict[str, Any],
        *,
        token_id: Optional[str] = None,
        return_response: bool = False,
        parse_response: bool = True,
) -> Union[str, Tuple[str, Dict[str, Any]], httpx.Response]:
    """执行开票请求，传入已构建好的 payload

    Args:
        parse_response: 是否解析响应提取 invoice_id，默认为 True
                       异常场景测试时设为 False，返回原始 Response
    """
    resp = safe_post(
        client,
        APPLY_INVOICE_ENDPOINT,
        json=payload,
        headers={"Authorization": f"Bearer {token_id}"},
    )

    if not parse_response:
        return resp

    invoice_id, response_json = _parse_apply_invoice_response(resp)
    if return_response:
        return invoice_id, response_json
        return invoice_id


# 申请开票（一站式：构建参数 + 执行请求）
def apply_invoice_for_order(
        client: httpx.Client,
        order_id: str,
        *,
        token_id: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
        return_response: bool = False,
) -> Union[str, Tuple[str, Dict[str, Any]]]:
    """为单个订单申请开票，自动构建请求参数并执行"""
    payload = build_apply_invoice_payload(order_id, token_id, extra=extra)

    return execute_apply_invoice(
        client,
        payload,
        token_id=token_id,
        return_response=return_response,
    )


# 封装查询开票状态接口
def query_invoice_status(
        client: httpx.Client,
        invoice_id: str,
        *,
        token_id: Optional[str] = None,
        return_response: bool = False,
) -> Union[str, Tuple[str, Dict[str, Any]]]:
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
        if not isinstance(response_json, dict):
            raise ValueError("开票状态响应不是字典")
        last_response = response_json
        logger.info("开票详情响应（%s/%s）: %s", attempt, max_attempts, response_json)

        data = last_response.get("data") if isinstance(
            last_response, dict) else None
        last_status = data.get("status") if isinstance(data, dict) else None

        logger.info("开票状态=%s", last_status)
        if last_status == "INVOICED":
            if return_response:
                return str(last_status), response_json
            return str(last_status)

        if attempt < max_attempts:
            time.sleep(2)

    raise RuntimeError(
        f"开票状态在{max_attempts}次轮询后仍未成功: "
        f"invoice_id={invoice_id}, status={last_status}, response={last_response}"
    )


# 封装发票状态刷新接口


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


# 封装红冲接口
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
