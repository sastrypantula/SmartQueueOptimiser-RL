#!/bin/bash
# Smart Queue Optimizer - Frontend Startup Script (macOS/Linux)
# This script starts the React frontend

echo ""
echo "========================================"
echo " Smart Queue Optimizer - Frontend Setup"
echo "========================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed or not in PATH"
    echo "Please install Node.js 14+ from https://nodejs.org"
    exit 1
fi

cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies (this may take a few minutes)..."
    npm install
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install npm dependencies"
        exit 1
    fi
fi

# Start the React app
echo ""
echo "========================================"
echo " Starting React Development Server"
echo "========================================"
echo ""
echo "Frontend will open at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm start
