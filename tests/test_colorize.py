"""Tests for the primary Kolyre.colorize function and helpers."""

import sys

import pytest

from kolyre import Kolyre


def test_colorize_applies_styles_when_tty(monkeypatch: pytest.MonkeyPatch) -> None:
    """Colorize should wrap text with codes when stdout is a TTY."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    result = Kolyre.colorize("hello", Kolyre.Style.BOLD, Kolyre.Foreground.RED)
    assert (
        result == f"{Kolyre.Style.BOLD}{Kolyre.Foreground.RED}hello{Kolyre.Style.RESET}"
    )


def test_colorize_with_no_codes_returns_original_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Colorize should return the original text if no codes are provided."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    assert Kolyre.colorize("nothing to see") == "nothing to see"
    assert Kolyre.colorize("") == ""


def test_colorize_with_deeply_nested_codes(monkeypatch: pytest.MonkeyPatch) -> None:
    """Colorize should correctly flatten deeply nested code sequences."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    codes = (Kolyre.Style.BOLD, [Kolyre.Foreground.RED, (Kolyre.Background.BLUE,)])
    result = Kolyre.colorize("nested", codes)
    expected = (
        f"{Kolyre.Style.BOLD}{Kolyre.Foreground.RED}"
        f"{Kolyre.Background.BLUE}nested{Kolyre.Style.RESET}"
    )
    assert result == expected


def test_colorize_force_applies_styles(monkeypatch: pytest.MonkeyPatch) -> None:
    """Colorize should apply styles with force=True even if not TTY."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)
    result = Kolyre.colorize(
        "world", Kolyre.Style.BOLD, Kolyre.Foreground.GREEN, force=True
    )
    assert (
        result
        == f"{Kolyre.Style.BOLD}{Kolyre.Foreground.GREEN}world{Kolyre.Style.RESET}"
    )


def test_colorize_returns_plain_when_not_tty(monkeypatch: pytest.MonkeyPatch) -> None:
    """Colorize should return plain text if not TTY and not forced."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)
    result = Kolyre.colorize("plain", Kolyre.Style.BOLD, Kolyre.Foreground.GREEN)
    assert result == "plain"


def test_colorize_type_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    """Colorize should raise TypeError on invalid argument types."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    with pytest.raises(TypeError):
        Kolyre.colorize(123, Kolyre.Foreground.RED)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        Kolyre.colorize("ok", 42)  # type: ignore[arg-type]


def test_colorize_uses_force_color_attribute(monkeypatch: pytest.MonkeyPatch) -> None:
    """Colorize should apply styles when Kolyre.FORCE_COLOR is True, even if not TTY."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)
    original_force_color = Kolyre.FORCE_COLOR
    try:
        Kolyre.FORCE_COLOR = True
        result_forced = Kolyre.colorize("forced", Kolyre.Foreground.CYAN)
        expected_forced = f"{Kolyre.Foreground.CYAN}forced{Kolyre.Style.RESET}"
        assert result_forced == expected_forced

        Kolyre.FORCE_COLOR = False
        result_not_forced = Kolyre.colorize("not forced", Kolyre.Foreground.CYAN)
        assert result_not_forced == "not forced"
    finally:
        Kolyre.FORCE_COLOR = original_force_color


def test_colorize_with_single_list(monkeypatch: pytest.MonkeyPatch) -> None:
    """Colorize should handle a single list of codes."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    codes = [Kolyre.Foreground.RED, Kolyre.Style.BOLD]
    result = Kolyre.colorize("list", codes)
    assert (
        result == f"{Kolyre.Foreground.RED}{Kolyre.Style.BOLD}list{Kolyre.Style.RESET}"
    )


def test_colorize_with_tuple(monkeypatch: pytest.MonkeyPatch) -> None:
    """Colorize should handle a tuple of codes."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    codes = (Kolyre.Foreground.GREEN, Kolyre.Style.UNDERLINE)
    result = Kolyre.colorize("tuple", codes)
    assert (
        result
        == f"{Kolyre.Foreground.GREEN}{Kolyre.Style.UNDERLINE}tuple{Kolyre.Style.RESET}"
    )


def test_colorize_with_multiple_lists(monkeypatch: pytest.MonkeyPatch) -> None:
    """Colorize should flatten and apply multiple lists of codes."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    codes1 = [Kolyre.Foreground.RED]
    codes2 = [Kolyre.Style.BOLD]
    result = Kolyre.colorize("lists", codes1, codes2)
    assert (
        result == f"{Kolyre.Foreground.RED}{Kolyre.Style.BOLD}lists{Kolyre.Style.RESET}"
    )


def test_colorize_with_mixed_list_and_string(monkeypatch: pytest.MonkeyPatch) -> None:
    """Colorize should handle mixed list and string codes."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    codes = [Kolyre.Foreground.RED]
    result = Kolyre.colorize("mixed", codes, Kolyre.Style.BOLD)
    assert (
        result == f"{Kolyre.Foreground.RED}{Kolyre.Style.BOLD}mixed{Kolyre.Style.RESET}"
    )
