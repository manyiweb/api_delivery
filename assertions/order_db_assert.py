import time
import allure
from utils.db_helper import query_order_exist


def assert_order_created(conn, order_id, timeout=10, interval=1):
    """
    校验订单是否成功入库（支持异步）
    """
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

    raise AssertionError(f"订单 {order_id} 在 {timeout}s 内未入库")
