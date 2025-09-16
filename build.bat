@echo off
REM Build script for Windows
REM Creates a standalone executable of the RHCI Menu System

echo RHCI Menu System - Build Script
echo ================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not found
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Install build dependencies if not present
echo 📦 Checking build dependencies...

python -c "import PyInstaller" 2>nul || (
    echo Installing PyInstaller...
    pip install pyinstaller
)

python -c "import asciimatics" 2>nul || (
    echo Installing asciimatics...
    pip install asciimatics
)

python -c "import yaml" 2>nul || (
    echo Installing PyYAML...
    pip install PyYAML
)

echo ✅ All dependencies ready

REM Run the build
echo 🔨 Starting build process...
python build.py

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Build completed successfully!
    echo.
    echo 📁 Your executable is in: menu_system_package\
    echo 🚀 To run: cd menu_system_package ^&^& menu_system.exe
    echo.
    echo 📖 See USAGE.md for detailed instructions
    pause
) else (
    echo ❌ Build failed
    pause
    exit /b 1
)
