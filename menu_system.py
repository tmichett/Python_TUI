#!/usr/bin/env python3
"""
Multi-level TUI Menu System using Asciimatics
Reads configuration from config.yml and provides a hierarchical menu interface.
"""

import yaml
import os
import subprocess
import sys
from typing import Dict, List, Any, Optional
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, Button, TextBox, Label, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.event import KeyboardEvent


class MenuConfig:
    """Handles loading and parsing of the YAML configuration file."""
    
    def __init__(self, config_path: str = "config.yml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: Configuration file '{self.config_path}' not found.")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            sys.exit(1)
    
    @property
    def title(self) -> str:
        """Get the main menu title."""
        return self.config.get('menu_title', 'TUI Menu System')
    
    @property
    def menu_items(self) -> List[Dict[str, Any]]:
        """Get the main menu items."""
        return self.config.get('menu_items', [])


class HelpPanel(Frame):
    """A frame that displays contextual help information."""
    
    def __init__(self, screen, help_text: str = ""):
        super(HelpPanel, self).__init__(screen,
                                      screen.height // 2,
                                      screen.width // 2,
                                      has_border=True,
                                      title="Help",
                                      x=(screen.width - screen.width // 2) // 2,
                                      y=(screen.height - screen.height // 2) // 2)
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        # Help text display
        self._help_text = TextBox(height=Widget.FILL_FRAME,
                                 as_string=True,
                                 readonly=True)
        self._help_text.value = help_text or "No help information available."
        layout.add_widget(self._help_text)
        
        # Close button
        layout2 = Layout([100])
        self.add_layout(layout2)
        layout2.add_widget(Button("Close", self._close))
        
        self.fix()
    
    def _close(self):
        """Close the help panel."""
        raise StopApplication("Close help")


class SubMenuFrame(Frame):
    """Frame for displaying sub-menu items."""
    
    def __init__(self, screen, menu_item: Dict[str, Any], menu_system):
        super(SubMenuFrame, self).__init__(screen,
                                         screen.height,
                                         screen.width,
                                         has_border=False,
                                         title=menu_item['name'])
        
        self._menu_item = menu_item
        self._menu_system = menu_system
        self._current_selection = 0
        
        # Main layout
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        # Title
        layout.add_widget(Label(f"=== {menu_item['name']} ===", align="^"))
        layout.add_widget(Divider())
        
        # Menu items list
        items = menu_item.get('items', [])
        menu_options = [(item['name'], i) for i, item in enumerate(items)]
        menu_options.append(("← Back to Main Menu", -1))
        menu_options.append(("Help", -2))
        menu_options.append(("Exit", -3))
        
        self._menu_list = ListBox(height=Widget.FILL_FRAME,
                                options=menu_options,
                                add_scroll_bar=True,
                                on_select=self._on_select,
                                on_change=self._on_change)
        layout.add_widget(self._menu_list)
        
        # Status/help area
        layout.add_widget(Divider())
        self._status_text = Text(label="Status:", disabled=True)
        self._status_text.value = "Use arrows to navigate, Enter to select, F1 for help"
        layout.add_widget(self._status_text)
        
        self.fix()
    
    def _on_change(self):
        """Handle selection changes to update help text."""
        selection = self._menu_list.value
        self._current_selection = selection
        
        if selection >= 0 and selection < len(self._menu_item.get('items', [])):
            item = self._menu_item['items'][selection]
            help_info = item.get('button_info', f"Execute: {item.get('command', 'No command')}")
            self._status_text.value = f"Help: {help_info.strip()}"
        else:
            self._status_text.value = "Use arrows to navigate, Enter to select, F1 for help"
    
    def _on_select(self):
        """Handle menu item selection."""
        selection = self._menu_list.value
        
        if selection == -1:  # Back to main menu
            self._menu_system.show_main_menu()
        elif selection == -2:  # Help
            self._show_help()
        elif selection == -3:  # Exit
            raise StopApplication("User requested exit")
        elif selection >= 0:
            # Execute command
            self._execute_command(selection)
    
    def _show_help(self):
        """Show help for current selection."""
        selection = self._current_selection
        help_text = "Navigation Help:\n\n"
        help_text += "↑↓ - Navigate menu items\n"
        help_text += "Enter - Select item\n"
        help_text += "F1 - Show this help\n"
        help_text += "Esc - Back to main menu\n\n"
        
        if selection >= 0 and selection < len(self._menu_item.get('items', [])):
            item = self._menu_item['items'][selection]
            help_text += f"Selected Item: {item['name']}\n\n"
            button_info = item.get('button_info', 'No additional information available.')
            help_text += f"Description:\n{button_info}"
        
        self._menu_system.show_help(help_text)
    
    def _execute_command(self, selection: int):
        """Execute the command for the selected menu item."""
        items = self._menu_item.get('items', [])
        if selection < len(items):
            item = items[selection]
            command = item.get('command', '')
            
            if command:
                # Update status
                self._status_text.value = f"Executing: {command}"
                self.screen.refresh()
                
                try:
                    # Execute command
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    
                    # Show result
                    result_text = f"Command: {command}\n\n"
                    if result.returncode == 0:
                        result_text += f"Output:\n{result.stdout}"
                    else:
                        result_text += f"Error (exit code {result.returncode}):\n{result.stderr}"
                    
                    self._menu_system.show_help(result_text)
                    
                except Exception as e:
                    self._menu_system.show_help(f"Error executing command: {str(e)}")
                
                # Reset status
                self._status_text.value = "Command completed. Press F1 for help."
            else:
                self._menu_system.show_help("No command defined for this item.")
    
    def process_event(self, event):
        """Process keyboard events."""
        if isinstance(event, KeyboardEvent):
            if event.key_code == Screen.KEY_F1:
                self._show_help()
                return None
            elif event.key_code == Screen.KEY_ESCAPE:
                self._menu_system.show_main_menu()
                return None
        
        return super(SubMenuFrame, self).process_event(event)


class MainMenuFrame(Frame):
    """Frame for the main menu."""
    
    def __init__(self, screen, config: MenuConfig, menu_system):
        super(MainMenuFrame, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          has_border=False,
                                          title=config.title)
        
        self._config = config
        self._menu_system = menu_system
        self._current_selection = 0
        
        # Main layout
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        # Title
        layout.add_widget(Label(f"=== {config.title} ===", align="^"))
        layout.add_widget(Divider())
        
        # Menu items
        menu_options = [(item['name'], i) for i, item in enumerate(config.menu_items)]
        menu_options.append(("💻 Command Shell", -1))
        menu_options.append(("Help", -2))
        menu_options.append(("Exit", -3))
        
        self._menu_list = ListBox(height=Widget.FILL_FRAME,
                                options=menu_options,
                                add_scroll_bar=True,
                                on_select=self._on_select,
                                on_change=self._on_change)
        layout.add_widget(self._menu_list)
        
        # Status area
        layout.add_widget(Divider())
        self._status_text = Text(label="Status:", disabled=True)
        self._status_text.value = "Select a menu category to continue"
        layout.add_widget(self._status_text)
        
        self.fix()
    
    def _on_change(self):
        """Handle selection changes to update status."""
        selection = self._menu_list.value
        self._current_selection = selection
        
        if selection >= 0 and selection < len(self._config.menu_items):
            item = self._config.menu_items[selection]
            help_info = item.get('button_info', f"Category: {item['name']}")
            self._status_text.value = f"Info: {help_info.strip()}"
        elif selection == -1:  # Command Shell
            self._status_text.value = "Open interactive command shell - type your own commands"
        else:
            self._status_text.value = "Use arrows to navigate, Enter to select, F1 for help"
    
    def _on_select(self):
        """Handle main menu selection."""
        selection = self._menu_list.value
        
        if selection == -1:  # Command Shell
            self._menu_system.open_shell()
        elif selection == -2:  # Help
            self._show_help()
        elif selection == -3:  # Exit
            raise StopApplication("User requested exit")
        elif selection >= 0:
            # Show submenu
            menu_item = self._config.menu_items[selection]
            self._menu_system.show_submenu(menu_item)
    
    def _show_help(self):
        """Show main menu help."""
        help_text = "RHCI Instructor VT Toolkit - Help\n\n"
        help_text += "Navigation:\n"
        help_text += "↑↓ - Navigate menu categories\n"
        help_text += "Enter - Select category\n"
        help_text += "F1 - Show this help\n"
        help_text += "Esc/q - Exit application\n\n"
        help_text += "💻 Command Shell:\n"
        help_text += "Opens an interactive command shell where you can type\n"
        help_text += "your own commands. Type 'exit' to return to the menu.\n\n"
        help_text += "Menu Categories:\n"
        
        for item in self._config.menu_items:
            help_text += f"\n• {item['name']}\n"
            if 'button_info' in item:
                help_text += f"  {item['button_info'].strip()}\n"
        
        self._menu_system.show_help(help_text)
    
    def process_event(self, event):
        """Process keyboard events."""
        if isinstance(event, KeyboardEvent):
            if event.key_code == Screen.KEY_F1:
                self._show_help()
                return None
            elif event.key_code == Screen.KEY_ESCAPE or event.key_code == ord('q'):
                raise StopApplication("User requested exit")
        
        return super(MainMenuFrame, self).process_event(event)


class MenuSystem:
    """Main menu system coordinator."""
    
    def __init__(self):
        self._config = MenuConfig()
        self._screen = None
        self._current_scene = None
    
    def show_main_menu(self):
        """Display the main menu."""
        if self._screen:
            main_frame = MainMenuFrame(self._screen, self._config, self)
            self._current_scene = Scene([main_frame], -1, name="main_menu")
            self._screen.play([self._current_scene], stop_on_resize=True, start_scene=self._current_scene)
    
    def show_submenu(self, menu_item: Dict[str, Any]):
        """Display a submenu."""
        if self._screen:
            submenu_frame = SubMenuFrame(self._screen, menu_item, self)
            self._current_scene = Scene([submenu_frame], -1, name="submenu")
            self._screen.play([self._current_scene], stop_on_resize=True, start_scene=self._current_scene)
    
    def show_help(self, help_text: str):
        """Display help information."""
        if self._screen:
            try:
                help_frame = HelpPanel(self._screen, help_text)
                help_scene = Scene([help_frame], -1, name="help")
                self._screen.play([help_scene], stop_on_resize=True, start_scene=help_scene)
            except StopApplication:
                # Return to current scene after help is closed
                if self._current_scene:
                    self._screen.play([self._current_scene], stop_on_resize=True, start_scene=self._current_scene)
    
    def open_shell(self):
        """Open an interactive command shell."""
        if self._screen:
            # Temporarily exit the TUI to run shell
            raise StopApplication("Open shell")
    
    def run(self):
        """Run the menu system."""
        while True:
            try:
                Screen.wrapper(self._run_with_screen)
                break
            except ResizeScreenError:
                # Handle screen resize
                continue
            except StopApplication as e:
                if str(e) == "Open shell":
                    print("DEBUG: Opening interactive shell...")
                    self._run_interactive_shell()
                    print("DEBUG: Shell session completed, restarting menu...")
                    continue
                else:
                    print(f"DEBUG: StopApplication received: {e}")
                    break
    
    def _run_with_screen(self, screen):
        """Run with screen context."""
        self._screen = screen
        self.show_main_menu()
    
    def _run_interactive_shell(self):
        """Run an interactive command shell."""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 60)
        print("Interactive Command Shell")
        print("=" * 60)
        print("Type commands and press Enter to execute them.")
        print("Type 'exit' to return to the menu.")
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
                
                # Handle exit command - be very explicit about this
                command_clean = command.lower().strip()
                if command_clean in ['exit', 'quit']:
                    print(f"\nDetected exit command: '{command_clean}'")
                    print("Returning to menu...")
                    break
                
                # Handle help command
                if command.lower() == 'help':
                    print("\nAvailable commands:")
                    print("  help    - Show this help")
                    print("  exit    - Return to menu (NOT shell exit!)")
                    print("  quit    - Return to menu")
                    print("  clear   - Clear screen")
                    print("  pwd     - Show current directory")
                    print("  ls      - List directory contents")
                    print("  cd <dir> - Change directory")
                    print("  Any other shell command...")
                    print("\nIMPORTANT: Type 'exit' to return to menu, not to exit the shell!")
                    print()
                    continue
                
                # Handle clear command
                if command.lower() == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    print("Interactive Command Shell - Type 'exit' to return to menu")
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
                
                # Prevent shell exit commands from terminating our application
                if command.lower().strip() in ['exit', 'quit', 'logout']:
                    print("To return to menu, just type: exit")
                    print("(Don't use shell exit commands)")
                    continue
                
                # Execute other commands
                try:
                    result = subprocess.run(command, shell=True, text=True)
                    # subprocess.run with shell=True will automatically display output
                    # No need to capture it for interactive shell
                    if result.returncode != 0:
                        print(f"\n[Command exited with code {result.returncode}]")
                except Exception as e:
                    print(f"Error executing command: {e}")
                
                print()  # Add blank line after command output
                
            except KeyboardInterrupt:
                print("\n\nUse 'exit' to return to menu.")
                continue
            except EOFError:
                print("\nReturning to menu...")
                break
        
        # Brief pause before returning to menu
        print("\n" + "=" * 60)
        print("Shell session ended. Returning to menu...")
        print("Press Enter to continue...")
        try:
            input()
        except (KeyboardInterrupt, EOFError):
            print("Forcing return to menu...")
        
        os.system('clear' if os.name == 'posix' else 'cls')
        print("DEBUG: Shell cleanup complete, returning to menu system...")


def main():
    """Main entry point."""
    try:
        menu_system = MenuSystem()
        menu_system.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
