import pytest

from scripts.notify_ci_failure import build_pipeline_message, get_pipeline_status

pytestmark = pytest.mark.unit


def test_pipeline_status_uses_success_message(monkeypatch):
    monkeypatch.setenv("CI_PIPELINE_STATUS", "success")

    assert get_pipeline_status() == ("执行成功", "🟢")


def test_pipeline_status_uses_failure_message(monkeypatch):
    monkeypatch.setenv("CI_PIPELINE_STATUS", "failed")

    assert get_pipeline_status() == ("执行失败", "🔴")


def test_pipeline_message_describes_current_status(monkeypatch):
    monkeypatch.setenv("CI_PIPELINE_STATUS", "success")
    monkeypatch.setenv("CI_PROJECT_NAME", "api-auto-test")
    monkeypatch.setenv("CI_PIPELINE_ID", "123")
    monkeypatch.setenv("CI_COMMIT_REF_NAME", "main")
    monkeypatch.setenv("CI_COMMIT_SHORT_SHA", "abc123")
    monkeypatch.setenv("CI_COMMIT_AUTHOR", "张三")

    message = build_pipeline_message()

    assert "[API自动化测试] 流水线执行成功" in message
    assert "流水线: #123" in message
    assert "分支: main" in message
    assert "提交: abc123" in message
    assert "作者: 张三" in message
