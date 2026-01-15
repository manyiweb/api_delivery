import httpx
import json
import time
import uuid
from typing import Tuple, Optional, Dict, Any
from functools import wraps

from config import config
from utils.logger import logger

# 使用配置模块中的BASE_URL
BASE_URL = config.BASE_URL
UAT_URL = config.UAT_URL


def generate_trace_id() -> str:
    """生成请求追踪ID"""
    return str(uuid.uuid4())


def retry_on_failure(max_retries: int = 3, delay: int = 2):
    """重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
    """
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
                        logger.warning(f"请求失败，{delay}秒后重试 ({attempt + 1}/{max_retries}): {e}")
                        time.sleep(delay)
                    else:
                        logger.error(f"请求失败，已达到最大重试次数 {max_retries}: {e}")
            raise last_exception
        return wrapper
    return decorator


def handle_response(response: httpx.Response, order_id: Optional[str] = None) -> Tuple[bool, Optional[Dict]]:
    """通用响应处理
    
    Args:
        response: HTTP响应对象
        order_id: 订单ID（可选）
        
    Returns:
        (是否成功, 响应数据字典)
    """
    logger.info(f"状态码: {response.status_code}")

    try:
        response_json = response.json()
        logger.info(f"响应内容: {json.dumps(response_json, indent=2, ensure_ascii=False)}")

        if response.status_code == 200 and response_json.get('data') == "OK":
            order_info = f"订单 {order_id}" if order_id else "请求"
            logger.info(f"{order_info} 推送成功")
            return True, response_json
        else:
            logger.error(f"推送失败，状态码: {response.status_code}，响应: {response_json}")
            return False, response_json

    except json.JSONDecodeError as e:
        logger.error(f"响应不是有效 JSON: {response.text}, 错误: {e}")
        return False, None
    except Exception as e:
        logger.error(f"处理响应时发生未知错误: {e}")
        return False, None


@retry_on_failure(max_retries=config.RETRY_TIMES, delay=config.RETRY_INTERVAL)
def safe_post(client: httpx.Client, endpoint: str, trace_id: Optional[str] = None, **kwargs) -> httpx.Response:
    """带异常处理和重试的 POST 请求
    
    Args:
        client: httpx客户端
        endpoint: API端点
        trace_id: 追踪ID
        **kwargs: 其他请求参数
        
    Returns:
        HTTP响应对象
        
    Raises:
        httpx.HTTPError: HTTP请求错误
    """
    trace_id = trace_id or generate_trace_id()
    start_time = time.time()
    
    try:
        logger.info(f"发送POST请求: {endpoint}, TraceID: {trace_id}")
        response = client.post(endpoint, **kwargs)
        elapsed_time = time.time() - start_time
        logger.info(f"请求耗时: {elapsed_time:.2f}秒")
        
        response.raise_for_status()
        return response
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP状态错误 (TraceID: {trace_id}): {e.response.status_code} - {e}")
        raise
    except httpx.RequestError as e:
        logger.error(f"请求错误 (TraceID: {trace_id}): {e}")
        raise
    except httpx.HTTPError as e:
        logger.error(f"HTTP请求错误 (TraceID: {trace_id}): {e}")
        raise
