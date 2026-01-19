"""Configuration module for tests and API clients."""
import os
from typing import Any, Dict, List


class Config:
    """Global configuration."""

    # API settings
    BASE_URL = os.getenv("BASE_URL", "http://fat-pos.reabam.com:60030/api")
    UAT_URL = os.getenv("UAT_URL", "https://pos.reabam.com:60030/api")

    # Database settings
    DB_CONFIG: Dict[str, Any] = {
        "host": os.getenv("DB_HOST", "192.168.1.151"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "zhoujiman@mop#mop"),
        "password": os.getenv("DB_PASSWORD", "reabam123@mop"),
        "database": os.getenv("DB_NAME", "rb_ts_core"),
        "charset": "utf8mb4",
    }

    # Notification settings
    WECHAT_WEBHOOK = os.getenv(
        "WECHAT_WEBHOOK",
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b97e1f07-9f2c-45b9-a2bc-999b744c2ca4",
    )

    # Business settings
    DEVELOPER_ID = os.getenv("DEVELOPER_ID", "106825")
    E_POI_ID = os.getenv("E_POI_ID", "reabamts_5ad586a8721e49518998aedef9fd3b5c")
    SIGN = os.getenv("SIGN", "146bcdd348c4f7e90895af13faa123e201fe2686")

    # Test settings
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    RETRY_TIMES = int(os.getenv("RETRY_TIMES", "3"))
    RETRY_INTERVAL = int(os.getenv("RETRY_INTERVAL", "2"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "logs")

    # Allure
    ALLURE_RESULTS_DIR = "reports/allure-results"
    ALLURE_REPORT_DIR = "reports/allure-report"

    @classmethod
    def get_base_url(cls) -> str:
        """Return base URL based on ENV."""
        env = os.getenv("ENV", "test")
        return cls.UAT_URL if env == "uat" else cls.BASE_URL

    @classmethod
    def get_final_payload_params(cls) -> Dict[str, str]:
        """Return common payload params for requests."""
        return {
            "developerId": cls.DEVELOPER_ID,
            "ePoiId": cls.E_POI_ID,
            "sign": cls.SIGN,
        }

    @classmethod
    def validate(cls) -> List[str]:
        """Return configuration warnings for missing env values."""
        warnings: List[str] = []

        if not os.getenv("DB_PASSWORD"):
            warnings.append("DB_PASSWORD not set; using default value from config.py")
        if not os.getenv("WECHAT_WEBHOOK"):
            warnings.append("WECHAT_WEBHOOK not set; notifications will be disabled")
        if not os.getenv("SIGN"):
            warnings.append("SIGN not set; using default value from config.py")
        if not os.getenv("DEVELOPER_ID"):
            warnings.append("DEVELOPER_ID not set; using default value from config.py")
        if not os.getenv("E_POI_ID"):
            warnings.append("E_POI_ID not set; using default value from config.py")

        return warnings


config = Config()
