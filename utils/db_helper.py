from utils.logger import logger
from typing import Dict, Optional, Tuple, Any
import pymysql
from contextlib import contextmanager


def query_order_exist(conn, sql: str, params: Optional[Tuple] = None) -> Optional[Dict]:
    """查询订单是否存在
    
    Args:
        conn: 数据库连接
        sql: SQL查询语句
        params: 查询参数
        
    Returns:
        查询结果字典，不存在返回None
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            logger.debug(f"查询订单存在性: SQL={sql}, params={params}, result={result}")
            return result
    except pymysql.Error as e:
        logger.error(f"查询订单存在性失败: {e}")
        raise


def query_order_count(conn, sql: str, params: Optional[Tuple] = None) -> Optional[Dict]:
    """查询订单数量
    
    Args:
        conn: 数据库连接
        sql: SQL查询语句
        params: 查询参数
        
    Returns:
        包含count字段的字典
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            logger.debug(f"查询订单数量: SQL={sql}, params={params}, result={result}")
            return result
    except pymysql.Error as e:
        logger.error(f"查询订单数量失败: {e}")
        raise


def cleanup_test_order(conn, order_id: str) -> bool:
    """清理测试生成的订单数据
    
    Args:
        conn: 数据库连接
        order_id: 订单ID
        
    Returns:
        清理是否成功
    """
    try:
        with conn.cursor() as cursor:
            # 删除测试订单
            delete_sql = "DELETE FROM dorder_dock WHERE dock_order_no = %s"
            cursor.execute(delete_sql, (order_id,))
            conn.commit()
            logger.info(f"✅ 已清理测试订单: {order_id}")
            return True
    except pymysql.Error as e:
        logger.error(f"❌ 清理测试订单失败: {e}")
        conn.rollback()
        return False

def cleanup_test_data(conn, test_prefix: str) -> bool:
    """清理指定前缀的测试数据
    
    Args:
        conn: 数据库连接
        test_prefix: 测试数据前缀
        
    Returns:
        清理是否成功
    """
    try:
        with conn.cursor() as cursor:
            # 删除测试期间创建的数据
            delete_sql = "DELETE FROM dorder_dock WHERE dock_order_no LIKE %s"
            cursor.execute(delete_sql, (f"{test_prefix}%",))
            deleted_count = cursor.rowcount
            conn.commit()
            logger.info(f"✅ 已清理前缀为 {test_prefix} 的测试数据，共 {deleted_count} 条")
            return True
    except pymysql.Error as e:
        logger.error(f"❌ 清理测试数据失败: {e}")
        conn.rollback()
        return False


def query_order_detail(conn, order_id: str) -> Optional[Dict[str, Any]]:
    """查询订单详细信息
    
    Args:
        conn: 数据库连接
        order_id: 订单ID
        
    Returns:
        订单详细信息字典
    """
    sql = """SELECT dock_order_no, order_status, total_amount, 
             create_time, update_time FROM dorder_dock 
             WHERE dock_order_no = %s"""
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (order_id,))
            result = cursor.fetchone()
            logger.debug(f"查询订单详情: order_id={order_id}, result={result}")
            return result
    except pymysql.Error as e:
        logger.error(f"查询订单详情失败: {e}")
        raise


@contextmanager
def get_db_connection(db_config: Dict):
    """数据库连接上下文管理器
    
    Args:
        db_config: 数据库配置字典
        
    Yields:
        数据库连接对象
    """
    conn = None
    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        logger.info("✅ 数据库连接成功")
        yield conn
    except pymysql.Error as e:
        logger.error(f"❌ 数据库连接失败: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("数据库连接已关闭")
