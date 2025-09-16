#!/bin/bash
# Build script for macOS/Linux
# Creates a standalone executable of the RHCI Menu System

set -e

echo "RHCI Menu System - Build Script"
echo "================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check for Xcode license on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Checking macOS requirements..."
    if ! xcodebuild -version >/dev/null 2>&1; then
        echo "⚠️  Xcode command line tools may not be installed or licensed"
        echo "   If build fails, run: sudo xcodebuild -license accept"
    else
        echo "✅ Xcode tools available"
    fi
fi

# Install build dependencies if not present
echo "📦 Checking build dependencies..."
python3 -c "import PyInstaller" 2>/dev/null || {
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
}

python3 -c "import asciimatics" 2>/dev/null || {
    echo "Installing asciimatics..."
    pip3 install asciimatics
}

python3 -c "import yaml" 2>/dev/null || {
    echo "Installing PyYAML..."
    pip3 install PyYAML
}

echo "✅ All dependencies ready"

# Run the build
echo "🔨 Starting build process..."
python3 build.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Build completed successfully!"
    echo ""
    echo "📁 Your executable is in: menu_system_package/"
    echo "🚀 To run: cd menu_system_package && ./menu_system"
    echo ""
    echo "📖 See USAGE.md for detailed instructions"
else
    echo "❌ Build failed"
    exit 1
fi
