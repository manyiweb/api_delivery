"""CI 登录前置检查，避免批量用例反复触发错误登录。"""

import os
import sys

import httpx

from config import config as app_config
from conftest import _extract_token_id


def main() -> int:
    payload = {
        "mobile": os.getenv("LOGIN_MOBILE", ""),
        "loginType": "checkstand",
        "appType": "pc",
        "appVersion": "1.6.2.1",
        "loginWord": os.getenv("LOGIN_WORD", ""),
        "clientVersion": "25091901",
        "systemVersion": "2512.29.34",
        "companyId": "",
    }
    login_url = app_config.get_base_url() + "/reabam-manage-login/user/login"

    with httpx.Client(timeout=app_config.DEFAULT_TIMEOUT) as client:
        response = client.post(login_url, json=payload)

    if response.status_code != 200:
        print(f"登录接口 HTTP 状态异常: status={response.status_code}", file=sys.stderr)
        return 1

    response_json = response.json()
    try:
        _extract_token_id(response_json)
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print("登录预检通过：已获取 tokenId")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
