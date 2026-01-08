import httpx
import allure
import json
from typing import Tuple, Optional

from api.base import BASE_URL, safe_post
from api.payload_builder import build_final_payload, build_cancel_payload, build_apply_refund_payload
from utils.file_loader import load_yaml_data, get_data_file_path
from utils.logger import logger


def push_order(client: httpx.Client, order_id: Optional[str] = None) -> Tuple[str, str]:
    """美团推单接口
    
    Args:
        client: HTTP客户端
        order_id: 订单ID（可选，用于幂等性测试）
        
    Returns:
        (API响应数据, 订单ID)
    """
    with allure.step("读取推单数据"):
        raw_data = load_yaml_data(get_data_file_path('delivery_data.yaml'))

    with allure.step("构建推单参数"):
        final_push_order_payload, order_id = build_final_payload(raw_data, order_id)
        allure.attach(str(order_id), name="生成的订单ID", attachment_type=allure.attachment_type.TEXT)
        logger.info(f"推单参数: {final_push_order_payload}")

    with allure.step("请求美团推单接口"):
        responses = safe_post(client, '/dock/mt/v2/order/callback', data=final_push_order_payload)
        response_data = responses.json()
        allure.attach(json.dumps(response_data, ensure_ascii=False, indent=2),
                      name="推单响应", attachment_type=allure.attachment_type.JSON)
        return response_data.get('data'), order_id


# 为了兼容性，保留旧的函数名，但使用新名称调用
def mt_push_order_callback(client: httpx.Client, order_id: Optional[str] = None) -> Tuple[str, str]:
    """美团推单回调（兼容旧命名）"""
    return push_order(client, order_id)


def cancel_order(client: httpx.Client, order_id: str) -> str:
    """美团取消订单接口
    
    Args:
        client: HTTP客户端
        order_id: 订单ID
        
    Returns:
        API响应数据
    """
    with allure.step("读取取消订单数据"):
        logger.info(f"取消订单中, 订单ID: {order_id}")
        raw_data = load_yaml_data(get_data_file_path('cancel_order.yaml'))
        logger.debug(f"取消订单原始数据: {raw_data}")

    with allure.step("构建取消订单参数"):
        final_cancel_order_payload = build_cancel_payload(raw_data, order_id)
        allure.attach(str(order_id), name="取消的订单ID", attachment_type=allure.attachment_type.TEXT)
        logger.info(f"取消订单参数: {final_cancel_order_payload}")

    with allure.step("请求取消订单接口"):
        responses = safe_post(client, '/dock/mt/v2/order/cancel/callback', data=final_cancel_order_payload)
        response_data = responses.json()
        allure.attach(json.dumps(response_data, ensure_ascii=False, indent=2),
                      name="取消订单响应", attachment_type=allure.attachment_type.JSON)
        return response_data.get('data')


# 为了兼容性，保留旧的函数名，但使用新名称调用
def mt_cancel_order_callback(client: httpx.Client, order_id: str) -> str:
    """美团取消订单回调（兼容旧命名）"""
    return cancel_order(client, order_id)


def refund_order(client: httpx.Client, order_id: str) -> str:
    """美团整单退款接口
    
    Args:
        client: HTTP客户端
        order_id: 订单ID
        
    Returns:
        API响应数据
    """
    with allure.step("读取申请订单整单退数据"):
        logger.info(f"生成整单退款订单中, 订单ID: {order_id}")
        raw_data = load_yaml_data(get_data_file_path('refund_order.yaml'))
        logger.debug(f"取消订单原始数据: {raw_data}")

    with allure.step("构建申请订单整单退参数"):
        final_full_order_payload = build_apply_refund_payload(raw_data, order_id)
        logger.info(f"整单退款最终请求数据: {final_full_order_payload}")

    with allure.step("请求申请订单整单退接口"):
        responses = safe_post(client, '/reabam-external-access/dock/mt/v2/order/refund/callback',
                              data=final_full_order_payload)
        response_data = responses.json()
        allure.attach(json.dumps(response_data, ensure_ascii=False, indent=2),
                      name="申请订单整单退响应", attachment_type=allure.attachment_type.JSON)
        return response_data.get('data')


# 为了兼容性，保留旧的函数名，但使用新名称调用
def mt_full_refund_callback(client: httpx.Client, order_id: str) -> str:
    """美团整单退款回调（兼容旧命名）"""
    return refund_order(client, order_id)


# 部分退款（待实现）
def partial_refund(client: httpx.Client):
    """部分退款接口（待实现）
    
    Args:
        client: HTTP客户端
    """
    partialRefund = client.post('/mt/v2/order/partial/refund/callback', json={})
    # TODO: 实现部分退款逻辑


if __name__ == '__main__':
    # def push_order(create_order):
    #     data = create_order
    #     print(data)
    with httpx.Client(base_url=BASE_URL) as client:
        print("推单中")
        result1, order_id = mt_push_order_callback(client)
        result2 = mt_cancel_order_callback(client, order_id)
        print("推单输出的结果是:", result1)
        print("取消输出的结果是:", result2)
        # cancel_order(client, order_id)
        result = mt_full_refund_callback(client, order_id)
        print("输出的结果是:", result)
