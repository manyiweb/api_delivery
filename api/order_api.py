import json
from typing import Any, Dict, Optional

import allure
import httpx

from api.base import safe_post
from utils.file_loader import (
    get_data_file_path,
    load_yaml_data,
)

ORDER_LIST_ENDPOINT = "/retail-order-front/app/Business/Order/List"
ORDER_DETAIL_ENDPOINT = "/retail-order-front/app/Business/Order/Dock/Detail"

# 加载订单数据
def _load_order_payload(section: str) -> Dict[str, Any]:
    raw_data = load_yaml_data(get_data_file_path("order_data.yaml")) or {}
    payload = raw_data.get(section)
    if not isinstance(payload, dict):
        raise ValueError(f"data/order_data.yaml 缺少或无效的配置段: '{section}'")
    return payload.copy()

# POS 订单列表接口
def pos_order_list(
    client: httpx.Client,
    token_id: str,
    *,
    order_remark: Optional[str] = None,
    page_index: Optional[int] = None,
    page_size: Optional[int] = None,
    extra: Optional[Dict[str, Any]] = None,
    attach: bool = False,
) -> Dict[str, Any]:
    """POS 订单列表"""
    payload = _load_order_payload("orderList")
    payload["tokenId"] = token_id

    if order_remark is not None:
        payload["orderRemark"] = order_remark
    if page_index is not None:
        payload["pageIndex"] = page_index
    if page_size is not None:
        payload["pageSize"] = page_size
    if extra:
        payload.update(extra)

    if attach:
        allure.attach(
            json.dumps(payload, ensure_ascii=False, indent=2),
            name="收银端订单列表请求",
            attachment_type=allure.attachment_type.JSON,
        )

    resp = safe_post(client, ORDER_LIST_ENDPOINT, json=payload)
    resp_json: Dict[str, Any] = resp.json()

    if attach:
        allure.attach(
            json.dumps(resp_json, ensure_ascii=False, indent=2),
            name="收银端订单列表响应",
            attachment_type=allure.attachment_type.JSON,
        )

    return resp_json

# POS 订单详情接口
def pos_order_detail(
    client: httpx.Client,
    token_id: str,
    order_id: str,
    *,
    user_id: Optional[str] = None,
    company_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
    attach: bool = False,
) -> Dict[str, Any]:
    """POS 订单详情"""
    payload = _load_order_payload("orderDetail")
    payload["tokenId"] = token_id
    payload["orderId"] = order_id

    if user_id is not None:
        payload["userId"] = user_id
    if company_id is not None:
        payload["companyId"] = company_id
    if extra:
        payload.update(extra)

    if attach:
        allure.attach(
            json.dumps(payload, ensure_ascii=False, indent=2),
            name="收银端订单详情请求",
            attachment_type=allure.attachment_type.JSON,
        )

    resp = safe_post(client, ORDER_DETAIL_ENDPOINT, json=payload)
    resp_json: Dict[str, Any] = resp.json()

    if attach:
        allure.attach(
            json.dumps(resp_json, ensure_ascii=False, indent=2),
            name="收银端订单详情响应",
            attachment_type=allure.attachment_type.JSON,
        )

    return resp_json
