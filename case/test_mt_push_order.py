import allure
from api.order_api import create_order, cancel_order


@allure.epic("美团外卖接口")
@allure.feature("订单管理")
class TestMtPushOrder:
    """美团推单成功"""

    @allure.story("推单接口")
    @allure.title("测试美团推单接口")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_push_order(self, client):
        with allure.step("执行推单操作"):
            print("推单中")
            result = create_order(client)
            print("输出的结果是:", result)
        with allure.step("验证推单结果"):
            allure.attach(str(result), name="推单响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"推单失败，返回结果: {result}"

    @allure.story("取消订单接口")
    @allure.title("测试美团取消订单接口")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cancel_order(self, client):
        with allure.step("执行取消订单操作"):
            print("取消订单中")
            result = cancel_order(client)
        with allure.step("验证取消订单结果"):
            allure.attach(str(result), name="取消订单响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"取消订单失败，返回结果: {result}"
            print("取消订单成功")
