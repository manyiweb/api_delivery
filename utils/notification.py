import json
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List, Optional

import requests

from utils.logger import logger

DEFAULT_HTTP_TIMEOUT = 10
DEFAULT_SMTP_TIMEOUT = 10


class NotificationSender:
    """通用通知发送器，支持企业微信、邮件和钉钉。"""

    def __init__(
        self,
        wechat_webhook: Optional[str] = None,
        smtp_config: Optional[Dict[str, any]] = None,
        dingtalk_webhook: Optional[str] = None,
    ):
        self.wechat_webhook = wechat_webhook
        self.smtp_config = smtp_config
        self.dingtalk_webhook = dingtalk_webhook

    def send_notification(
        self,
        content: str,
        title: str = "通知",
        notification_types: Optional[List[str]] = None,
    ) -> Dict[str, bool]:
        """发送通知。"""
        if notification_types is None:
            notification_types = ["wechat"]

        results = {}
        for ntype in notification_types:
            if ntype == "wechat":
                results["wechat"] = self.send_wechat_work_message(content, title)
            elif ntype == "email":
                results["email"] = self.send_email(content, title)
            elif ntype == "dingtalk":
                results["dingtalk"] = self.send_dingtalk_message(content, title)
        return results

    def send_wechat_work_message(self, content: str, title: str = "通知") -> bool:
        """发送企业微信消息。"""
        if not self.wechat_webhook:
            logger.error("未配置企业微信 webhook 地址")
            return False

        headers = {"Content-Type": "application/json"}
        full_content = f"{title}\n{content}"
        payload = {"msgtype": "text", "text": {"content": full_content}}

        try:
            response = requests.post(
                self.wechat_webhook,
                headers=headers,
                data=json.dumps(payload),
                timeout=DEFAULT_HTTP_TIMEOUT,
            )
            response.raise_for_status()
            result = response.json()

            if result.get("errcode") == 0:
                logger.info("企业微信消息发送成功")
                return True

            logger.error(f"企业微信消息发送失败: {result.get('errmsg')}")
            return False

        except requests.exceptions.RequestException as e:
            logger.error(f"发送企业微信消息时发生错误: {e}")
            return False

    def send_email(self, content: str, subject: str = "通知") -> bool:
        """发送邮件通知。"""
        if not self.smtp_config or not self.smtp_config.get("to_emails"):
            logger.error("未配置 SMTP 或收件人邮箱")
            return False

        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_config["username"]
            msg["To"] = ", ".join(self.smtp_config["to_emails"])
            msg["Subject"] = subject
            msg.attach(MIMEText(content, "plain", "utf-8"))

            server = smtplib.SMTP(
                self.smtp_config["server"],
                self.smtp_config["port"],
                timeout=DEFAULT_SMTP_TIMEOUT,
            )
            server.starttls()
            server.login(self.smtp_config["username"], self.smtp_config["password"])

            text = msg.as_string()
            server.sendmail(self.smtp_config["username"], self.smtp_config["to_emails"], text)
            server.quit()

            logger.info("邮件发送成功")
            return True

        except Exception as e:
            logger.error(f"发送邮件时发生错误: {e}")
            return False

    def send_dingtalk_message(self, content: str, title: str = "通知") -> bool:
        """发送钉钉消息。"""
        if not self.dingtalk_webhook:
            logger.error("未配置钉钉 webhook 地址")
            return False

        headers = {"Content-Type": "application/json"}
        full_content = f"{title}\n{content}"
        payload = {"msgtype": "text", "text": {"content": full_content}}

        try:
            response = requests.post(
                self.dingtalk_webhook,
                headers=headers,
                data=json.dumps(payload),
                timeout=DEFAULT_HTTP_TIMEOUT,
            )
            response.raise_for_status()
            result = response.json()

            if result.get("errcode") == 0:
                logger.info("钉钉消息发送成功")
                return True

            logger.error(f"钉钉消息发送失败: {result.get('errmsg')}")
            return False

        except requests.exceptions.RequestException as e:
            logger.error(f"发送钉钉消息时发生错误: {e}")
            return False


def get_current_time() -> str:
    """获取当前时间字符串。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_test_report_message(passed: int = 0, failed: int = 0, skipped: int = 0, total: int = 0) -> str:
    """创建测试报告消息。"""
    status_text = "全部通过" if failed == 0 and passed > 0 else "存在失败"
    content = f"""
【自动化测试报告】
总测试数: {total}
通过: {passed}
失败: {failed}
跳过: {skipped}

状态: {status_text}
执行时间: {get_current_time()}
    """.strip()
    return content
