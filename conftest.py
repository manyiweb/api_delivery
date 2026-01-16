import pymysql
import pytest
import httpx
import allure
import sys
import os

from config import config
from utils.db_helper import cleanup_test_order, get_db_connection

@pytest.fixture(scope="session")
def client():
    """创建 HTTP 客户端，测试结束自动关闭"""
    base_url = config.get_base_url()
    with httpx.Client(base_url=base_url, timeout=config.DEFAULT_TIMEOUT) as c:
        allure.attach(base_url, name="API Base URL", attachment_type=allure.attachment_type.TEXT)
        yield c


@pytest.fixture(scope="session")
def db_conn():
    """创建数据库连接，测试结束自动关闭"""
    conn = pymysql.connect(
        **config.DB_CONFIG,
        cursorclass=pymysql.cursors.DictCursor
    )
    allure.attach(
        f"Database: {config.DB_CONFIG['host']}:{config.DB_CONFIG['port']}/{config.DB_CONFIG['database']}",
        name="数据库连接信息",
        attachment_type=allure.attachment_type.TEXT
    )
    yield conn
    conn.close()

@pytest.fixture(scope="function")
def cleanup_order(db_conn):
    """测试用例级别的订单清理 fixture"""
    created_orders = []
    yield created_orders
    # Teardown: 清理测试数据
    for order_id in created_orders:
        cleanup_test_order(db_conn, order_id)
