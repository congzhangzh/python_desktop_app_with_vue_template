@echo off
REM Windows build script for Python Desktop App with Vue
REM Prerequisites: mamba environment 'desktop_app_by_webview' activated

REM Check if we're in the right environment
python -c "import PySide6" 2>nul || (
    echo Error: PySide6 not found. Please activate mamba environment:
    echo   mamba activate desktop_app_by_webview
    echo   mamba install pyside6
    exit /b 1
)

REM Step 1: Build frontend
echo [1/2] Building Vue frontend...
pushd .
cd frontend
call npm install || (
    echo Error: npm install failed
    exit /b 1
)
call npm run build-only || (
    echo Error: npm run build failed
    exit /b 1
)
if not exist "frontend\dist\index.html" (
    echo Error: Frontend build failed - dist/index.html not found
    exit /b 1
)
popd .

REM Step 2: Build Python executable
echo [2/2] Building Python executable...
pyinstaller --name=DesktopHybridApp_Python_Plus_Vue ^
    --windowed ^
    --onedir ^
    --add-data "frontend\dist;frontend\dist" ^
    --distpath=dist ^
    --workpath=build ^
    --specpath=. ^
    main.py ||  (
    echo Error: PyInstaller build failed
    exit /b 1
)

echo Executable: dist\DesktopApp\DesktopApp.exe
