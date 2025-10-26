"""Tests for Kolyre's static ANSI color and style constants."""

import pytest

from kolyre import Kolyre


def test_instantiation_is_prevented() -> None:
    """Verify that attempting to instantiate Kolyre raises a TypeError."""
    with pytest.raises(TypeError, match="cannot be instantiated"):
        Kolyre()


@pytest.mark.parametrize(
    "name,code",
    [
        ("RESET", "0"),
        ("BOLD", "1"),
        ("DIM", "2"),
        ("ITALIC", "3"),
        ("UNDERLINE", "4"),
        ("DOUBLE_UNDERLINE", "21"),
        ("REVERSED", "7"),
        ("HIDDEN", "8"),
        ("STRIKETHROUGH", "9"),
        ("OVERLINE", "53"),
        ("RESET_BOLD_DIM", "22"),
        ("RESET_ITALIC", "23"),
        ("RESET_UNDERLINE", "24"),
        ("RESET_REVERSED", "27"),
        ("RESET_HIDDEN", "28"),
        ("RESET_STRIKETHROUGH", "29"),
        ("RESET_OVERLINE", "55"),
        ("RESET_FOREGROUND", "39"),
        ("RESET_BACKGROUND", "49"),
    ],
)
def test_style_constants(name: str, code: str) -> None:
    """Verify all text style constants."""
    assert getattr(Kolyre.Style, name) == f"\033[{code}m"


@pytest.mark.parametrize(
    "name,code",
    [
        ("BLACK", 30),
        ("RED", 31),
        ("GREEN", 32),
        ("YELLOW", 33),
        ("BLUE", 34),
        ("MAGENTA", 35),
        ("CYAN", 36),
        ("WHITE", 37),
        ("BRIGHT_BLACK", 90),
        ("BRIGHT_RED", 91),
        ("BRIGHT_GREEN", 92),
        ("BRIGHT_YELLOW", 93),
        ("BRIGHT_BLUE", 94),
        ("BRIGHT_MAGENTA", 95),
        ("BRIGHT_CYAN", 96),
        ("BRIGHT_WHITE", 97),
    ],
)
def test_foreground_constants(name: str, code: int) -> None:
    """Verify all 16-color foreground constants."""
    assert getattr(Kolyre.Foreground, name) == f"\033[{code}m"


@pytest.mark.parametrize(
    "name,code",
    [
        ("BLACK", 40),
        ("RED", 41),
        ("GREEN", 42),
        ("YELLOW", 43),
        ("BLUE", 44),
        ("MAGENTA", 45),
        ("CYAN", 46),
        ("WHITE", 47),
        ("BRIGHT_BLACK", 100),
        ("BRIGHT_RED", 101),
        ("BRIGHT_GREEN", 102),
        ("BRIGHT_YELLOW", 103),
        ("BRIGHT_BLUE", 104),
        ("BRIGHT_MAGENTA", 105),
        ("BRIGHT_CYAN", 106),
        ("BRIGHT_WHITE", 107),
    ],
)
def test_background_constants(name: str, code: int) -> None:
    """Verify all 16-color background constants."""
    assert getattr(Kolyre.Background, name) == f"\033[{code}m"
