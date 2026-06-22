from types import SimpleNamespace

import pytest

from case.test_showdoc_member_smoke import (
    _allure_display_title,
    _allure_feature,
    _allure_story,
    _case_id,
    _normalize_loaded_cases,
    _set_allure_case_metadata,
    _unavailable_reason,
)

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


def test_showdoc_case_allure_display_matches_business_case_style():
    case = {
        "page_id": "3092",
        "title": "优惠券列表",
        "catalog_path": ["会员", "优惠券"],
        "method": "POST",
        "url": "/app/Business/member/coupon/list",
    }

    assert _case_id(case) == "3092 优惠券列表"
    assert _allure_display_title(case) == "3092 优惠券列表"
    assert _allure_feature(case) == "店务助手_智慧收银台/会员"
    assert _allure_story(case) == "优惠券"


def test_showdoc_case_allure_display_falls_back_to_url_when_title_missing():
    case = {
        "page_id": "unknown",
        "catalog_path": ["会员"],
        "method": "GET",
        "url": "/member/profile",
    }

    assert _case_id(case) == "unknown /member/profile"
    assert _allure_display_title(case) == "unknown /member/profile"
    assert _allure_feature(case) == "店务助手_智慧收银台/会员"
    assert _allure_story(case) == "会员接口探活"


def test_showdoc_case_allure_metadata_hides_raw_case_parameter(monkeypatch):
    calls = []

    monkeypatch.setattr(
        "case.test_showdoc_member_smoke.allure.dynamic.title",
        lambda value: calls.append(("title", value)),
    )
    monkeypatch.setattr(
        "case.test_showdoc_member_smoke.allure.dynamic.feature",
        lambda value: calls.append(("feature", value)),
    )
    monkeypatch.setattr(
        "case.test_showdoc_member_smoke.allure.dynamic.story",
        lambda value: calls.append(("story", value)),
    )
    monkeypatch.setattr(
        "case.test_showdoc_member_smoke.allure.dynamic.parameter",
        lambda name, value, **kwargs: calls.append(("parameter", name, value, kwargs)),
    )

    _set_allure_case_metadata(
        {
            "page_id": "3092",
            "title": "优惠券列表",
            "catalog_path": ["会员", "优惠券"],
            "method": "POST",
            "url": "/app/Business/member/coupon/list",
        }
    )

    assert ("title", "3092 优惠券列表") in calls
    assert ("feature", "店务助手_智慧收银台/会员") in calls
    assert ("story", "优惠券") in calls
    assert calls[3][:3] == ("parameter", "case", "3092 优惠券列表")
    assert calls[3][3]["mode"].name == "HIDDEN"
    assert ("parameter", "page_id", "3092", {}) in calls
    assert ("parameter", "method", "POST", {}) in calls
    assert ("parameter", "url", "/app/Business/member/coupon/list", {}) in calls


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
