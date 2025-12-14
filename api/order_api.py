import os
import pytest
import httpx
import json

from api.base import BASE_URL, safe_post
from utils import load_yaml_data, build_final_payload, get_data_file_path


# 美团推单接口
# @pytest.mark.paramret()
def create_order(client):
    # 读取订单数据
    raw_data = load_yaml_data(get_data_file_path('delivery_data.yaml'))
    # 构建订单参数
    final_payload, order_id = build_final_payload(raw_data)
    print(final_payload)

    # 请求美团推单接口
    responses = safe_post(client, '/mt/v2/order/callback', data=final_payload)
    return responses.json().get('data')

# 部分退款

def partial_refund(client):
    partialRefund = client.post('/mt/v2/order/partial/refund/callback', json={

    })


# 整单退款
@pytest.fixture
def drict_refund(client):
    drictRefund = client.post('/mt/v2/order/refund/callback', json={

    })


# 取消订单
def cancel_order(client):
    raw_data = load_yaml_data(get_data_file_path('cancel_order.yaml'))




if __name__ == '__main__':
    # def push_order(create_order):
    #     data = create_order
    #     print(data)
    with httpx.Client(base_url=BASE_URL) as client:
        print("推单中")
        result = create_order(client)
        print("输出的结果是:", result)
