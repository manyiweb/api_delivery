from contextlib import contextmanager
from typing import Any, Dict, Optional, Tuple

import pymysql

from utils.logger import logger


def query_order_exist(conn, sql: str, params: Optional[Tuple] = None) -> Optional[Dict]:
    """若存在则返回单条订单记录"""
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            logger.debug(
                f"Query order exist: sql={sql}, params={params}, result={result}"
            )
            return result
    except pymysql.Error as e:
        logger.error(f"Query order exist failed: {e}")
        raise


def query_order_count(conn, sql: str, params: Optional[Tuple] = None) -> Optional[Dict]:
    """返回订单数量"""
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            logger.debug(
                f"清除订单数量: sql={sql}, params={params}, result={result}"
            )
            return result
    except pymysql.Error as e:
        logger.error(f"查询订单数量失败: {e}")
        raise


def cleanup_test_order(conn, order_id: str) -> bool:
    """按订单 ID 删除测试订单"""
    try:
        with conn.cursor() as cursor:
            delete_sql = "DELETE FROM dorder WHERE SourceNo = %s"
            cursor.execute(delete_sql, (order_id,))
            conn.commit()
            logger.info(f"[OK] 清除测试订单: {order_id}")
            return True
    except pymysql.Error as e:
        logger.error(f"[FAIL] 清除测试订单失败: {e}")
        conn.rollback()
        return False


def cleanup_test_data(conn, test_prefix: str) -> bool:
    """按订单 ID 前缀删除测试数据"""
    try:
        with conn.cursor() as cursor:
            delete_sql = "DELETE FROM dorder WHERE SourceNo = %s"
            cursor.execute(delete_sql, (f"{test_prefix}%",))
            deleted_count = cursor.rowcount
            conn.commit()
            logger.info(
                f"[OK] 清理测试数据前缀={test_prefix}, 数量={deleted_count}"
            )
            return True
    except pymysql.Error as e:
        logger.error(f"[FAIL] cleanup test data failed: {e}")
        conn.rollback()
        return False


def query_order_detail(conn, order_id: str) -> Optional[Dict[str, Any]]:
    """按订单 ID 查询订单详情"""
    sql = (
        "SELECT dock_order_no, order_status, total_amount, create_time, update_time "
        "FROM dorder_dock WHERE dock_order_no = %s"
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (order_id,))
            result = cursor.fetchone()
            logger.debug(f"查询订单详情: order_id={order_id}, result={result}")
            return result
    except pymysql.Error as e:
        logger.error(f"查询订单详情失败: {e}")
        raise

def query_order_status(conn, sql: str, order_id: str) ->  Optional[Dict]:
    """按订单 ID 查询订单状态"""
    # sql = "SELECT OrderStatus FROM dorder WHERE SourceNo = %s"
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (order_id,))
            result = cursor.fetchone()
            logger.info(f"查询订单状态: order_id={order_id}, result={result}")
            return result["OrderStatus"] if result else None
    except pymysql.Error as e:
        logger.error(f"查询订单状态失败: {e}")
        raise

@contextmanager
def get_db_connection(db_config: Dict):
    """上下文管理的数据库连接"""
    conn = None
    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        logger.info("[OK] 数据库连接已建立")
        yield conn
    except pymysql.Error as e:
        logger.error(f"[FAIL] 数据库连接失败: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("数据库连接已关闭")

