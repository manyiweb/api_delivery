import os

import allure
import httpx
import pymysql
import pytest

from config import config
from utils.db_helper import cleanup_test_order
from utils.logger import logger
from utils.notification import NotificationSender, create_test_report_message


@pytest.fixture(scope="session")
def client():
    """创建 HTTP 客户端，测试结束自动关闭。"""
    base_url = config.get_base_url()
    with httpx.Client(base_url=base_url, timeout=config.DEFAULT_TIMEOUT) as c:
        allure.attach(base_url, name="API 基础地址", attachment_type=allure.attachment_type.TEXT)
        yield c


@pytest.fixture(scope="session")
def db_conn():
    """创建数据库连接，测试结束自动关闭。"""
    conn = pymysql.connect(
        **config.DB_CONFIG,
        cursorclass=pymysql.cursors.DictCursor,
    )
    allure.attach(
        f"数据库: {config.DB_CONFIG['host']}:{config.DB_CONFIG['port']}/{config.DB_CONFIG['database']}",
        name="数据库连接信息",
        attachment_type=allure.attachment_type.TEXT,
    )
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def cleanup_order(db_conn):
    """收集测试过程中创建的订单，测试结束后清理。"""
    created_orders = []
    yield created_orders
    for order_id in created_orders:
        cleanup_test_order(db_conn, order_id)


def pytest_runtest_logreport(report):
    """记录失败用例的详细信息到日志。"""
    if report.outcome != "failed" or getattr(report, "wasxfail", False):
        return
    nodeid = getattr(report, "nodeid", "unknown")
    logger.error(f"用例失败: {nodeid}")
    longrepr = getattr(report, "longreprtext", None)
    if longrepr:
        logger.error(longrepr)
    else:
        logger.error(str(getattr(report, "longrepr", report)))


def pytest_terminal_summary(terminalreporter, exitstatus, pytest_config):
    """发送测试结果汇总通知。"""
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    skipped = len(terminalreporter.stats.get("skipped", []))
    total = passed + failed + skipped

    logger.info(
        f"测试统计: 总数={total}, 通过={passed}, 失败={failed}, 跳过={skipped}"
    )

    sender = NotificationSender(wechat_webhook=config.WECHAT_WEBHOOK)
    content = create_test_report_message(
        passed=passed,
        failed=failed,
        skipped=skipped,
        total=total,
    )

    logger.info("正在发送测试结果通知...")

    results = sender.send_notification(
        content=content,
        title="自动化测试报告",
        notification_types=["wechat"],
    )

    for ntype, success in results.items():
        if success:
            logger.info(f"{ntype} 通知发送成功")
        else:
            logger.error(f"{ntype} 通知发送失败")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(pytest_config):
    """在 pytest 配置阶段写入 Allure 环境信息。"""
    allure_dir = config.ALLURE_RESULTS_DIR
    if not os.path.exists(allure_dir):
        os.makedirs(allure_dir)

    env_properties = os.path.join(allure_dir, "environment.properties")
    for warning in config.validate():
        logger.warning(warning)

    with open(env_properties, "w", encoding="utf-8") as f:
        f.write(f"测试环境={os.getenv('ENV', 'test')}\n")
        f.write(f"API地址={config.get_base_url()}\n")
        f.write(f"数据库={config.DB_CONFIG['host']}:{config.DB_CONFIG['port']}\n")
        f.write(f"Python版本={os.sys.version}\n")
