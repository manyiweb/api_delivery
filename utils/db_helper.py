from contextlib import contextmanager
from typing import Any, Dict, Optional, Tuple

import pymysql

from utils.logger import logger


def query_order_exist(conn, sql: str, params: Optional[Tuple] = None) -> Optional[Dict]:
    """Return a single order record if it exists."""
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
    """Return order count."""
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            logger.debug(
                f"Query order count: sql={sql}, params={params}, result={result}"
            )
            return result
    except pymysql.Error as e:
        logger.error(f"Query order count failed: {e}")
        raise


def cleanup_test_order(conn, order_id: str) -> bool:
    """Delete a test order by ID."""
    try:
        with conn.cursor() as cursor:
            delete_sql = "DELETE FROM dorder_dock WHERE dock_order_no = %s"
            cursor.execute(delete_sql, (order_id,))
            conn.commit()
            logger.info(f"[OK] cleaned test order: {order_id}")
            return True
    except pymysql.Error as e:
        logger.error(f"[FAIL] cleanup test order failed: {e}")
        conn.rollback()
        return False


def cleanup_test_data(conn, test_prefix: str) -> bool:
    """Delete test data by order ID prefix."""
    try:
        with conn.cursor() as cursor:
            delete_sql = "DELETE FROM dorder_dock WHERE dock_order_no LIKE %s"
            cursor.execute(delete_sql, (f"{test_prefix}%",))
            deleted_count = cursor.rowcount
            conn.commit()
            logger.info(
                f"[OK] cleaned test data prefix={test_prefix}, count={deleted_count}"
            )
            return True
    except pymysql.Error as e:
        logger.error(f"[FAIL] cleanup test data failed: {e}")
        conn.rollback()
        return False


def query_order_detail(conn, order_id: str) -> Optional[Dict[str, Any]]:
    """Query order details by ID."""
    sql = (
        "SELECT dock_order_no, order_status, total_amount, create_time, update_time "
        "FROM dorder_dock WHERE dock_order_no = %s"
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (order_id,))
            result = cursor.fetchone()
            logger.debug(f"Query order detail: order_id={order_id}, result={result}")
            return result
    except pymysql.Error as e:
        logger.error(f"Query order detail failed: {e}")
        raise


@contextmanager
def get_db_connection(db_config: Dict):
    """Context-managed DB connection."""
    conn = None
    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        logger.info("[OK] database connection established")
        yield conn
    except pymysql.Error as e:
        logger.error(f"[FAIL] database connection failed: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")
