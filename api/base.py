"""API 帮助函数，用于 HTTP 调用和响应处理"""
import json
import time
import uuid
from functools import wraps
from typing import Dict, Optional, Tuple

import httpx

from config import config
from utils.logger import logger

BASE_URL = config.get_base_url()


def generate_trace_id() -> str:
    """生成请求跟踪 ID"""
    return str(uuid.uuid4())


def retry_on_failure(max_retries: int = 3, delay: int = 2):
    """HTTP 调用的重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except httpx.HTTPError as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"请求失败，{delay}s 后重试 "
                            f"({attempt + 1}/{max_retries}): {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"请求失败，重试 {max_retries} 次后仍失败: {e}"
                        )
            raise last_exception
        return wrapper
    return decorator


def handle_response(
    response: httpx.Response, order_id: Optional[str] = None
) -> Tuple[bool, Optional[Dict]]:
    """解析 JSON 响应并记录详细信息"""
    logger.info(f"状态码: {response.status_code}")

    try:
        response_json = response.json()
        logger.info(
            "响应内容: %s",
            json.dumps(response_json, indent=2, ensure_ascii=False),
        )

        if response.status_code == 200 and response_json.get("data") == "OK":
            order_info = f"订单 {order_id}" if order_id else "请求"
            logger.info(f"[成功] {order_info} 成功")
            return True, response_json

        logger.error(
            f"[失败] status={response.status_code}, response={response_json}"
        )
        return False, response_json

    except json.JSONDecodeError as e:
        logger.error(f"响应不是合法 JSON: {response.text}, 错误={e}")
        return False, None
    except Exception as e:
        logger.error(f"处理响应时发生未知错误: {e}")
        return False, None


@retry_on_failure(max_retries=config.RETRY_TIMES, delay=config.RETRY_INTERVAL)
def safe_post(
    client: httpx.Client,
    endpoint: str,
    trace_id: Optional[str] = None,
    **kwargs,
) -> httpx.Response:
    """带重试和错误日志的 POST 请求"""
    trace_id = trace_id or generate_trace_id()
    start_time = time.time()

    try:
        logger.info(f"发送请求 {endpoint}，追踪号={trace_id}")
        response = client.post(endpoint, **kwargs)
        elapsed_time = time.time() - start_time
        logger.info(f"请求耗时: {elapsed_time:.2f}s")

        response.raise_for_status()
        return response

    except httpx.HTTPStatusError as e:
        logger.error(
            f"状态码错误（追踪号: {trace_id}）: "
            f"{e.response.status_code} - {e}"
        )
        raise
    except httpx.RequestError as e:
        logger.error(f"请求错误（追踪号: {trace_id}）: {e}")
        raise
    except httpx.HTTPError as e:
        logger.error(f"网络错误（追踪号: {trace_id}）: {e}")
        raise
