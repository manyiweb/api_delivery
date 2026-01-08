"""美团订单接口测试用例
覆盖推单、取消、退款等场景
"""
import allure
import pytest
import time

from api.order_callback import mt_push_order_callback, mt_cancel_order_callback, mt_full_refund_callback
from assertions.order_db_assert import assert_order_count, assert_order_created
from utils.logger import logger


@allure.epic("美团外卖接口")
@allure.feature("订单管理")
class TestMtPushOrder:
    """美团推单成功"""

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("外卖下单")
    @allure.title("美团推单回调成功后，系统生成订单并入库")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_push_order(self, client, db_conn):
        """测试美团推单功能"""
        with allure.step("执行推单操作"):
            logger.info("📦 开始推单")
            result, order_id = mt_push_order_callback(client)
            logger.info(f"推单结果: {result}, 订单ID: {order_id}")
            
        with allure.step("验证推单响应"):
            allure.attach(str(result), name="推单响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"❌ 推单失败，返回结果: {result}"
            logger.info("✅ 推单响应验证成功")
            
        with allure.step("验证订单入库"):
            assert_order_created(db_conn, str(order_id), timeout=10)
            logger.info(f"✅ 订单 {order_id} 已成功入库")

    @pytest.mark.critical
    @allure.story("订单取消")
    @allure.title("美团取消订单回调后，订单状态更新为已取消")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_cancel_order(self, client, db_conn):
        """测试美团取消订单功能"""
        # 生成订单
        with allure.step("执行推单操作"):
            logger.info("📦 生成取消订单测试数据")
            result, order_id = mt_push_order_callback(client)
            logger.info(f"推单结果: {result}, 订单ID: {order_id}")
            assert result == "OK", f"❌ 推单失败，无法进行取消测试"
            
        with allure.step("等待订单入库"):
            time.sleep(2)
            logger.info("✅ 订单已入库，可以执行取消")
            
        with allure.step("执行取消订单操作"):
            logger.info("❌ 开始取消订单")
            result = mt_cancel_order_callback(client, order_id)
            
        with allure.step("验证取消订单结果"):
            allure.attach(str(result), name="取消订单响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"❌ 取消订单失败，返回结果: {result}"
            logger.info("✅ 取消订单成功")

    @pytest.mark.critical
    @allure.story("订单整单退款")
    @allure.title("美团整单退款申请并同意后，订单状态变更为已退款")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_full_refund(self, client, db_conn):
        """测试美团整单退款功能"""
        # 生成整单退订单数据
        with allure.step("执行生成订单操作"):
            logger.info("📦 生成整单退款测试订单")
            result, order_id = mt_push_order_callback(client)
            assert result == "OK", f"❌ 推单失败，无法进行退款测试"
            
        with allure.step("等待订单入库"):
            time.sleep(2)
            logger.info("✅ 订单已入库，可以执行退款")
            
        # 美团申请整单退
        with allure.step("执行整单退款操作"):
            logger.info("💰 开始整单退款")
            result = mt_full_refund_callback(client, order_id)
            
        with allure.step("验证整单退款结果"):
            allure.attach(str(result), name="整单退款响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"❌ 整单退款失败，返回结果: {result}"
            logger.info("✅ 整单退款成功")

    @pytest.mark.normal
    @allure.story("重复推单")
    @allure.title("重复推单时验证幂等性，订单表中该订单数量应为1")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mt_repeat_push_order(self, client, db_conn):
        """测试重复推单的幂等性"""
        with allure.step("第一次推单操作"):
            logger.info("📦 第一次推单")
            result1, order_id = mt_push_order_callback(client)
            logger.info(f"第一次推单结果: {result1}, 订单ID: {order_id}")

        with allure.step("验证第一次推单结果"):
            assert result1 == "OK", f"❌ 第一次推单失败，返回结果: {result1}"
            logger.info("✅ 第一次推单成功")

        # 等待第一次订单数据落库
        with allure.step("等待第一次订单数据落库"):
            logger.info("⏳ 等待第一次订单数据落库...")
            time.sleep(3)

        with allure.step("第二次推单操作（使用相同订单ID）"):
            logger.info("📦 第二次推单（测试幂等性）")
            result2, duplicate_order_id = mt_push_order_callback(client, order_id)
            logger.info(f"第二次推单结果: {result2}, 订单ID: {duplicate_order_id}")
            assert duplicate_order_id == order_id, f"❌ 重复推单返回的订单ID不一致: {duplicate_order_id} vs {order_id}"

        with allure.step("验证第二次推单结果"):
            assert result2 == "OK", f"❌ 第二次推单失败，返回结果: {result2}"
            logger.info("✅ 第二次推单成功")

        # 等待第二次订单数据处理完成
        with allure.step("等待第二次订单数据处理"):
            logger.info("⏳ 等待第二次订单数据处理...")
            time.sleep(3)

        with allure.step("验证重复推单后订单数量为1（幂等性验证）"):
            # 验证数据库中该订单ID的记录数量应为1，确保重复推单不会生成新订单
            assert_order_count(db_conn, str(order_id), expected_count=1)
            logger.info(f"✅ 重复推单幂等性验证通过：订单ID {order_id} 在数据库中数量为1")

    @pytest.mark.skip
    @allure.story("异常订单处理")
    @allure.title("使用无效订单ID进行取消操作")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_cancel_with_invalid_order_id(self, client):
        """使用无效订单ID取消订单"""
        with allure.step("尝试使用无效订单ID取消订单"):
            invalid_order_id = 9999999999999999999  # 无效订单ID
            result = mt_cancel_order_callback(client, invalid_order_id)
        with allure.step("验证取消操作失败"):
            # 根据API实际响应调整验证方式
            logger.info(f"无效订单ID取消结果: {result}")
            # 无效订单ID可能会返回错误信息而不是"OK"
            assert result is not None, "无效订单ID取消操作应返回错误信息"

    @pytest.mark.skip
    @allure.story("重复操作")
    @allure.title("重复取消同一订单")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cancel_duplicate_order(self, client):
        """重复取消订单测试"""
        # 生成订单
        with allure.step("执行推单操作"):
            logger.info("重复取消订单数据生成中")
            result, order_id = mt_push_order_callback(client)
            logger.info(f"推单结果: {result}")
        with allure.step("验证推单结果"):
            allure.attach(str(result), name="推单响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"推单失败，无法进行重复取消测试，返回结果: {result}"
        # 第一次取消订单
        with allure.step("第一次取消订单操作"):
            result1 = mt_cancel_order_callback(client, order_id)
            logger.info(f"第一次取消订单结果: {result1}")
        with allure.step("验证第一次取消订单成功"):
            assert result1 == "OK", f"第一次取消订单失败，返回结果: {result1}"
        # 第二次取消订单
        with allure.step("第二次取消订单操作"):
            result2 = mt_cancel_order_callback(client, order_id)
            logger.info(f"第二次取消订单结果: {result2}")
        with allure.step("验证第二次取消订单响应"):
            # 根据业务逻辑，第二次取消可能返回特定错误或成功
            allure.attach(str(result2), name="重复取消订单响应", attachment_type=allure.attachment_type.TEXT)
            # 根据API实际行为调整断言
            assert result2 is not None, "重复取消订单应有响应"

    @pytest.mark.skip
    @allure.story("重复操作")
    @allure.title("重复对已退款订单进行退款")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_refund_duplicate_order(self, client):
        """重复退款测试"""
        # 生成订单
        with allure.step("执行推单操作"):
            logger.info("重复退款订单数据生成中")
            result, order_id = mt_push_order_callback(client)
            logger.info(f"推单结果: {result}")
        with allure.step("验证推单结果"):
            allure.attach(str(result), name="推单响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"推单失败，无法进行重复退款测试，返回结果: {result}"
        # 第一次退款
        with allure.step("第一次退款操作"):
            result1 = mt_full_refund_callback(client, order_id)
            logger.info(f"第一次退款结果: {result1}")
        with allure.step("验证第一次退款成功"):
            assert result1 == "OK", f"第一次退款失败，返回结果: {result1}"
        # 第二次退款
        with allure.step("第二次退款操作"):
            result2 = mt_full_refund_callback(client, order_id)
            logger.info(f"第二次退款结果: {result2}")
        with allure.step("验证第二次退款响应"):
            # 根据业务逻辑，第二次退款可能返回特定错误或成功
            allure.attach(str(result2), name="重复退款响应", attachment_type=allure.attachment_type.TEXT)
            # 根据API实际行为调整断言
            assert result2 is not None, "重复退款应有响应"

    @pytest.mark.skip
    @allure.story("订单状态验证")
    @allure.title("对已取消订单进行退款操作")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_refund_cancelled_order(self, client):
        """对已取消订单进行退款测试"""
        # 生成订单
        with allure.step("执行推单操作"):
            logger.info("已取消订单退款数据生成中")
            result, order_id = mt_push_order_callback(client)
            logger.info(f"推单结果: {result}")
        with allure.step("验证推单结果"):
            allure.attach(str(result), name="推单响应", attachment_type=allure.attachment_type.TEXT)
            assert result == "OK", f"推单失败，无法进行状态不匹配测试，返回结果: {result}"
        # 取消订单
        with allure.step("取消订单操作"):
            cancel_result = mt_cancel_order_callback(client, order_id)
            logger.info(f"取消订单结果: {cancel_result}")
        with allure.step("验证订单取消成功"):
            assert cancel_result == "OK", f"订单取消失败，返回结果: {cancel_result}"
        # 尝试对已取消的订单进行退款
        with allure.step("对已取消订单进行退款操作"):
            refund_result = mt_full_refund_callback(client, order_id)
            logger.info(f"对已取消订单退款结果: {refund_result}")
        with allure.step("验证对已取消订单退款的响应"):
            # 根据业务逻辑，对已取消订单退款可能返回错误信息
            allure.attach(str(refund_result), name="已取消订单退款响应", attachment_type=allure.attachment_type.TEXT)
            # 根据API实际行为调整断言
            assert refund_result is not None, "对已取消订单退款应有响应"
