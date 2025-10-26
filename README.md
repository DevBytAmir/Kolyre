# Kolyre

![Version](https://img.shields.io/badge/version-2.0.0-FF8C00?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10%2B-27496D?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-cross--platform-455A64?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-388E3C?style=for-the-badge)

**Kolyre** is a lightweight Python library for **styling and coloring terminal text using ANSI codes**, supporting standard and extended colors, text styles, and 24-bit RGB (truecolor) output.

## Features

- **Text Styles:** Bold, Dim, Italic, Underline, Reversed, Strikethrough, Overline
- **Colors:** Standard 16 colors + bright variants for foreground and background
- **256-Color Palette:** Extended ANSI palette (0–255)
- **Truecolor (RGB) Support:** 24-bit RGB for precise coloring
- **Cross-Platform:** Works on Linux, macOS, and Windows
- **Package:** Installable via GitHub (no external dependencies)

## Installation

Install Kolyre via **pip** (recommended):

```bash
pip install git+https://github.com/DevBytAmir/kolyre.git
```

For manual installation, download the repository from [GitHub](https://github.com/DevBytAmir/kolyre) and place the `kolyre` folder (containing `__init__.py`, `core.py`, and `demo.py`) in your project directory.

## Quick Start

```python
from kolyre import Kolyre

# Store ANSI codes in variables
red = Kolyre.Foreground.RED
bold = Kolyre.Style.BOLD

# Use variables or codes directly
print(f"{red}Hello World{Kolyre.Style.RESET}")
print(f"{bold}{Kolyre.Foreground.CYAN}Bold and Cyan{Kolyre.Style.RESET}")
print(f"{Kolyre.Background.WHITE}Text with white background{Kolyre.Style.RESET_BACKGROUND}")

# Using the colorize method to combine multiple styles
print(Kolyre.colorize("Bold, Yellow, and Underlined", Kolyre.Style.BOLD, Kolyre.Foreground.YELLOW, Kolyre.Style.UNDERLINE))

# 256-color example
print(f"{Kolyre.foreground_256(128)}Hello 256-color{Kolyre.Style.RESET}")

# Truecolor example using a variable
rgb_color = (255, 100, 50)
print(f"{Kolyre.foreground_rgb(rgb_color)}Hello RGB{Kolyre.Style.RESET}")

# Truecolor example parameter by parameter
print(f"{Kolyre.background_rgb(50, 200, 150)}Hello RGB{Kolyre.Style.RESET}")

# Truecolor example using hex
print(f"{Kolyre.foreground_rgb("#FF8800")}Hello Hex RGB{Kolyre.Style.RESET}")
```

## Demo

Kolyre includes a built-in demo showcasing:

- Text styles (bold, italic, underline, etc.)
- Standard 16-color palette
- 256-color palette
- Truecolor (RGB) gradients

### Demo Execution

#### Installed via pip

Run the demo from anywhere:

```bash
kolyre --all
```

#### Local Clone Execution

If you cloned the repository and have not installed the package, run from the project root:

```bash
python -m kolyre.demo --all
```

This launches the full demo and previews all available styling features.

### Command-Line Options

You can run individual demo parts or modify execution behavior:

```bash
kolyre --styles       # Show all text styles
kolyre --palette16    # Show 16-color ANSI palette
kolyre --palette256   # Show extended 256-color palette
kolyre --rgb          # Show truecolor RGB gradient
kolyre --all          # Run all demos
kolyre --force        # Force execution even if ANSI support is unavailable
```

#### Customizing the RGB Gradient

```bash
kolyre --rgb --rgb-step 51 --rgb-block-fg ABC --rgb-block-bg XYZ
```

- `--rgb-step N` sets the step size for RGB components (1–255, default 51).  
- `--rgb-block-fg BLOCK` specifies the text for the foreground RGB gradient.  
- `--rgb-block-bg BLOCK` specifies the text for the background RGB gradient.

## Notes

- Truecolor (RGB) support may vary depending on your terminal emulator.
- On Windows, calling `Kolyre.enable_ansi_support()` may be necessary in older or non-VT enabled consoles.
- You can set `Kolyre.FORCE_COLOR = True` to override automatic terminal capability detection and force ANSI output.

## References

- **ANSI Escape Codes:** Comprehensive overview of ANSI escape sequences for text styling and terminal colors. See the [Wikipedia page on ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code).  
- **Windows ANSI Support:** Official Microsoft documentation on enabling ANSI escape sequences in Windows consoles. See [Microsoft Console Modes](https://learn.microsoft.com/en-us/windows/console/setconsolemode).  

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
