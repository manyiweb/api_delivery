@echo off
chcp 65001 > nul
echo 正在运行测试用例...
pytest

echo.
echo 正在生成 Allure 报告...
allure generate reports/allure-results -o reports/allure-report --clean

echo.
echo 正在打开 Allure 报告...
start reports/allure-report/index.html
