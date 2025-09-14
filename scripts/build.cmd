@echo on
pushd .

cd /d %~dp0\..

REM Windows build script for Python Desktop App with Vue
REM Prerequisites: mamba environment 'desktop_app_by_webview' activated

REM Check if we're in the right environment

REM use python in python_desktop_dev as your python 
REM Trick: vs code does not works with micromamba, you need to activate it by yourself
REM micromamba activate python_desktop_dev
python -c "import PySide6" 2>nul

REM TODO: why somecommand
if errorlevel 1 (
    echo Error: PySide6 not found. Please activate mamba environment:
    echo   mamba activate python_desktop_dev ^(change to your environment name^)
    echo   mamba install pyside6
    exit /b 1
)

REM Step 1: Build frontend
echo [1/2] Building Vue frontend...
pushd .
cd frontend
call npm install
if errorlevel 1 (
    echo Error: npm install failed
    exit /b 1
)
call npm run build-only
if errorlevel 1 (
    echo Error: npm run build failed
    exit /b 1
)
if not exist "dist\index.html" (
    echo Error: Frontend build failed - dist/index.html not found
    exit /b 1
)
popd

REM Step 2: Build Python executable
echo [2/2] Building Python executable...

pushd .
REM remove --noconfirm ^ if you want to debug the spec file

if not exist "build" (
    mkdir build
)

pyinstaller --name=DesktopHybridApp_Python_Plus_Vue ^
    --noconsole ^
    --onedir ^
    --add-data "frontend\dist;frontend\dist" ^
    --distpath=dist ^
    --workpath=build ^
    --icon=frontend\public\favicon.ico ^
    --noconfirm ^
    main.py

if errorlevel 1 (
    echo Error: PyInstaller build failed
    exit /b 1
)

popd
echo Executable: dist\DesktopHybridApp_Python_Plus_Vue\DesktopHybridApp_Python_Plus_Vue
start dist\DesktopHybridApp_Python_Plus_Vue\DesktopHybridApp_Python_Plus_Vue

popd
