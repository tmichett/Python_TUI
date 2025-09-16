#!/usr/bin/env python3
"""
Setup script for the Python TUI Menu System.
This script installs dependencies and verifies the installation.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def verify_installation():
    """Verify that all components work correctly."""
    print("\nVerifying installation...")
    
    try:
        # Test imports
        import yaml
        print("✓ PyYAML is available")
        
        import asciimatics
        print("✓ asciimatics is available")
        
        # Test menu system import
        from menu_system import MenuSystem, MenuConfig
        print("✓ Menu system modules imported successfully")
        
        # Test config loading
        if os.path.exists('config.yml'):
            config = MenuConfig('config.yml')
            print(f"✓ Configuration loaded: '{config.title}'")
        else:
            print("ⓘ No config.yml found (this is normal for first run)")
        
        print("\n✅ Installation verification completed successfully!")
        print("\nYou can now run the menu system with:")
        print("  python menu_system.py")
        print("  or")
        print("  python test_menu.py")
        
        return True
        
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False

def main():
    """Main setup function."""
    print("Python TUI Menu System Setup")
    print("=" * 40)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not verify_installation():
        sys.exit(1)
    
    print("\nSetup completed successfully! 🎉")

if __name__ == "__main__":
    main()
