from typing import Any, Dict, Optional

import httpx

from api.base import safe_post
from conftest import access_token
from utils.file_loader import load_yaml_data, get_data_file_path

ADD_ITEM_SHOPPING_CART = "/retail-shoppingcart-front/app/shopping/cart/item/addShopCartItem"
ADD_ORDER_CASH = "/retail-order-front/app/sales/order/add"
CASH_PAY = "/retail-pay-front/app/pay/CashPay"


# 构建请求参数
def build_request_params(
        data_List_name: str,
        *,
        token_id: Optional[str] = None,
        order_id: Optional[str] = None,
) -> Dict[str, Any]:
    read_payload = load_yaml_data(get_data_file_path("order_data.yaml")) or {}
    final_payload = read_payload.get(data_List_name)
    if not isinstance(final_payload, dict):
        raise ValueError(f"Missing/invalid payload section: {data_List_name!r}")

    final_payload = final_payload.copy()
    final_payload["tokenId"] = token_id or access_token()
    if order_id is not None:
        final_payload["orderId"] = order_id
    return final_payload


# 添加购物车商品
def add_item_shopppingcart(client: httpx.Client, token):
    payload = build_request_params("createOrder", token_id=token)
    resp = safe_post(client,
                     ADD_ITEM_SHOPPING_CART,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)

    return resp


# 新增订单
def add_order_cash(client: httpx.Client, token):
    payload = build_request_params("addOrder", token_id=token)
    resp = safe_post(client,
                     ADD_ORDER_CASH,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    order_id = resp.json().get("data").get("orderId")
    return resp, order_id


# 现金支付
def cash_pay(client: httpx.Client, token, order_id):
    payload = build_request_params("cashPay", token_id=token, order_id=order_id)
    resp = safe_post(client,
                     CASH_PAY,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)

    return resp



