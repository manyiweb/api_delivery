import json
import time
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import allure
import httpx

from api.order_api import (
    pos_order_detail,
    pos_order_list,
)
from config import config
from utils.logger import logger


def _iter_dicts(obj: Any) -> Iterable[Dict[str, Any]]:
    stack: List[Any] = [obj]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            yield current
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)


def _is_hex32(value: str) -> bool:
    if len(value) != 32:
        return False
    for ch in value:
        if ch not in "0123456789abcdefABCDEF":
            return False
    return True


def _extract_order_ids(list_resp_json: Dict[str, Any]) -> List[str]:
    order_ids: List[str] = []
    for d in _iter_dicts(list_resp_json):
        if "orderId" not in d:
            continue
        value = d.get("orderId")
        if isinstance(value, str) and value.strip():
            order_ids.append(value.strip())

    if not order_ids:
        return []

    # 优先返回像 32 位十六进制的订单ID（符合常见的内部订单ID）
    hex32 = [oid for oid in order_ids if _is_hex32(oid)]
    if hex32:
        return list(dict.fromkeys(hex32))

    return list(dict.fromkeys(order_ids))


def _detail_matches_source_no(detail_resp_json: Dict[str, Any], expected_source_no: str) -> Tuple[bool, Optional[str]]:
    expected = str(expected_source_no)

    candidate_keys = {
        "SourceNo",
        "sourceNo",
        "outOrderNo",
        "outOrderId",
        "dockOrderNo",
        "dock_order_no",
        "orderIdView",
        "platformOrderId",
        "thirdOrderNo",
    }

    for d in _iter_dicts(detail_resp_json):
        for key, value in d.items():
            if key in candidate_keys and value is not None and str(value) == expected:
                return True, key

    return False, None


def assert_order_persisted_via_list_detail(
    client: httpx.Client,
    token_id: str,
    expected_source_no: str,
    *,
    order_remark: Optional[str] = None,
    timeout: Optional[int] = None,
    interval: int = 2,
    max_pages: int = 3,
    page_size: int = 20,
    user_id: Optional[str] = None,
    company_id: Optional[str] = None,
) -> str:
    """非 FAT 环境：通过 list->detail 方式断言订单已可查询（视为落库成功）。

    - list 接口用于获取候选 orderId
    - detail 接口用于用外卖侧唯一号（expected_source_no）做最终匹配

    返回：匹配到的内部 orderId
    """

    effective_timeout = timeout if timeout is not None else max(
        config.DEFAULT_TIMEOUT, 30)
    start = time.time()
    seen_order_ids: Set[str] = set()

    last_list_resp: Optional[Dict[str, Any]] = None
    last_detail_resp: Optional[Dict[str, Any]] = None

    while time.time() - start < effective_timeout:
        for page_index in range(1, max_pages + 1):
            list_resp = pos_order_list(
                client,
                token_id,
                order_remark=order_remark,
                page_index=page_index,
                page_size=page_size,
            )
            last_list_resp = list_resp
            logger.info(f"订单列表第{page_index}页，响应={list_resp}")
            order_ids = _extract_order_ids(list_resp)
            logger.info(
                f"订单列表第{page_index}页，候选={len(order_ids)}，已检查={len(seen_order_ids)}"
            )

            for internal_order_id in order_ids:
                if internal_order_id in seen_order_ids:
                    continue
                seen_order_ids.add(internal_order_id)

                detail_resp = pos_order_detail(
                    client,
                    token_id,
                    internal_order_id,
                    user_id=user_id,
                    company_id=company_id,
                )
                last_detail_resp = detail_resp

                matched, matched_key = _detail_matches_source_no(
                    detail_resp, str(expected_source_no))
                if matched:
                    allure.attach(
                        str(expected_source_no),
                        name="期望的外卖单号",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    allure.attach(
                        internal_order_id,
                        name="匹配到的内部订单编号",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    if matched_key:
                        allure.attach(
                            matched_key,
                            name="匹配字段",
                            attachment_type=allure.attachment_type.TEXT,
                        )
                    allure.attach(
                        json.dumps(list_resp, ensure_ascii=False, indent=2),
                        name="订单列表响应（匹配）",
                        attachment_type=allure.attachment_type.JSON,
                    )
                    allure.attach(
                        json.dumps(detail_resp, ensure_ascii=False, indent=2),
                        name="订单详情响应（匹配）",
                        attachment_type=allure.attachment_type.JSON,
                    )
                    return internal_order_id

        time.sleep(interval)

    if last_list_resp is not None:
        allure.attach(
            json.dumps(last_list_resp, ensure_ascii=False, indent=2),
            name="订单列表响应（最后一次）",
            attachment_type=allure.attachment_type.JSON,
        )
    if last_detail_resp is not None:
        allure.attach(
            json.dumps(last_detail_resp, ensure_ascii=False, indent=2),
            name="订单详情响应（最后一次）",
            attachment_type=allure.attachment_type.JSON,
        )

    raise AssertionError(
        f"在 {effective_timeout}s 内未通过 list/detail 找到订单；expected_source_no={expected_source_no}"
    )


def _extract_order_status(detail_resp_json: Dict[str, Any]) -> Optional[str]:
    candidate_keys = {
        "orderStatus",
        "OrderStatus",
        "order_status",
    }

    for d in _iter_dicts(detail_resp_json):
        for key in candidate_keys:
            if key in d and d.get(key) is not None:
                return str(d.get(key))

    return None


def assert_order_status_via_detail(
    client: httpx.Client,
    token_id: str,
    internal_order_id: str,
    expected_status: str,
    *,
    timeout: Optional[int] = None,
    interval: int = 2,
    user_id: Optional[str] = None,
    company_id: Optional[str] = None,
) -> str:
    """通过详情接口轮询校验订单状态。

    返回：实际订单状态（匹配后返回）
    """

    effective_timeout = timeout if timeout is not None else max(
        config.DEFAULT_TIMEOUT, 30)
    start = time.time()
    last_detail_resp: Optional[Dict[str, Any]] = None
    last_status: Optional[str] = None

    while time.time() - start < effective_timeout:
        detail_resp = pos_order_detail(
            client,
            token_id,
            internal_order_id,
            user_id=user_id,
            company_id=company_id,
        )
        last_detail_resp = detail_resp

        status = _extract_order_status(detail_resp)
        last_status = status
        logger.info(f"订单状态轮询：内部订单编号={internal_order_id}，当前状态={status}")

        if status is not None and str(status) == str(expected_status):
            allure.attach(
                str(expected_status),
                name="期望订单状态",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                str(status),
                name="实际订单状态",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                json.dumps(detail_resp, ensure_ascii=False, indent=2),
                name="订单详情响应（状态匹配）",
                attachment_type=allure.attachment_type.JSON,
            )
            return str(status)

        time.sleep(interval)

    if last_detail_resp is not None:
        allure.attach(
            json.dumps(last_detail_resp, ensure_ascii=False, indent=2),
            name="订单详情响应（状态校验，最后一次）",
            attachment_type=allure.attachment_type.JSON,
        )

    raise AssertionError(
        f"在 {effective_timeout}s 内订单状态未变为 {expected_status}，当前状态={last_status}"
    )
