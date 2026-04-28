import os

import httpx
import pymysql
import pytest

from config import config
from utils.allure_helper import attach_text, step
from utils.db_helper import cleanup_test_order
from utils.logger import logger
from utils.notification import (
    NotificationSender,
    create_test_report_message,
)
from api.handover_api import ensure_handover_open

print("读取到的 BASE_URL:", os.getenv("BASE_URL"))
@pytest.fixture(scope="session")
def client():
    """创建用于测试的 HTTP 客户端"""
    base_url = config.get_base_url()
    with httpx.Client(base_url=base_url, timeout=config.DEFAULT_TIMEOUT) as c:
        attach_text("接口基础地址", base_url)
        yield c


@pytest.fixture(scope="session")
def access_token():
    """创建用于测试的访问令牌"""
    with httpx.Client(timeout=config.DEFAULT_TIMEOUT) as c:
        resp = c.post(
            config.get_base_url() + "/reabam-manage-login/user/login",
            json={
                "mobile": "19977958582",
                "loginType": "checkstand",
                "appType": "pc",
                "appVersion": "1.6.2.1",
                "loginWord": "e10adc3949ba59abbe56e057f20f883e",
                "clientVersion": "25091901",
                "systemVersion": "2512.29.34",
                "companyId": ""
            },
        )
        assert resp.status_code == 200, "获取访问令牌失败"
        return resp.json()["data"].get("tokenId")


@pytest.fixture(scope="session", autouse=True)
def ensure_handover(client, access_token):
    """确保门店已开班（自动执行）

    在测试会话开始时自动检查开交班状态：
    - 如果门店状态为CLOSE（需要交班），自动执行交班和开班
    - 如果门店状态为OPEN（已开班），跳过操作

    使用 autouse=True 使其在所有测试前自动执行
    """
    with step("检查并确保门店已开班"):
        logger.info("=" * 50)
        logger.info("开始检查门店开交班状态")
        logger.info("=" * 50)

        result = ensure_handover_open(client, access_token)

        if result:
            logger.info("门店开班状态检查完成")
            attach_text("开交班状态", "门店已开班，可以正常执行测试")
        else:
            logger.error("门店开班操作失败，测试可能受到影响")
            attach_text("开交班状态警告", "门店开班操作失败，部分接口可能无法使用")

        logger.info("=" * 50)

        yield result

@pytest.fixture(scope="session")
def db_conn():
    """创建用于测试的数据库连接"""
    if os.getenv("ENV") == "uat":
        pytest.skip("生产环境不进行数据库连接")
    conn = pymysql.connect(
        **config.DB_CONFIG,
        cursorclass=pymysql.cursors.DictCursor,
    )
    attach_text(
        "数据库连接信息",
        f"Database: {config.DB_CONFIG['host']}:{config.DB_CONFIG['port']}/{config.DB_CONFIG['database']}",
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

# @pytest.fixture(scope="session")
# def

def pytest_runtest_logreport(report):
    """将失败的测试详情记录到文件日志"""
    if report.outcome != "failed" or getattr(report, "wasxfail", False):
        return
    nodeid = getattr(report, "nodeid", "unknown")
    logger.error(f"用例失败: {nodeid}")
    longrepr = getattr(report, "longreprtext", None)
    if longrepr:
        logger.error(longrepr)
    else:
        logger.error(str(getattr(report, "longrepr", report)))


# def pytest_terminal_summary(terminalreporter):
#     """发送测试汇总通知"""
#     passed = len(terminalreporter.stats.get("passed", []))
#     failed = len(terminalreporter.stats.get("failed", []))
#     skipped = len(terminalreporter.stats.get("skipped", []))
#     xfailed = len(terminalreporter.stats.get("xfailed", []))
#     xpassed = len(terminalreporter.stats.get("xpassed", []))
#     total = passed + failed + skipped + xfailed

#     logger.info(
#         f"测试汇总: 总数={total}, 通过={passed}, 失败={failed}, 跳过={skipped}, 预期失败={xfailed}, 预期通过={xpassed}"
#     )

#     sender = NotificationSender(wechat_webhook=config.WECHAT_WEBHOOK)
#     content = create_test_report_message(
#         passed=passed,
#         failed=failed,
#         skipped=skipped,
#         xfailed=xfailed,
#         xpassed=xpassed,
#         total=total,
#     )

#     logger.info("发送测试结果通知")

#     results = sender.send_notification(
#         content=content,
#         title="自动化测试报告",
#         notification_types=["wechat"],
#     )

#     for ntype, success in results.items():
#         if success:
#             logger.info(f"[成功] {ntype} 通知发送成功")
#         else:
#             logger.error(f"[失败] {ntype} 通知发送失败")


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


if __name__ == '__main__':
    print(access_token())
