#!/usr/bin/env python3
"""
Build script for creating a standalone executable of the menu system.
Uses PyInstaller to create a self-contained binary package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class MenuSystemBuilder:
    """Builder class for creating the menu system executable."""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.build_dir = self.project_dir / "build"
        self.dist_dir = self.project_dir / "dist"
        self.spec_file = self.project_dir / "menu_system.spec"
        self.main_script = self.project_dir / "menu_system.py"
        
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        print("Checking dependencies...")
        
        required_packages = ['pyinstaller', 'asciimatics', 'PyYAML']
        missing_packages = []
        
        for package in required_packages:
            try:
                if package == 'pyinstaller':
                    import PyInstaller
                elif package == 'asciimatics':
                    import asciimatics
                elif package == 'PyYAML':
                    import yaml
                print(f"✓ {package} is available")
            except ImportError:
                missing_packages.append(package)
                print(f"✗ {package} is missing")
        
        if missing_packages:
            print(f"\nMissing packages: {', '.join(missing_packages)}")
            print("Install with: pip install " + " ".join(missing_packages))
            return False
        
        print("✓ All dependencies are available")
        return True
    
    def clean_build_dirs(self):
        """Clean existing build directories."""
        print("Cleaning build directories...")
        
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"✓ Removed {dir_path}")
        
        if self.spec_file.exists():
            self.spec_file.unlink()
            print(f"✓ Removed {self.spec_file}")
    
    def create_spec_file(self):
        """Create PyInstaller spec file with proper configuration."""
        print("Creating PyInstaller spec file...")
        
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Data files to include
added_files = [
    ('config.yml', '.'),
    ('*.md', '.'),
]

a = Analysis(
    ['menu_system.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'asciimatics.widgets',
        'asciimatics.scene',
        'asciimatics.screen',
        'asciimatics.exceptions',
        'asciimatics.event',
        'yaml',
        'subprocess',
        'threading',
        'queue'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='menu_system',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''
        
        with open(self.spec_file, 'w') as f:
            f.write(spec_content)
        
        print(f"✓ Created {self.spec_file}")
    
    def build_executable(self):
        """Build the executable using PyInstaller."""
        print("Building executable with PyInstaller...")
        
        # Build command
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            str(self.spec_file)
        ]
        
        print(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✓ Build completed successfully")
            if result.stdout:
                print("Build output:")
                print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("✗ Build failed")
            print("Error output:")
            print(e.stderr)
            
            # Check for common macOS issues
            if "install_name_tool" in str(e.stderr) and "Xcode license" in str(e.stderr):
                print("\n🍎 macOS Issue Detected:")
                print("You need to accept the Xcode license agreement.")
                print("Run this command and try building again:")
                print("  sudo xcodebuild -license accept")
            
            return False
        
        return True
    
    def verify_build(self):
        """Verify that the build was successful."""
        print("Verifying build...")
        
        executable_name = "menu_system"
        if os.name == 'nt':  # Windows
            executable_name += ".exe"
        
        executable_path = self.dist_dir / executable_name
        
        if executable_path.exists():
            size_mb = executable_path.stat().st_size / (1024 * 1024)
            print(f"✓ Executable created: {executable_path}")
            print(f"✓ Size: {size_mb:.1f} MB")
            
            # Check if config.yml is bundled
            if (self.dist_dir / "config.yml").exists():
                print("✓ config.yml included in distribution")
            else:
                print("⚠ config.yml not found in distribution directory")
            
            return True
        else:
            print("✗ Executable not found")
            return False
    
    def create_distribution_package(self):
        """Create a complete distribution package."""
        print("Creating distribution package...")
        
        # Create package directory
        package_dir = self.project_dir / "menu_system_package"
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        # Copy executable and required files
        executable_name = "menu_system"
        if os.name == 'nt':
            executable_name += ".exe"
        
        exe_src = self.dist_dir / executable_name
        exe_dst = package_dir / executable_name
        
        if exe_src.exists():
            shutil.copy2(exe_src, exe_dst)
            print(f"✓ Copied executable to {exe_dst}")
            
            # Make executable on Unix systems
            if os.name != 'nt':
                os.chmod(exe_dst, 0o755)
                print("✓ Made executable permissions")
        
        # Copy documentation and config files
        files_to_copy = [
            'config.yml',
            'README.md',
            'FIXES_APPLIED.md',
            'SHELL_FIX_SUMMARY.md'
        ]
        
        for file_name in files_to_copy:
            src_file = self.project_dir / file_name
            if src_file.exists():
                shutil.copy2(src_file, package_dir / file_name)
                print(f"✓ Copied {file_name}")
        
        # Create usage instructions
        self.create_usage_instructions(package_dir)
        
        print(f"✓ Distribution package created in {package_dir}")
        return package_dir
    
    def create_usage_instructions(self, package_dir):
        """Create usage instructions for the packaged executable."""
        instructions = """# RHCI Instructor VT Toolkit - Standalone Executable

## Quick Start

### Running the Menu System
```bash
# On macOS/Linux:
./menu_system

# On Windows:
menu_system.exe
```

### First Time Setup
1. Make sure `config.yml` is in the same directory as the executable
2. Run the executable from a terminal/command prompt
3. Navigate using arrow keys, Enter to select, Esc to go back

## Features
- Multi-level menu system based on config.yml
- Interactive shell interface (💻 Command Shell)
- Command execution with output display
- Built-in help system (F1 key)

## Configuration
Edit `config.yml` to customize your menu structure:
- Add new menu categories
- Define shell commands to execute
- Add help text for menu items

## Shell Interface
The built-in shell runs within the TUI:
- Type commands like `ls`, `pwd`, `date`
- Use `cd` to change directories
- Type `exit` to return to main menu
- Note: Tab completion is not available (TUI limitation)

## Troubleshooting

### Common Issues
- **Permission denied**: Make sure executable has run permissions
- **Config not found**: Ensure config.yml is in the same directory
- **Display issues**: Run from a proper terminal with color support

### Getting Help
- Press F1 in any menu for context-sensitive help
- Check README.md for detailed documentation
- Review FIXES_APPLIED.md for recent improvements

## Files Included
- `menu_system` (or `menu_system.exe`) - Main executable
- `config.yml` - Menu configuration file
- `README.md` - Complete documentation
- `FIXES_APPLIED.md` - Recent bug fixes and improvements
- `SHELL_FIX_SUMMARY.md` - Shell implementation details

## System Requirements
- Any modern operating system (Windows, macOS, Linux)
- Terminal with color support
- No Python installation required (self-contained)

---
Built with PyInstaller - No dependencies required!
"""
        
        with open(package_dir / "USAGE.md", 'w') as f:
            f.write(instructions)
        
        print("✓ Created USAGE.md")
    
    def build(self):
        """Main build process."""
        print("=" * 60)
        print("RHCI Menu System - Build Process")
        print("=" * 60)
        
        if not self.main_script.exists():
            print(f"✗ Main script not found: {self.main_script}")
            return False
        
        steps = [
            ("Checking dependencies", self.check_dependencies),
            ("Cleaning build directories", lambda: self.clean_build_dirs() or True),
            ("Creating spec file", lambda: self.create_spec_file() or True),
            ("Building executable", self.build_executable),
            ("Verifying build", self.verify_build),
            ("Creating distribution package", lambda: self.create_distribution_package() is not None),
        ]
        
        for step_name, step_func in steps:
            print(f"\n{step_name}...")
            if not step_func():
                print(f"✗ Failed at: {step_name}")
                return False
        
        print("\n" + "=" * 60)
        print("✅ Build completed successfully!")
        print("\nYour standalone executable is ready in:")
        print(f"  📁 {self.project_dir}/menu_system_package/")
        print("\nTo run:")
        executable_name = "menu_system.exe" if os.name == 'nt' else "./menu_system"
        print(f"  {executable_name}")
        print("\n🎉 No Python installation required on target systems!")
        
        return True

def main():
    """Main entry point."""
    builder = MenuSystemBuilder()
    success = builder.build()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
