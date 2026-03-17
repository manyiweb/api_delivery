"""API 基础模块。
提供通用的 HTTP 请求处理、响应解析和异常处理。
"""
import json
import time
import uuid
from functools import wraps
from typing import Dict, Optional, Tuple

import httpx

from config import config
from utils.logger import logger


def generate_trace_id() -> str:
    """生成请求追踪 ID。"""
    return str(uuid.uuid4())


def retry_on_failure(max_retries: int = 3, delay: int = 2):
    """重试装饰器。"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except httpx.HTTPStatusError as e:
                    last_exception = e
                    logger.error(
                        f"HTTP 状态错误 (尝试 {attempt + 1}/{max_retries}): "
                        f"状态码 {e.response.status_code} - {e}"
                    )
                    if attempt < max_retries - 1:
                        logger.warning(f"{delay} 秒后重试...")
                        time.sleep(delay)
                except httpx.RequestError as e:
                    last_exception = e
                    logger.error(
                        f"请求错误 (尝试 {attempt + 1}/{max_retries}): {e}"
                    )
                    if attempt < max_retries - 1:
                        logger.warning(f"{delay} 秒后重试...")
                        time.sleep(delay)
                except httpx.HTTPError as e:
                    last_exception = e
                    logger.error(
                        f"HTTP 错误 (尝试 {attempt + 1}/{max_retries}): {e}"
                    )
                    if attempt < max_retries - 1:
                        logger.warning(f"{delay} 秒后重试...")
                        time.sleep(delay)

            logger.error(f"请求失败，已达到最大重试次数 {max_retries}")
            raise last_exception
        return wrapper
    return decorator


def handle_response(
    response: httpx.Response, order_id: Optional[str] = None
) -> Tuple[bool, Optional[Dict]]:
    """通用响应处理。"""
    logger.info(f"状态码: {response.status_code}")

    try:
        response_json = response.json()
        logger.info(
            "响应内容: %s",
            json.dumps(response_json, indent=2, ensure_ascii=False),
        )

        if response.status_code == 200 and response_json.get("data") == "OK":
            order_info = f"订单 {order_id}" if order_id else "请求"
            logger.info(f"{order_info} 推送成功")
            return True, response_json

        logger.error(
            f"推送失败，状态码: {response.status_code}，响应: {response_json}"
        )
        return False, response_json

    except json.JSONDecodeError as e:
        logger.error(f"响应不是有效 JSON: {response.text}, 错误: {e}")
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
    """带重试的 POST 请求。"""
    trace_id = trace_id or generate_trace_id()
    start_time = time.time()

    logger.info(f"发送 POST 请求: {endpoint}, TraceID: {trace_id}")
    response = client.post(endpoint, **kwargs)
    elapsed_time = time.time() - start_time
    logger.info(f"请求耗时: {elapsed_time:.2f} 秒")

    response.raise_for_status()
    return response
