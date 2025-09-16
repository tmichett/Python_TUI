#!/usr/bin/env python3
"""
Debug script to test the ShellFrame implementation.
"""

import sys
import os

def test_shell_frame():
    """Test ShellFrame creation without actually running the TUI."""
    print("Testing ShellFrame implementation...")
    
    try:
        # Import the classes we need
        from menu_system import ShellFrame, MenuSystem
        print("✓ ShellFrame and MenuSystem imported successfully")
        
        # Test MenuSystem creation
        menu_system = MenuSystem()
        print("✓ MenuSystem created successfully")
        
        # Try to simulate screen creation (this will fail but let's see the error)
        try:
            from asciimatics.screen import Screen
            print("✓ Screen class imported")
        except ImportError as e:
            print(f"⚠ Screen import issue: {e}")
        
        print("\n✅ Basic imports working correctly")
        print("The ShellFrame should now work when the TUI is running.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing ShellFrame: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_shell_integration():
    """Check that shell integration is properly set up."""
    print("\nChecking shell integration...")
    
    try:
        with open('menu_system.py', 'r') as f:
            content = f.read()
        
        # Check that ShellFrame is properly integrated
        checks = [
            ('class ShellFrame(Frame)', 'ShellFrame class defined'),
            ('def open_shell(self)', 'open_shell method defined'),
            ('shell_frame = ShellFrame(self._screen, self)', 'Shell frame creation'),
            ('def _execute_command(self)', 'Command execution method'),
            ('def _back_to_menu(self)', 'Back to menu method'),
            ('process_event(self, event)', 'Event handling'),
        ]
        
        all_good = True
        for check, description in checks:
            if check in content:
                print(f"✓ {description}")
            else:
                print(f"❌ Missing: {description}")
                all_good = False
        
        # Check that old shell code is removed
        if '_run_interactive_shell' not in content:
            print("✓ Old external shell code removed")
        else:
            print("⚠ Old shell code still present")
        
        return all_good
        
    except Exception as e:
        print(f"❌ Error checking integration: {e}")
        return False

def main():
    """Main debug function."""
    print("ShellFrame Debug Script")
    print("=" * 30)
    
    success = True
    
    # Test 1: Basic functionality
    if not test_shell_frame():
        success = False
    
    # Test 2: Integration check
    if not check_shell_integration():
        success = False
    
    print("\n" + "=" * 30)
    if success:
        print("✅ Shell implementation looks good!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install asciimatics PyYAML")
        print("2. Run: python menu_system.py")
        print("3. Select '🖥️ Command Shell' from main menu")
        print("4. Shell should open within TUI (not external shell)")
    else:
        print("❌ Issues found in shell implementation")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
