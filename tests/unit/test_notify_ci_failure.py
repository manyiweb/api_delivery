import os
import subprocess
import sys

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


def test_notify_script_can_run_from_ci_script_path_without_pythonpath():
    code = """
import os
import runpy
from unittest.mock import patch

os.environ["WECHAT_WEBHOOK"] = "https://example.test/webhook"
with patch("utils.notification.requests.post") as post:
    post.return_value.raise_for_status.return_value = None
    post.return_value.json.return_value = {"errcode": 0}
    module = runpy.run_path("scripts/notify_ci_failure.py", run_name="notify_ci_failure_test")
    exit_code = module["main"]()
    assert exit_code == 0
    assert post.called
"""

    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=os.getcwd(),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "No module named 'utils'" not in result.stderr
