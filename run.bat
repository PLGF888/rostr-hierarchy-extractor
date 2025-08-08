@echo off
chcp 65001 >nul
echo ================================================
echo 🚀 Starting Python Application...
echo ================================================

REM Verify Python installation
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed or not found in PATH.
    pause
    exit /b 1
)

REM Verify main.py exists
IF NOT EXIST "main.py" (
    echo ❌ main.py file not found!
    pause
    exit /b 1
)

REM Execute the main Python script
python main.py

REM Check execution status
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ The Python script terminated with errors.
) ELSE (
    echo ✅ The Python script executed successfully.
)

echo ================================================
pause
