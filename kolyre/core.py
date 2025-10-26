"""Kolyre class implementation for terminal text styling and coloring.

This module contains the primary Kolyre class, including all ANSI escape code
constants, color utilities (256-color and RGB), and Windows ANSI support
functions.
"""

import sys
from typing import Any, Final, final


@final
class Kolyre:
    """ANSI terminal text styling and coloring utility.

    Provides methods for applying standard, 256-color, and truecolor (24-bit RGB)
    ANSI codes. The `colorize()` method allows applying multiple styles at once, and
    `enable_ansi_support()` can help display ANSI codes correctly on some
    Windows terminals.

    Truecolor support may vary depending on the terminal.

    Attributes:
        FORCE_COLOR (bool): If True, forces ANSI codes to be returned even if
            `sys.stdout.isatty()` is False. Defaults to False.
        Style: Nested class containing constants for text styles
            (e.g., BOLD, UNDERLINE).
        Foreground: Nested class containing constants for standard
            (8/16-bit) foreground colors.
        Background: Nested class containing constants for standard
            (8/16-bit) background colors.
    """

    FORCE_COLOR: bool = False

    class Style:
        """ANSI escape codes for text styling in the terminal."""

        # pylint: disable=R0903

        BOLD: Final[str] = "\033[1m"
        DIM: Final[str] = "\033[2m"
        ITALIC: Final[str] = "\033[3m"
        UNDERLINE: Final[str] = "\033[4m"
        DOUBLE_UNDERLINE: Final[str] = "\033[21m"
        REVERSED: Final[str] = "\033[7m"
        HIDDEN: Final[str] = "\033[8m"
        STRIKETHROUGH: Final[str] = "\033[9m"
        OVERLINE: Final[str] = "\033[53m"

        RESET: Final[str] = "\033[0m"

        RESET_BOLD_DIM: Final[str] = "\033[22m"
        RESET_ITALIC: Final[str] = "\033[23m"
        RESET_UNDERLINE: Final[str] = "\033[24m"
        RESET_REVERSED: Final[str] = "\033[27m"
        RESET_HIDDEN: Final[str] = "\033[28m"
        RESET_STRIKETHROUGH: Final[str] = "\033[29m"
        RESET_OVERLINE: Final[str] = "\033[55m"

        RESET_FOREGROUND: Final[str] = "\033[39m"
        RESET_BACKGROUND: Final[str] = "\033[49m"

    class Foreground:
        """ANSI escape codes for foreground colors."""

        # pylint: disable=R0903

        BLACK: Final[str] = "\033[30m"
        RED: Final[str] = "\033[31m"
        GREEN: Final[str] = "\033[32m"
        YELLOW: Final[str] = "\033[33m"
        BLUE: Final[str] = "\033[34m"
        MAGENTA: Final[str] = "\033[35m"
        CYAN: Final[str] = "\033[36m"
        WHITE: Final[str] = "\033[37m"

        BRIGHT_BLACK: Final[str] = "\033[90m"
        BRIGHT_RED: Final[str] = "\033[91m"
        BRIGHT_GREEN: Final[str] = "\033[92m"
        BRIGHT_YELLOW: Final[str] = "\033[93m"
        BRIGHT_BLUE: Final[str] = "\033[94m"
        BRIGHT_MAGENTA: Final[str] = "\033[95m"
        BRIGHT_CYAN: Final[str] = "\033[96m"
        BRIGHT_WHITE: Final[str] = "\033[97m"

    class Background:
        """ANSI escape codes for background colors."""

        # pylint: disable=R0903

        BLACK: Final[str] = "\033[40m"
        RED: Final[str] = "\033[41m"
        GREEN: Final[str] = "\033[42m"
        YELLOW: Final[str] = "\033[43m"
        BLUE: Final[str] = "\033[44m"
        MAGENTA: Final[str] = "\033[45m"
        CYAN: Final[str] = "\033[46m"
        WHITE: Final[str] = "\033[47m"

        BRIGHT_BLACK: Final[str] = "\033[100m"
        BRIGHT_RED: Final[str] = "\033[101m"
        BRIGHT_GREEN: Final[str] = "\033[102m"
        BRIGHT_YELLOW: Final[str] = "\033[103m"
        BRIGHT_BLUE: Final[str] = "\033[104m"
        BRIGHT_MAGENTA: Final[str] = "\033[105m"
        BRIGHT_CYAN: Final[str] = "\033[106m"
        BRIGHT_WHITE: Final[str] = "\033[107m"

    def __init__(self) -> None:
        """Prevent instantiation of this utility class."""
        raise TypeError(
            f"Class {self.__class__.__name__} is a static utility "
            f"and cannot be instantiated."
        )

    @staticmethod
    def _flatten(item: str | tuple[Any, ...] | list[Any]) -> list[str]:
        """Flatten nested ANSI codes into a flat list of strings.

        Args:
            item (str | tuple[Any, ...] | list[Any]): A string or nested lists/tuples
                of ANSI codes.

        Returns:
            list[str]: A flat list of ANSI code strings.

        Raises:
            TypeError: If an element is not a string, list, or tuple.
        """
        flattened: list[str] = []
        stack: list[str | tuple[Any, ...] | list[Any]] = [item]
        while stack:
            current = stack.pop()
            if isinstance(current, str):
                flattened.append(current)
            elif isinstance(current, (list, tuple)):
                stack.extend(reversed(current))
            else:
                raise TypeError(
                    f"ANSI code must be a string, list, or tuple of strings, "
                    f"got {type(current).__name__}"
                )

        return flattened

    @staticmethod
    def _validate_256(color_index: int) -> int:
        """Validate a 256-color index for ANSI escape codes.

        Args:
            color_index (int): The color index to validate.

        Returns:
            int: The validated color index.

        Raises:
            TypeError: If `color_index` is not an integer or is a boolean.
            ValueError: If `color_index` is outside the range 0-255.
        """
        if isinstance(color_index, bool):
            raise TypeError("color_index cannot be a boolean")

        if not isinstance(color_index, int):
            raise TypeError(
                f"color_index must be an integer, got {type(color_index).__name__}"
            )

        if not 0 <= color_index <= 255:
            raise ValueError(
                f"color_index must be between 0 and 255, got {color_index}"
            )

        return color_index

    @staticmethod
    def _normalize_rgb(
        rgb: str | tuple[int, int, int] | list[int] | int,
        green: int | None,
        blue: int | None,
    ) -> tuple[int, int, int]:
        """Internal helper to parse and validate RGB input formats.

        Args:
            rgb: The red component (0-255). This can also be a hex string (e.g.,
                '#FF8800' or 'F80'), or a sequence (tuple/list) of three integers
                (R, G, B).
            green: The green component (0-255) if rgb is a single integer.
            blue: The blue component (0-255) if rgb is a single integer.

        Returns:
            tuple[int, int, int]: A validated (red, green, blue) tuple of integers
                from 0 to 255.

        Raises:
            ValueError: If any component is outside the 0-255 range, a hex string is
                malformed, or a sequence doesn't contain exactly three values.
            TypeError: If any component is not an integer or is a boolean, or if
                the input type is invalid.
        """
        # pylint: disable=R0912

        if isinstance(rgb, str):
            hex_str = rgb.strip().lstrip("#")
            if len(hex_str) == 3:
                hex_str = "".join([c * 2 for c in hex_str])
            if len(hex_str) != 6:
                raise ValueError(
                    f"Hex color must be 6 characters (RRGGBB), got '{hex_str}'"
                )
            try:
                red = int(hex_str[0:2], 16)
                green = int(hex_str[2:4], 16)
                blue = int(hex_str[4:6], 16)
            except ValueError as exc:
                raise ValueError(f"Invalid hex color format: '{hex_str}'") from exc

        elif isinstance(rgb, (tuple, list)):
            if len(rgb) != 3:
                raise ValueError(
                    f"RGB sequence must have exactly 3 values, got {len(rgb)}"
                )
            red, green, blue = rgb

        elif isinstance(rgb, int):
            if green is None or blue is None:
                raise ValueError(
                    "When providing a single integer, green and blue "
                    "must also be provided"
                )
            red = rgb
        else:
            raise TypeError(
                "Invalid RGB input. Provide a hex string, (r, g, b), [r, g, b], or "
                "three separate integers."
            )

        for name, value in zip(("red", "green", "blue"), (red, green, blue)):
            if isinstance(value, bool):
                raise TypeError(f"{name} cannot be a boolean")
            if not isinstance(value, int):
                raise TypeError(
                    f"{name} must be an integer, got {type(value).__name__}"
                )
            if not 0 <= value <= 255:
                raise ValueError(f"{name} must be between 0 and 255, got {value}")

        return red, green, blue

    @staticmethod
    def colorize(
        text: str,
        *ansi_codes: str | tuple[Any, ...] | list[Any],
        force: bool | None = None,
    ) -> str:
        """Apply one or more ANSI codes to the given text.

        Args:
            text (str): The text to style.
            *ansi_codes (str | tuple[Any, ...] | list[Any]): One or more ANSI codes,
                individually or nested in lists/tuples.
            force (bool, optional): If True, forces styling regardless of TTY or
                Kolyre.FORCE_COLOR setting. If None, the class-level Kolyre.FORCE_COLOR
                is used as the override. Defaults to None.

        Returns:
            str: The styled text, reset with `Kolyre.RESET`.

        Raises:
            TypeError: If `text` is not a `str`, or if any provided ANSI code
                is not a `str`.
        """
        if not isinstance(text, str):
            raise TypeError(f"text must be a string, got {type(text).__name__}")
        if not ansi_codes:
            return text

        codes: list[str] = []
        for code in ansi_codes:
            codes.extend(Kolyre._flatten(code))

        if (
            not (force if force is not None else Kolyre.FORCE_COLOR)
            and not sys.stdout.isatty()
        ):
            return text

        return f"{''.join(codes)}{text}{Kolyre.Style.RESET}"

    @staticmethod
    def foreground_256(color_index: int) -> str:
        """Return a 256-color ANSI escape code for the foreground.

        Args:
            color_index (int): Integer between 0 and 255, representing a color
                in the ANSI 256-color palette.

        Returns:
            str: ANSI escape sequence for the specified foreground color.

        Raises:
            TypeError: If `color_index` is not an integer or is a boolean.
            ValueError: If `color_index` is outside the range 0-255.
        """
        validated_index = Kolyre._validate_256(color_index)
        return f"\033[38;5;{validated_index}m"

    @staticmethod
    def background_256(color_index: int) -> str:
        """Return a 256-color ANSI escape code for the background.

        Args:
            color_index (int): Integer between 0 and 255, representing a color
                in the ANSI 256-color palette.

        Returns:
            str: ANSI escape sequence for the specified background color.

        Raises:
            TypeError: If `color_index` is not an integer or is a boolean.
            ValueError: If `color_index` is outside the range 0-255.
        """
        validated_index = Kolyre._validate_256(color_index)
        return f"\033[48;5;{validated_index}m"

    @staticmethod
    def foreground_rgb(
        rgb: str | tuple[int, int, int] | list[int] | int,
        green: int | None = None,
        blue: int | None = None,
    ) -> str:
        """Return a truecolor (24-bit RGB) ANSI escape code for the foreground.

        Args:
            rgb (str, tuple, list, or int):
                - Hex string (e.g., "#FF8800", "CC33AA", or shorthand "F80")
                - Tuple or list of three integers (R, G, B)
                - Single red integer if `green` and `blue` are provided
            green (int, optional): Green value if `rgb` is a single int.
            blue (int, optional): Blue value if `rgb` is a single int.

        Returns:
            str: ANSI escape sequence for the specified RGB foreground color.

        Raises:
            TypeError: If any component is not an integer or is a boolean.
            ValueError: If any RGB component is outside 0-255, or if the input
                is malformed.
        """
        red, green, blue = Kolyre._normalize_rgb(rgb, green, blue)
        return f"\033[38;2;{red};{green};{blue}m"

    @staticmethod
    def background_rgb(
        rgb: str | tuple[int, int, int] | list[int] | int,
        green: int | None = None,
        blue: int | None = None,
    ) -> str:
        """Return a truecolor (24-bit RGB) ANSI escape code for the background.

        Args:
            rgb (str, tuple, list, or int):
                - Hex string (e.g., "#FF8800", "CC33AA", or shorthand "F80")
                - Tuple or list of three integers (R, G, B)
                - Single red integer if `green` and `blue` are provided
            green (int, optional): Green value if `rgb` is a single int.
            blue (int, optional): Blue value if `rgb` is a single int.

        Returns:
            str: ANSI escape sequence for the specified RGB background color.

        Raises:
            TypeError: If any component is not an integer or is a boolean.
            ValueError: If any RGB component is outside 0-255, or if the input
                is malformed.
        """
        red, green, blue = Kolyre._normalize_rgb(rgb, green, blue)
        return f"\033[48;2;{red};{green};{blue}m"

    @staticmethod
    def enable_ansi_support() -> bool:
        """Enable ANSI escape sequences on Windows terminals.

        Returns:
            bool: True if ANSI support is active or not needed; False if
                enabling failed.
        """
        if sys.platform != "win32":
            return True

        try:
            # pylint: disable=C0415
            import ctypes
        except ImportError:
            return False

        try:
            std_output_handle = -11
            enable_virtual_terminal_processing = 0x0004

            handle = ctypes.windll.kernel32.GetStdHandle(std_output_handle)
            if handle in (0, -1):
                return False

            mode = ctypes.c_uint32()
            if not ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                return False

            return bool(
                ctypes.windll.kernel32.SetConsoleMode(
                    handle, mode.value | enable_virtual_terminal_processing
                )
            )
        except (AttributeError, OSError):
            return False
