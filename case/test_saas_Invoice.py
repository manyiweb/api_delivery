import allure
import httpx
import pytest

from api.Invoice_api import mgr_apply_invoice, query_invoice_status, refresh_invoice_status, red_punch_invoice
from api.create_order_cash import add_service_guide, add_item_shoppingcart, add_order_cash, cash_pay
from conftest import access_token
from utils.logger import logger


@pytest.fixture(scope="class")
def create_invoice_order(client: httpx.Client, access_token):
    token_id = access_token
    with allure.step("创建开票订单"):
        # 添加服务导购
        add_service_guide(client, token_id)
        # 新增购物车商品
        add_item_shoppingcart(client, token_id)
        # 新增现金支付订单
        order_id = add_order_cash(client, token_id)
        # 现金支付
        cash_pay(client, token_id, order_id)
        logger.info("订单 %s 创建成功", order_id)
        return order_id




@allure.epic("开票 API")
@allure.feature("SaaS 开票")
class TestSaasInvoice:
    @pytest.mark.critical
    @allure.story("申请开票")
    @allure.title("申请开票后查询开票状态并获取开票信息")
    def test_apply_invoice(self, client, create_invoice_order, access_token):
        order_id = create_invoice_order
        token_id = access_token
        # 申请开票
        invoice_id = mgr_apply_invoice(client, order_id, token_id=token_id)
        # 刷新开票状态
        refresh_invoice_status(client, invoice_id, token_id=token_id)
        # 查询开票状态
        invoice_status = query_invoice_status(client, order_id, token_id=token_id)
        assert invoice_status == "INVOICED"

    @allure.story("红冲开票")
    @allure.title("申请开票后红冲开票")
    def test_red_punch(self, client, create_invoice_order, access_token):
        order_id = create_invoice_order
        token_id = access_token
        # 申请开票
        invoice_id = mgr_apply_invoice(client, order_id, token_id=token_id)
        # 刷新开票状态
        refresh_invoice_status(client, invoice_id, token_id=token_id)
        # 查询开票状态
        invoice_status = query_invoice_status(client, order_id, token_id=token_id)
        # 红冲发票
        red_punch_invoice(client, invoice_id, token_id=token_id)

    @allure.story("合并开票")
    def test_together_invoice(self, client, create_invoice_order, access_token):
