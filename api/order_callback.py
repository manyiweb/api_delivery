import json
from typing import Optional, Tuple

import allure
import httpx

from api.base import handle_response, safe_post
from api.payload_builder import (
    build_apply_refund_payload,
    build_cancel_payload,
    build_final_payload,
)
from utils.file_loader import get_data_file_path, load_yaml_data
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

    if response_json is not None and isinstance(response_json, dict):
        allure.attach(
            json.dumps(response_json, ensure_ascii=False, indent=2),
            name=attach_name,
            attachment_type=allure.attachment_type.JSON,
        )
        return response_json.get("data")

    if response_json is None:
        logger.warning(f"API调用失败或响应解析失败: {attach_name}")

    allure.attach(
        response.text,
        name=attach_name,
        attachment_type=allure.attachment_type.TEXT,
    )
    return None


def mt_push_order_callback(client: httpx.Client, order_id: Optional[str] = None) -> Tuple[Optional[str], str]:
    """美团推单回调。"""
    with allure.step("读取推单数据"):
        raw_data = load_yaml_data(get_data_file_path("delivery_data.yaml"))

    with allure.step("构建推单参数"):
        final_payload, order_id = build_final_payload(raw_data, order_id)
        allure.attach(
            str(order_id),
            name="生成的订单ID",
            attachment_type=allure.attachment_type.TEXT,
        )
        logger.info(f"推单参数: {final_payload}")

    with allure.step("请求美团推单回调接口"):
        result = _post_and_extract(
            client,
            "/dock/mt/v2/order/callback",
            final_payload,
            attach_name="推单响应",
            order_id=str(order_id),
        )
        return result, order_id


def mt_cancel_order_callback(client: httpx.Client, order_id: str) -> Optional[str]:
    """美团取消订单回调。"""
    with allure.step("读取取消订单数据"):
        logger.info(f"取消订单中，订单ID: {order_id}")
        raw_data = load_yaml_data(get_data_file_path("cancel_order.yaml"))

    with allure.step("构建取消订单参数"):
        final_payload = build_cancel_payload(raw_data, order_id)
        allure.attach(
            str(order_id),
            name="取消的订单ID",
            attachment_type=allure.attachment_type.TEXT,
        )
        logger.info(f"取消订单参数: {final_payload}")

    with allure.step("请求取消订单回调接口"):
        return _post_and_extract(
            client,
            "/dock/mt/v2/order/cancel/callback",
            final_payload,
            attach_name="取消订单响应",
            order_id=str(order_id),
        )


def mt_full_refund_callback(client: httpx.Client, order_id: str) -> Optional[str]:
    """美团整单退款回调。"""
    with allure.step("读取退款数据"):
        logger.info(f"整单退款中，订单ID: {order_id}")
        raw_data = load_yaml_data(get_data_file_path("refund_order.yaml"))

    with allure.step("构建退款参数"):
        final_payload = build_apply_refund_payload(raw_data, order_id)
        logger.info(f"整单退款参数: {final_payload}")

    with allure.step("请求整单退款回调接口"):
        return _post_and_extract(
            client,
            "/reabam-external-access/dock/mt/v2/order/refund/callback",
            final_payload,
            attach_name="整单退款响应",
            order_id=str(order_id),
        )



