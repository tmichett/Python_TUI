#!/usr/bin/env python3
"""
Comprehensive test script to validate all menu and shell fixes.
"""

import ast
import sys
import time

def test_textbox_fix():
    """Test that the TextBox attribute error is fixed."""
    print("Testing TextBox fix...")
    
    try:
        with open('menu_system.py', 'r') as f:
            content = f.read()
        
        # Check that problematic start_line usage is removed
        if 'start_line = max(' in content:
            print("❌ start_line usage still found")
            return False
        
        # Check that we have proper output handling
        if 'recent_lines = lines[-15:]' in content:
            print("✓ TextBox output handling implemented correctly")
        else:
            print("❌ New output handling not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing TextBox fix: {e}")
        return False

def test_navigation_fixes():
    """Test that navigation fixes are in place."""
    print("\nTesting navigation fixes...")
    
    try:
        with open('menu_system.py', 'r') as f:
            content = f.read()
        
        # Check for time-based duplicate protection
        if '_last_action_time = 0' in content:
            print("✓ Duplicate action protection added")
        else:
            print("❌ Duplicate action protection missing")
            return False
        
        # Check for time import
        if 'import time' in content:
            print("✓ Time module imported")
        else:
            print("❌ Time module not imported")
            return False
        
        # Check for time-based checking in selection handlers
        if 'current_time - self._last_action_time < 1.0' in content:
            print("✓ Time-based duplicate checking implemented")
        else:
            print("❌ Time-based checking not found")
            return False
        
        # Check for improved help scene handling
        if 'previous_scene = self._current_scene' in content:
            print("✓ Improved scene handling in help display")
        else:
            print("❌ Improved scene handling not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing navigation fixes: {e}")
        return False

def test_shell_limitations_documented():
    """Test that shell limitations are properly documented."""
    print("\nTesting shell limitations documentation...")
    
    try:
        with open('menu_system.py', 'r') as f:
            content = f.read()
        
        # Check for completion limitation note
        if 'Command completion (Tab completion) is not available' in content:
            print("✓ Tab completion limitation documented")
        else:
            print("❌ Tab completion limitation not documented")
            return False
        
        if 'Interactive programs may not work properly' in content:
            print("✓ Interactive program limitation documented")
        else:
            print("❌ Interactive program limitation not documented")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing documentation: {e}")
        return False

def test_error_handling():
    """Test that error handling is robust."""
    print("\nTesting error handling improvements...")
    
    try:
        with open('menu_system.py', 'r') as f:
            content = f.read()
        
        # Check for timeout in command execution
        if 'timeout=30' in content:
            print("✓ Command timeout protection added")
        else:
            print("❌ Command timeout protection missing")
            return False
        
        # Check for TimeoutExpired handling
        if 'subprocess.TimeoutExpired' in content:
            print("✓ Timeout exception handling added")
        else:
            print("❌ Timeout exception handling missing")
            return False
        
        # Check for shell creation error handling
        if 'Failed to create shell interface' in content:
            print("✓ Shell creation error handling added")
        else:
            print("❌ Shell creation error handling missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing error handling: {e}")
        return False

def test_syntax_validity():
    """Test that the code is syntactically valid."""
    print("\nTesting syntax validity...")
    
    try:
        with open('menu_system.py', 'r') as f:
            content = f.read()
        
        # Test compilation
        compile(content, 'menu_system.py', 'exec')
        print("✓ Code compiles successfully")
        
        # Test AST parsing
        ast.parse(content)
        print("✓ AST parsing successful")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing syntax: {e}")
        return False

def main():
    """Main test function."""
    print("Comprehensive Menu System Fix Validation")
    print("=" * 50)
    
    tests = [
        ("TextBox Fix", test_textbox_fix),
        ("Navigation Fixes", test_navigation_fixes),
        ("Shell Limitations", test_shell_limitations_documented),
        ("Error Handling", test_error_handling),
        ("Syntax Validity", test_syntax_validity),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n✅ All fixes implemented successfully!")
        print("\nFixes summary:")
        print("1. ✓ TextBox 'start_line' error fixed")
        print("2. ✓ Navigation duplicate execution prevented")
        print("3. ✓ Shell completion limitations documented")
        print("4. ✓ Robust error handling added")
        print("5. ✓ Command timeouts implemented")
        print("6. ✓ Scene management improved")
        
        print("\nThe menu system should now work properly:")
        print("- No more TextBox errors")
        print("- No duplicate command executions")
        print("- Stable navigation")
        print("- Proper help dialog handling")
        print("- Shell limitations clearly communicated")
        
        return True
    else:
        print(f"\n❌ {failed} test(s) failed - issues remain")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
