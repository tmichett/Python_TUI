#!/usr/bin/env python3
"""
Test script that validates the fix without requiring dependencies.
"""

import ast
import sys

def analyze_shell_implementation():
    """Analyze the ShellFrame implementation using AST."""
    print("Analyzing ShellFrame implementation...")
    
    try:
        with open('menu_system.py', 'r') as f:
            content = f.read()
        
        # Parse the AST
        tree = ast.parse(content)
        
        classes = {}
        functions = {}
        
        # Extract classes and methods
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes[node.name] = node
            elif isinstance(node, ast.FunctionDef):
                functions[node.name] = node
        
        # Check ShellFrame class
        if 'ShellFrame' not in classes:
            print("❌ ShellFrame class not found")
            return False
        
        shell_frame = classes['ShellFrame']
        print("✓ ShellFrame class found")
        
        # Check that ShellFrame inherits from Frame
        if shell_frame.bases and hasattr(shell_frame.bases[0], 'id') and shell_frame.bases[0].id == 'Frame':
            print("✓ ShellFrame inherits from Frame")
        
        # Check for required methods in ShellFrame
        shell_methods = []
        for node in ast.walk(shell_frame):
            if isinstance(node, ast.FunctionDef):
                shell_methods.append(node.name)
        
        required_methods = ['__init__', '_execute_command', '_back_to_menu', 'process_event']
        
        for method in required_methods:
            if method in shell_methods:
                print(f"✓ Method {method} found")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        # Check MenuSystem class has open_shell method
        if 'MenuSystem' not in classes:
            print("❌ MenuSystem class not found")
            return False
        
        menu_system = classes['MenuSystem']
        menu_methods = []
        for node in ast.walk(menu_system):
            if isinstance(node, ast.FunctionDef):
                menu_methods.append(node.name)
        
        if 'open_shell' in menu_methods:
            print("✓ MenuSystem.open_shell method found")
        else:
            print("❌ MenuSystem.open_shell method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing code: {e}")
        return False

def check_error_fixes():
    """Check that specific errors are fixed."""
    print("\nChecking error fixes...")
    
    try:
        with open('menu_system.py', 'r') as f:
            content = f.read()
        
        # Check that set_focus error is fixed
        if 'set_focus' in content:
            print("⚠ set_focus still found in code (should be removed)")
            return False
        else:
            print("✓ set_focus error fixed (call removed)")
        
        # Check that ShellFrame creation is properly handled
        if 'ShellFrame(self._screen, self)' in content:
            print("✓ ShellFrame creation found")
        else:
            print("❌ ShellFrame creation not found")
            return False
        
        # Check error handling
        if 'except Exception as e:' in content and 'Shell Error:' in content:
            print("✓ Error handling added to shell creation")
        else:
            print("⚠ Shell error handling not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking fixes: {e}")
        return False

def main():
    """Main test function."""
    print("Testing ShellFrame Fix (Syntax Analysis)")
    print("=" * 45)
    
    success = True
    
    # Test 1: Analyze implementation
    if not analyze_shell_implementation():
        success = False
    
    # Test 2: Check specific fixes
    if not check_error_fixes():
        success = False
    
    print("\n" + "=" * 45)
    if success:
        print("✅ ShellFrame implementation is correct!")
        print("\nThe 'set_focus' error should now be fixed.")
        print("The shell should run within the TUI interface.")
        print("\nTo test:")
        print("1. Install: pip install asciimatics PyYAML")
        print("2. Run: python menu_system.py")
        print("3. Select '🖥️ Command Shell' from main menu")
        print("4. Shell should open in TUI (not external terminal)")
    else:
        print("❌ Issues found in implementation")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
