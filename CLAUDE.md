# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a desktop application template combining Python backend (PySide6) with Vue.js frontend. The application uses QWebEngineView to render a Vue frontend within a native desktop window, with intelligent environment detection for development vs production modes.

## Architecture
- **Backend**: Python with PySide6 for native desktop window and WebView
- **Frontend**: Vue 3 + TypeScript + Vite with modern tooling (Pinia, Vue Router)
- **Communication**: Direct WebView integration (no HTTP API between frontend/backend)
- **Environment Detection**: Automatic dev server detection with fallback to built assets

The main Python application (`main.py`) implements:
1. LocalHTTPServer class for serving built frontend assets
2. MainWindow class with QWebEngineView for rendering frontend
3. Smart URL determination: dev server (`localhost:5173`) → local HTTP server → error fallback

## Development Commands

### Environment Setup
```bash
# Create and activate mamba environment
mamba create -n desktop_app_by_webview python=3.11
mamba activate desktop_app_by_webview
mamba install pyside6
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..
```

### Development Mode
```bash
# Frontend dev server (hot reload)
cd frontend && npm run dev

# Python application (separate terminal)
python main.py

# VS Code: Use F5 → "🚀 Dev Mode (Frontend + Python)"
```

### Frontend Commands
```bash
cd frontend
npm run dev          # Development server
npm run build        # Build for production
npm run type-check   # TypeScript checking
npm run lint         # ESLint
npm run test:unit    # Vitest unit tests
npm run test:e2e     # Playwright E2E tests
```

### Production Build
```bash
# Full build using script
./scripts/build.sh   # Linux/macOS
.\scripts\build.cmd  # Windows

# Manual build steps
cd frontend && npm run build-only && cd ..
pyinstaller DesktopApp.spec
```

## Key Dependencies
- **Python**: PySide6, requests, pyinstaller
- **Frontend**: Vue 3, Vite, TypeScript, Pinia, Vue Router, Vitest, Playwright, ESLint

## VS Code Configuration
The project includes comprehensive VS Code debugging configurations:
- **🚀 Dev Mode**: Auto-starts frontend dev server + Python debugging
- **🏗️ Production Mode**: Builds frontend first, then starts Python
- **🐍 Python Only**: Python debugging without frontend
- **🔧 Python Debug (Attach)**: Attach debugger to running Python process

## Testing
- **Unit Tests**: `npm run test:unit` (Vitest)
- **E2E Tests**: `npm run test:e2e` (Playwright)
- **Type Checking**: `npm run type-check` (vue-tsc)
- **Linting**: `npm run lint` (ESLint)

## Environment Variables
- `DEV_MODE=1`: Force development mode
- `PROD_MODE=1`: Force production mode

## Build Output
- **Development**: Uses live dev server at `localhost:5173`
- **Production**: Packaged executable in `dist/DesktopApp/`
- **Frontend Assets**: Built to `frontend/dist/`