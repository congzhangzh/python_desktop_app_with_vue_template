#!/bin/bash
# Linux/macOS build script for Python Desktop App with Vue
# Prerequisites: mamba environment 'desktop_app_by_webview' activated

set -e  # Exit on any error

# Step 1: Build frontend
pushd .
echo "[1/3] Building Vue frontend..."

cd frontend
npm install
npm run build-only
popd .

# Step 2: Build Python executable
echo
echo "[3/3] Building Python executable..."
pyinstaller --name=DesktopHybridApp_Python_Plus_Vue \
    --windowed \
    --onedir \
    --add-data "frontend/dist:frontend/dist" \
    --distpath=dist \
    --workpath=build \
    --specpath=. \
    main.py
