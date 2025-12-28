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
        host='你的DB_HOST',
        port=3306,
        user='你的DB_USER',
        password='你的DB_PASSWORD',
        database='你的DB_NAME',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    yield conn
    conn.close()