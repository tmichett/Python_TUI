# RHCI Instructor VT Toolkit - Standalone Executable

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
