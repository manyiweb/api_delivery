@echo off
chcp 65001 > nul
echo Running tests...
python -m pytest

echo.
where allure >nul 2>nul
if %errorlevel% neq 0 (
  echo Allure CLI not found, skipping report generation.
  exit /b 0
)

echo Generating Allure report...
allure generate reports/allure-results -o reports/allure-report --clean

echo.
echo Opening Allure report...
start reports/allure-report/index.html
