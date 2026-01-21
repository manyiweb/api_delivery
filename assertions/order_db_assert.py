"""订单测试的数据库断言"""
import time
from typing import Any, Dict, Optional

import allure
from utils.log_helper import logger

from config import config
from utils.db_helper import query_order_count, query_order_exist, query_order_status


def assert_order_created(conn, order_id: str, timeout: int = None, interval: int = 1):
    """断言订单在超时内写入数据库"""
    timeout = timeout or config.DEFAULT_TIMEOUT
    sql = "SELECT * FROM dorder_dock WHERE dock_order_no = %s"
    start = time.time()

    while time.time() - start < timeout:
        result = query_order_exist(conn, sql, (order_id,))
        if result:
            allure.attach(
                str(result),
                name="order created",
                attachment_type=allure.attachment_type.TEXT,
            )
            return
        time.sleep(interval)

    raise AssertionError(f"Order {order_id} not created within {timeout}s")


def assert_order_count(
    conn, order_id: str, expected_count: int = 1, timeout: int = None, interval: int = 1
):
    """断言订单数量在超时内等于预期值"""
    timeout = timeout or config.DEFAULT_TIMEOUT
    sql = "SELECT COUNT(*) as count FROM dorder_dock WHERE dock_order_no = %s"
    start = time.time()

    while time.time() - start < timeout:
        result = query_order_count(conn, sql, (order_id,))
        if result:
            if isinstance(result, dict):
                actual_count = result.get("count", 0)
            else:
                actual_count = result[0] if result else 0
        else:
            actual_count = 0

        if actual_count == expected_count:
            allure.attach(
                f"order {order_id} count ok: {actual_count}",
                name="order count validated",
                attachment_type=allure.attachment_type.TEXT,
            )
            return

        time.sleep(interval)

    raise AssertionError(
        f"Order {order_id} count mismatch: expected {expected_count}, actual {actual_count}"
    )


def assert_order_status(
    conn,
    order_id: str,
    expected_status: str,
    timeout: int = None,
    interval: int = 1,
):
    """断言订单状态为已退货"""
    timeout = timeout or config.DEFAULT_TIMEOUT
    sql = "SELECT OrderStatus FROM dorder WHERE SourceNo = %s"
    start = time.time()

    while time.time() - start < timeout:
        result = query_order_status(conn, sql, (order_id,))
        logger
        if result:
            if isinstance(result, dict):
                actual_status = result.get("OrderStatus")
            else:
                actual_status = result[0] if result else None
        else:
            actual_status = None

        if str(actual_status) == str(expected_status):
            allure.attach(
                f"订单 {order_id} 状态为: {actual_status}",
                name="订单状态验证成功",
                attachment_type=allure.attachment_type.TEXT,
            )
            return

        time.sleep(interval)

    raise AssertionError(
        f"订单 {order_id} 期望状态： {expected_status}, 实际结果： {actual_status}"
    )