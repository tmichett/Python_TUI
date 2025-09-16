# Build Documentation - RHCI Menu System

This document explains how to build a standalone executable of the RHCI Menu System using PyInstaller.

## Overview

The build process creates a self-contained executable that includes:
- Python interpreter
- All required libraries (asciimatics, PyYAML, etc.)
- Menu system code
- Configuration files
- Documentation

**Result**: A single executable that works without Python installation!

## Build Methods

### Method 1: Quick Build (Recommended)

#### On macOS/Linux:
```bash
./build.sh
```

#### On Windows:
```cmd
build.bat
```

### Method 2: Manual Build

```bash
# Install build dependencies
pip install -r build-requirements.txt

# Run build script
python build.py
```

### Method 3: Direct PyInstaller

```bash
# Install dependencies
pip install pyinstaller asciimatics PyYAML

# Create spec file and build
python build.py
```

## Build Requirements

### System Requirements
- Python 3.7 or higher
- At least 500MB free disk space
- Internet connection (for downloading dependencies)

### Python Packages
```
pyinstaller>=5.0      # Build tool
asciimatics>=1.15.0   # TUI framework  
PyYAML>=6.0          # YAML parsing
upx-ucl>=3.96        # Optional: compression
```

## Build Process Details

### 1. Dependency Check
The build script automatically checks for:
- Python installation
- Required packages (installs if missing)
- Build tools availability

### 2. Environment Setup
- Cleans previous build artifacts
- Creates PyInstaller spec file
- Configures build parameters

### 3. Code Analysis
PyInstaller analyzes the code to find:
- All imported modules
- Hidden dependencies
- Data files to include

### 4. Binary Creation
- Bundles Python interpreter
- Includes all dependencies
- Compresses the executable
- Adds configuration files

### 5. Package Creation
Creates a distribution package with:
- Standalone executable
- Configuration file (config.yml)
- Documentation files
- Usage instructions

## Build Output

### Generated Files

```
menu_system_package/
├── menu_system          # Main executable (Unix)
├── menu_system.exe      # Main executable (Windows)  
├── config.yml           # Menu configuration
├── README.md           # Full documentation
├── USAGE.md            # Quick start guide
├── FIXES_APPLIED.md    # Recent improvements
└── SHELL_FIX_SUMMARY.md # Shell implementation details
```

### Executable Details
- **Size**: ~15-25MB (self-contained)
- **Startup**: ~2-3 seconds (first run)
- **Dependencies**: None (fully self-contained)
- **Platforms**: Windows, macOS, Linux

## Build Configuration

### PyInstaller Spec File
The build creates `menu_system.spec` with:

```python
# Data files included
datas=[
    ('config.yml', '.'),
    ('*.md', '.'),
]

# Hidden imports for TUI functionality
hiddenimports=[
    'asciimatics.widgets',
    'asciimatics.screen', 
    'yaml',
    'subprocess'
]

# Single-file executable
onefile=True
console=True
```

### Build Optimization
- **UPX Compression**: Reduces executable size
- **Strip Debug**: Removes debugging symbols
- **Optimize Imports**: Only includes used modules

## Troubleshooting

### Common Build Issues

#### 1. Missing Dependencies
**Error**: `ModuleNotFoundError: No module named 'asciimatics'`
**Solution**: 
```bash
pip install -r build-requirements.txt
```

#### 2. PyInstaller Not Found
**Error**: `command not found: pyinstaller`
**Solution**:
```bash
pip install pyinstaller
```

#### 3. Permission Denied
**Error**: `Permission denied: ./build.sh`
**Solution**:
```bash
chmod +x build.sh
./build.sh
```

#### 4. Xcode License Not Accepted (macOS)
**Error**: `You have not agreed to the Xcode license agreements`
**Solution**: 
```bash
sudo xcodebuild -license accept
```

#### 5. Import Errors in Built Executable
**Error**: Built exe fails to import modules
**Solution**: Add missing imports to hiddenimports in build.py

### Build Verification

Test the built executable:

```bash
# Navigate to package
cd menu_system_package

# Run executable
./menu_system  # Unix
menu_system.exe  # Windows

# Test features
# 1. Main menu loads
# 2. Navigation works
# 3. Shell interface opens
# 4. Commands execute
# 5. Help system works
```

## Distribution

### Single Machine
Copy the `menu_system_package/` folder to target system.

### Multiple Machines
Create an archive:

```bash
# Create distributable archive
tar -czf menu_system_v1.0.tar.gz menu_system_package/

# Or zip for Windows
zip -r menu_system_v1.0.zip menu_system_package/
```

### Network Distribution
Upload to file server, cloud storage, or version control.

## Platform-Specific Notes

### macOS
- **Xcode License Required**: Must accept Xcode license before building
  ```bash
  sudo xcodebuild -license accept
  ```
- Executable may show security warning on first run
- Use: System Preferences → Security & Privacy → Allow
- Consider code signing for production distribution

### Windows  
- Windows Defender may scan the executable
- Add build folder to antivirus exclusions during build
- Consider signing for production distribution

### Linux
- Executable should work on most modern distributions
- Requires glibc compatibility
- Test on target distribution family

## Advanced Build Options

### Custom Build Configuration

Edit `build.py` to customize:

```python
# Add more data files
added_files = [
    ('config.yml', '.'),
    ('custom_themes/', 'themes/'),
    ('help_files/*.txt', 'help/')
]

# Additional hidden imports
hiddenimports=[
    'your_custom_module',
    'third_party_dependency'
]

# Build options
upx=True,           # Enable compression
debug=False,        # Disable debug mode
console=True,       # Keep console window
onefile=True,       # Single executable
```

### Development vs Production Builds

**Development** (faster, larger):
```python
debug=True,
onefile=False,
upx=False
```

**Production** (slower, smaller):
```python
debug=False, 
onefile=True,
upx=True
```

## Performance Notes

### Build Time
- Initial build: 2-5 minutes
- Subsequent builds: 1-2 minutes
- Depends on system speed and dependencies

### Executable Performance
- Startup time: 2-3 seconds (cold start)
- Runtime performance: Same as Python script
- Memory usage: ~50-100MB

### Size Optimization
- Base executable: ~15MB
- With compression: ~10-12MB
- Additional data files add to size

---

## Quick Reference

### Build Commands
```bash
# Quick build
./build.sh                    # Unix
build.bat                     # Windows

# Manual build  
python build.py

# Install dependencies only
pip install -r build-requirements.txt
```

### Test Built Executable
```bash
cd menu_system_package
./menu_system                 # Unix  
menu_system.exe              # Windows
```

### Verify Package Contents
```bash
ls -la menu_system_package/
```

---

**🎉 Your standalone RHCI Menu System is ready for distribution!**

No Python installation required on target systems.
