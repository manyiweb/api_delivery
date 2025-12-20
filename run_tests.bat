@echo off
chcp 65001 > nul
echo 🧪 正在运行测试用例...
pytest

if %errorlevel% equ 0 (
    echo.
    echo ✅ 测试运行成功！
    echo 📊 正在生成 Allure 报告...
    timeout /t 2 /nobreak
    allure serve ./reports/allure-results
) else (
    echo.
    echo ❌ 测试失败，请检查错误日志
    pause
    exit /b 1
)
