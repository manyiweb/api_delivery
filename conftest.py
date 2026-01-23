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
    """创建用于测试的 HTTP 客户端"""
    base_url = config.get_base_url()
    with httpx.Client(base_url=base_url, timeout=config.DEFAULT_TIMEOUT) as c:
        allure.attach(base_url, name="API Base URL", attachment_type=allure.attachment_type.TEXT)
        yield c


@pytest.fixture(scope="session")
def db_conn():
    """创建用于测试的数据库连接"""
    if os.getenv("ENV") == "uat":
        pytest.skip("生产环境不进行数据库连接")
    conn = pymysql.connect(
        **config.DB_CONFIG,
        cursorclass=pymysql.cursors.DictCursor,
    )
    allure.attach(
        f"Database: {config.DB_CONFIG['host']}:{config.DB_CONFIG['port']}/{config.DB_CONFIG['database']}",
        name="Database connection info",
        attachment_type=allure.attachment_type.TEXT,
    )
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def cleanup_order(db_conn):
    """收集已创建的订单用于清理"""
    created_orders = []
    yield created_orders
    for order_id in created_orders:
        cleanup_test_order(db_conn, order_id)


def pytest_runtest_logreport(report):
    """将失败的测试详情记录到文件日志"""
    if report.outcome != "failed" or getattr(report, "wasxfail", False):
        return
    nodeid = getattr(report, "nodeid", "unknown")
    logger.error(f"Test failed: {nodeid}")
    longrepr = getattr(report, "longreprtext", None)
    if longrepr:
        logger.error(longrepr)
    else:
        logger.error(str(getattr(report, "longrepr", report)))


def pytest_terminal_summary(terminalreporter):
    """发送测试汇总通知"""
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    skipped = len(terminalreporter.stats.get("skipped", []))
    xfailed = len(terminalreporter.stats.get("xfailed", []))
    xpassed = len(terminalreporter.stats.get("xpassed", []))
    total = passed + failed + skipped + xfailed

    logger.info(
        f"测试汇总: 总数={total}, 通过={passed}, 失败={failed}, 跳过={skipped}, 预期失败={xfailed}, 预期通过={xpassed}"
    )

    sender = NotificationSender(wechat_webhook=config.WECHAT_WEBHOOK)
    content = create_test_report_message(
        passed=passed,
        failed=failed,
        skipped=skipped,
        xfailed=xfailed,
        xpassed=xpassed,
        total=total,
    )

    logger.info("发送测试结果通知")

    results = sender.send_notification(
        content=content,
        title="Automated test report",
        notification_types=["wechat"],
    )

    for ntype, success in results.items():
        if success:
            logger.info(f"[OK] {ntype} 通知发送成功")
        else:
            logger.error(f"[FAIL] {ntype} notification failed")


@pytest.hookimpl(tryfirst=True)
def pytest_configure():
    """写入 Allure 环境属性"""
    allure_dir = config.ALLURE_RESULTS_DIR
    if not os.path.exists(allure_dir):
        os.makedirs(allure_dir)

    env_properties = os.path.join(allure_dir, "environment.properties")
    for warning in config.validate():
        logger.warning(warning)

    with open(env_properties, "w", encoding="utf-8") as f:
        f.write(f"ENV={os.getenv('ENV', 'test')}\n")
        f.write(f"API_BASE_URL={config.get_base_url()}\n")
        f.write(f"DB_HOST={config.DB_CONFIG['host']}\n")
        f.write(f"DB_PORT={config.DB_CONFIG['port']}\n")
        f.write(f"PYTHON_VERSION={os.sys.version}\n")
