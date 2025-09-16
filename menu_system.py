#!/usr/bin/env python3
"""
Multi-level TUI Menu System using Asciimatics
Reads configuration from config.yml and provides a hierarchical menu interface.
"""

import yaml
import os
import subprocess
import sys
import time
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


class ShellFrame(Frame):
    """Interactive shell frame within the TUI."""
    
    def __init__(self, screen, menu_system):
        super(ShellFrame, self).__init__(screen,
                                       screen.height,
                                       screen.width,
                                       has_border=False,
                                       title="Interactive Shell")
        
        self._menu_system = menu_system
        self._current_dir = os.getcwd()
        self._command_history = []
        self._history_index = 0
        
        # Main layout
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        # Title
        layout.add_widget(Label("=== Interactive Command Shell ===", align="^"))
        layout.add_widget(Divider())
        
        # Output area
        self._output = TextBox(height=screen.height - 8,
                              as_string=True,
                              readonly=True,
                              line_wrap=True)
        self._output.value = self._get_initial_text()
        layout.add_widget(self._output)
        
        # Input area
        layout.add_widget(Divider())
        
        # Command input layout
        input_layout = Layout([20, 80])
        self.add_layout(input_layout)
        
        # Prompt
        self._prompt_label = Label(self._get_prompt())
        input_layout.add_widget(self._prompt_label, 0)
        
        # Command input - make it focusable by default
        self._command_input = Text()
        input_layout.add_widget(self._command_input, 1)
        
        # Button layout
        button_layout = Layout([25, 25, 25, 25])
        self.add_layout(button_layout)
        button_layout.add_widget(Button("Execute", self._execute_command), 0)
        button_layout.add_widget(Button("Clear", self._clear_output), 1)
        button_layout.add_widget(Button("Help", self._show_help), 2)
        button_layout.add_widget(Button("← Back to Menu", self._back_to_menu), 3)
        
        self.fix()
    
    def _get_initial_text(self):
        """Get initial shell text."""
        text = "Interactive Command Shell\n"
        text += "=" * 50 + "\n\n"
        text += f"Current directory: {self._current_dir}\n"
        text += "Type commands and press Execute or Enter\n"
        text += "Type 'exit' to return to menu\n"
        text += "Type 'help' for available commands\n\n"
        return text
    
    def _get_prompt(self):
        """Get the current shell prompt."""
        return f"[{os.path.basename(self._current_dir)}]$ "
    
    def _execute_command(self):
        """Execute the entered command."""
        command = self._command_input.value.strip()
        
        if not command:
            return
        
        # Add to history
        if command not in self._command_history:
            self._command_history.append(command)
        
        # Add command to output
        current_output = self._output.value
        current_output += f"{self._get_prompt()}{command}\n"
        
        # Handle special commands
        if command.lower() in ['exit', 'quit']:
            current_output += "Returning to menu...\n"
            self._output.value = current_output
            self.screen.refresh()
            self._back_to_menu()
            return
        
        if command.lower() == 'help':
            current_output += self._get_help_text() + "\n"
            self._output.value = current_output
            self._command_input.value = ""
            self.screen.refresh()
            return
        
        if command.lower() == 'clear':
            self._clear_output()
            return
        
        # Handle cd command
        if command.startswith('cd '):
            new_dir = command[3:].strip()
            try:
                if not new_dir:
                    new_dir = os.path.expanduser('~')
                os.chdir(os.path.expanduser(new_dir))
                self._current_dir = os.getcwd()
                current_output += f"Changed directory to: {self._current_dir}\n"
                self._prompt_label.text = self._get_prompt()
            except Exception as e:
                current_output += f"cd: {e}\n"
            
            self._output.value = current_output + "\n"
            self._command_input.value = ""
            self.screen.refresh()
            return
        
        # Execute other commands
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self._current_dir,
                timeout=30  # 30 second timeout
            )
            
            if result.stdout:
                current_output += result.stdout
            if result.stderr:
                current_output += result.stderr
            if result.returncode != 0:
                current_output += f"\n[Command exited with code {result.returncode}]\n"
            
        except subprocess.TimeoutExpired:
            current_output += "Command timed out after 30 seconds\n"
        except Exception as e:
            current_output += f"Error executing command: {e}\n"
        
        current_output += "\n"
        self._output.value = current_output
        self._command_input.value = ""
        
        # Auto-scroll to bottom by updating the value which will trigger refresh
        lines = current_output.split('\n')
        if len(lines) > 20:  # If more than ~20 lines, show recent output
            recent_lines = lines[-15:]  # Show last 15 lines
            self._output.value = '\n'.join(recent_lines)
        
        self.screen.refresh()
    
    def _get_help_text(self):
        """Get help text for shell commands."""
        return """Available commands:
  help        - Show this help
  exit, quit  - Return to menu
  clear       - Clear output
  cd <dir>    - Change directory
  pwd         - Show current directory
  ls          - List files
  Any other shell command...

Navigation:
  Tab/Shift+Tab - Navigate between fields
  Enter         - Execute command
  Esc           - Return to menu

Note: This is a TUI-based shell interface.
Command completion (Tab completion) is not available.
Interactive programs may not work properly.
For full shell features, use the system terminal."""
    
    def _clear_output(self):
        """Clear the output area."""
        self._output.value = self._get_initial_text()
        self.screen.refresh()
    
    def _show_help(self):
        """Show help."""
        current_output = self._output.value
        current_output += f"{self._get_prompt()}help\n"
        current_output += self._get_help_text() + "\n\n"
        self._output.value = current_output
        self.screen.refresh()
    
    def _back_to_menu(self):
        """Return to the main menu."""
        self._menu_system.show_main_menu()
    
    def process_event(self, event):
        """Process keyboard events."""
        if isinstance(event, KeyboardEvent):
            if event.key_code == Screen.KEY_ESCAPE:
                self._back_to_menu()
                return None
            elif event.key_code == 10 or event.key_code == 13:  # Enter key
                # Execute command when Enter is pressed
                self._execute_command()
                return None
        
        return super(ShellFrame, self).process_event(event)


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
        self._last_action_time = 0  # Prevent rapid duplicate actions
        
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
        current_time = time.time()
        # Prevent rapid duplicate selections (within 1 second)
        if current_time - self._last_action_time < 1.0:
            return
        self._last_action_time = current_time
        
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
                    # Execute command with timeout
                    result = subprocess.run(
                        command, 
                        shell=True, 
                        capture_output=True, 
                        text=True, 
                        timeout=30
                    )
                    
                    # Show result
                    result_text = f"Command: {command}\n\n"
                    if result.returncode == 0:
                        result_text += f"Output:\n{result.stdout}"
                        if result.stderr:
                            result_text += f"\nWarnings:\n{result.stderr}"
                    else:
                        result_text += f"Error (exit code {result.returncode}):\n{result.stderr}"
                        if result.stdout:
                            result_text += f"\nOutput:\n{result.stdout}"
                    
                    result_text += f"\n\nPress Enter or Close to return to menu."
                    self._menu_system.show_help(result_text)
                    
                except subprocess.TimeoutExpired:
                    self._menu_system.show_help(f"Command '{command}' timed out after 30 seconds.\n\nPress Enter or Close to return to menu.")
                except Exception as e:
                    self._menu_system.show_help(f"Error executing command '{command}':\n{str(e)}\n\nPress Enter or Close to return to menu.")
                
                # Reset status after help is shown
                self._status_text.value = "Use arrows to navigate, Enter to select, F1 for help"
                self.screen.refresh()
            else:
                self._menu_system.show_help("No command defined for this item.\n\nPress Enter or Close to return to menu.")
    
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
        self._last_action_time = 0  # Prevent rapid duplicate actions
        
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
        current_time = time.time()
        # Prevent rapid duplicate selections (within 1 second)
        if current_time - self._last_action_time < 1.0:
            return
        self._last_action_time = current_time
        
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
            # Store the current scene before showing help
            previous_scene = self._current_scene
            try:
                help_frame = HelpPanel(self._screen, help_text)
                help_scene = Scene([help_frame], -1, name="help")
                self._screen.play([help_scene], stop_on_resize=True, start_scene=help_scene)
            except StopApplication:
                pass  # Help was closed
            
            # Always return to the previous scene
            if previous_scene:
                self._current_scene = previous_scene
                self._screen.play([self._current_scene], stop_on_resize=True, start_scene=self._current_scene)
    
    def open_shell(self):
        """Open an interactive command shell."""
        if self._screen:
            try:
                shell_frame = ShellFrame(self._screen, self)
                self._current_scene = Scene([shell_frame], -1, name="shell")
                self._screen.play([self._current_scene], stop_on_resize=True, start_scene=self._current_scene)
            except Exception as e:
                # If shell frame fails, show error and return to menu
                error_text = f"Shell Error: {e}\n\nFailed to create shell interface.\nReturning to main menu..."
                self.show_help(error_text)
                self.show_main_menu()
    
    def run(self):
        """Run the menu system."""
        while True:
            try:
                Screen.wrapper(self._run_with_screen)
                break
            except ResizeScreenError:
                # Handle screen resize
                continue
    
    def _run_with_screen(self, screen):
        """Run with screen context."""
        self._screen = screen
        self.show_main_menu()
    


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
