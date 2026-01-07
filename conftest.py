import pymysql
import pytest
import httpx
import allure
import sys
import os

from api.base import BASE_URL
from utils.db_helper import cleanup_test_order

@pytest.fixture(scope="session")
def client():
    """创建 HTTP 客户端，测试结束自动关闭"""
    with httpx.Client(base_url=BASE_URL) as c:
        allure.attach(BASE_URL, name="API Base URL", attachment_type=allure.attachment_type.TEXT)
        yield c


@pytest.fixture(scope="session")
def db_conn():
    conn = pymysql.connect(
        host='192.168.1.151',
        port=3306,
        user='zhoujiman@mop#mop',
        password='reabam123@mop',
        database='rb_ts_core',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    yield conn
    conn.close()

@pytest.fixture
def cleanup_order():
    created_orders = []
    yield created_orders
    # Teardown: 清理测试数据
    for order_id in created_orders:
        db_conn = db_conn()  # 获取连接
        cleanup_test_order(db_conn, order_id)
        db_conn.close()

# 添加pytest钩子函数来发送通知
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """在终端输出摘要时调用"""
    # 这个钩子函数在pytest输出测试结果到终端后调用
    # 可以用来获取测试统计信息并发送通知
    from utils.notification import NotificationSender, create_test_report_message
    from utils.logger import logger
    
    # 获取测试统计
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    total = passed + failed + skipped
    
    logger.info(f"测试统计: 总数={total}, 通过={passed}, 失败={failed}, 跳过={skipped}")
    
    # 创建通知发送器
    sender = NotificationSender(
        wechat_webhook="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b97e1f07-9f2c-45b9-a2bc-999b744c2ca4"
    )
    
    # 创建测试报告消息
    content = create_test_report_message(
        passed=passed,
        failed=failed, 
        skipped=skipped,
        total=total
    )
    
    logger.info("正在发送测试结果通知...")
    
    # 发送通知
    results = sender.send_notification(
        content=content,
        title="【自动化测试报告】",
        notification_types=['wechat']
    )
    
    # 检查发送结果
    for ntype, success in results.items():
        if success:
            logger.info(f"✅ {ntype} 通知发送成功")
        else:
            logger.error(f"❌ {ntype} 通知发送失败")
