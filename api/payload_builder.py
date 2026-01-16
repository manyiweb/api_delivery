"""Payload builder for Meituan callbacks."""
import copy
import json
import time
from typing import Dict, Optional, Tuple

import allure

from config import config
from utils.logger import logger


def _require_keys(data: Dict, keys):
    missing = [key for key in keys if key not in data]
    if missing:
        raise KeyError(f"Missing required keys: {', '.join(missing)}")


def build_final_payload(raw_data: Dict, order_id: Optional[str] = None) -> Tuple[Dict[str, str], str]:
    """Build payload for push order callback."""
    if not raw_data:
        raise ValueError("raw_data is empty")

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

    reconciliation_extras_str = json.dumps(
        data["reconciliation_extras"],
        ensure_ascii=False,
        separators=(",", ":"),
    )

    poi_receive_detail = data["poi_receive_detail"].copy()
    poi_receive_detail["reconciliationExtras"] = reconciliation_extras_str

    order_dict = data["order_core_params"].copy()
    order_dict["ctime"] = timestamp_part
    order_dict["utime"] = timestamp_part
    order_dict["orderId"] = order_id
    order_dict["orderIdView"] = order_id
    order_dict["detail"] = json.dumps(
        data["detail_list"],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    order_dict["extras"] = json.dumps(
        data["extras_list"],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    order_dict["poiReceiveDetail"] = json.dumps(
        poi_receive_detail,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    final_payload = config.get_final_payload_params().copy()
    final_payload["order"] = json.dumps(
        order_dict,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    logger.debug(f"Push order payload built for order_id={order_id}")
    return final_payload, order_id


def build_cancel_payload(raw_data: Dict, order_id: str) -> Dict[str, str]:
    """Build payload for cancel order callback."""
    if not raw_data:
        raise ValueError("raw_data is empty")

    data = copy.deepcopy(raw_data)
    _require_keys(data, ["orderCancel_list"])

    cancel_order_list = data["orderCancel_list"].copy()
    cancel_order_list["orderId"] = order_id
    cancel_order_json = json.dumps(
        cancel_order_list,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    cancel_payload = config.get_final_payload_params().copy()
    cancel_payload["orderCancel"] = cancel_order_json
    logger.debug(f"Cancel order payload built for order_id={order_id}")

    return cancel_payload


def build_apply_refund_payload(raw_data: Dict, order_id: str) -> Dict[str, str]:
    """Build payload for full refund callback."""
    if not raw_data:
        raise ValueError("raw_data is empty")

    data = copy.deepcopy(raw_data)
    _require_keys(data, ["orderRefund_list"])

    order_refund_list = data["orderRefund_list"].copy()
    order_refund_list["orderId"] = order_id
    order_refund_json = json.dumps(
        order_refund_list,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2),
        name="refund request raw data",
        attachment_type=allure.attachment_type.JSON,
    )

    final_payload = config.get_final_payload_params().copy()
    final_payload["orderRefund"] = order_refund_json
    logger.debug(f"Refund payload built for order_id={order_id}")

    return final_payload

