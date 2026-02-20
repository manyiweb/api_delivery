from api.create_order_cash import (
    add_item_shoppingcart,
    add_order,
    add_service_guide,
    cash_pay,
    get_shoppingcart_gift_list,
    get_system_pay_type,
    select_shoppingcart_gift,
    update_shoppingcart_custom_discount,
    update_shoppingcart_promotion_plan,
    clearup_ShoppingCart_product,
    get_card_card_options,
    select_card_recharge_scheme,
    card_top_up,
    query_card_top_up_record,
    card_refund,
    integral_pay,
    add_member,
    Mcard_pay,
    get_card_bag,
    shop_cart_entity_card_pre_calculate,
    entity_card_pay,
)

import allure
import pytest


@pytest.fixture(scope="function")
def empty_shopping_cart(client, access_token):
    """测试前清空购物车"""
    clearup_ShoppingCart_product(client, access_token)


@allure.story("支付业务")
@allure.severity(allure.severity_level.CRITICAL)
class TestSaaSPay:
    @allure.story("现金购买支付")
    def test_cash_pay(self, client, access_token):
        token = access_token
        # 添加服务导购
        add_service_guide(client, token)
        # 新增购物车商品
        add_item_shoppingcart(client, token)
        # 获取支付金额
        actual_pay_amount = get_system_pay_type(client, token)[0]
        # 新增现金支付订单
        resp, order_id = add_order(
            client, token, actual_pay_amount, section="cashPay")
        # 现金支付
        resp = cash_pay(client, token, order_id, actual_pay_amount)
        assert resp.json().get("code") == "200", "现金支付失败：返回码不为200"

    @allure.story("订单优惠金额")
    def test_order_discount_amount(self, client, access_token):
        token = access_token
        # 添加服务导购
        add_service_guide(client, token)
        # 添加times1商品到购物车
        add_item_shoppingcart(
            client, token, section="addShoppingCartItemForDiscount")
        # 新增整单优惠-金额
        update_shoppingcart_custom_discount(client, token)
        # 获取支付金额
        actual_pay_amount = get_system_pay_type(client, token)[0]
        # 新增现金支付订单
        resp, order_id = add_order(
            client, token, actual_pay_amount, section="cashPay")
        # 现金支付
        resp = cash_pay(client, token, order_id, actual_pay_amount)
        assert resp.json().get("code") == "200", "订单优惠金额支付失败：返回码不为200"

    @allure.story("订单优惠折扣")
    def test_order_discount_rate(self, client, access_token):
        token = access_token
        # 添加服务导购
        add_service_guide(client, token)
        # 添加times1商品到购物车
        add_item_shoppingcart(
            client, token, section="addShoppingCartItemForDiscount")
        # 新增整单优惠-折扣
        update_shoppingcart_custom_discount(
            client, token, section="updateShoppingcartCustomDiscountForRate")
        # 获取支付金额
        actual_pay_amount = get_system_pay_type(client, token)[0]
        # 新增现金支付订单
        resp, order_id = add_order(
            client, token, actual_pay_amount, section="cashPay")
        # 现金支付
        resp = cash_pay(client, token, order_id, actual_pay_amount)
        assert resp.json().get("code") == "200", "订单优惠折扣支付失败：返回码不为200"

    @allure.story("订单优惠-满折")
    def test_order_discount_full_discount(self, client, access_token):
        token = access_token
        # 添加服务导购
        add_service_guide(client, token)
        # 添加times1商品到购物车
        add_item_shoppingcart(
            client, token, section="addShoppingCartItemForDiscount")
        # 新增整单优惠-满减
        update_shoppingcart_promotion_plan(
            client, token, section="updateShopCartPromotionPlanForFullDiscount")
        # 获取支付金额
        actual_pay_amount = get_system_pay_type(client, token)[0]
        # 新增现金支付订单
        resp, order_id = add_order(
            client, token, actual_pay_amount, section="cashPay")
        # 现金支付
        resp = cash_pay(client, token, order_id, actual_pay_amount)
        assert resp.json().get("code") == "200", "订单优惠满折支付失败：返回码不为200"

    @allure.story("订单优惠-满增")
    def test_order_discount_full_send(self, client, access_token):
        token = access_token
        # 添加服务导购
        add_service_guide(client, token)
        # 添加times1商品到购物车
        add_item_shoppingcart(
            client, token, section="addShoppingCartItemForDiscount")
        # 新增整单优惠-满增
        update_shoppingcart_promotion_plan(
            client, token, section="updateShopCartPromotionPlanForFullSend")
        # 获取赠品列表
        spec_id, quantity, _ = get_shoppingcart_gift_list(client, token)
        # 选择赠品
        select_shoppingcart_gift(client, token, spec_id, quantity)
        # 获取支付金额
        actual_pay_amount = get_system_pay_type(client, token)[0]
        # 新增现金支付订单
        resp, order_id = add_order(
            client, token, actual_pay_amount, section="cashPay")
        # 现金支付
        resp = cash_pay(client, token, order_id, actual_pay_amount)
        assert resp.json().get("code") == "200", "订单优惠满增支付失败：返回码不为200"

    @allure.story("订单优惠-满减")
    def test_order_discount_full_reduction(self, client, access_token, empty_shopping_cart):
        token = access_token
        # 添加服务导购
        add_service_guide(client, token)
        # 添加times1商品到购物车
        add_item_shoppingcart(
            client, token, section="addShoppingCartItemForDiscount")
        # 新增整单优惠-满减
        update_shoppingcart_promotion_plan(
            client, token, section="updateShopCartPromotionPlanForFullReduction")
        # 获取支付金额
        actual_pay_amount = get_system_pay_type(client, token)[0]
        # 新增现金支付订单
        resp, order_id = add_order(
            client, token, actual_pay_amount, section="cashPay")
        # 现金支付
        resp = cash_pay(client, token, order_id, actual_pay_amount)
        assert resp.json().get("code") == "200", "订单优惠满减支付失败：返回码不为200"

    @allure.story("购物卡充值")
    def test_card_recharge(self, client, access_token):
        token = access_token
        # 获取购物卡充值列表
        coId, giveItemId, saleValue = get_card_card_options(client, token)
        # 选择购物卡充值方案
        select_card_recharge_scheme(client, token, coId)
        # 生成卡充值记录
        resp, order_id, actual_pay_amount, order_type = card_top_up(
            client, token, coId, giveItemId, saleValue)
        # 新增购物卡充值订单支付记录
        resp = cash_pay(client, token, order_id, actual_pay_amount, order_type)
        assert resp.json().get("code") == "200", "购物卡充值支付失败：返回码不为200"

    @allure.story("购物卡充值后退款")
    def test_card_refund(self, client, access_token):
        token = access_token
        # 获取购物卡充值列表
        coId, giveItemId, saleValue = get_card_card_options(client, token)
        # 选择购物卡充值方案
        select_card_recharge_scheme(client, token, coId)
        # 生成卡充值记录
        resp, order_id, actual_pay_amount, order_type = card_top_up(
            client, token, coId, giveItemId, saleValue)
        # 新增购物卡充值订单支付记录
        cash_pay(client, token, order_id, actual_pay_amount, order_type)
        # 查询购物卡充值记录
        sourceId, _ = query_card_top_up_record(client, token, order_id)
        # 购物卡退款
        resp = card_refund(client, token, sourceId, actual_pay_amount)
        assert resp.json().get("code") == "200", "购物卡退款失败：返回码不为200"

    @allure.story("会员积分支付")
    def test_member_integral_pay(self, client, access_token):
        token = access_token
        # 添加服务导购
        add_service_guide(client, token)
        # 添加会员
        add_member(client, token)
        # 添加times1商品到购物车
        add_item_shoppingcart(
            client, token, section="addShoppingCartItemForDiscount")
        # 获取支付金额
        actual_pay_amount = get_system_pay_type(
            client, token, section="IntegralPay")[0]
        # 新增积分支付订单
        resp, order_id = add_order(
            client, token, actual_pay_amount, section="IntegralPay")
        # 积分支付
        resp = integral_pay(client, token, order_id, actual_pay_amount)
        assert resp.json().get("code") == "200", "会员积分支付失败：返回码不为200"

    @allure.story("购物卡支付")
    def test_card_pay(self, client, access_token):
        token = access_token
        # 添加服务导购
        add_service_guide(client, token)
        # 添加会员
        add_member(client, token)
        # 添加times1商品到购物车
        add_item_shoppingcart(
            client, token, section="addShoppingCartItemForDiscount")
        # 获取支付金额
        actual_pay_amount = get_system_pay_type(
            client, token, section="MCardPay")[0]
        # 新增购物卡支付订单
        resp, order_id = add_order(
            client, token, actual_pay_amount, section="MCardPay")
        # 购物卡支付
        resp = Mcard_pay(client, token, order_id, actual_pay_amount)
        assert resp.json().get("code") == "200", "购物卡支付失败：返回码不为200"

    @allure.story("实体卡支付")
    def test_entity_card_pay(self, client, access_token):
        token = access_token
        # 添加服务导购
        add_service_guide(client, token)
        # 添加会员
        add_member(client, token)
        # 添加times1商品到购物车
        add_item_shoppingcart(
            client, token, section="addShoppingCartItemForDiscount")
        # 获取支付金额
        actual_pay_amount = get_system_pay_type(
            client, token, section="EntityCard")[0]
        # 获取卡包列表，遍历找到可用实体卡
        card_no, _ = get_card_bag(client, token, actual_pay_amount)
        # 实体卡计算接口，获取实际支付金额
        pay_amount, _ = shop_cart_entity_card_pre_calculate(
            client, token, card_no)
        # 新增实体卡支付订单
        resp, order_id = add_order(
            client, token, pay_amount, section="EntityCard")
        # 实体卡支付
        resp = entity_card_pay(client, token, order_id, pay_amount, card_no)
        assert resp.json().get("code") == "200", "实体卡支付失败：返回码不为200"
