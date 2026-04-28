import os
from dataclasses import dataclass
from typing import Any, Optional

import allure
import pytest

from api.mt_order_callback import (
    mt_cancel_order_callback,
    mt_full_refund_callback,
    mt_push_order_callback,
)
from assertions.order_db_assert import (
    assert_order_count,
    assert_order_created,
    assert_order_status,
)
from assertions.order_api_assert import (
    assert_order_persisted_via_list_detail,
    assert_order_status_via_detail,
)
from utils.allure_helper import attach_text, step
from utils.logger import logger


@dataclass
class MtOrderContext:
    mt_order_id: Any
    db_conn: Any = None
    cleanup_order: Optional[list] = None
    token_id: Optional[str] = None
    internal_order_id: Optional[str] = None


def _is_fat_env() -> bool:
    return os.getenv("ENV") == "fat"


def _create_mt_order(
    client,
    step_title: str,
    *,
    log_message: str,
    fail_message: str = "推单失败",
) -> Any:
    with step(step_title):
        logger.info(log_message)
        result, mt_order_id = mt_push_order_callback(client)
        logger.info(f"推单结果: {result}, 订单号: {mt_order_id}")
        assert result == "OK", fail_message
        return mt_order_id


def _wait_order_persisted(
    client,
    request,
    mt_order_id: Any,
    *,
    fat_step_title: str = "等待订单落库",
    api_step_title: str = "等待订单落库（通过列表+详情接口）",
) -> MtOrderContext:
    context = MtOrderContext(mt_order_id=mt_order_id)

    if _is_fat_env():
        context.db_conn = request.getfixturevalue("db_conn")
        context.cleanup_order = request.getfixturevalue("cleanup_order")
        with step(fat_step_title):
            assert_order_created(context.db_conn, str(context.mt_order_id), timeout=10)
            logger.info(f"数据库已创建订单: {context.mt_order_id}")
        return context

    context.token_id = request.getfixturevalue("access_token")
    with step(api_step_title):
        context.internal_order_id = assert_order_persisted_via_list_detail(
            client,
            context.token_id,
            str(context.mt_order_id),
            timeout=60,
        )
        logger.info(f"接口验证订单已可查询，内部订单编号: {context.internal_order_id}")
    return context


def _prepare_created_order(
    client,
    request,
    *,
    create_step_title: str,
    log_message: str,
    fail_message: str = "推单失败",
) -> MtOrderContext:
    mt_order_id = _create_mt_order(
        client,
        create_step_title,
        log_message=log_message,
        fail_message=fail_message,
    )
    return _wait_order_persisted(client, request, mt_order_id)


def _assert_order_status_r4(
    client,
    context: MtOrderContext,
    *,
    fat_step_title: str,
    api_step_title: str,
) -> None:
    with step(fat_step_title if _is_fat_env() else api_step_title):
        if _is_fat_env():
            assert context.db_conn is not None
            assert_order_status(
                context.db_conn,
                str(context.mt_order_id),
                expected_status="R4",
            )
            return

        assert context.internal_order_id is not None
        assert context.token_id is not None
        assert_order_status_via_detail(
            client,
            context.token_id,
            context.internal_order_id,
            expected_status="R4",
            timeout=60,
        )


def _mark_for_cleanup(context: MtOrderContext) -> None:
    if _is_fat_env() and context.cleanup_order is not None:
        context.cleanup_order.append(str(context.mt_order_id))


def _attach_response(step_title: str, name: str, result) -> None:
    with step(step_title):
        attach_text(name, result)


@allure.epic("美团外卖业务")
@allure.feature("订单回调")
class TestMtPushOrder:
    """订单回调场景"""

    @pytest.mark.critical
    @allure.story("推单")
    @allure.title("美团推单回调成功后，系统生成订单并入库")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_push_order(self, client, request):
        logger.info(f"当前请求 BASE_URL: {client.base_url}")
        """推单应返回 OK 并创建数据库记录"""
        with step("发送推单回调"):
            logger.info("开始推单")
            mt_push_result, mt_order_id = mt_push_order_callback(client)
            logger.info(f"推单结果: {mt_push_result}, 订单号: {mt_order_id}")

        with step("校验推单响应"):
            attach_text("推单响应", mt_push_result)
            assert mt_push_result == "OK", f"推单失败: {mt_push_result}"
            logger.info("推单响应校验通过")

        context = _wait_order_persisted(
            client,
            request,
            mt_order_id,
            fat_step_title="校验订单已写入数据库",
            api_step_title="生产环境：通过列表+详情接口验证订单落库",
        )
        _mark_for_cleanup(context)

    # @pytest.mark.skip
    @pytest.mark.critical
    @allure.story("订单取消")
    @allure.title("美团取消订单回调后，订单状态更新为已退货")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_cancel_order(self, client, request):
        """成功推单后，取消订单应返回 OK"""
        context = _prepare_created_order(
            client,
            request,
            create_step_title="创建订单用于取消",
            log_message="创建订单用于取消测试",
            fail_message="推单失败，取消用例终止",
        )

        with step("发送取消回调"):
            logger.info("开始取消订单")
            mt_cancel_result = mt_cancel_order_callback(client, context.mt_order_id)

        _attach_response("校验取消响应", "取消订单响应", mt_cancel_result)

        _assert_order_status_r4(
            client,
            context,
            fat_step_title="校验订单状态",
            api_step_title="校验订单状态（通过详情接口）",
        )
        _mark_for_cleanup(context)
        logger.info("取消订单状态校验通过")

    # @pytest.mark.skip
    @pytest.mark.critical
    @allure.story("全额退款")
    @allure.title("美团全额退款回调后，订单状态更新为已退款")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_full_refund(self, client, request):
        """成功推单后，全额退款应返回 OK"""
        context = _prepare_created_order(
            client,
            request,
            create_step_title="创建订单用于退款",
            log_message="创建订单用于退款测试",
            fail_message="推单失败，退款用例终止",
        )

        with step("发送全额退款回调"):
            logger.info("开始全额退款")
            result = mt_full_refund_callback(client, context.mt_order_id)

        _attach_response("校验全额退款响应", "全额退款响应", result)

        _assert_order_status_r4(
            client,
            context,
            fat_step_title="校验订单状态",
            api_step_title="校验订单状态（通过详情接口）",
        )
        _mark_for_cleanup(context)
        logger.info("整单退款状态校验通过")

    # @pytest.mark.skip
    @pytest.mark.normal
    @allure.story("幂等性")
    @allure.title("重复推单时验证幂等性，订单表中该订单数量应为1")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mt_repeat_push_order(self, client, db_conn, cleanup_order):
        """相同订单号的第二次推单不应产生重复记录"""
        with step("第一次推单"):
            logger.info("第一次推单")
            result1, order_id = mt_push_order_callback(client)
            logger.info(f"第一次推单结果: {result1}, 订单号: {order_id}")

        with step("校验第一次推单"):
            assert result1 == "OK", f"第一次推单失败: {result1}"
            # assert_order_created(db_conn, str(order_id), timeout=10)

        with step("相同订单号的第二次推单"):
            result2, duplicate_order_id = mt_push_order_callback(
                client, order_id)
            logger.info(
                f"第二次推单结果: {result2}, 订单号: {duplicate_order_id}"
            )
            assert duplicate_order_id == order_id, (
                f"订单号不一致: {duplicate_order_id} vs {order_id}"
            )

        if _is_fat_env():
            with step("校验第二次推单及数据库数量"):
                assert result2 == "OK", f"第二次推单失败: {result2}"
                assert_order_count(db_conn, str(order_id), expected_count=1)
                cleanup_order.append(str(order_id))
                logger.info("幂等性校验通过")

    # @pytest.mark.skip
    @allure.story("异常订单处理")
    @allure.title("使用无效订单ID进行取消操作")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_mt_cancel_with_invalid_order_id(self, client):
        """取消接口应能优雅处理无效订单号"""
        with step("发送无效订单号取消请求"):
            invalid_order_id = 9999999999999999999
            result = mt_cancel_order_callback(client, invalid_order_id)
        with step("校验响应"):
            logger.info(f"无效订单取消结果: {result}")
            assert result is not None

    # @pytest.mark.skip
    @allure.story("重复取消")
    @allure.title("对同一订单进行两次取消操作")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_cancel_duplicate_order(self, client, request):
        """重复取消同一订单应被正确处理"""
        context = _prepare_created_order(
            client,
            request,
            create_step_title="创建订单",
            log_message="创建订单用于重复取消测试",
        )

        with step("第一次取消"):
            result1 = mt_cancel_order_callback(client, context.mt_order_id)
            logger.info(f"第一次取消结果: {result1}")

        _assert_order_status_r4(
            client,
            context,
            fat_step_title="校验第一次取消后订单状态为 R4",
            api_step_title="校验第一次取消后订单状态为 R4",
        )

        with step("第二次取消"):
            result2 = mt_cancel_order_callback(client, context.mt_order_id)
            logger.info(f"第二次取消结果: {result2}")

        _assert_order_status_r4(
            client,
            context,
            fat_step_title="校验第二次取消后订单状态仍为 R4",
            api_step_title="校验第二次取消后订单状态仍为 R4",
        )

        _attach_response("校验第二次取消响应", "重复取消响应", result2)

        assert result1 == result2
        _mark_for_cleanup(context)

    # @pytest.mark.skip
    @allure.story("重复退款")
    @allure.title("对同一订单进行两次退款操作")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_refund_duplicate_order(self, client, request):
        """重复退款同一订单应被正确处理"""
        context = _prepare_created_order(
            client,
            request,
            create_step_title="创建订单",
            log_message="创建订单用于重复退款测试",
        )

        with step("第一次退款"):
            result1 = mt_full_refund_callback(client, context.mt_order_id)
            logger.info(f"第一次退款结果: {result1}")

        _assert_order_status_r4(
            client,
            context,
            fat_step_title="校验第一次退款后订单状态为 R4",
            api_step_title="校验第一次退款后订单状态为 R4",
        )

        with step("第二次退款"):
            result2 = mt_full_refund_callback(client, context.mt_order_id)
            logger.info(f"第二次退款结果: {result2}")

        _assert_order_status_r4(
            client,
            context,
            fat_step_title="校验第二次退款后订单状态仍为 R4",
            api_step_title="校验第二次退款后订单状态仍为 R4",
        )

        _attach_response("校验第二次退款响应", "重复退款响应", result2)

        assert result1 == result2
        _mark_for_cleanup(context)

    # @pytest.mark.skip
    @allure.story("订单状态验证")
    @allure.title("对已取消订单进行退款操作")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_mt_refund_cancelled_order(self, client, request):
        """对已取消订单退款应被正确处理"""
        context = _prepare_created_order(
            client,
            request,
            create_step_title="创建订单",
            log_message="创建订单用于已取消订单退款测试",
        )

        with step("取消订单"):
            cancel_result = mt_cancel_order_callback(client, context.mt_order_id)

        _assert_order_status_r4(
            client,
            context,
            fat_step_title="校验取消后订单状态为 R4",
            api_step_title="校验取消后订单状态为 R4",
        )

        with step("已取消订单退款"):
            refund_result = mt_full_refund_callback(client, context.mt_order_id)
            logger.info(f"已取消订单退款结果: {refund_result}")

        _assert_order_status_r4(
            client,
            context,
            fat_step_title="校验退款后订单状态仍为 R4",
            api_step_title="校验退款后订单状态仍为 R4",
        )

        _attach_response("校验退款响应", "取消后退款响应", refund_result)

        assert cancel_result == refund_result
        _mark_for_cleanup(context)
