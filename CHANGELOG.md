# Changelog

This project adheres to [Semantic Versioning](https://semver.org/)  
and follows the guidelines of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [2.0.0] - 2025-10-26
### Added
- Modular **package structure** replacing the previous single-file design.
- Dedicated **`demo` module** separated from the main implementation for improved modularity and import performance.
- **Static Utility Enforcement:**
  - Decorated the `Kolyre` class with `@final` to explicitly prevent subclassing.  
  - Overrode the `__init__()` constructor to raise a `TypeError`, ensuring the class cannot be instantiated.  
- **Nested classes for better organization:**
  - `Kolyre.Style` — text style and reset codes.
  - `Kolyre.Foreground` — standard and bright foreground colors.
  - `Kolyre.Background` — standard and bright background colors.
- **Additional reset constants:**
  - `RESET_BOLD_DIM`, `RESET_ITALIC`, `RESET_UNDERLINE`, `RESET_REVERSED`, `RESET_HIDDEN`, `RESET_STRIKETHROUGH`, `RESET_OVERLINE`
  - `RESET_FOREGROUND`, `RESET_BACKGROUND`
- **Helper methods for color validation and normalization:**
  - `_flatten()` for flattening nested ANSI code inputs.
  - `_validate_256()` for strict validation of 256-color values.
  - `_normalize_rgb()` for hex, tuple, or RGB argument support.
- `FORCE_COLOR` attribute to override TTY color detection globally.

### Changed
- **Refactored** the entire library into a structured package (`kolyre/`) for maintainability.
- **Enhanced `colorize()` method:**
  - Now respects the global `Kolyre.FORCE_COLOR` flag.
  - Added an optional `force` argument for per-call color overrides.
  - Improved recursion and flattening for nested ANSI lists.
- **Improved RGB methods:**
  - `foreground_rgb()` and `background_rgb()` now support hex color inputs.
  - Added robust error messages and stricter type validation.
- **Improved code clarity and maintainability:**
  - Simplified redundant reset constants.
  - Expanded inline documentation and type hints.
  - Reorganized private helper methods for readability.
- Enhanced Windows ANSI compatibility and error handling.
- **Tests reorganized** into separate files for improved maintainability and clarity.

### Removed
- Removed the built-in demo from the main implementation file.
- Deprecated validation logic and redundant constants.

---

## [1.0.0] - 2025-10-26
### Added
- Initial release of **Kolyre** as a single-file module.
- **Support for:**
  - Common text styles: `BOLD`, `ITALIC`, `UNDERLINE`, `STRIKETHROUGH`, etc.
  - 16 standard and bright foreground/background colors.
  - 256-color and Truecolor (24-bit RGB) ANSI codes.
- **Helper methods:**
  - `colorize()` for combining multiple ANSI codes.
  - `enable_ansi_support()` for Windows terminal compatibility.
  - `demo()` showcasing color, style, and RGB examples.

---