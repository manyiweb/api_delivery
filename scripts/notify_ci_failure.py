"""GitLab CI 失败通知脚本

在 .gitlab-ci.yml 的 notify stage 中调用，仅在 pipeline 失败时执行。
读取 GitLab 预置环境变量，构造失败通知消息并发送到企业微信 webhook。
"""
import os
import sys
from datetime import datetime

from utils.logger import logger
from utils.notification import NotificationSender


def get_env(name: str, default: str = "未知") -> str:
    """读取环境变量，缺失时返回默认值。"""
    return os.getenv(name, default).strip()


def build_failure_message() -> str:
    """构造企业微信失败通知文本。"""
    project_name = get_env("CI_PROJECT_NAME", "api-auto-test")
    project_url = get_env("CI_PROJECT_URL", "")
    pipeline_id = get_env("CI_PIPELINE_ID", "")
    pipeline_url = get_env("CI_PIPELINE_URL", "")
    branch = get_env("CI_COMMIT_REF_NAME", "")
    commit_sha = get_env("CI_COMMIT_SHORT_SHA", "")
    commit_author = get_env("CI_COMMIT_AUTHOR", "")
    commit_msg = get_env("CI_COMMIT_MESSAGE", "")
    pages_url = get_env("CI_PAGES_URL", "")

    # 如果 CI_PAGES_URL 未设置，尝试按常见格式拼一个备用地址
    if not pages_url:
        project_path = get_env("CI_PROJECT_PATH", "")
        if project_path:
            pages_url = f"https://{project_path.split('/')[0]}.gitlab.io/{project_path.split('/')[-1]}"

    report_line = f"Allure报告: {pages_url}" if pages_url else "Allure报告: 请查看 pipeline artifacts"

    content = f"""[API自动化测试] 流水线执行失败

项目: {project_name}
分支: {branch}
提交: {commit_sha}
作者: {commit_author}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{report_line}
流水线详情: {pipeline_url}
项目主页: {project_url}
"""
    return content


def main() -> int:
    webhook = os.getenv("WECHAT_WEBHOOK", "").strip()
    if not webhook:
        logger.error("未配置 WECHAT_WEBHOOK，无法发送失败通知")
        return 1

    sender = NotificationSender(wechat_webhook=webhook)
    content = build_failure_message()
    title = "🔴 API 自动化测试流水线失败"

    results = sender.send_notification(content=content, title=title, notification_types=["wechat"])
    if results.get("wechat"):
        logger.info("企业微信失败通知发送成功")
        return 0

    logger.error("企业微信失败通知发送失败")
    return 1


if __name__ == "__main__":
    sys.exit(main())
