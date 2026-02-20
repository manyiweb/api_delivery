from typing import Any, Dict, Optional

import httpx

from api.base import safe_post
from conftest import access_token
from utils.file_loader import (
    load_yaml_data,
    get_data_file_path,
)
from utils.logger import logger
# 清空购物车商品接口
CLEARUP_SHOPPINGCART_PRODUCT_API = "/retail-shoppingcart-front/app/shopping/cart/clearUpShopCartProduct"
# 添加购物车商品接口
ADD_ITEM_SHOPPING_CART_API = "/retail-shoppingcart-front/app/shopping/cart/item/addShopCartItem"
# 添加订单接口
ADD_ORDER_CASH_API = "/retail-order-front/app/sales/order/add"
# 现金支付接口
CASH_PAY_API = "/retail-pay-front/app/pay/CashPay"
# 添加服务导购接口
ADD_SERVICE_GUIDE_API = "/retail-shoppingcart-front/app/shopping/cart/updateItemStaff"
# 更新购物车自定义优惠接口
UPDATE_SHOPPINGCART_CUSTOM_DISCOUNT_API = "/retail-shoppingcart-front/app/shopping/cart/updateShopCartCustomDiscount"
# 获取购物车详情接口
GET_SHOPPINGCART_DETAIL_API = "/retail-shoppingcart-front/app/shopping/cart/getShoppingCartDetail"
# 获取系统支付方式接口
GET_SYSTEM_PAY_TYPE_API = "/reabam-retail-pay-front/retail-pay-front/appc/custompay/systemPayType"
# 更新购物车促销计划接口
UPDATE_SHOPPINGCART_PROMOTION_PLAN_API = "/retail-shoppingcart-front/app/shopping/cart/updateShopCartPromotionPlan"
# 获取购物车赠品列表接口
GET_SHOPPINGCART_GIFT_LIST_API = "/retail-shoppingcart-front/app/shopping/cart/shopCartGiftList"
# 选择购物车赠品接口
SELECT_SHOPPINGCART_GIFT_API = "/retail-shoppingcart-front/app/shopping/cart/shopCartGiftSelection"
# 获取会员卡选项接口
GET_CARD_CARD_OPTIONS_API = "/retail/app/Business/Member/CardOptions"
# 选择会员卡充值接口
SELECT_CARD_RECHARGE_API = "/retail/app/Business/Member/CardOptions/GiveItem"
# 获取会员卡充值选项接口
GET_CARD_RECHARGE_OPTIONS_API = "/retail/app/Business/Member/CardRechargeOptions"
# 购物卡充值接口
CARD_TOP_UP_API = "/retail/app/Business/Member/CardTopUp"
# 查询购物卡充值记录接口
QUERY_CARD_TOP_UP_RECORD_API = "/mem/card/amount/records"
# 购物卡退款接口
CARD_REFUND_API = "/retail/app/Business/Member/CardTop/refund"
# 添加会员接口
ADD_MEMBER_API = "/retail-shoppingcart-front/app/shopping/cart/updateShopCartMemberInfo"
# 积分支付接口
INTEGRAL_PAY_API = "/retail-pay-front/app/pay/IntegralPay"
# 购物卡支付接口
MCARD_PAY_API = "/retail-pay-front/app/pay/MCardPay"
# 获取卡包列表接口
GET_CARD_BAG_API = "/reabam-retail-fast/app/Business/member/card_bag"
# 实体卡计算接口
SHOP_CART_ENTITY_CARD_PRE_CALCULATE_API = "/retail-shoppingcart-front/app/shopping/cart/entityCard/shopCartEntityCardPreCalculate"
# 实体卡支付接口
ENTITY_CARD_PAY_API = "/retail-pay-front/app/pay/EntityCard"

# 构建请求参数


def build_request_params(
        data_List_name: str,
        *,
        token_id: Optional[str] = None,
        order_id: Optional[str] = None,
        actual_pay_amount: Optional[float] = None,
) -> Dict[str, Any]:
    read_payload = load_yaml_data(get_data_file_path("order_data.yaml")) or {}
    final_payload = read_payload.get(data_List_name)
    if not isinstance(final_payload, dict):
        raise ValueError(
            f"缺少或无效的配置段: {data_List_name!r}")

    if data_List_name == "cashPay" or data_List_name == "integralPay":
        final_payload["payAmount"] = actual_pay_amount
        final_payload["offlinePayParameter"]["guestPayment"] = actual_pay_amount

    final_payload = final_payload.copy()
    final_payload["tokenId"] = token_id
    if actual_pay_amount is not None:
        final_payload["actualPayAmount"] = actual_pay_amount

    if order_id is not None:
        final_payload["orderId"] = order_id
    return final_payload

# 清空购物车商品接口


def clearup_ShoppingCart_product(client: httpx.Client, token):
    payload = build_request_params("clearShoppingCart", token_id=token)
    logger.info("清空购物车接口请求: %s", payload)
    resp = safe_post(client,
                     CLEARUP_SHOPPINGCART_PRODUCT_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("清空购物车接口响应: %s", resp.json())
    return resp

# 添加购物车商品接口


def add_item_shoppingcart(
        client: httpx.Client,
        token: str,
        *,
        section: Optional[str] = None,
):
    """添加商品到购物车

    Args:
        section: YAML 配置段名称，默认为 addShoppingCartItem
    """
    section = section if section else "addShoppingCartItem"
    payload = build_request_params(section, token_id=token)
    logger.info("添加购物车接口请求: %s", payload)

    resp = safe_post(client,
                     ADD_ITEM_SHOPPING_CART_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("添加购物车接口响应: %s", resp.json())
    return resp


# 新增订单接口
def add_order(client: httpx.Client, token, actual_pay_amount, section: Optional[str] = None):
    payload = build_request_params(
        "addOrder", token_id=token, actual_pay_amount=actual_pay_amount)
    payload["payType"] = section
    logger.info("新增订单接口请求: %s", payload)
    resp = safe_post(client,
                     ADD_ORDER_CASH_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("新增订单接口响应: %s", resp.json())
    order_id = resp.json()["data"]["orderId"]
    return resp, order_id


# 现金支付接口
def cash_pay(client: httpx.Client, token, order_id, actual_pay_amount, order_type="order"):
    payload = build_request_params(
        "cashPay", token_id=token, order_id=order_id, actual_pay_amount=actual_pay_amount)

    # 判断订单类型 card or order
    payload["orderType"] = order_type

    logger.info("现金支付接口请求: %s", payload)
    resp = safe_post(client,
                     CASH_PAY_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("现金支付接口响应: %s", resp.json())
    return resp

# 添加服务导购接口


def add_service_guide(client: httpx.Client, token):
    payload = build_request_params("addServiceGuide", token_id=token)
    logger.info("添加服务导购接口请求: %s", payload)
    resp = safe_post(client,
                     ADD_SERVICE_GUIDE_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("添加服务导购接口响应: %s", resp.json())
    return resp

# 获取购物车详情接口


def get_shoppingcart_detail(client: httpx.Client, token):
    payload = build_request_params("getShoppingCartDetail", token_id=token)
    logger.info("获取购物车详情接口请求: %s", payload)
    resp = safe_post(client,
                     GET_SHOPPINGCART_DETAIL_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("获取购物车详情接口响应: %s", resp.json())
    return resp

# 新增优惠接口


def update_shoppingcart_custom_discount(client: httpx.Client, token, section: Optional[str] = None):
    section = section if section else "updateShoppingcartCustomDiscountForAmount"
    payload = build_request_params(
        data_List_name=section, token_id=token)
    logger.info("新增优惠接口请求: %s", payload)
    resp = safe_post(client,
                     UPDATE_SHOPPINGCART_CUSTOM_DISCOUNT_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("新增优惠接口响应: %s", resp.json())
    return resp

# 获取支付金额接口


def get_system_pay_type(client: httpx.Client, token, section: Optional[str] = None):
    payload = build_request_params("getSystemPayType", token_id=token)
    payload["code"] = section
    logger.info("获取支付金额接口请求: %s", payload)
    resp = safe_post(client,
                     GET_SYSTEM_PAY_TYPE_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("获取支付金额接口响应: %s", resp.json())
    actual_pay_amount = resp.json()["data"]["itemsAmountActuallyPaid"]
    return actual_pay_amount, resp.json()

# 更新购物车优惠计划接口


def update_shoppingcart_promotion_plan(client: httpx.Client, token, section: Optional[str] = None):
    payload = build_request_params(
        section, token_id=token)
    logger.info("更新购物车优惠计划接口请求: %s", payload)
    resp = safe_post(client,
                     UPDATE_SHOPPINGCART_PROMOTION_PLAN_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("更新购物车优惠计划接口响应: %s", resp.json())
    return resp


# 获取赠品列表接口
def get_shoppingcart_gift_list(client: httpx.Client, token):
    """获取赠品列表

    Returns:
        (spec_id, quantity, resp): 赠品规格ID、可选数量、响应对象
    """
    payload = build_request_params("getShoppingcartGiftList", token_id=token)
    logger.info("获取赠品列表接口请求: %s", payload)
    resp = safe_post(client,
                     GET_SHOPPINGCART_GIFT_LIST_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("获取赠品列表接口响应: %s", resp.json())
    # 提取赠品列表第一个赠品的 specId 和 quantity
    data = resp.json().get("data", {})
    # 从 itemsPage.content 中获取第一个赠品的 specId
    content = data.get("itemsPage", {}).get("content", [])
    spec_id = content[0].get("specId", "") if content else ""
    # 从 data 中获取可选赠品数量
    quantity = data.get("quantity", 2)
    return spec_id, quantity, resp


# 选择赠品接口
def select_shoppingcart_gift(client: httpx.Client, token, spec_id: str, quantity: int, section: Optional[str] = None):
    """选择赠品

    Args:
        spec_id: 赠品规格ID（来自赠品列表接口）
        quantity: 可选赠品数量（来自赠品列表接口）
        section: YAML 配置段名称，默认为 selectShoppingcartGift
    """
    section = section if section else "selectShoppingcartGift"
    payload = build_request_params(section, token_id=token)
    # 替换为赠品列表接口返回的实际值
    payload["productList"] = [{
        "specId": spec_id,
        "quantity": quantity,
        "uniqueCodeSet": [],
        "batchList": []
    }]
    logger.info("选择赠品接口请求: %s", payload)
    resp = safe_post(client,
                     SELECT_SHOPPINGCART_GIFT_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("选择赠品接口响应: %s", resp.json())
    return resp

# 获取购物卡充值列表接口


def get_card_card_options(client: httpx.Client, token):
    payload = build_request_params("getCardCardOptions", token_id=token)
    logger.info("获取购物卡充值列表接口请求: %s", payload)
    resp = safe_post(client,
                     GET_CARD_CARD_OPTIONS_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("获取购物卡充值列表接口响应: %s", resp.json())
    data = resp.json().get("DataLine", [{}])[0]
    coId = data.get("coId", "")
    giveItemId = data.get("giveItemId", "")
    saleValue = data.get("saleValue", 0)
    return coId, giveItemId, saleValue

# 选择购物卡充值方案接口


def select_card_recharge_scheme(client: httpx.Client, token, coId):
    payload = build_request_params("GiveItem", token_id=token)
    payload["coId"] = coId
    logger.info("选择购物卡充值接口请求: %s", payload)
    resp = safe_post(client,
                     SELECT_CARD_RECHARGE_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("选择购物卡充值接口响应: %s", resp.json())
    return resp

# 生成卡充值记录接口


def card_top_up(client: httpx.Client, token, coId, giveItemId, saleValue):
    payload = build_request_params("cardTopUp", token_id=token)
    payload["coId"] = coId
    payload["giveItemId"] = giveItemId
    payload["salePrice"] = saleValue
    logger.info("生成卡充值记录接口请求: %s", payload)
    resp = safe_post(client,
                     CARD_TOP_UP_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("生成卡充值记录接口响应: %s", resp.json())
    orderId = resp.json().get("orderId", "")
    payAmount = resp.json().get("payAmount", 0)
    orderType = resp.json().get("orderType", "")
    return resp, orderId, payAmount, orderType

# 查询购物卡充值记录接口


def query_card_top_up_record(client: httpx.Client, token, order_id):
    payload = build_request_params("queryCardTopUpRecord", token_id=token)
    logger.info("查询购物卡充值记录接口请求: %s", payload)
    resp = safe_post(client,
                     QUERY_CARD_TOP_UP_RECORD_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("查询购物卡充值记录接口响应: %s", resp.json())
    # 遍历 pageData.content 查找匹配的充值记录
    content = resp.json().get("data", {}).get("pageData", {}).get("content", [])
    sourceId = ""
    for record in content:
        if record.get("sourceId") == order_id:
            sourceId = record.get("sourceId", "")
            logger.info("找到匹配的充值记录, sourceId: %s, order_id: %s",
                        sourceId, order_id)
            break
    if not sourceId:
        logger.warning("未找到匹配的充值记录, order_id: %s", order_id)
    return sourceId, resp

# 购物卡退款接口


def card_refund(client: httpx.Client, token, souceId, refund_amount):
    payload = build_request_params("cardRefund", token_id=token)
    payload["cardOrderId"] = souceId
    payload["rechargeAmount"] = refund_amount
    payload["refundAmount"] = refund_amount
    logger.info("购物卡退款接口请求: %s", payload)
    resp = safe_post(client,
                     CARD_REFUND_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("购物卡退款接口响应: %s", resp.json())
    return resp

# 添加会员接口


def add_member(client: httpx.Client, token):
    payload = build_request_params("addMember", token_id=token)
    logger.info("添加会员接口请求: %s", payload)
    resp = safe_post(client,
                     ADD_MEMBER_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("添加会员接口响应: %s", resp.json())
    return resp

# 积分支付接口


def integral_pay(client: httpx.Client, token, order_id, actual_pay_amount):
    payload = build_request_params(
        "integralPay", token_id=token, actual_pay_amount=actual_pay_amount)
    payload["orderId"] = order_id
    logger.info("积分支付接口请求: %s", payload)
    resp = safe_post(client,
                     INTEGRAL_PAY_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("积分支付接口响应: %s", resp.json())
    return resp

# 购物卡支付接口


def Mcard_pay(client: httpx.Client, token, order_id, actual_pay_amount):
    payload = build_request_params(
        "McardPay", token_id=token, actual_pay_amount=actual_pay_amount)
    payload["orderId"] = order_id
    logger.info("购物卡支付接口请求: %s", payload)
    resp = safe_post(client,
                     MCARD_PAY_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("购物卡支付接口响应: %s", resp.json())
    return resp


# 获取卡包列表接口
def get_card_bag(client: httpx.Client, token, actual_pay_amount):
    payload = build_request_params("getCardBag", token_id=token)
    logger.info("获取卡包列表接口请求: %s", payload)
    resp = safe_post(client,
                     GET_CARD_BAG_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("获取卡包列表接口响应: %s", resp.json())
    # 遍历卡包列表，查找 balance >= actual_pay_amount 的实体卡
    data_line = resp.json().get("DataLine", [])
    card_no = ""
    for card in data_line:
        balance = float(card.get("balance", 0))
        if balance >= actual_pay_amount:
            card_no = card.get("cardNo", "")
            logger.info("找到可用实体卡, cardNo: %s, balance: %s", card_no, balance)
            break
    if not card_no:
        raise ValueError("无可抵扣完金额的实体卡")
    return card_no, resp


# 实体卡计算接口
def shop_cart_entity_card_pre_calculate(client: httpx.Client, token, card_no):
    payload = build_request_params(
        "shopCartEntityCardPreCalculate", token_id=token)
    payload["entityCardNo"] = card_no
    logger.info("实体卡计算接口请求: %s", payload)
    resp = safe_post(client,
                     SHOP_CART_ENTITY_CARD_PRE_CALCULATE_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("实体卡计算接口响应: %s", resp.json())
    # 提取 payAmount
    pay_amount = resp.json().get("data", {}).get("payAmount", 0)
    return pay_amount, resp


# 实体卡支付接口
def entity_card_pay(client: httpx.Client, token, order_id, pay_amount, card_no):
    payload = build_request_params("entityCardPay", token_id=token)
    payload["orderId"] = order_id
    payload["payAmount"] = pay_amount
    payload["offlinePayParameter"]["guestPayment"] = pay_amount
    payload["offlinePayParameter"]["cardNo"] = card_no
    logger.info("实体卡支付接口请求: %s", payload)
    resp = safe_post(client,
                     ENTITY_CARD_PAY_API,
                     headers={"Authorization": f"Bearer {token}"},
                     json=payload)
    logger.info("实体卡支付接口响应: %s", resp.json())
    return resp
