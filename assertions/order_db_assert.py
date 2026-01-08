"""订单数据库断言模块
提供订单相关的数据库断言方法
"""
import time
import allure
from typing import Optional, Any, Dict

from config import config
from utils.db_helper import query_order_exist, query_order_count, query_order_detail


def assert_order_created(conn, order_id: str, timeout: int = None, interval: int = 1):
    """校验订单是否成功入库（支持异步）
    
    Args:
        conn: 数据库连接
        order_id: 订单ID
        timeout: 超时时间（秒）
        interval: 轮询间隔（秒）
        
    Raises:
        AssertionError: 订单未在预期时间内入库
    """
    timeout = timeout or config.DEFAULT_TIMEOUT
    sql = "SELECT * FROM dorder_dock WHERE dock_order_no = %s"
    start = time.time()

    while time.time() - start < timeout:
        result = query_order_exist(conn, sql, (order_id,))
        if result:
            allure.attach(
                str(result),
                name="订单入库成功",
                attachment_type=allure.attachment_type.TEXT
            )
            return

        time.sleep(interval)

    raise AssertionError(f"❌ 订单 {order_id} 在 {timeout}s 内未入库")


def assert_order_count(conn, order_id: str, expected_count: int = 1, timeout: int = None, interval: int = 1):
    """校验订单在数据库中的数量，用于验证重复推单的幂等性
    
    Args:
        conn: 数据库连接
        order_id: 订单ID
        expected_count: 期望的订单数量
        timeout: 超时时间（秒）
        interval: 轮询间隔（秒）
        
    Raises:
        AssertionError: 订单数量不符合预期
    """
    timeout = timeout or config.DEFAULT_TIMEOUT
    sql = "SELECT COUNT(*) as count FROM dorder_dock WHERE dock_order_no = %s"
    start = time.time()

    while time.time() - start < timeout:
        result = query_order_count(conn, sql, (order_id,))
        if result:
            # 如果result是字典格式，使用'count'键获取值
            if isinstance(result, dict):
                actual_count = result.get('count', 0) if result else 0
            else:
                # 如果result是元组格式，使用索引获取值
                actual_count = result[0] if result else 0
        else:
            actual_count = 0
        
        if actual_count == expected_count:
            allure.attach(
                f"✅ 订单 {order_id} 数量验证成功: {actual_count}",
                name="订单数量验证",
                attachment_type=allure.attachment_type.TEXT
            )
            return

        time.sleep(interval)

    raise AssertionError(f"❌ 订单 {order_id} 数量验证失败: 期望 {expected_count}, 实际 {actual_count}")
