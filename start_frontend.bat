@echo off
REM Smart Queue Optimizer - Frontend Startup Script (Windows)
REM This script starts the React frontend

echo.
echo ========================================
echo  Smart Queue Optimizer - Frontend Setup
echo ========================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 14+ from https://nodejs.org
    pause
    exit /b 1
)

cd frontend

REM Install dependencies if node_modules doesn't exist
if not exist node_modules (
    echo Installing npm dependencies (this may take a few minutes)...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install npm dependencies
        pause
        exit /b 1
    )
)

REM Start the React app
echo.
echo ========================================
echo  Starting React Development Server
echo ========================================
echo.
echo Frontend will open at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm start

pause
