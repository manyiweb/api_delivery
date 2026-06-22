import os
import subprocess
import sys

import pytest

from scripts.notify_ci_failure import (
    build_allure_artifact_links,
    build_notification_title,
    build_pipeline_message,
    get_pipeline_status,
    read_allure_summary,
)

pytestmark = pytest.mark.unit


def test_pipeline_status_uses_success_message(monkeypatch):
    monkeypatch.setenv("CI_PIPELINE_STATUS", "success")

    assert get_pipeline_status() == ("执行成功", "🟢")


def test_pipeline_status_uses_failure_message(monkeypatch):
    monkeypatch.setenv("CI_PIPELINE_STATUS", "failed")

    assert get_pipeline_status() == ("执行失败", "🔴")


def test_pipeline_message_highlights_test_result_and_real_artifact_links(monkeypatch, tmp_path):
    report_dir = tmp_path / "reports" / "allure-report" / "widgets"
    report_dir.mkdir(parents=True)
    (report_dir / "summary.json").write_text(
        """
        {
          "statistic": {
            "total": 118,
            "passed": 67,
            "failed": 11,
            "broken": 15,
            "skipped": 25
          }
        }
        """,
        encoding="utf-8",
    )

    monkeypatch.setenv("CI_PIPELINE_STATUS", "success")
    monkeypatch.setenv("CI_PROJECT_NAME", "api-auto-test")
    monkeypatch.setenv("CI_PROJECT_URL", "https://gitlab.reabam.com/zhoujiman/api_auto_test")
    monkeypatch.setenv("CI_PIPELINE_ID", "123")
    monkeypatch.setenv("CI_PIPELINE_URL", "https://gitlab.reabam.com/zhoujiman/api_auto_test/pipelines/123")
    monkeypatch.setenv("CI_COMMIT_REF_NAME", "main")
    monkeypatch.setenv("CI_COMMIT_SHORT_SHA", "abc123")
    monkeypatch.setenv("CI_COMMIT_AUTHOR", "张三")
    monkeypatch.delenv("CI_PAGES_URL", raising=False)

    message = build_pipeline_message(project_root=tmp_path)

    assert "测试结果: 存在失败或异常" in message
    assert "总数: 118 | 通过: 67 | 失败: 11 | 异常: 15 | 跳过: 25" in message
    assert "报告在线浏览: https://gitlab.reabam.com/zhoujiman/api_auto_test/-/jobs/artifacts/main/browse/reports/allure-report?job=allure_report" in message
    assert "报告压缩包: https://gitlab.reabam.com/zhoujiman/api_auto_test/-/jobs/artifacts/main/download?job=allure_report" in message
    assert "example.com" not in message
    assert "流水线: #123" in message
    assert "分支: main" in message
    assert "提交: abc123" in message
    assert "作者: 张三" in message


def test_notification_title_uses_test_summary_before_pipeline_status():
    assert build_notification_title(
        {"total": 10, "passed": 10, "failed": 0, "broken": 0, "skipped": 0}
    ) == "🟢 API 自动化测试通过 10/10"
    assert build_notification_title(
        {"total": 10, "passed": 8, "failed": 1, "broken": 1, "skipped": 0}
    ) == "🔴 API 自动化测试异常 失败1 异常1"


def test_read_allure_summary_defaults_to_zero_when_missing(tmp_path):
    assert read_allure_summary(tmp_path) == {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "broken": 0,
        "skipped": 0,
    }


def test_artifact_links_use_gitlab_job_artifacts_not_pages(monkeypatch):
    monkeypatch.setenv("CI_PROJECT_URL", "https://gitlab.reabam.com/zhoujiman/api_auto_test")
    monkeypatch.setenv("CI_COMMIT_REF_NAME", "master")

    links = build_allure_artifact_links()

    assert links["browse"] == "https://gitlab.reabam.com/zhoujiman/api_auto_test/-/jobs/artifacts/master/browse/reports/allure-report?job=allure_report"
    assert links["download"] == "https://gitlab.reabam.com/zhoujiman/api_auto_test/-/jobs/artifacts/master/download?job=allure_report"


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
