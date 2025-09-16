# macOS Build Fix - Xcode License Issue

## 🚨 Problem

When building on macOS, you get this error:

```
SystemError: install_name_tool command (['install_name_tool', '-delete_rpath', ...
You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
```

## ✅ Solution

This is a common macOS issue. PyInstaller requires Xcode command line tools, and Apple requires you to accept their license first.

### Step 1: Accept Xcode License

**Quick accept** (recommended):
```bash
sudo xcodebuild -license accept
```

**Or review then accept**:
```bash
sudo xcodebuild -license
# Read through license, then type: agree
```

### Step 2: Retry Build

After accepting the license:
```bash
./build.sh
```

## 🔧 Why This Happens

- macOS requires Xcode command line tools for development
- PyInstaller uses these tools to process binary dependencies
- Apple requires license acceptance before first use
- This is a one-time requirement per system

## 🍎 macOS Build Requirements

To build successfully on macOS, you need:

1. **Xcode Command Line Tools**:
   ```bash
   xcode-select --install
   ```

2. **Accepted Xcode License**:
   ```bash
   sudo xcodebuild -license accept
   ```

3. **Python and Dependencies**:
   ```bash
   pip install pyinstaller asciimatics PyYAML
   ```

## 🚀 After Fix

Once you've accepted the license:

1. ✅ Build will proceed normally
2. ✅ No need to accept again (until Xcode updates)
3. ✅ All PyInstaller builds will work
4. ✅ Other development tools will also work

## 📋 Verification

You can verify Xcode tools are ready:
```bash
xcodebuild -version
# Should show Xcode version without errors
```

## 🔄 Alternative Solutions

If you don't want to accept the Xcode license:

### Option 1: Use Different System
Build on a Linux system or use CI/CD that handles licensing.

### Option 2: Use Docker
```bash
# Build in Linux container (more complex setup)
docker run --rm -v $(pwd):/app python:3.12 /bin/bash -c "
  cd /app && 
  pip install pyinstaller asciimatics PyYAML &&
  python build.py
"
```

### Option 3: Cross-Platform Build
- Build on Windows/Linux for those platforms
- Use GitHub Actions or similar for automated builds

## 📖 More Information

- [Apple Developer Documentation](https://developer.apple.com/xcode/)
- [PyInstaller macOS Requirements](https://pyinstaller.readthedocs.io/en/stable/requirements.html#macos)
- [Xcode Command Line Tools Guide](https://developer.apple.com/xcode/features/)

---

## Quick Fix Summary

```bash
# Fix the issue
sudo xcodebuild -license accept

# Retry build  
./build.sh

# ✅ Done!
```

This is a one-time setup per macOS system. After this, all PyInstaller builds will work normally.
