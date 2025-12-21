import httpx
import pytest
import allure
import json

from api.base import BASE_URL, safe_post
from api.payload_builder import build_final_payload, build_cancel_payload, build_apply_refund_payload
from utils import load_yaml_data, get_data_file_path


def mt_push_order_callback(client):
    with allure.step("读取推单数据"):
        raw_data = load_yaml_data(get_data_file_path('delivery_data.yaml'))

    with allure.step("构建推单参数"):
        final_push_order_payload, order_id = build_final_payload(raw_data)
        allure.attach(str(order_id), name="生成的订单ID", attachment_type=allure.attachment_type.TEXT)
        print(final_push_order_payload)

    with allure.step("请求美团推单接口"):
        responses = safe_post(client, 'dock/mt/v2/order/callback', data=final_push_order_payload)
        response_data = responses.json()
        allure.attach(json.dumps(response_data, ensure_ascii=False, indent=2),
                      name="推单响应", attachment_type=allure.attachment_type.JSON)
        return response_data.get('data'), order_id


def mt_cancel_order_callback(client, order_id):
    with allure.step("读取取消订单数据"):
        print("取消订单中", order_id)
        raw_data = load_yaml_data(get_data_file_path('cancel_order.yaml'))
        print('raw_data2', raw_data)

    with allure.step("构建取消订单参数"):
        final_cancel_order_payload = build_cancel_payload(raw_data, order_id)
        allure.attach(str(order_id), name="取消的订单ID", attachment_type=allure.attachment_type.TEXT)
        print('cancel_payload', final_cancel_order_payload)

    with allure.step("请求取消订单接口"):
        responses = safe_post(client, '/dock/mt/v2/order/cancel/callback', data=final_cancel_order_payload)
        response_data = responses.json()
        allure.attach(json.dumps(response_data, ensure_ascii=False, indent=2),
                      name="取消订单响应", attachment_type=allure.attachment_type.JSON)
        return response_data.get('data')


# 整单退款
def mt_full_refund_callback(client):
    with allure.step("读取申请订单整单退数据"):
        raw_data = load_yaml_data(get_data_file_path('refund_order.yaml'))

    with allure.step("构建申请订单整单退参数"):
        final_full_order_payload = build_apply_refund_payload(raw_data)
        print('最终请求接口数据为', final_full_order_payload)

    with allure.step("请求申请订单整单退接口"):
        responses = safe_post(client, '/reabam-external-access/mt/v2/order/refund/callback',
                              data=final_full_order_payload)
        response_data = responses.json()
        allure.attach(json.dumps(response_data, ensure_ascii=False, indent=2),
                      name="申请订单整单退响应", attachment_type=allure.attachment_type.JSON)
        return response_data.get('data')


# 部分退款
def partial_refund(client):
    partialRefund = client.post('/mt/v2/order/partial/refund/callback', json={

    })


if __name__ == '__main__':
    # def push_order(create_order):
    #     data = create_order
    #     print(data)
    with httpx.Client(base_url=BASE_URL) as client:
        print("推单中")
        result1 = mt_push_order_callback(client)
        result2 = mt_cancel_order_callback(client)
        print("推单输出的结果是:", result1)
        print("取消输出的结果是:", result2)
        # cancel_order(client, order_id)
        result = mt_full_refund_callback(client)
        print("输出的结果是:", result)
