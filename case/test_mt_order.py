"""美团订单回调测试
涵盖推单、取消、退款和幂等场景
"""
import os

import allure
import pytest

from api.order_callback import (
    mt_cancel_order_callback,
    mt_full_refund_callback,
    mt_push_order_callback,
)
from assertions.order_db_assert import assert_order_count, assert_order_created, assert_order_status
from utils.logger import logger


@allure.epic("Meituan API")
@allure.feature("订单回调")
class TestMtPushOrder:
    """订单回调场景"""

    @pytest.mark.skip
    @pytest.mark.critical
    @allure.story("推单")
    @allure.title("美团推单回调成功后，系统生成订单并入库")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_push_order(self, client, request):
        """推单应返回 OK 并创建数据库记录"""
        with allure.step("发送推单回调"):
            logger.info("开始推单")
            result, order_id = mt_push_order_callback(client)
            logger.info(f"推单结果: {result}, 订单号: {order_id}")

        with allure.step("校验推单响应"):
            allure.attach(
                str(result),
                name="push order response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert result == "OK", f"Push order failed: {result}"
            logger.info("推单响应校验通过")

        if os.getenv("ENV") == "fat":
            db_conn = request.getfixturevalue("db_conn")
            cleanup_order = request.getfixturevalue("cleanup_order")
            with allure.step("校验订单已写入数据库"):
                assert_order_created(db_conn, str(order_id), timeout=10)
                cleanup_order.append(str(order_id))
                logger.info(f"数据库已创建订单: {order_id}")

    @pytest.mark.critical
    @allure.story("订单取消")
    @allure.title("美团取消订单回调后，订单状态更新为已取消")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_cancel_order(self, client, db_conn, cleanup_order, request):
        """成功推单后，取消订单应返回 OK"""
        with allure.step("创建订单用于取消"):
            logger.info("创建订单用于取消测试")
            result, order_id = mt_push_order_callback(client)
            logger.info(f"推单结果: {result}, 订单号: {order_id}")
            assert result == "OK", "Push order failed; cancel test aborted"

        with allure.step("等待订单落库"):
            assert_order_created(db_conn, str(order_id), timeout=10)

        with allure.step("发送取消回调"):
            logger.info("开始取消订单")
            result = mt_cancel_order_callback(client, order_id)

        with allure.step("校验取消响应"):
            allure.attach(
                str(result),
                name="cancel order response",
                attachment_type=allure.attachment_type.TEXT,
            )
        if os.getenv("ENV") == "fat":
            db_conn = request.getfixturevalue("db_conn")
            cleanup_order = request.getfixturevalue("cleanup_order")
            with allure.step("校验订单状态"):
                assert_order_status(db_conn, str(order_id), expected_status="R4")
                cleanup_order.append(str(order_id))
                logger.info("取消订单成功")

    @pytest.mark.skip
    @pytest.mark.critical
    @allure.story("全额退款")
    @allure.title("美团全额退款回调后，订单状态更新为已退款")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_full_refund(self, client, db_conn, cleanup_order):
        """成功推单后，全额退款应返回 OK"""
        with allure.step("创建订单用于退款"):
            logger.info("创建订单用于退款测试")
            result, order_id = mt_push_order_callback(client)
            assert result == "OK", "Push order failed; refund test aborted"

        with allure.step("等待订单落库"):
            assert_order_created(db_conn, str(order_id), timeout=10)

        with allure.step("发送全额退款回调"):
            logger.info("开始全额退款")
            result = mt_full_refund_callback(client, order_id)

        with allure.step("校验全额退款响应"):
            allure.attach(
                str(result),
                name="full refund response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert result == "OK", f"Full refund failed: {result}"
            cleanup_order.append(str(order_id))
            logger.info("全额退款成功")

    @pytest.mark.skip
    @pytest.mark.normal
    @allure.story("幂等性")
    @allure.title("重复推单时验证幂等性，订单表中该订单数量应为1")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mt_repeat_push_order(self, client, db_conn, cleanup_order):
        """相同订单号的第二次推单不应产生重复记录"""
        with allure.step("第一次推单"):
            logger.info("第一次推单")
            result1, order_id = mt_push_order_callback(client)
            logger.info(f"第一次推单结果: {result1}, 订单号: {order_id}")

        with allure.step("校验第一次推单"):
            assert result1 == "OK", f"First push failed: {result1}"
            assert_order_created(db_conn, str(order_id), timeout=10)

        with allure.step("相同订单号的第二次推单"):
            result2, duplicate_order_id = mt_push_order_callback(client, order_id)
            logger.info(
                f"第二次推单结果: {result2}, 订单号: {duplicate_order_id}"
            )
            assert duplicate_order_id == order_id, (
                f"Order ID mismatch: {duplicate_order_id} vs {order_id}"
            )

        with allure.step("校验第二次推单及数据库数量"):
            assert result2 == "OK", f"Second push failed: {result2}"
            assert_order_count(db_conn, str(order_id), expected_count=1)
            cleanup_order.append(str(order_id))
            logger.info("幂等性校验通过")

    @pytest.mark.skip
    @allure.story("异常订单处理")
    @allure.title("使用无效订单ID进行取消操作")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_cancel_with_invalid_order_id(self, client):
        """取消接口应能优雅处理无效订单号"""
        with allure.step("发送无效订单号取消请求"):
            invalid_order_id = 9999999999999999999
            result = mt_cancel_order_callback(client, invalid_order_id)
        with allure.step("校验响应"):
            logger.info(f"无效订单取消结果: {result}")
            assert result is not None

    @pytest.mark.skip
    @allure.story("重复取消")
    @allure.title("对同一订单进行两次取消操作")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cancel_duplicate_order(self, client, cleanup_order):
        """重复取消同一订单应被正确处理"""
        with allure.step("创建订单"):
            result, order_id = mt_push_order_callback(client)
            assert result == "OK", "Push order failed"
            cleanup_order.append(str(order_id))

        with allure.step("第一次取消"):
            result1 = mt_cancel_order_callback(client, order_id)
            logger.info(f"第一次取消结果: {result1}")
            assert result1 == "OK", f"First cancel failed: {result1}"

        with allure.step("第二次取消"):
            result2 = mt_cancel_order_callback(client, order_id)
            logger.info(f"第二次取消结果: {result2}")

        with allure.step("校验第二次取消响应"):
            allure.attach(
                str(result2),
                name="duplicate cancel response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert result2 is not None

    @pytest.mark.skip
    @allure.story("重复退款")
    @allure.title("对同一订单进行两次退款操作")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_refund_duplicate_order(self, client, cleanup_order):
        """重复退款同一订单应被正确处理"""
        with allure.step("创建订单"):
            result, order_id = mt_push_order_callback(client)
            assert result == "OK", "Push order failed"
            cleanup_order.append(str(order_id))

        with allure.step("第一次退款"):
            result1 = mt_full_refund_callback(client, order_id)
            logger.info(f"第一次退款结果: {result1}")
            assert result1 == "OK", f"First refund failed: {result1}"

        with allure.step("第二次退款"):
            result2 = mt_full_refund_callback(client, order_id)
            logger.info(f"第二次退款结果: {result2}")

        with allure.step("校验第二次退款响应"):
            allure.attach(
                str(result2),
                name="duplicate refund response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert result2 is not None

    @pytest.mark.skip
    @allure.story("订单状态验证")
    @allure.title("对已取消订单进行退款操作")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_refund_cancelled_order(self, client, cleanup_order):
        """对已取消订单退款应被正确处理"""
        with allure.step("创建订单"):
            result, order_id = mt_push_order_callback(client)
            assert result == "OK", "Push order failed"
            cleanup_order.append(str(order_id))

        with allure.step("取消订单"):
            cancel_result = mt_cancel_order_callback(client, order_id)
            assert cancel_result == "OK", "Cancel failed"

        with allure.step("已取消订单退款"):
            refund_result = mt_full_refund_callback(client, order_id)
            logger.info(f"已取消订单退款结果: {refund_result}")

        with allure.step("校验退款响应"):
            allure.attach(
                str(refund_result),
                name="refund canceled order response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert refund_result == "ERROR"
