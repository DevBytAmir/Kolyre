"""Kolyre: Lightweight Python library for cross-platform terminal styling.

Provides comprehensive functionality for generating ANSI escape codes to style
console output. This includes support for standard colors, the 256-color palette,
and 24-bit Truecolor (RGB) capabilities.
"""

from .core import Kolyre

__version__ = "2.0.0"
__author__ = "DevBytAmir"
__license__ = "MIT"

__all__ = [
    "Kolyre",
    "__version__",
    "__author__",
    "__license__",
]
