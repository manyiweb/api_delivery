import httpx
import pytest
import allure
import json

from api.base import BASE_URL, safe_post
from utils import load_yaml_data, build_final_payload, get_data_file_path, build_cancel_payload


GLOBAL_ORDER_ID = None


def create_order(client):
    global GLOBAL_ORDER_ID
    with allure.step("读取推单数据"):
        raw_data = load_yaml_data(get_data_file_path('delivery_data.yaml'))
    
    with allure.step("构建推单参数"):
        final_payload, order_id = build_final_payload(raw_data)
        GLOBAL_ORDER_ID = order_id
        allure.attach(str(order_id), name="生成的订单ID", attachment_type=allure.attachment_type.TEXT)
        print(final_payload)
    
    with allure.step("请求美团推单接口"):
        responses = safe_post(client, '/mt/v2/order/callback', data=final_payload)
        response_data = responses.json()
        allure.attach(json.dumps(response_data, ensure_ascii=False, indent=2), 
                      name="推单响应", attachment_type=allure.attachment_type.JSON)
        return response_data.get('data')


def cancel_order(client):
    with allure.step("读取取消订单数据"):
        print("取消订单中", GLOBAL_ORDER_ID)
        raw_data = load_yaml_data(get_data_file_path('cancel_order.yaml'))
        print('raw_data2', raw_data)
    
    with allure.step("构建取消订单参数"):
        cancel_payload = build_cancel_payload(raw_data, GLOBAL_ORDER_ID)
        allure.attach(str(GLOBAL_ORDER_ID), name="取消的订单ID", attachment_type=allure.attachment_type.TEXT)
        print('cancel_payload', cancel_payload)
    
    with allure.step("请求取消订单接口"):
        responses = safe_post(client, '/mt/v2/order/cancel/callback', data=cancel_payload)
        response_data = responses.json()
        allure.attach(json.dumps(response_data, ensure_ascii=False, indent=2), 
                      name="取消订单响应", attachment_type=allure.attachment_type.JSON)
        return response_data.get('data')


# 部分退款
def partial_refund(client):
    partialRefund = client.post('/mt/v2/order/partial/refund/callback', json={

    })


# 整单退款
@pytest.fixture
def drict_refund(client):
    drictRefund = client.post('/mt/v2/order/refund/callback', json={

    })


if __name__ == '__main__':
    # def push_order(create_order):
    #     data = create_order
    #     print(data)
    with httpx.Client(base_url=BASE_URL) as client:
        print("推单中")
        result1 = create_order(client)
        result2 = cancel_order(client)
        print("推单输出的结果是:", result1)
        print("取消输出的结果是:", result2)
    # cancel_order(client, order_id)