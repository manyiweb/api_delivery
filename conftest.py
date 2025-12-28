import pymysql
import pytest
import httpx
import allure

from api.base import BASE_URL

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