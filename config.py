"""Configuration module for tests and API clients."""
import os
from typing import Any, Dict, List

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


class Config:
    """Global configuration."""

    # API settings
    BASE_URL = os.getenv("BASE_URL")
    UAT_URL = os.getenv("UAT_URL")

    # Database settings
    DB_CONFIG: Dict[str, Any] = {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "charset": "utf8mb4",
    }

    # Notification settings
    WECHAT_WEBHOOK = os.getenv(
        "WECHAT_WEBHOOK"
    )

    # Business settings
    DEVELOPER_ID = os.getenv("DEVELOPER_ID")
    E_POI_ID = os.getenv("E_POI_ID")
    SIGN = os.getenv("SIGN")

    # Test settings
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT"))
    RETRY_TIMES = int(os.getenv("RETRY_TIMES"))
    RETRY_INTERVAL = int(os.getenv("RETRY_INTERVAL"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL")
    LOG_DIR = os.getenv("LOG_DIR")

    # Allure
    ALLURE_RESULTS_DIR = "reports/allure-results"
    ALLURE_REPORT_DIR = "reports/allure-report"

    @classmethod
    def get_base_url(cls) -> str:
        """Return base URL based on ENV."""
        env = os.getenv("ENV")
        return cls.UAT_URL if env == "uat" else cls.BASE_URL

    @classmethod
    def get_final_payload_params(cls) -> Dict[str, str]:
        """Return common payload params for requests."""
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

if __name__ == '__main__':
    print(f"加载前: {os.getenv('ENV')}")
    # load_dotenv()
    print(f"加载后: {os.getenv('ENV')}")
    print("生产地址", config.get_base_url())
    print(config.get_final_payload_params())
