from utils import logger


def query_order_exist(conn, sql, params=None):
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()


def query_order_count(conn, sql, params=None):
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        result = cursor.fetchone()
        return result


def cleanup_test_order(conn, order_id):
    """
    清理测试生成的订单数据
    """
    try:
        with conn.cursor() as cursor:
            # 删除测试订单
            delete_sql = "DELETE FROM dorder WHERE order_id = %s"
            cursor.execute(delete_sql, (order_id,))
            conn.commit()
            logger.info(f"已清理测试订单: {order_id}")
    except Exception as e:
        logger.error(f"清理测试订单失败: {e}")

def cleanup_test_data(conn, test_prefix):
    """
    清理指定前缀的测试数据
    """
    try:
        with conn.cursor() as cursor:
            # 删除测试期间创建的数据
            delete_sql = "DELETE FROM dorder WHERE order_id LIKE %s"
            cursor.execute(delete_sql, (f"{test_prefix}%",))
            conn.commit()
            logger.info(f"已清理前缀为 {test_prefix} 的测试数据")
    except Exception as e:
        logger.error(f"清理测试数据失败: {e}")
