import pytest
import httpx
import json

from utils.logger import logger

BASE_URL = 'http://fat-pos.reabam.com:60030/api'


# @pytest.fixture(scope="function")
# def client():
#     return httpx.Client(base_url=BASE_URL)


def handle_response(response, order_id=None):
    """通用响应处理"""
    logger.info(f"状态码: {response.status_code}")

    try:
        response_json = response.json()
        logger.info(f"响应内容: {json.dumps(response_json, indent=2, ensure_ascii=False)}")

        if response.status_code == 200 and response_json.get('data') == "OK":
            logger.info(f"✅ 订单 {order_id} 推送成功")
            return True, response_json
        else:
            logger.error("❌ 推送失败，请检查响应内容")
            return False, response_json

    except json.JSONDecodeError:
        logger.error(f"❌ 响应不是有效 JSON: {response.text}")
        return False, None


def safe_post(client, endpoint, **kwargs):
    """带异常处理的 POST 请求"""
    try:
        return client.post(endpoint, **kwargs)
    except httpx.HTTPError as e:
        logger.error(f"❌ HTTP 请求错误: {e}")
        raise
