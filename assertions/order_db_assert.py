"""Database assertions for order tests."""
import time
from typing import Any, Dict, Optional

import allure

from config import config
from utils.db_helper import query_order_count, query_order_exist


def assert_order_created(conn, order_id: str, timeout: int = None, interval: int = 1):
    """Assert the order exists in DB within timeout."""
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
    """Assert order count equals expected within timeout."""
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
