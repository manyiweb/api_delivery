from copy import deepcopy
import os
from pathlib import Path
from typing import Any, Optional

import allure
import pytest
import yaml

from utils.allure_helper import attach_json, attach_text, step
from utils.logger import logger


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "showdoc_member_smoke_cases.yaml"
COMMON_RESPONSE_FIELDS = {"code", "msg", "data", "success"}


def _load_cases() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return _normalize_loaded_cases(yaml.safe_load(file) or {})


def _normalize_loaded_cases(raw_data: Any) -> list[dict[str, Any]]:
    """将项目风格 YAML 配置段转换为测试执行结构。"""
    if isinstance(raw_data, list):
        return raw_data

    if not isinstance(raw_data, dict):
        return []

    cases: list[dict[str, Any]] = []
    for case_key, section in raw_data.items():
        if not isinstance(section, dict):
            continue

        meta = section.get("_meta", {})
        if not isinstance(meta, dict):
            meta = {}

        request_body = {
            key: value
            for key, value in section.items()
            if key != "_meta"
        }
        case = dict(meta)
        case["case_key"] = str(case_key)
        case["request_body"] = request_body
        cases.append(case)

    return cases


def _case_parameters():
    for case in _load_cases():
        if case.get("risk_level") == "mutation" and os.getenv("RUN_SHOWDOC_MUTATION_SMOKE") != "1":
            yield pytest.param(
                case,
                marks=pytest.mark.skip(reason="写操作接口默认跳过；如需执行，请设置 RUN_SHOWDOC_MUTATION_SMOKE=1"),
            )
        else:
            yield case


def _case_id(case: dict[str, Any]) -> str:
    page_id = case.get("page_id") or "unknown"
    title = case.get("title") or case.get("url") or "未命名接口"
    return f"{page_id}-{title}"


def _inject_runtime_values(payload: Any, token_id: str) -> Any:
    if isinstance(payload, dict):
        result = {}
        for key, value in payload.items():
            if key == "tokenId":
                result[key] = token_id
            else:
                result[key] = _inject_runtime_values(value, token_id)
        return result

    if isinstance(payload, list):
        return [_inject_runtime_values(item, token_id) for item in payload]

    return payload


def _assert_json_contract(response_json: dict[str, Any], case: dict[str, Any]) -> None:
    documented_fields = set(case.get("response_fields") or [])
    accepted_fields = documented_fields | COMMON_RESPONSE_FIELDS
    matched_fields = accepted_fields & set(response_json.keys())
    assert matched_fields, (
        f"响应缺少文档声明字段或常见业务字段，"
        f"期望字段={sorted(accepted_fields)}，实际字段={sorted(response_json.keys())}"
    )


def _unavailable_reason(response, response_json: dict[str, Any]) -> Optional[str]:
    """返回当前环境不可达的可跳过原因。"""
    error = str(response_json.get("error", ""))
    if response.status_code == 404 and "No static resource" in error:
        return "当前环境网关未映射该接口"
    if response.status_code == 503 and "Unable to find instance" in error:
        return "当前环境服务实例不可用"
    return None


@allure.epic("ShowDoc 接口冒烟")
@allure.feature("店务助手_智慧收银台/会员")
class TestShowDocMemberSmoke:
    @pytest.mark.smoke
    @pytest.mark.parametrize("case", _case_parameters(), ids=_case_id)
    @allure.story("会员接口探活")
    def test_member_showdoc_api_smoke(self, client, access_token, case):
        method = str(case.get("method", "POST")).upper()
        url = str(case["url"])
        payload = _inject_runtime_values(deepcopy(case.get("request_body", {})), access_token)

        with step("发送 ShowDoc 冒烟请求"):
            attach_text("接口标题", case.get("title"))
            attach_text("接口地址", url)
            attach_text("请求方法", method)
            attach_json("请求参数", payload)
            logger.info("执行 ShowDoc 冒烟接口: %s %s", method, url)

            if method == "GET":
                response = client.get(url, params=payload if isinstance(payload, dict) else None)
            else:
                response = client.request(method, url, json=payload)

        with step("校验 HTTP 响应"):
            attach_text("响应状态码", response.status_code)
            try:
                response_json = response.json()
            except ValueError:
                response_json = {}
            unavailable_reason = _unavailable_reason(response, response_json)
            if unavailable_reason:
                pytest.skip(unavailable_reason)
            assert response.status_code < 500, (
                f"接口返回服务端错误，status={response.status_code}, body={response.text}"
            )

        with step("校验 JSON 契约"):
            try:
                response_json = response.json()
            except ValueError as exc:
                raise AssertionError(f"响应不是合法 JSON: {response.text}") from exc
            attach_json("响应内容", response_json)
            unavailable_reason = _unavailable_reason(response, response_json)
            if unavailable_reason:
                pytest.skip(unavailable_reason)
            assert isinstance(response_json, dict), f"响应 JSON 不是对象: {response_json}"
            _assert_json_contract(response_json, case)
