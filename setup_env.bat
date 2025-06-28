@echo off
echo ========================================
echo ElderWise Environment Setup
echo ========================================
echo.

REM Check if conda is installed
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Conda is not installed or not in PATH
    echo Please install Anaconda or Miniconda first:
    echo https://www.anaconda.com/products/distribution
    pause
    exit /b 1
)

echo Creating conda environment 'elderwise'...
conda create -n elderwise python=3.11 -y

if %errorlevel% neq 0 (
    echo Error creating environment
    pause
    exit /b 1
)

echo.
echo Activating environment...
call conda activate elderwise

echo.
echo Installing Python packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error installing packages
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Your ElderWise environment is ready!
echo.
echo To start the application:
echo 1. Run: conda activate elderwise
echo 2. Run: streamlit run app.py
echo.
echo Or simply double-click run.bat
echo.
pause
