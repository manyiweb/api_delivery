import pytest
import httpx

BASE_URL = 'http://localhost:5000'


@pytest.fixture
def client():
    return httpx.Client(base_url=BASE_URL)


@pytest.fixture
def create_order(client):
    create_resp = client.post('/callback', json={
        ''
    })
    assert create_resp.status_code == 201
    return create_resp.json()['order_id']
