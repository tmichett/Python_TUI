#!/usr/bin/env python3
"""
Demo script to show the interactive shell functionality
without needing the full TUI dependencies.
"""

import os
import subprocess
import sys

def run_interactive_shell():
    """Standalone version of the interactive shell."""
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 60)
    print("Interactive Command Shell Demo")
    print("=" * 60)
    print("This demonstrates the shell functionality that will be")
    print("integrated into the TUI menu system.")
    print("Type commands and press Enter to execute them.")
    print("Type 'exit' to quit this demo.")
    print("Type 'help' for shell commands help.")
    print("-" * 60)
    
    while True:
        try:
            # Get current directory for prompt
            current_dir = os.getcwd()
            prompt = f"[{os.path.basename(current_dir)}]$ "
            
            # Get user input
            command = input(prompt).strip()
            
            if not command:
                continue
            
            # Handle exit command - demonstrate proper exit behavior
            command_clean = command.lower().strip()
            if command_clean in ['exit', 'quit']:
                print(f"\nDetected exit command: '{command_clean}'")
                print("Exiting shell demo...")
                break
            
            # Handle help command
            if command.lower() == 'help':
                print("\nAvailable commands:")
                print("  help    - Show this help")
                print("  exit    - Exit demo")
                print("  quit    - Exit demo")
                print("  clear   - Clear screen")
                print("  pwd     - Show current directory")
                print("  ls      - List directory contents")
                print("  cd <dir> - Change directory")
                print("  Any other shell command...")
                print()
                continue
            
            # Handle clear command
            if command.lower() == 'clear':
                os.system('clear' if os.name == 'posix' else 'cls')
                print("Interactive Command Shell Demo - Type 'exit' to quit")
                print("-" * 60)
                continue
            
            # Handle cd command specially
            if command.startswith('cd '):
                try:
                    new_dir = command[3:].strip()
                    if not new_dir:
                        new_dir = os.path.expanduser('~')
                    os.chdir(os.path.expanduser(new_dir))
                    print(f"Changed directory to: {os.getcwd()}")
                except Exception as e:
                    print(f"cd: {e}")
                continue
            
            # Execute other commands
            try:
                result = subprocess.run(command, shell=True, text=True)
                if result.returncode != 0:
                    print(f"\n[Command exited with code {result.returncode}]")
            except Exception as e:
                print(f"Error executing command: {e}")
            
            print()  # Add blank line after command output
            
        except KeyboardInterrupt:
            print("\n\nUse 'exit' to quit the demo.")
            continue
        except EOFError:
            print("\nExiting shell demo...")
            break

def main():
    """Main demo function."""
    print("Shell Functionality Demo")
    print("This shows the interactive shell that has been added")
    print("to the TUI menu system.\n")
    
    try:
        run_interactive_shell()
        print("\n✅ Shell demo completed!")
        print("This same functionality is now integrated into the")
        print("TUI menu system as the '🖥️ Command Shell' option.")
        
    except Exception as e:
        print(f"Demo error: {e}")

if __name__ == "__main__":
    main()
