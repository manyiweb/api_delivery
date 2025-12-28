import allure
from api.order_callback import mt_push_order_callback, mt_cancel_order_callback, mt_full_refund_callback
from assertions.order_db_assert import assert_order_created
from utils.logger import logger
# 添加time模块用于延迟
import time


@allure.epic("美团外卖接口")
@allure.feature("订单管理")
class TestMtPushOrder:
    """美团推单成功"""

    @allure.story("外卖下单")
    @allure.title("美团推单回调成功后，系统生成订单并入库")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_push_order(self, client,):
        with allure.step("执行推单操作"):
            logger.info("推单中")
            result, order_id = mt_push_order_callback(client)
            logger.info(f"推单结果: {result}")

        # # 记录生成的订单ID，用于后续清理
        # cleanup_order.append(order_id)

        with allure.step("验证推单结果"):
            allure.attach(str(result), name="推单响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"推单失败，返回结果: {result}"

        # 添加适当延迟，确保消息被完全消费并落库
        with allure.step("等待订单数据落库"):
            logger.info("等待订单数据落库...")
            time.sleep(3)  # 等待3秒以确保数据持久化

        # with allure.step("验证订单是否已存入数据库"):
        #     # 断言订单是否已存入数据库dorder表中order_id字段
        #     assert_order_created(db_conn, str(order_id))
        #     logger.info(f"数据库验证通过：订单ID {order_id} 已成功存入数据库")

    @allure.story("订单取消")
    @allure.title("美团取消订单回调后，订单状态更新为已取消")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_cancel_order(self, client):
        # 生成订单
        with allure.step("执行推单操作"):
            logger.info("取消订单数据生成中")
            # 添加小延迟确保订单生成
            time.sleep(2)
            result, order_id = mt_push_order_callback(client)
            logger.info(f"推单结果: {result}")
        with allure.step("执行取消订单操作"):
            logger.info("取消订单中")
            result = mt_cancel_order_callback(client, order_id)
        with allure.step("验证取消订单结果"):
            allure.attach(str(result), name="取消订单响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"取消订单失败，返回结果: {result}"
            logger.info("取消订单成功")

    @allure.story("订单整单退款")
    @allure.title("美团整单退款申请并同意后，订单状态变更为已退款")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_full_refund(self, client):
        # 生成整单退订单数据
        with allure.step("执行生成订单操作"):
            logger.info("生成整单退订单数据中")
            # 添加小延迟确保订单生成
            time.sleep(2)
            result, order_id = mt_push_order_callback(client)
        # 美团申请整单退
        with allure.step("执行整单退款操作"):
            logger.info("整单退款中")
            result = mt_full_refund_callback(client, order_id)
        with allure.step("验证整单退款结果"):
            allure.attach(str(result), name="整单退款响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"整单退款失败，返回结果: {result}"
            logger.info("整单退款成功")
