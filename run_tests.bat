@echo off
chcp 65001 > nul
echo 正在执行测试...
python -m pytest

echo.
where allure >nul 2>nul
if %errorlevel% neq 0 (
  echo 未检测到 Allure CLI，跳过报告生成。
  exit /b 0
)

echo 正在生成 Allure 报告...
allure generate reports/allure-results -o reports/allure-report --clean

echo.
echo 正在打开 Allure 报告...
start reports/allure-report/index.html
