from types import SimpleNamespace

import pytest

from case.test_showdoc_member_smoke import _normalize_loaded_cases, _unavailable_reason

pytestmark = pytest.mark.unit


def test_normalize_loaded_cases_uses_project_style_yaml_sections():
    raw_data = {
        "showdoc_1": {
            "tokenId": "",
            "memberId": "",
            "_meta": {
                "page_id": "1",
                "title": "有效接口",
                "url": "/valid/url",
                "method": "POST",
                "risk_level": "read",
                "response_fields": ["data"],
            },
        }
    }

    assert _normalize_loaded_cases(raw_data) == [
        {
            "case_key": "showdoc_1",
            "page_id": "1",
            "title": "有效接口",
            "url": "/valid/url",
            "method": "POST",
            "risk_level": "read",
            "response_fields": ["data"],
            "request_body": {
                "tokenId": "",
                "memberId": "",
            },
        }
    ]


def test_unavailable_reason_detects_gateway_missing_resource_response():
    response = SimpleNamespace(status_code=404)
    response_json = {
        "error": "No static resource app/Business/member/coupon/list.",
        "status": 404,
    }

    assert _unavailable_reason(response, response_json) == "当前环境网关未映射该接口"


def test_unavailable_reason_detects_missing_service_instance_response():
    response = SimpleNamespace(status_code=503)
    response_json = {
        "error": "Unable to find instance for reabam-b2b",
        "status": 503,
    }

    assert _unavailable_reason(response, response_json) == "当前环境服务实例不可用"


def test_unavailable_reason_ignores_normal_business_response():
    response = SimpleNamespace(status_code=200)
    response_json = {"code": "200", "success": True, "data": {}}

    assert _unavailable_reason(response, response_json) is None
