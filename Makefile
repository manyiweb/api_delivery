.PHONY: help install unit smoke critical report clean lint

PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
ALLURE := $(VENV)/bin/allure

help:
	@echo "api-auto-test 本地开发/测试命令"
	@echo "  make install   创建虚拟环境并安装依赖"
	@echo "  make unit      运行单元测试（不访问外部接口）"
	@echo "  make smoke     运行 smoke 集成测试"
	@echo "  make critical  运行 critical 集成测试"
	@echo "  make report    生成 Allure HTML 报告"
	@echo "  make clean     清理报告、缓存和虚拟环境"
	@echo "  make lint      运行代码风格检查"

$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install: $(VENV)/bin/activate
	@echo "依赖安装完成，虚拟环境位于 $(VENV)"

unit: $(VENV)/bin/activate
	ENV=fat SKIP_HANDOVER=1 $(PYTEST) tests/unit -m unit -v \
		--alluredir=./reports/allure-results/unit

smoke: $(VENV)/bin/activate
	$(PYTEST) case -m smoke -v \
		--alluredir=./reports/allure-results/smoke \
		--reruns 2 --reruns-delay 1

critical: $(VENV)/bin/activate
	$(PYTEST) case -m critical -v \
		--alluredir=./reports/allure-results/critical \
		--reruns 2 --reruns-delay 1

report: $(VENV)/bin/activate
	$(ALLURE) generate ./reports/allure-results \
		-o ./reports/allure-report --clean
	@echo "报告已生成: ./reports/allure-report/index.html"

clean:
	rm -rf $(VENV) reports/ logs/ .pytest_cache/ .pip-cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

lint: $(VENV)/bin/activate
	$(PIP) install -q ruff
	$(VENV)/bin/ruff check .
