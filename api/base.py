import pytest
import httpx
import json

BASE_URL = 'http://fat-pos.reabam.com:60030/api/dock'


@pytest.fixture
def client():
    return httpx.Client(base_url=BASE_URL)


# 美团推单
# @pytest.mark.paramret()
# @pytest.fixture
def create_order(client):
    order_dict = {
        "avgSendTime": 1802.0,
        "backupRecipientPhone": "[\"17896091441_7679\",\"13009618046_6213\",\"13059921880_3255\"]",
        "caution": "[预订人]18449039731_7333 收餐人隐私号 18449039731_7333，手机号 199****8582 环保单，顾客不需要附带餐具",
        "cityId": 653200,
        "ctime": 1764745851,
        "daySeq": "1",
        "deliveryAvailable": 0,
        "deliveryTime": 0,
        "detail": [
            {
                "actual_price": 0.01,
                "app_food_code": "20981718554",
                "box_num": 1.0,
                "box_price": 0.01,
                "cart_id": 0,
                "detail_extra": {},
                "detail_id": 7767751894993,
                "food_discount": 1.0,
                "food_name": "芒果蛋糕",
                "food_property": "",
                "isSharpShooter": False,
                "mt_sku_id": 43032019621,
                "mt_spu_id": 27730486360,
                "mt_tag_id": 12128293648,
                "original_price": 0.01,
                "premiumAttrs": "",
                "price": 0.01,
                "quantity": 1,
                "single_increase_amount": 0.0,
                "sku_id": "a79c4d7c902c486ca2d1b228b48e339d",
                "spec": "500克",
                "sub_detail_list": [],
                "unit": "500克",
                "weight": 500
            }
        ],
        "dinnersNumber": 99,
        "ePoiId": "reabamts_5ad586a8721e49518998aedef9fd3b5c",
        "extras": [
            {
                "mt_charge": 0.0,
                "poi_charge": 3.88,
                "reduce_fee": 3.88,
                "remark": "减配送费3.88元",
                "type": 25
            }
        ],
        "favorites": False,
        "hasInvoiced": 0,
        "incmpCode": 0,
        "incmpModules": "[]",
        "invMakeType": 4,
        "invoiceTitle": "",
        "isFavorites": False,
        "isPoiFirstOrder": False,
        "isThirdShipping": 0,
        "latitude": 36.266318,
        "logisticsCode": "2002",
        "longitude": 81.744618,
        "lowincomeOrder": 1,
        "oneOneUrgentDelivery": 0,
        "oneOneUrgentDeliveryTag": 0,
        "orderEntranceType": 0,
        "orderId": 5301890193521352377,
        "orderIdView": 5301890193521352377,
        "orderTagList": "[]",
        "originalPrice": 3.9,
        "payType": 2,
        "phfSsf": 0.0,
        "poiAddress": "新疆维吾尔自治区和田地区于田县阿羌乡喀什塔什村",
        "poiFirstOrder": False,
        "poiId": 27280112,
        "poiName": "压测测试门店_合作中心测试勿动01_062",
        "poiPhone": "025-59260000",
        "poiReceiveDetail": {"onlinePayment": 2},
        "recipientAddress": "xxxxxxx",
        "recipientAddressDesensitization": "xxxx",
        "recipientName": "钵先生",
        "recipientPhone": "18449039731_7333",
        "shipperPhone": "",
        "shippingFee": 3.88,
        "sqtNeedInvoice": 0,
        "sqtOrder": 2,
        "status": 2,
        "taxpayerId": "",
        "total": 0.02,
        "utime": 1764745851,
        "wmPoiReceiveCent": 0
    }
    payload = {
        "developerId": "106825",
        "ePoiId": "reabamts_5ad586a8721e49518998aedef9fd3b5c",
        "order": json.dumps(order_dict, ensure_ascii=False),
        "sign": "146bcdd348c4f7e90895af13faa123e201fe2686"
    }
    create_resp = client.post(
        "/mt/v2/order/callback",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert create_resp.json()['data'] == "OK"
    print("调通了！！")
    return create_resp.json().get('data')


# 部分退款
@pytest.fixture
def partial_refund(client):
    partialRefund = client.post('/mt/v2/order/partial/refund/callback', json={

    })


# 整单退款
@pytest.fixture
def drict_refund(client):
    drictRefund = client.post('/mt/v2/order/refund/callback', json={

    })


# 取消订单
@pytest.fixture
def cancel_order(client):
    cnacelOrder = client.post('/mt/v2/order/cancel/callback', josn={

    })


if __name__ == '__main__':
    # def push_order(create_order):
    #     data = create_order
    #     print(data)
    # 1. 手动实例化 Client
    with httpx.Client(base_url=BASE_URL) as client:
        # 2. 调用逻辑函数
        result = create_order(client)
        print("最终结果:", result)
