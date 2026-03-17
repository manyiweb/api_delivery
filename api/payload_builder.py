"""Payload 构建器模块。
负责构建美团接口请求参数。
"""
import copy
import json
import time
from typing import Any, Dict, List, Optional, Tuple

import allure

from config import config
from utils.logger import logger


def _require_keys(data: Dict[str, Any], keys: List[str]) -> None:
    """验证必要字段是否存在。"""
    missing = [key for key in keys if key not in data]
    if missing:
        raise KeyError(f"缺少必要字段: {', '.join(missing)}")


def _to_json_string(data: Any) -> str:
    """将数据转换为紧凑的 JSON 字符串。"""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def build_final_payload(raw_data: Dict[str, Any], order_id: Optional[str] = None) -> Tuple[Dict[str, str], str]:
    """构建推单回调请求参数。"""
    if not raw_data:
        raise ValueError("原始数据为空")

    data = copy.deepcopy(raw_data)
    _require_keys(
        data,
        [
            "reconciliation_extras",
            "poi_receive_detail",
            "order_core_params",
            "detail_list",
            "extras_list",
        ],
    )

    timestamp_part = int(time.time() * 1000)
    if order_id is None:
        order_id = int("5301890196" + str(timestamp_part)[-9:])

    poi_receive_detail = data["poi_receive_detail"].copy()
    poi_receive_detail["reconciliationExtras"] = _to_json_string(data["reconciliation_extras"])

    order_dict = data["order_core_params"].copy()
    order_dict.update({
        "ctime": timestamp_part,
        "utime": timestamp_part,
        "orderId": order_id,
        "orderIdView": order_id,
        "detail": _to_json_string(data["detail_list"]),
        "extras": _to_json_string(data["extras_list"]),
        "poiReceiveDetail": _to_json_string(poi_receive_detail),
    })

    final_payload = config.get_final_payload_params().copy()
    final_payload["order"] = _to_json_string(order_dict)

    logger.debug(f"已构建推单 payload，订单ID={order_id}")
    return final_payload, order_id


def build_cancel_payload(raw_data: Dict[str, Any], order_id: str) -> Dict[str, str]:
    """构建取消订单回调请求参数。"""
    if not raw_data:
        raise ValueError("原始数据为空")

    data = copy.deepcopy(raw_data)
    _require_keys(data, ["orderCancel_list"])

    cancel_order_list = data["orderCancel_list"].copy()
    cancel_order_list["orderId"] = order_id

    cancel_payload = config.get_final_payload_params().copy()
    cancel_payload["orderCancel"] = _to_json_string(cancel_order_list)
    logger.debug(f"已构建取消订单 payload，订单ID={order_id}")

    return cancel_payload


def build_apply_refund_payload(raw_data: Dict[str, Any], order_id: str) -> Dict[str, str]:
    """构建整单退款回调请求参数。"""
    if not raw_data:
        raise ValueError("原始数据为空")

    data = copy.deepcopy(raw_data)
    _require_keys(data, ["orderRefund_list"])

    order_refund_list = data["orderRefund_list"].copy()
    order_refund_list["orderId"] = order_id

    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2),
        name="退款请求原始数据",
        attachment_type=allure.attachment_type.JSON,
    )

    final_payload = config.get_final_payload_params().copy()
    final_payload["orderRefund"] = _to_json_string(order_refund_list)
    logger.debug(f"已构建退款 payload，订单ID={order_id}")

    return final_payload
