#!/usr/bin/env python3
"""
Test script to verify the menu system works correctly.
This script creates a minimal test configuration and runs the menu.
"""

import yaml
import os
import sys

def create_test_config():
    """Create a test configuration file if the main one doesn't exist."""
    if not os.path.exists('config.yml'):
        test_config = {
            'menu_title': 'Test TUI Menu System',
            'menu_items': [
                {
                    'name': 'Test Category 1',
                    'button_info': 'This is a test category with sample commands.',
                    'items': [
                        {
                            'name': 'List Directory',
                            'command': 'ls -la',
                            'button_info': 'Lists files in the current directory'
                        },
                        {
                            'name': 'Show Date',
                            'command': 'date',
                            'button_info': 'Displays the current date and time'
                        },
                        {
                            'name': 'Show System Info',
                            'command': 'uname -a',
                            'button_info': 'Shows system information'
                        }
                    ]
                },
                {
                    'name': 'Test Category 2',
                    'button_info': 'Another test category with different commands.',
                    'items': [
                        {
                            'name': 'Current User',
                            'command': 'whoami',
                            'button_info': 'Shows the current username'
                        },
                        {
                            'name': 'Current Directory',
                            'command': 'pwd',
                            'button_info': 'Shows the current working directory'
                        }
                    ]
                }
            ]
        }
        
        with open('config.yml', 'w') as f:
            yaml.dump(test_config, f, default_flow_style=False)
        
        print("Created test config.yml file")
        return True
    
    return False

def main():
    """Main test function."""
    print("Testing TUI Menu System...")
    
    # Check if asciimatics is available
    try:
        import asciimatics
        print("✓ asciimatics is available")
    except ImportError:
        print("✗ asciimatics not found. Install with: pip install asciimatics")
        return False
    
    # Check if PyYAML is available
    try:
        import yaml
        print("✓ PyYAML is available")
    except ImportError:
        print("✗ PyYAML not found. Install with: pip install PyYAML")
        return False
    
    # Create test config if needed
    create_test_config()
    
    # Import and test the menu system
    try:
        from menu_system import MenuSystem
        print("✓ Menu system module imported successfully")
        
        print("\nStarting menu system...")
        print("Use F1 for help, arrows to navigate, Enter to select")
        print("Press Ctrl+C or 'q' to exit")
        print("-" * 50)
        
        menu = MenuSystem()
        menu.run()
        
    except Exception as e:
        print(f"✗ Error running menu system: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    
    print("\nMenu system test completed successfully!")
