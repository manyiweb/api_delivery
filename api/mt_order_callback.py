import json
import os
from typing import Optional, Tuple

import allure
import httpx

from api.base import (
    handle_response,
    safe_post,
)
from api.mt_order_payload_builder import (
    build_mt_apply_refund_payload,
    build_mt_cancel_payload,
    build_mt_push_payload,
)
from utils.file_loader import (
    get_data_file_path,
    load_yaml_data,
)
from utils.logger import logger


def _post_and_extract(
    client: httpx.Client,
    endpoint: str,
    payload: dict,
    attach_name: str,
    order_id: Optional[str] = None,
) -> Optional[str]:
    response = safe_post(client, endpoint, data=payload)
    success, response_json = handle_response(response, order_id)

    if response_json is not None:
        allure.attach(
            json.dumps(response_json, ensure_ascii=False, indent=2),
            name=attach_name,
            attachment_type=allure.attachment_type.JSON,
        )
        return response_json.get("data")

    allure.attach(
        response.text,
        name=attach_name,
        attachment_type=allure.attachment_type.TEXT,
    )
    return None


def mt_push_order(client: httpx.Client, mt_order_id: Optional[str] = None) -> Tuple[str, str]:
    """推单回调"""
    if os.getenv("ENV") == "uat":
        with allure.step("加载推单数据"):
            mt_push_data = load_yaml_data(
                get_data_file_path("mt_delivery_data_uat.yaml"))
    else:
        with allure.step("加载推单数据"):
            mt_push_data = load_yaml_data(
                get_data_file_path("mt_delivery_data.yaml"))

    with allure.step("构建推单请求体"):
        final_payload, mt_order_id = build_mt_push_payload(
            mt_push_data, mt_order_id)
        allure.attach(
            str(mt_order_id),
            name="外卖单号",
            attachment_type=allure.attachment_type.TEXT,
        )
        logger.info(f"推单请求体: {final_payload}")

    with allure.step("发送推单回调"):
        result = _post_and_extract(
            client,
            "/dock/mt/v2/order/callback",
            final_payload,
            attach_name="推单响应",
            order_id=str(mt_order_id),
        )
        return result, mt_order_id


def mt_push_order_callback(client: httpx.Client, mt_order_id: Optional[str] = None) -> Tuple[str, str]:
    """推单回调的兼容包装"""
    return mt_push_order(client, mt_order_id)


def mt_cancel_order(client: httpx.Client, mt_order_id: str) -> Optional[str]:
    """取消订单回调"""
    with allure.step("加载取消订单数据"):
        logger.info(f"取消订单美团单号: {mt_order_id}")
        mt_cancel_data = load_yaml_data(
            get_data_file_path("mt_cancel_order.yaml"))

    with allure.step("构建取消订单请求体"):
        final_payload = build_mt_cancel_payload(mt_cancel_data, mt_order_id)
        allure.attach(
            str(mt_order_id),
            name="取消订单ID",
            attachment_type=allure.attachment_type.TEXT,
        )
        logger.info(f"取消订单请求体: {final_payload}")

    with allure.step("发送取消订单回调"):
        return _post_and_extract(
            client,
            "/dock/mt/v2/order/cancel/callback",
            final_payload,
            attach_name="取消订单响应",
            order_id=str(mt_order_id),
        )


def mt_cancel_order_callback(client: httpx.Client, order_id: str) -> Optional[str]:
    """取消订单回调的兼容包装"""
    return mt_cancel_order(client, order_id)


def mt_refund_order(client: httpx.Client, mt_order_id: str) -> Optional[str]:
    """全额退款回调"""
    with allure.step("加载退款数据"):
        logger.info(f"美团退款订单号: {mt_order_id}")
        mt_refund_data = load_yaml_data(
            get_data_file_path("mt_refund_order.yaml"))

    with allure.step("构建退款请求体"):
        final_payload = build_mt_apply_refund_payload(
            mt_refund_data, mt_order_id)
        logger.info(f"退款请求体: {final_payload}")

    with allure.step("发送退款回调"):
        return _post_and_extract(
            client,
            "/reabam-external-access/dock/mt/v2/order/refund/callback",
            final_payload,
            attach_name="退款响应",
            order_id=str(mt_order_id),
        )


def mt_full_refund_callback(client: httpx.Client, order_id: str) -> Optional[str]:
    """全额退款回调的兼容包装"""
    return mt_refund_order(client, order_id)


def mt_partial_refund(client: httpx.Client):
    """部分退款占位实现"""
    logger.warning("部分退款暂未实现")
    client.post("/mt/v2/order/partial/refund/callback", json={})
