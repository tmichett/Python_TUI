# Python TUI Menu System

A multi-level Terminal User Interface (TUI) menu system built with asciimatics that reads configuration from YAML files.

## Features

- **Multi-level Navigation**: Hierarchical menu system with main categories and sub-menus
- **YAML Configuration**: All menu structure defined in `config.yml`
- **Contextual Help**: Built-in help system with `button_info` descriptions
- **Command Execution**: Execute shell commands directly from menu items
- **Interactive Shell**: Built-in command shell for typing custom commands
- **Keyboard Navigation**: Full keyboard control with intuitive navigation
- **Responsive Design**: Handles screen resizing gracefully

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install asciimatics>=1.15.0 PyYAML>=6.0
   ```

2. **Make Scripts Executable**:
   ```bash
   chmod +x menu_system.py test_menu.py
   ```

## Usage

### Basic Usage

Run the menu system with your existing `config.yml`:
```bash
python menu_system.py
```

### Test Mode

To test the system with sample data:
```bash
python test_menu.py
```

This will create a test `config.yml` if one doesn't exist and run the menu system.

### Demo Mode

To test just the interactive shell functionality (without TUI dependencies):
```bash
python demo_shell.py
```

This demonstrates the command shell that's integrated into the menu system.

## Configuration

The menu system reads its structure from `config.yml`. Here's the format:

```yaml
menu_title: Your Application Title

menu_items:
  - name: Category Name
    button_info: |
      Description of what this category contains
    items:
      - name: Menu Item 1
        command: echo "Command to execute"
        button_info: |
          Detailed description of what this item does
      - name: Menu Item 2
        command: ls -la
        button_info: |
          Another description
          
  - name: Another Category
    items:
      - name: Some Action
        command: date
```

### Configuration Fields

- **menu_title**: Main title displayed at the top of the menu
- **menu_items**: List of main menu categories
  - **name**: Display name for the category
  - **button_info** _(optional)_: Help text for the category
  - **items**: List of sub-menu items
    - **name**: Display name for the menu item
    - **command**: Shell command to execute
    - **button_info** _(optional)_: Help text for the item

## Navigation

### Main Menu
- **↑↓ arrows**: Navigate between categories
- **Enter**: Enter selected category
- **F1**: Show help
- **q/Esc**: Exit application

### Sub-Menus
- **↑↓ arrows**: Navigate between items
- **Enter**: Execute selected command
- **F1**: Show contextual help
- **Esc**: Return to main menu
- **← Back to Main Menu**: Navigation option

### Help System
- **F1**: Context-sensitive help anywhere in the application
- **Enter**: Close help panels

## Command Execution

When you select a menu item with a command:

1. The command is executed using the system shell
2. Output is captured and displayed in a help panel
3. Both stdout and stderr are shown
4. Exit codes are displayed for failed commands

## Interactive Shell

The menu system includes a built-in interactive shell accessible from both the main menu and sub-menus:

### Features
- **Full Shell Access**: Type any command as if you were in a terminal
- **Directory Navigation**: Use `cd` to change directories
- **Built-in Commands**: 
  - `help` - Show available shell commands
  - `clear` - Clear the screen
  - `exit` or `quit` - Return to menu
- **Command History**: Standard shell command execution with real-time output
- **Error Handling**: Graceful handling of invalid commands

### Usage
1. Select **🖥️ Command Shell** from any menu
2. Type commands and press Enter
3. Use `exit` to return to the menu
4. All standard shell commands are available (`ls`, `pwd`, `cd`, etc.)

## File Structure

```
Python_TUI/
├── menu_system.py      # Main TUI application
├── test_menu.py        # Test script with sample data
├── config.yml          # Your menu configuration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Example Configuration

The included `config.yml` provides a complete example for an RHCI Instructor toolkit with multiple categories and various system administration commands.

## Error Handling

- **Missing config.yml**: Application exits with error message
- **Invalid YAML**: Parser errors are displayed
- **Command failures**: Error output and exit codes are shown
- **Screen resize**: Application handles terminal resizing gracefully

## Troubleshooting

### Dependencies
If you get import errors:
```bash
pip install asciimatics PyYAML
```

### Configuration Issues
- Ensure `config.yml` is in the same directory as `menu_system.py`
- Validate YAML syntax using `python -c "import yaml; yaml.safe_load(open('config.yml'))"`

### Display Issues
- Ensure your terminal supports color and cursor control
- Try resizing the terminal window if display appears corrupted
- Use `python test_menu.py` to verify basic functionality

## Development

The menu system is built with a modular architecture:

- **MenuConfig**: Handles YAML loading and parsing
- **MainMenuFrame**: Main menu display and navigation
- **SubMenuFrame**: Sub-menu display and command execution
- **HelpPanel**: Contextual help display
- **MenuSystem**: Coordinator class managing screen and navigation

## Contributing

When modifying the code:

1. Follow PEP 8 style guidelines
2. Add type hints for new functions
3. Update help text and documentation
4. Test with various terminal sizes
5. Ensure keyboard navigation remains intuitive

---

Built with [asciimatics](https://github.com/peterbrittain/asciimatics) - A package to help people create full-screen text UIs.
