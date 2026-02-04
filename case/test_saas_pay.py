from api.create_order_cash import add_item_shoppingcart, add_order_cash, cash_pay


class TestSaaSPay:
    def test_cash_pay(self, client, access_token):
        token = access_token
        # 新增购物车商品
        add_item_shoppingcart(client, token)
        # 新增现金支付订单
        resp, order_id = add_order_cash(client, token)
        # 现金支付
        cash_pay(client, token, order_id)
