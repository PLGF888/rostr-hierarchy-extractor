@echo off
chcp 65001 >nul
echo ================================================
echo 🐍 Installing Python Project Dependencies...
echo ================================================

REM Check if requirements.txt exists
IF NOT EXIST "requirements.txt" (
    echo ❌ requirements.txt file not found!
    pause
    exit /b 1
)

REM Upgrade pip first (optional but recommended)
python -m pip install --upgrade pip

REM Install required packages
pip install -r requirements.txt

REM Check if pip install succeeded
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install some packages. Please check above for errors.
    pause
    exit /b %ERRORLEVEL%
)

echo ✅ Packages installed successfully!
echo ================================================
pause