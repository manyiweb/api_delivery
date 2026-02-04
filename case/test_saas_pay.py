from api.create_order_cash import add_item_shoppingcart, add_order_cash, cash_pay, add_service_guide

import allure


@allure.story("现金支付测试")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("现金支付")
class TestSaaSPay:
    def test_cash_pay(self, client, access_token):
        token = access_token
        # 添加服务导购
        add_service_guide(client, token)
        # 新增购物车商品weqw
        add_result = add_item_shoppingcart(client, token)
        # 新增现金支付订单
        resp, order_id = add_order_cash(client, token)
        # 现金支付
        cash_pay(client, token, order_id)
