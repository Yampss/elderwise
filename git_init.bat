@echo off
echo Initializing Git repository for ElderWise...
echo.

REM Initialize git repository
git init
if %errorlevel% neq 0 (
    echo Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/downloads
    pause
    exit /b 1
)

REM Add all files
echo Adding all files to git...
git add .

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: ElderWise - AI-powered intergenerational storytelling platform

Features:
- Voice recording interface for seniors
- AI-powered transcription using Google Gemini
- Smart story categorization and search
- Mentorship matching system
- Community features and analytics
- Comprehensive documentation and deployment guides

Tech stack: Python, Streamlit, Google Gemini API, Conda"

REM Set main branch
git branch -M main

echo.
echo ✅ Git repository initialized successfully!
echo.
echo 🚀 Next steps:
echo 1. Create a new repository on GitHub named 'elderwise'
echo 2. Copy the repository URL
echo 3. Run: git remote add origin https://github.com/yourusername/elderwise.git
echo 4. Run: git push -u origin main
echo.
echo 📋 Suggested GitHub repository settings:
echo - Description: "AI-powered platform connecting generations through storytelling"
echo - Topics: python, streamlit, ai, gemini, storytelling, seniors, mentorship
echo - License: MIT
echo - Enable Issues and Discussions
echo.
pause
