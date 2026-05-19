# API Delivery 自动化测试框架

基于 pytest + httpx + allure 的接口自动化框架，支持 YAML 数据驱动、接口回调封装、数据库断言与测试报告。

## 特性
- pytest 用例组织与标记
- YAML 测试数据驱动
- httpx 请求封装与重试
- DB 断言与测试数据清理
- Allure 报告输出
- 企业微信通知（可配置）

## 目录结构
```
api/            # 接口封装与 payload 构建
assertions/     # DB 断言
case/           # 测试用例
data/           # YAML 测试数据
utils/          # 工具模块（日志、DB、通知等）
config.py       # 配置与环境变量
conftest.py     # pytest fixtures
pytest.ini      # pytest 配置
```

## 环境要求
- Python 3.12+
- Allure CLI（生成报告用，需自行安装）

## 安装依赖
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

如需自动加载 `.env`，请安装：
```bash
pip install python-dotenv
```

## 配置
复制并修改：
```bash
cp .env.example .env
```

常用环境变量（见 `.env.example`）：
- `ENV`：fat/uat
- `BASE_URL` / `UAT_URL`
- `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` / `DB_NAME`
- `WECHAT_WEBHOOK`
- `DEVELOPER_ID` / `E_POI_ID` / `SIGN`
- `DEVELOPER_ID_UAT` / `E_POI_ID_UAT` / `SIGN_UAT`（当 `ENV=uat`）
- `DEFAULT_TIMEOUT` / `RETRY_TIMES` / `RETRY_INTERVAL`
- `LOG_LEVEL` / `LOG_DIR`

说明：
- 当 `ENV=uat` 时，`conftest.py` 会跳过数据库连接。
- `config.py` 会根据 `ENV` 选择不同的 base url 和签名参数。

## 运行测试
```bash
pytest
```

仅运行本地单元测试：
```bash
pytest tests/unit
```

运行核心链路门禁：
```bash
pytest -m smoke
```

运行关键回归集：
```bash
pytest -m "smoke or critical"
```

联调用例说明：
- `case/` 下用例会访问 `.env` 指定环境，依赖门店授权、登录账号、商品、会员、数据库等测试数据。
- 若环境数据变更，可能出现店铺未授权、商品失效、会员类型不支持、开票状态未流转等业务失败；需要先校准环境数据再回归。
- 失败排查优先查看 `logs/test_*.log` 和 `reports/allure-results`。

Windows 一键脚本：
```bat
run_tests.bat
```

## 生成 Allure 报告
```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

Allure 附件默认使用摘要模式并自动脱敏，避免报告过大或泄露 token/sign/password。
可通过环境变量调整：
- `ALLURE_ATTACH_LEVEL=summary`：默认，仅保留摘要
- `ALLURE_ATTACH_LEVEL=full`：调试时保留完整脱敏附件
- `ALLURE_ATTACH_LEVEL=off`：关闭手工附件
- `ALLURE_MAX_ATTACHMENT_CHARS=8000`：控制单个附件最大字符数

## 备注
- 测试数据位于 `data/`，payload 构建在 `api/payload_builder.py`。
- 订单创建相关用例会使用 DB 断言与清理。
