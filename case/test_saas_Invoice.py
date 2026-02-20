import json
from typing import Any, List

import allure
import httpx
import pytest

from api.Invoice_api import (
    apply_invoice_for_order,
    build_apply_invoice_payload,
    build_empty_order_id_payload,
    build_merge_invoice_payload,
    build_none_order_invoice_payload,
    execute_apply_invoice,
    query_invoice_status,
    refresh_invoice_status,
    red_punch_invoice,
)
from api.create_order_cash import (
    add_service_guide,
    add_item_shoppingcart,
    add_order_cash,
    cash_pay,
)
from assertions.order_invoice_assert import (
    assert_apply_response,
    assert_detail_response,
    assert_refresh_response,
    assert_red_punch_response,
)
# from utils.db_helper import cleanup_test_order
from utils.logger import logger


def _attach_json(name: str, data: Any) -> None:
    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def _attach_text(name: str, value: Any) -> None:
    allure.attach(
        str(value),
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )


def _create_invoice_order(client: httpx.Client, token_id: str, index: int) -> str:
    with allure.step(f"创建第{index}笔订单"):
        with allure.step("添加服务导购"):
            add_service_guide(client, token_id)
        with allure.step("添加购物车商品"):
            add_item_shoppingcart(client, token_id)
        with allure.step("创建现金订单"):
            order_id = add_order_cash(client, token_id)
        with allure.step("现金支付"):
            cash_pay(client, token_id, order_id)
        logger.info("第%s笔订单创建成功，订单号=%s", index, order_id)
        _attach_text(f"第{index}笔订单号", order_id)
        return order_id


@pytest.fixture(scope="function")
def create_invoice_order(client: httpx.Client, access_token):
    token_id = access_token
    with allure.step("创建开票订单"):
        order_id = _create_invoice_order(client, token_id, 1)
        yield order_id
        # # 测试结束后清理订单（需要内网数据库连接）
        # with allure.step("清理测试订单"):
        #     cleanup_test_order(db_conn, order_id)


@pytest.fixture(scope="function")
def create_merge_invoice_orders(client: httpx.Client, access_token) -> List[str]:
    token_id = access_token
    with allure.step("创建合并开票订单"):
        order_ids = [
            _create_invoice_order(client, token_id, 1),
            _create_invoice_order(client, token_id, 2),
        ]
        _attach_json("合并订单号列表", order_ids)
        yield order_ids
        # # 测试结束后清理订单（需要内网数据库连接）
        # with allure.step("清理测试订单"):
        #     for order_id in order_ids:
        #         cleanup_test_order(db_conn, order_id)


@allure.epic("开票业务")
@allure.feature("品牌端开票")
class TestSaasInvoice:
    # @pytest.mark.critical
    @allure.story("申请开票")
    @allure.title("申请开票后刷新并查询状态")
    def test_apply_invoice(self, client, create_invoice_order, access_token):
        order_id = create_invoice_order
        token_id = access_token

        with allure.step("申请开票"):
            invoice_id, apply_resp = apply_invoice_for_order(
                client, order_id, token_id=token_id, return_response=True
            )
            _attach_text("开票号", invoice_id)
            _attach_json("开票接口响应", apply_resp)
            assert_apply_response(apply_resp, invoice_id, order_id)

        with allure.step("刷新开票状态"):
            refresh_resp = refresh_invoice_status(
                client, invoice_id, token_id=token_id)
            _attach_json("刷新开票状态接口响应", refresh_resp)
            assert_refresh_response(refresh_resp)

        with allure.step("查询开票状态"):
            invoice_status, detail_resp = query_invoice_status(
                client, invoice_id, token_id=token_id, return_response=True
            )
            _attach_text("开票状态", invoice_status)
            _attach_json("查询开票状态接口响应", detail_resp)
            assert_detail_response(
                detail_resp, invoice_id, order_id, invoice_status)

    @allure.story("红冲开票")
    @allure.title("申请开票后红冲")
    def test_red_punch(self, client, create_invoice_order, access_token):
        order_id = create_invoice_order
        token_id = access_token

        with allure.step("申请开票"):
            invoice_id, apply_resp = apply_invoice_for_order(
                client, order_id, token_id=token_id, return_response=True
            )
            _attach_text("开票号", invoice_id)
            _attach_json("开票接口响应", apply_resp)
            assert_apply_response(apply_resp, invoice_id, order_id)

        with allure.step("刷新开票状态"):
            refresh_resp = refresh_invoice_status(
                client, invoice_id, token_id=token_id)
            _attach_json("刷新开票状态接口响应", refresh_resp)
            assert_refresh_response(refresh_resp)

        with allure.step("查询开票状态"):
            invoice_status, detail_resp = query_invoice_status(
                client, invoice_id, token_id=token_id, return_response=True
            )
            _attach_text("开票状态", invoice_status)
            _attach_json("查询开票状态接口响应", detail_resp)
            assert_detail_response(
                detail_resp, invoice_id, order_id, invoice_status)

        with allure.step("红冲开票"):
            red_resp = red_punch_invoice(client, invoice_id, token_id=token_id)
            _attach_json("红冲接口响应", red_resp)
            assert_red_punch_response(red_resp)
            logger.info("红冲完成，开票号=%s", invoice_id)

    @allure.story("合并开票")
    @allure.title("合并开票后红冲")
    def test_merge_invoice(self, client, create_merge_invoice_orders, access_token):
        order_ids = create_merge_invoice_orders
        token_id = access_token
        payload = build_merge_invoice_payload(order_ids, token_id)
        logger.info("构建合并开票请求参数: %s", payload)
        with allure.step("合并开票"):
            _attach_json("合并开票请求参数", payload)
            invoice_id, apply_resp = execute_apply_invoice(
                client, payload, token_id=token_id, return_response=True
            )
            _attach_text("开票号", invoice_id)
            _attach_json("开票接口响应", apply_resp)
            assert_apply_response(apply_resp, invoice_id, order_ids)

        with allure.step("刷新开票状态"):
            refresh_resp = refresh_invoice_status(
                client, invoice_id, token_id=token_id)
            _attach_json("刷新开票状态接口响应", refresh_resp)
            assert_refresh_response(refresh_resp)

        with allure.step("查询开票状态"):
            invoice_status, detail_resp = query_invoice_status(
                client, invoice_id, token_id=token_id, return_response=True
            )
            _attach_text("开票状态", invoice_status)
            _attach_json("查询开票状态接口响应", detail_resp)
            assert_detail_response(
                detail_resp, invoice_id, order_ids, invoice_status)

        with allure.step("红冲开票"):
            red_resp = red_punch_invoice(client, invoice_id, token_id=token_id)
            _attach_json("红冲接口响应", red_resp)
            assert_red_punch_response(red_resp)
            logger.info("红冲完成，开票号=%s", invoice_id)

    @pytest.mark.critical
    @allure.story("异常场景")
    @allure.title("合并开票订单号为空字符串时接口返回空指针异常")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_merge_invoice_empty_order_id_return_null_pointer(self, client, access_token):
        """orderAmountList 中 orderId 为空时，接口应返回 500 空指针错误"""
        token_id = access_token

        with allure.step("构建 orderId 为空的请求参数"):
            payload = build_empty_order_id_payload(token_id)
            _attach_json("开票请求参数", payload)
            logger.info("构建 orderId 为空的合并开票请求参数: %s", payload)

        with allure.step("发送合并开票请求"):
            resp = execute_apply_invoice(
                client, payload, token_id=token_id, parse_response=False)
            _attach_text("响应状态码", resp.status_code)
            _attach_json("响应内容", resp.json())
            logger.info("接口响应状态码: %s", resp.status_code)
            logger.info("接口响应内容: %s", resp.json())

        with allure.step("校验返回订单不存在错误"):
            response_json = resp.json()
            assert response_json.get(
                "success") is False, f"期望 success 为 False，实际 {response_json.get('success')}"
            assert "订单【】不存在" in response_json.get("msg", ""), (
                f"响应中未包含预期错误信息，实际 msg: {response_json.get('msg')}"
            )
            logger.info("订单不存在错误校验通过")

    @allure.story("异常场景")
    @allure.title("合并开票金额数量不一致时提示异常")
    def test_merge_invoice_amount_mismatch(self, access_token):
        token_id = access_token
        order_ids = ["order-1", "order-2"]
        with allure.step("构建合并开票请求"):
            with pytest.raises(ValueError) as exc_info:
                build_merge_invoice_payload(
                    order_ids, token_id, amount_list=[2])
            _attach_text("异常信息", str(exc_info.value))

    @pytest.mark.critical
    @allure.story("逆向场景")
    @allure.title("无效令牌申请开票返回登录已失效")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_apply_invoice_invalid_token(self, client, create_invoice_order):
        """使用过期 token 申请开票，应返回登录已失效错误"""
        order_id = create_invoice_order
        # 固定一个无效的过期 token
        invalid_token = "d7fcce6b432323324a5c322fb30dab"
        payload = build_apply_invoice_payload(order_id, invalid_token)

        with allure.step("准备无效令牌请求"):
            _attach_json("开票请求参数", payload)
            _attach_text("使用的无效令牌", invalid_token)
            logger.info("使用固定过期令牌申请开票%s", payload)

        with allure.step("发送开票请求"):
            resp = execute_apply_invoice(
                client, payload, token_id=invalid_token, parse_response=False)
            _attach_text("响应状态码", resp.status_code)
            _attach_json("响应内容", resp.json())
            logger.info("接口响应状态码: %s", resp.status_code)
            logger.info("接口响应内容: %s", resp.json())

        with allure.step("校验返回登录已失效错误"):
            response_json = resp.json()
            result_string = response_json.get("ResultString", "")
            assert result_string == "登录已失效，请重登录或认证", (
                f"期望错误信息为'登录已失效，请重登录或认证'，实际: {result_string}"
            )
            logger.info("登录已失效错误校验通过")
        # # 清理测试订单（需要内网数据库连接）
        # finally:
        #     with allure.step("清理测试订单"):
        #         cleanup_test_order(db_conn, order_id)

    @pytest.mark.critical
    @allure.story("异常场景")
    @allure.title("开票金额大于订单金额时返回错误")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_apply_invoice_exceed_amount(self, client, create_invoice_order, access_token):
        """开票金额大于订单金额时，接口应返回 500 错误"""
        order_id = create_invoice_order
        token_id = access_token

        with allure.step("构建高开票金额请求参数"):
            # 通过 extra 参数设置高开票金额
            extra = {"orderAmountList": [
                {"orderId": order_id, "currentInvoiceAmount": 3, "replaceType": "none"}]}
            payload = build_apply_invoice_payload(
                order_id, token_id, extra=extra)
            _attach_json("开票请求参数", payload)
            logger.info("构建高开票金额请求参数: %s", payload)

        with allure.step("发送开票请求"):
            resp = execute_apply_invoice(
                client, payload, token_id=token_id, parse_response=False)
            _attach_text("响应状态码", resp.status_code)
            _attach_json("响应内容", resp.json())
            logger.info("接口响应状态码: %s", resp.status_code)
            logger.info("接口响应内容: %s", resp.json())

        with allure.step("校验返回开票金额超限错误"):
            response_json = resp.json()
            assert response_json.get("code") == "500", (
                f"期望错误码为 '500'，实际: {response_json.get('code')}"
            )
            expected_msg = f"开票金额大于可开票金额"
            assert expected_msg in response_json.get("msg", ""), (
                f"期望错误信息包含 '{expected_msg}'，实际 msg: {response_json.get('msg')}"
            )
            logger.info("开票金额超限错误校验通过")

    @pytest.mark.critical
    @allure.story("无订单开票")
    @allure.title("无订单开票成功并红冲")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_none_order_invoice(self, client, access_token):
        """无订单开票时，接口应返回成功，验证后进行红冲形成闭环"""
        token_id = access_token
        invoice_id = None

        with allure.step("构建无订单开票请求参数"):
            payload = build_none_order_invoice_payload(token_id)
            _attach_json("无订单开票请求参数", payload)
            logger.info("构建无订单开票请求参数: %s", payload)

        with allure.step("发送无订单开票请求"):
            invoice_id, apply_resp = execute_apply_invoice(
                client, payload, token_id=token_id, return_response=True)
            _attach_text("开票号", invoice_id)
            _attach_json("开票接口响应", apply_resp)
            logger.info("无订单开票成功，开票号: %s", invoice_id)

        with allure.step("刷新开票状态"):
            refresh_resp = refresh_invoice_status(
                client, invoice_id, token_id=token_id)
            _attach_json("刷新开票状态接口响应", refresh_resp)
            logger.info("刷新开票状态完成")

        with allure.step("查询开票状态"):
            invoice_status, detail_resp = query_invoice_status(
                client, invoice_id, token_id=token_id, return_response=True
            )
            _attach_text("开票状态", invoice_status)
            _attach_json("查询开票状态接口响应", detail_resp)
            logger.info("查询开票状态完成，当前状态: %s", invoice_status)

        with allure.step("红冲开票"):
            red_resp = red_punch_invoice(client, invoice_id, token_id=token_id)
            _attach_json("红冲接口响应", red_resp)
            assert_red_punch_response(red_resp)
            logger.info("红冲完成，开票号=%s", invoice_id)
