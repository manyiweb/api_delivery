"""GitLab CI 企业微信通知脚本

在 .gitlab-ci.yml 的 notify stage 中调用，在 pipeline 结束后执行。
读取 GitLab 预置环境变量，构造结果通知消息并发送到企业微信 webhook。
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.logger import logger
from utils.notification import NotificationSender


def get_env(name: str, default: str = "未知") -> str:
    """读取环境变量，缺失时返回默认值。"""
    return os.getenv(name, default).strip()


def get_pipeline_status() -> tuple[str, str]:
    """返回流水线状态文案和标题图标。"""
    status = (
        os.getenv("CI_PIPELINE_STATUS")
        or os.getenv("CI_JOB_STATUS")
        or ""
    ).strip().lower()

    status_map = {
        "success": ("执行成功", "🟢"),
        "failed": ("执行失败", "🔴"),
        "canceled": ("已取消", "🟡"),
        "cancelled": ("已取消", "🟡"),
        "skipped": ("已跳过", "🟡"),
        "manual": ("等待手动处理", "🟡"),
    }
    return status_map.get(status, ("已结束", "🔵"))


def _zero_summary() -> dict[str, int]:
    return {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "broken": 0,
        "skipped": 0,
    }


def read_allure_summary(project_root: Path = PROJECT_ROOT) -> dict[str, int]:
    """读取 Allure summary.json，返回用例统计。"""
    summary_file = project_root / "reports" / "allure-report" / "widgets" / "summary.json"
    if not summary_file.exists():
        return _zero_summary()

    try:
        summary_json = json.loads(summary_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.warning("读取 Allure summary.json 失败: %s", summary_file)
        return _zero_summary()

    statistic = summary_json.get("statistic") or {}
    result = _zero_summary()
    for key in result:
        try:
            result[key] = int(statistic.get(key) or 0)
        except (TypeError, ValueError):
            result[key] = 0
    return result


def has_test_errors(summary: dict[str, int]) -> bool:
    return summary.get("failed", 0) > 0 or summary.get("broken", 0) > 0


def build_test_result_text(summary: dict[str, int]) -> str:
    if summary.get("total", 0) <= 0:
        return "未读取到测试结果"
    if has_test_errors(summary):
        return "存在失败或异常"
    return "全部通过"


def build_notification_title(summary: dict[str, int]) -> str:
    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    broken = summary.get("broken", 0)

    if total <= 0:
        status_text, icon = get_pipeline_status()
        return f"{icon} API 自动化测试{status_text}"
    if failed or broken:
        return f"🔴 API 自动化测试异常 失败{failed} 异常{broken}"
    return f"🟢 API 自动化测试通过 {passed}/{total}"


def build_allure_artifact_links() -> dict[str, str]:
    """生成 GitLab artifact 链接，替代未启用 Pages 时的无效 CI_PAGES_URL。"""
    project_url = get_env("CI_PROJECT_URL", "")
    ref_name = quote(get_env("CI_COMMIT_REF_NAME", "master"), safe="")

    if not project_url:
        return {"browse": "", "download": ""}

    base = f"{project_url}/-/jobs/artifacts/{ref_name}"
    return {
        "browse": f"{base}/browse/reports/allure-report?job=allure_report",
        "download": f"{base}/download?job=allure_report",
    }


def build_pipeline_message(project_root: Path = PROJECT_ROOT) -> str:
    """构造企业微信流水线结果通知文本。"""
    project_name = get_env("CI_PROJECT_NAME", "api-auto-test")
    project_url = get_env("CI_PROJECT_URL", "")
    pipeline_id = get_env("CI_PIPELINE_ID", "")
    pipeline_url = get_env("CI_PIPELINE_URL", "")
    branch = get_env("CI_COMMIT_REF_NAME", "")
    commit_sha = get_env("CI_COMMIT_SHORT_SHA", "")
    commit_author = get_env("CI_COMMIT_AUTHOR", "")
    status_text, _ = get_pipeline_status()
    summary = read_allure_summary(project_root)
    links = build_allure_artifact_links()

    browse_line = (
        f"报告在线浏览: {links['browse']}"
        if links["browse"]
        else "报告在线浏览: 请在 pipeline 的 allure_report job artifacts 中查看"
    )
    download_line = (
        f"报告压缩包: {links['download']}"
        if links["download"]
        else "报告压缩包: 请在 pipeline 的 allure_report job artifacts 中下载"
    )

    content = f"""[API自动化测试] 测试结果: {build_test_result_text(summary)}

总数: {summary['total']} | 通过: {summary['passed']} | 失败: {summary['failed']} | 异常: {summary['broken']} | 跳过: {summary['skipped']}
流水线状态: {status_text}

项目: {project_name}
流水线: #{pipeline_id}
分支: {branch}
提交: {commit_sha}
作者: {commit_author}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{browse_line}
{download_line}
流水线详情: {pipeline_url}
项目主页: {project_url}
"""
    return content


def main() -> int:
    webhook = os.getenv("WECHAT_WEBHOOK", "").strip()
    if not webhook:
        logger.error("未配置 WECHAT_WEBHOOK，无法发送流水线通知")
        return 1

    sender = NotificationSender(wechat_webhook=webhook)
    summary = read_allure_summary()
    content = build_pipeline_message()
    title = build_notification_title(summary)

    results = sender.send_notification(content=content, title=title, notification_types=["wechat"])
    if results.get("wechat"):
        logger.info("企业微信流水线通知发送成功")
        return 0

    logger.error("企业微信流水线通知发送失败")
    return 1


if __name__ == "__main__":
    sys.exit(main())
