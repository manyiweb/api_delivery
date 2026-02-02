"""用于测试和 API 客户端的配置模块"""
import os
from typing import Any, Dict, List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    """全局配置"""

    # 接口设置
    BASE_URL = os.getenv("BASE_URL")
    UAT_URL = os.getenv("UAT_URL")

    # 数据库设置
    DB_CONFIG: Dict[str, Any] = {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "charset": "utf8mb4",
    }

    # 通知设置
    WECHAT_WEBHOOK = os.getenv(
        "WECHAT_WEBHOOK"
    )
    print("WECHAT_WEBHOOK", WECHAT_WEBHOOK)

    # 业务设置
    DEVELOPER_ID = os.getenv("DEVELOPER_ID")
    E_POI_ID = os.getenv("E_POI_ID")
    SIGN = os.getenv("SIGN")

    # 测试设置
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT"))
    RETRY_TIMES = int(os.getenv("RETRY_TIMES"))
    RETRY_INTERVAL = int(os.getenv("RETRY_INTERVAL"))

    # 日志设置
    LOG_LEVEL = os.getenv("LOG_LEVEL")
    LOG_DIR = os.getenv("LOG_DIR")

    # 测试报告设置
    ALLURE_RESULTS_DIR = "reports/allure-results"
    ALLURE_REPORT_DIR = "reports/allure-report"

    @classmethod
    def get_base_url(cls) -> str:
        """根据 ENV 返回基础 URL"""
        env = os.getenv("ENV")
        return cls.UAT_URL if env == "uat" else cls.BASE_URL

    @classmethod
    def get_final_payload_params(cls) -> Dict[str, str]:
        """返回请求通用的参数"""
        print(os.getenv("ENV"))
        if os.getenv("ENV") == "uat":
            return {
                'developerId': os.getenv('DEVELOPER_ID_UAT'),
                'ePoiId': os.getenv('E_POI_ID_UAT'),
                'sign': os.getenv('SIGN_UAT')
            }

        return {
            'developerId': cls.DEVELOPER_ID,
            'ePoiId': cls.E_POI_ID,
            'sign': cls.SIGN
        }

    @classmethod
    def validate(cls) -> List[str]:
        """返回缺失环境变量的配置警告"""
        warnings: List[str] = []

        if not os.getenv("DB_PASSWORD"):
            warnings.append("未设置 DB_PASSWORD；请在环境变量或 .env 中配置")
        if not os.getenv("WECHAT_WEBHOOK"):
            warnings.append("未设置 WECHAT_WEBHOOK；通知将被禁用")
        if not os.getenv("SIGN"):
            warnings.append("未设置 SIGN；请在环境变量或 .env 中配置")
        if not os.getenv("DEVELOPER_ID"):
            warnings.append("未设置 DEVELOPER_ID；请在环境变量或 .env 中配置")
        if not os.getenv("E_POI_ID"):
            warnings.append("未设置 E_POI_ID；请在环境变量或 .env 中配置")

        return warnings


config = Config()

if __name__ == '__main__':
    print(f"加载前: {os.getenv('ENV')}")
    # 如需加载 .env，可调用 load_dotenv()
    print(f"加载后: {os.getenv('ENV')}")
    print("生产地址", config.get_base_url())
    print(config.get_final_payload_params())
