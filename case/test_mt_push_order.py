from api.order_api import create_order


class TestMtPushOrder:
    """美团推单接口测试"""
    def test_push_order(self, client):
        print("推单中")
        result = create_order(client)
        print("输出的结果是:", result)
        assert result == "OK", f"推单失败，返回结果: {result}"
