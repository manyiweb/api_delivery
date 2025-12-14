import pytest
import httpx

from api.base import BASE_URL


@pytest.fixture(scope="session")
def client():
    """创建 HTTP 客户端，测试结束自动关闭"""
    with httpx.Client(base_url=BASE_URL) as c:
        yield c  # yield 之后的代码会在测试结束后执行
