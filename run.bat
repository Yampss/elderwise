@echo off
echo Starting ElderWise - Connecting Generations Through Stories
echo.
echo Please make sure you have your Gemini API key ready!
echo You can get one free at: https://makersuite.google.com/app/apikey
echo.
echo Activating conda environment...
call conda activate elderwise
if %errorlevel% neq 0 (
    echo Error: Could not activate elderwise environment. Creating it now...
    call conda create -n elderwise python=3.11 -y
    call conda activate elderwise
    pip install -r requirements.txt
)
echo.
echo Starting the application...
streamlit run app.py --server.port 8501
