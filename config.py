"""配置管理模块
集中管理所有配置项，支持环境变量覆盖。
"""
import os
from typing import Any, Dict, List


class Config:
    """全局配置类。"""

    # API 配置
    BASE_URL = os.getenv("BASE_URL", "http://fat-pos.reabam.com:60030/api")
    UAT_URL = os.getenv("UAT_URL", "https://pos.reabam.com:60030/api")

    # 数据库配置
    DB_CONFIG: Dict[str, Any] = {
        "host": os.getenv("DB_HOST", "192.168.1.151"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "zhoujiman@mop#mop"),
        "password": os.getenv("DB_PASSWORD", "reabam123@mop"),
        "database": os.getenv("DB_NAME", "rb_ts_core"),
        "charset": "utf8mb4",
    }

    # 通知配置
    WECHAT_WEBHOOK = os.getenv(
        "WECHAT_WEBHOOK",
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b97e1f07-9f2c-45b9-a2bc-999b744c2ca4",
    )

    # 业务配置
    DEVELOPER_ID = os.getenv("DEVELOPER_ID", "106825")
    E_POI_ID = os.getenv("E_POI_ID", "reabamts_5ad586a8721e49518998aedef9fd3b5c")
    SIGN = os.getenv("SIGN", "146bcdd348c4f7e90895af13faa123e201fe2686")

    # 测试配置
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    RETRY_TIMES = int(os.getenv("RETRY_TIMES", "3"))
    RETRY_INTERVAL = int(os.getenv("RETRY_INTERVAL", "2"))

    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "logs")

    # Allure 报告配置
    ALLURE_RESULTS_DIR = "reports/allure-results"
    ALLURE_REPORT_DIR = "reports/allure-report"

    @classmethod
    def get_base_url(cls) -> str:
        """根据 ENV 获取基础 URL。"""
        env = os.getenv("ENV", "test")
        return cls.UAT_URL if env == "uat" else cls.BASE_URL

    @classmethod
    def get_final_payload_params(cls) -> Dict[str, str]:
        """获取通用的请求参数。"""
        return {
            "developerId": cls.DEVELOPER_ID,
            "ePoiId": cls.E_POI_ID,
            "sign": cls.SIGN,
        }

    @classmethod
    def validate(cls) -> List[str]:
        """返回配置缺失的提示信息。"""
        warnings: List[str] = []

        if not os.getenv("DB_PASSWORD"):
            warnings.append("未设置 DB_PASSWORD，使用 config.py 默认值")
        if not os.getenv("WECHAT_WEBHOOK"):
            warnings.append("未设置 WECHAT_WEBHOOK，通知将被禁用")
        if not os.getenv("SIGN"):
            warnings.append("未设置 SIGN，使用 config.py 默认值")
        if not os.getenv("DEVELOPER_ID"):
            warnings.append("未设置 DEVELOPER_ID，使用 config.py 默认值")
        if not os.getenv("E_POI_ID"):
            warnings.append("未设置 E_POI_ID，使用 config.py 默认值")

        return warnings


config = Config()
