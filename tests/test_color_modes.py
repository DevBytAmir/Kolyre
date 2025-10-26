"""Tests for Kolyre's 256-color and RGB color functions."""

import pytest

from kolyre import Kolyre


def test_foreground_256_valid_inputs() -> None:
    """Foreground 256-color codes should map correctly for valid inputs."""
    assert Kolyre.foreground_256(0) == "\033[38;5;0m"
    assert Kolyre.foreground_256(255) == "\033[38;5;255m"
    assert Kolyre.foreground_256(42) == "\033[38;5;42m"


def test_foreground_256_invalid_inputs() -> None:
    """Foreground 256-color should raise on invalid input."""
    with pytest.raises(TypeError):
        Kolyre.foreground_256("red")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="boolean"):
        Kolyre.foreground_256(True)
    with pytest.raises(ValueError):
        Kolyre.foreground_256(-1)
    with pytest.raises(ValueError):
        Kolyre.foreground_256(256)


def test_background_256_valid_inputs() -> None:
    """Background 256-color codes should map correctly for valid inputs."""
    assert Kolyre.background_256(0) == "\033[48;5;0m"
    assert Kolyre.background_256(255) == "\033[48;5;255m"
    assert Kolyre.background_256(100) == "\033[48;5;100m"


def test_background_256_invalid_inputs() -> None:
    """Background 256-color should raise on invalid input."""
    with pytest.raises(TypeError):
        Kolyre.background_256("blue")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="boolean"):
        Kolyre.background_256(False)
    with pytest.raises(ValueError):
        Kolyre.background_256(-10)
    with pytest.raises(ValueError):
        Kolyre.background_256(999)


def test_foreground_rgb_with_tuple_or_list() -> None:
    """Foreground RGB should accept tuple and list values."""
    assert Kolyre.foreground_rgb((1, 2, 3)) == "\033[38;2;1;2;3m"
    assert Kolyre.foreground_rgb([255, 128, 0]) == "\033[38;2;255;128;0m"


def test_foreground_rgb_with_hex_strings() -> None:
    """Foreground RGB should accept hex string values."""
    assert Kolyre.foreground_rgb("#FF8800") == "\033[38;2;255;136;0m"
    assert Kolyre.foreground_rgb("00AABB") == "\033[38;2;0;170;187m"
    assert Kolyre.foreground_rgb("F80") == "\033[38;2;255;136;0m"
    assert Kolyre.foreground_rgb("#333") == "\033[38;2;51;51;51m"


def test_foreground_rgb_with_integers() -> None:
    """Foreground RGB should accept three integer arguments."""
    assert Kolyre.foreground_rgb(10, 20, 30) == "\033[38;2;10;20;30m"


def test_foreground_rgb_invalid_inputs() -> None:
    """Foreground RGB should raise on invalid inputs."""
    with pytest.raises(ValueError, match="must have exactly 3 values"):
        Kolyre.foreground_rgb((1, 2))  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="cannot be a boolean"):
        Kolyre.foreground_rgb((1, 2, False))
    with pytest.raises(TypeError, match="must be an integer"):
        Kolyre.foreground_rgb((1, "2", 3))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="must be between 0 and 255"):
        Kolyre.foreground_rgb((1, 2, 300))
    with pytest.raises(ValueError, match="green and blue must also be provided"):
        Kolyre.foreground_rgb(10)
    with pytest.raises(ValueError, match="Invalid hex color format"):
        Kolyre.foreground_rgb("GGGGGG")
    with pytest.raises(ValueError, match="Hex color must be 6 characters"):
        Kolyre.foreground_rgb("1234")


def test_background_rgb_with_tuple_or_list() -> None:
    """Background RGB should accept tuple and list values."""
    assert Kolyre.background_rgb((11, 22, 33)) == "\033[48;2;11;22;33m"
    assert Kolyre.background_rgb([200, 100, 50]) == "\033[48;2;200;100;50m"


def test_background_rgb_with_hex_strings() -> None:
    """Background RGB should accept hex string values."""
    assert Kolyre.background_rgb("FF0000") == "\033[48;2;255;0;0m"
    assert Kolyre.background_rgb("19A") == "\033[48;2;17;153;170m"


def test_background_rgb_with_integers() -> None:
    """Background RGB should accept three integer arguments."""
    assert Kolyre.background_rgb(100, 150, 200) == "\033[48;2;100;150;200m"


def test_background_rgb_invalid_inputs() -> None:
    """Background RGB should raise on invalid inputs."""
    with pytest.raises(ValueError, match="exactly 3 values"):
        Kolyre.background_rgb([1, 2])
    with pytest.raises(TypeError, match="cannot be a boolean"):
        Kolyre.background_rgb((1, 2, True))
    with pytest.raises(TypeError, match="must be an integer"):
        Kolyre.background_rgb((1, None, 3))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="must be between 0 and 255"):
        Kolyre.background_rgb((1, 2, 999))
    with pytest.raises(ValueError, match="green and blue must also be provided"):
        Kolyre.background_rgb(128)
    with pytest.raises(ValueError, match="Invalid hex color format"):
        Kolyre.background_rgb("FF00GG")
    with pytest.raises(ValueError, match="Hex color must be 6 characters"):
        Kolyre.background_rgb("12345")
