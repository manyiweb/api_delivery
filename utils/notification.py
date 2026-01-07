import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from utils.logger import logger


class NotificationSender:
    """通用通知发送器，支持企业微信、邮件和钉钉"""

    def __init__(self, wechat_webhook=None, smtp_config=None, dingtalk_webhook=None):
        """
        初始化通知发送器
        :param wechat_webhook: 企业微信webhook地址
        :param smtp_config: 邮件SMTP配置 {'server': 'smtp.server.com', 'port': 587, 'username': 'user', 'password': 'pwd', 'to_emails': ['to@domain.com']}
        :param dingtalk_webhook: 钉钉webhook地址
        """
        self.wechat_webhook = wechat_webhook
        self.smtp_config = smtp_config
        self.dingtalk_webhook = dingtalk_webhook

    def send_notification(self, content, title="通知", notification_types=['wechat']):
        """
        发送通知
        :param content: 通知内容
        :param title: 通知标题
        :param notification_types: 通知类型列表，可选 'wechat', 'email', 'dingtalk'
        :return: 发送结果字典
        """
        results = {}

        for ntype in notification_types:
            if ntype == 'wechat':
                results['wechat'] = self.send_wechat_work_message(content, title)
            elif ntype == 'email':
                results['email'] = self.send_email(content, title)
            elif ntype == 'dingtalk':
                results['dingtalk'] = self.send_dingtalk_message(content, title)

        return results

    def send_wechat_work_message(self, content, title="通知"):
        """
        发送企业微信消息
        :param content: 消息内容
        :param title: 消息标题
        """
        if not self.wechat_webhook:
            logger.error("❌ 未配置企业微信webhook地址")
            return False

        headers = {
            'Content-Type': 'application/json'
        }

        full_content = f"{title}\n{content}"

        payload = {
            "msgtype": "text",
            "text": {
                "content": full_content
            }
        }

        try:
            response = requests.post(self.wechat_webhook, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()

            if result.get('errcode') == 0:
                logger.info("✅ 企业微信消息发送成功")
                return True
            else:
                logger.error(f"❌ 企业微信消息发送失败: {result.get('errmsg')}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 发送企业微信消息时发生错误: {e}")
            return False

    def send_email(self, content, subject="通知"):
        """
        发送邮件
        :param content: 邮件内容
        :param subject: 邮件主题
        """
        if not self.smtp_config or not self.smtp_config.get('to_emails'):
            logger.error("❌ 未配置SMTP或收件人邮箱")
            return False

        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = ', '.join(self.smtp_config['to_emails'])
            msg['Subject'] = subject

            # 添加邮件正文
            msg.attach(MIMEText(content, 'plain', 'utf-8'))

            # 连接SMTP服务器并发送邮件
            server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])

            text = msg.as_string()
            server.sendmail(self.smtp_config['username'], self.smtp_config['to_emails'], text)
            server.quit()

            logger.info("✅ 邮件发送成功")
            return True

        except Exception as e:
            logger.error(f"❌ 发送邮件时发生错误: {e}")
            return False

    def send_dingtalk_message(self, content, title="通知"):
        """
        发送钉钉消息
        :param content: 消息内容
        :param title: 消息标题
        """
        if not self.dingtalk_webhook:
            logger.error("❌ 未配置钉钉webhook地址")
            return False

        headers = {
            'Content-Type': 'application/json'
        }

        full_content = f"{title}\n{content}"

        payload = {
            "msgtype": "text",
            "text": {
                "content": full_content
            }
        }

        try:
            response = requests.post(self.dingtalk_webhook, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()

            if result.get('errcode') == 0:
                logger.info("✅ 钉钉消息发送成功")
                return True
            else:
                logger.error(f"❌ 钉钉消息发送失败: {result.get('errmsg')}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 发送钉钉消息时发生错误: {e}")
            return False


def get_current_time():
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_test_report_message(passed=0, failed=0, skipped=0, total=0):
    """创建测试报告消息"""
    status_text = '✅ 全部通过' if failed == 0 and passed > 0 else '❌ 存在失败'

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