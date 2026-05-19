import importlib
import json

import pytest

pytestmark = pytest.mark.unit


def _reload_helper(monkeypatch, *, attach_level=None, max_chars=None):
    if attach_level is None:
        monkeypatch.delenv("ALLURE_ATTACH_LEVEL", raising=False)
    else:
        monkeypatch.setenv("ALLURE_ATTACH_LEVEL", attach_level)

    if max_chars is None:
        monkeypatch.delenv("ALLURE_MAX_ATTACHMENT_CHARS", raising=False)
    else:
        monkeypatch.setenv("ALLURE_MAX_ATTACHMENT_CHARS", str(max_chars))

    import utils.allure_helper as allure_helper

    return importlib.reload(allure_helper)


def test_attach_json_defaults_to_redacted_summary(monkeypatch):
    helper = _reload_helper(monkeypatch)
    attachments = []

    monkeypatch.setattr(
        helper.allure,
        "attach",
        lambda body, name, attachment_type: attachments.append(
            (body, name, attachment_type)
        ),
    )

    helper.attach_json(
        "响应内容",
        {
            "code": "200",
            "success": True,
            "tokenId": "secret-token",
            "sign": "secret-sign",
            "nested": {
                "password": "secret-password",
                "items": [{"id": 1}, {"id": 2}, {"id": 3}],
            },
        },
    )

    body, name, attachment_type = attachments[0]
    payload = json.loads(body)

    assert name == "响应内容"
    assert attachment_type == helper.allure.attachment_type.JSON
    assert payload["code"] == "200"
    assert payload["success"] is True
    assert payload["tokenId"] == "***"
    assert payload["sign"] == "***"
    assert payload["nested"]["password"] == "***"
    assert payload["nested"]["items"] == ["<list len=3>"]


def test_attach_json_full_mode_keeps_full_redacted_payload(monkeypatch):
    helper = _reload_helper(monkeypatch, attach_level="full")
    attachments = []
    monkeypatch.setattr(
        helper.allure,
        "attach",
        lambda body, name, attachment_type: attachments.append(body),
    )

    helper.attach_json(
        "完整响应",
        {"data": {"items": [{"id": 1}, {"id": 2}]}, "Authorization": "Bearer abc"},
    )

    payload = json.loads(attachments[0])
    assert payload["data"]["items"] == [{"id": 1}, {"id": 2}]
    assert payload["Authorization"] == "***"


def test_attach_json_off_mode_skips_attachment(monkeypatch):
    helper = _reload_helper(monkeypatch, attach_level="off")
    monkeypatch.setattr(
        helper.allure,
        "attach",
        lambda body, name, attachment_type: (_ for _ in ()).throw(
            AssertionError("allure.attach should not be called")
        ),
    )

    helper.attach_json("不会写入", {"code": "200"})


def test_attach_text_truncates_long_values(monkeypatch):
    helper = _reload_helper(monkeypatch, max_chars=12)
    attachments = []
    monkeypatch.setattr(
        helper.allure,
        "attach",
        lambda body, name, attachment_type: attachments.append(body),
    )

    helper.attach_text("长文本", "abcdefghijklmnop")

    assert attachments == ["abcdefghijkl...<truncated>"]
