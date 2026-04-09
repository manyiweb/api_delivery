"""开交班相关API接口"""
from typing import Dict, Any, Tuple
import time

import httpx

from api.base import safe_post
from utils.file_loader import load_yaml_data, get_data_file_path
from utils.logger import logger

# 获取开交班状态接口（v2）
GET_HANDOVER_STATE_API = "/retail-order-fast/orderfast/app/Handover/v2/GetHandoverState"
# 确认交班接口
CONFIRM_HANDOVER_API = "/retail-order-front/app/Handover/Confirm"
# 开班接口
ADD_HANDOVER_API = "/retail-order-front/app/Handover/ADD"


def build_handover_params(
    data_key: str,
    token_id: str,
) -> Dict[str, Any]:
    """构建开交班请求参数

    Args:
        data_key: YAML配置段名称
        token_id: 访问令牌

    Returns:
        请求参数字典
    """
    read_payload = load_yaml_data(get_data_file_path("order_data.yaml")) or {}
    final_payload = read_payload.get(data_key)
    if not isinstance(final_payload, dict):
        raise ValueError(f"缺少或无效的配置段: {data_key!r}")

    final_payload = final_payload.copy()
    final_payload["tokenId"] = token_id
    return final_payload


def get_handover_state(client: httpx.Client, token_id: str) -> Tuple[int, Dict[str, Any]]:
    """获取开交班状态（v2）

    Args:
        client: HTTP客户端
        token_id: 访问令牌

    Returns:
        (状态码, 响应数据) - data.code 为 0 表示已开班，非0 表示未开班
    """
    payload = build_handover_params("getHandoverState", token_id)

    # 添加时间戳参数
    timestamp = int(time.time() * 1000)
    url = f"{GET_HANDOVER_STATE_API}?newgetTime={timestamp}"

    logger.info("获取开交班状态接口请求: %s", payload)
    resp = safe_post(
        client,
        url,
        headers={"Authorization": f"Bearer {token_id}"},
        json=payload
    )

    response_data = resp.json()
    logger.info("获取开交班状态接口响应: %s", response_data)

    # v2接口通过 data.code 判断状态，0=已开班
    data = response_data.get("data", {})
    state_code = data.get("code", -1)
    return state_code, response_data


def confirm_handover(client: httpx.Client, token_id: str) -> Dict[str, Any]:
    """确认交班

    Args:
        client: HTTP客户端
        token_id: 访问令牌

    Returns:
        响应数据
    """
    payload = build_handover_params("confirmHandover", token_id)

    # 添加时间戳参数
    timestamp = int(time.time() * 1000)
    url = f"{CONFIRM_HANDOVER_API}?newgetTime={timestamp}"

    logger.info("确认交班接口请求: %s", payload)
    resp = safe_post(
        client,
        url,
        headers={"Authorization": f"Bearer {token_id}"},
        json=payload
    )

    response_data = resp.json()
    logger.info("确认交班接口响应: %s", response_data)
    return response_data


def add_handover(client: httpx.Client, token_id: str) -> Tuple[str, Dict[str, Any]]:
    """开班

    Args:
        client: HTTP客户端
        token_id: 访问令牌

    Returns:
        (班次ID, 响应数据)
    """
    payload = build_handover_params("addHandover", token_id)

    # 添加时间戳参数
    timestamp = int(time.time() * 1000)
    url = f"{ADD_HANDOVER_API}?newgetTime={timestamp}"

    logger.info("开班接口请求: %s", payload)
    resp = safe_post(
        client,
        url,
        headers={"Authorization": f"Bearer {token_id}"},
        json=payload
    )

    response_data = resp.json()
    logger.info("开班接口响应: %s", response_data)

    dh_id = response_data.get("dhId", "")
    return dh_id, response_data


def ensure_handover_open(client: httpx.Client, token_id: str) -> bool:
    """确保门店已开班

    检查开交班状态，如果未开班则自动进行交班和开班操作

    Args:
        client: HTTP客户端
        token_id: 访问令牌

    Returns:
        True表示已开班，False表示操作失败
    """
    try:
        # 1. 获取当前开交班状态
        state_code, state_data = get_handover_state(client, token_id)

        # 2. data.code == 0 表示已开班，非0表示需要交班再开班
        if state_code == 0:
            logger.info("门店已开班，无需操作")
        else:
            logger.info("检测到门店未开班(code=%s)，开始执行交班+开班操作", state_code)

            # 2.1 确认交班
            confirm_result = confirm_handover(client, token_id)
            if confirm_result.get("ResultString") != "success":
                logger.error("交班失败: %s", confirm_result)
                return False
            logger.info("交班成功")

            # 2.2 开班
            dh_id, add_result = add_handover(client, token_id)
            if add_result.get("ResultString") != "success":
                logger.error("开班失败: %s", add_result)
                return False
            logger.info("开班成功，班次ID: %s", dh_id)

        return True

    except Exception as e:
        logger.error("开交班操作异常: %s", e)
        return False
