import json
import os
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


def push_order(client: httpx.Client, order_id: Optional[str] = None) -> Tuple[str, str]:
    """Push order callback."""
    if os.getenv("ENV") == "uat":
        with allure.step("Load push order data"):
            raw_data = load_yaml_data(get_data_file_path("delivery_data_uat.yaml"))
    else:
        with allure.step("Load push order data"):
            raw_data = load_yaml_data(get_data_file_path("delivery_data.yaml"))

    with allure.step("Build push order payload"):
        final_payload, order_id = build_final_payload(raw_data, order_id)
        allure.attach(
            str(order_id),
            name="order_id",
            attachment_type=allure.attachment_type.TEXT,
        )
        logger.info(f"Push order payload: {final_payload}")

    with allure.step("Send push order callback"):
        result = _post_and_extract(
            client,
            "/dock/mt/v2/order/callback",
            final_payload,
            attach_name="push order response",
            order_id=str(order_id),
        )
        return result, order_id


def mt_push_order_callback(client: httpx.Client, order_id: Optional[str] = None) -> Tuple[str, str]:
    """Compatibility wrapper for push order callback."""
    return push_order(client, order_id)


def cancel_order(client: httpx.Client, order_id: str) -> Optional[str]:
    """Cancel order callback."""
    with allure.step("Load cancel order data"):
        logger.info(f"Cancel order: {order_id}")
        raw_data = load_yaml_data(get_data_file_path("cancel_order.yaml"))

    with allure.step("Build cancel order payload"):
        final_payload = build_cancel_payload(raw_data, order_id)
        allure.attach(
            str(order_id),
            name="cancel order id",
            attachment_type=allure.attachment_type.TEXT,
        )
        logger.info(f"Cancel order payload: {final_payload}")

    with allure.step("Send cancel order callback"):
        return _post_and_extract(
            client,
            "/dock/mt/v2/order/cancel/callback",
            final_payload,
            attach_name="cancel order response",
            order_id=str(order_id),
        )


def mt_cancel_order_callback(client: httpx.Client, order_id: str) -> Optional[str]:
    """Compatibility wrapper for cancel order callback."""
    return cancel_order(client, order_id)


def refund_order(client: httpx.Client, order_id: str) -> Optional[str]:
    """Full refund callback."""
    with allure.step("Load refund data"):
        logger.info(f"Refund order: {order_id}")
        raw_data = load_yaml_data(get_data_file_path("refund_order.yaml"))

    with allure.step("Build refund payload"):
        final_payload = build_apply_refund_payload(raw_data, order_id)
        logger.info(f"Refund payload: {final_payload}")

    with allure.step("Send refund callback"):
        return _post_and_extract(
            client,
            "/reabam-external-access/dock/mt/v2/order/refund/callback",
            final_payload,
            attach_name="refund response",
            order_id=str(order_id),
        )


def mt_full_refund_callback(client: httpx.Client, order_id: str) -> Optional[str]:
    """Compatibility wrapper for full refund callback."""
    return refund_order(client, order_id)


def partial_refund(client: httpx.Client):
    """Placeholder for partial refund."""
    logger.warning("Partial refund not implemented")
    client.post("/mt/v2/order/partial/refund/callback", json={})
