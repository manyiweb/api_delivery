import json
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from utils.logger import logger

DEFAULT_HTTP_TIMEOUT = 10
DEFAULT_SMTP_TIMEOUT = 10


class NotificationSender:
    """Send notifications via WeChat Work, email, and DingTalk."""

    def __init__(self, wechat_webhook=None, smtp_config=None, dingtalk_webhook=None):
        self.wechat_webhook = wechat_webhook
        print("NotificationSender initialized""生产地址", self.wechat_webhook)
        self.smtp_config = smtp_config
        self.dingtalk_webhook = dingtalk_webhook

    def send_notification(self, content, title="Notification", notification_types=None):
        """Send notifications via configured channels."""
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

    def send_wechat_work_message(self, content, title="Notification"):
        """Send a WeChat Work message."""
        if not self.wechat_webhook:
            logger.error("WeChat webhook not configured")
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
                logger.info("WeChat message sent")
                return True

            logger.error(f"WeChat message failed: {result.get('errmsg')}")
            return False

        except requests.exceptions.RequestException as e:
            logger.error(f"WeChat message error: {e}")
            return False

    def send_email(self, content, subject="Notification"):
        """Send an email message."""
        if not self.smtp_config or not self.smtp_config.get("to_emails"):
            logger.error("SMTP config or recipients missing")
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

            logger.info("Email sent")
            return True

        except Exception as e:
            logger.error(f"Email send error: {e}")
            return False

    def send_dingtalk_message(self, content, title="Notification"):
        """Send a DingTalk message."""
        if not self.dingtalk_webhook:
            logger.error("DingTalk webhook not configured")
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
                logger.info("DingTalk message sent")
                return True

            logger.error(f"DingTalk message failed: {result.get('errmsg')}")
            return False

        except requests.exceptions.RequestException as e:
            logger.error(f"DingTalk message error: {e}")
            return False


def get_current_time():
    """Return current time string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_test_report_message(passed=0, failed=0, skipped=0, total=0, xfailed=0):
    """Create a test report message."""
    status_text = "ALL PASSED" if failed == 0 and passed > 0 else "FAILURES PRESENT"
    content = f"""
[自动化测试报告]
总数: {total}
通过: {passed}
错误: {failed}
跳过: {skipped}
预错误: {xfailed}


状态: {status_text}
时间: {get_current_time()}
    """.strip()
    return content


if __name__ == '__main__':
    NotificationSender = NotificationSender()
