"""订单数据库断言模块。"""
import time
from typing import Any, Dict, Optional

import allure
import pymysql

from config import config
from utils.db_helper import query_order_count, query_order_exist


def assert_order_created(
    conn: pymysql.connections.Connection,
    order_id: str,
    timeout: Optional[int] = None,
    interval: int = 1,
) -> None:
    """校验订单是否在指定时间内入库。"""
    timeout = timeout or config.DEFAULT_TIMEOUT
    sql = "SELECT * FROM dorder_dock WHERE dock_order_no = %s"
    start = time.time()
    end_time = start + timeout

    while True:
        result = query_order_exist(conn, sql, (order_id,))
        if result:
            allure.attach(
                str(result),
                name="订单入库成功",
                attachment_type=allure.attachment_type.TEXT,
            )
            return

        # 检查是否超时，避免不必要的 sleep
        if time.time() >= end_time:
            break

        time.sleep(interval)

    raise AssertionError(f"订单 {order_id} 在 {timeout}s 内未入库")


def assert_order_count(
    conn: pymysql.connections.Connection,
    order_id: str,
    expected_count: int = 1,
    timeout: Optional[int] = None,
    interval: int = 1,
) -> None:
    """校验订单数量是否符合预期。"""
    timeout = timeout or config.DEFAULT_TIMEOUT
    sql = "SELECT COUNT(*) as count FROM dorder_dock WHERE dock_order_no = %s"
    start = time.time()
    end_time = start + timeout
    actual_count = 0  # 初始化变量，避免未定义错误

    while True:
        result = query_order_count(conn, sql, (order_id,))
        actual_count = result.get("count", 0) if result else 0

        if actual_count == expected_count:
            allure.attach(
                f"订单 {order_id} 数量验证成功: {actual_count}",
                name="订单数量验证",
                attachment_type=allure.attachment_type.TEXT,
            )
            return

        # 检查是否超时，避免不必要的 sleep
        if time.time() >= end_time:
            break

        time.sleep(interval)

    raise AssertionError(
        f"订单 {order_id} 数量验证失败: 期望 {expected_count}, 实际 {actual_count}"
    )
