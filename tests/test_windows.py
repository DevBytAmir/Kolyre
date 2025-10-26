"""Tests for Kolyre.enable_ansi_support, focusing on Windows-specific logic."""

import builtins
import sys
import types
from typing import Any

import pytest

from kolyre import Kolyre


def test_enable_ansi_support_non_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    """On non-Windows platforms, ANSI support should always be enabled."""
    monkeypatch.setattr(sys, "platform", "linux")
    assert Kolyre.enable_ansi_support() is True


def test_enable_ansi_support_windows_without_ctypes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """On Windows without ctypes, ANSI support should not be enabled."""
    monkeypatch.setattr(sys, "platform", "win32")

    def fake_import(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "ctypes":
            raise ImportError
        return builtins.__import__(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    assert Kolyre.enable_ansi_support() is False


@pytest.mark.parametrize("invalid_handle", [0, -1])
def test_enable_ansi_support_windows_get_handle_failure(
    monkeypatch: pytest.MonkeyPatch, invalid_handle: int
) -> None:
    """Simulate GetStdHandle returning 0 or -1 (failure indicators)."""
    monkeypatch.setattr(sys, "platform", "win32")

    class DummyKernel32:
        """Mock Kernel32 DLL for simulating API failures."""

        def GetStdHandle(self, _: Any) -> int:  # pylint: disable=invalid-name
            """Mocks GetStdHandle."""
            return invalid_handle

        def GetConsoleMode(self, *_: Any) -> bool:  # pylint: disable=invalid-name
            """Mocks GetConsoleMode."""
            return True

    dummy_ctypes = types.SimpleNamespace(
        windll=types.SimpleNamespace(kernel32=DummyKernel32()),
        c_uint32=lambda: types.SimpleNamespace(value=0),
        byref=lambda x: x,
    )
    sys.modules["ctypes"] = dummy_ctypes  # type: ignore[assignment]
    assert Kolyre.enable_ansi_support() is False


def test_enable_ansi_support_windows_get_mode_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate GetConsoleMode returning False (API failure)."""
    monkeypatch.setattr(sys, "platform", "win32")

    class DummyKernel32:
        """Mock Kernel32 DLL for GetConsoleMode failure."""

        def GetStdHandle(self, _: Any) -> int:  # pylint: disable=invalid-name
            """Mocks GetStdHandle."""
            return 42

        def GetConsoleMode(self, _handle: Any, _mode: Any) -> bool:  # pylint: disable=invalid-name
            """Mocks GetConsoleMode returning False."""
            return False

        def SetConsoleMode(self, _handle: Any, _mode: Any) -> bool:  # pylint: disable=invalid-name
            """Mocks SetConsoleMode."""
            return True

    dummy_ctypes = types.SimpleNamespace(
        windll=types.SimpleNamespace(kernel32=DummyKernel32()),
        c_uint32=lambda: types.SimpleNamespace(value=0),
        byref=lambda x: x,
    )
    sys.modules["ctypes"] = dummy_ctypes  # type: ignore[assignment]
    assert Kolyre.enable_ansi_support() is False


def test_enable_ansi_support_windows_api_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate an exception (like OSError) during Windows API calls."""
    monkeypatch.setattr(sys, "platform", "win32")

    class DummyKernel32:
        """Mock Kernel32 DLL for simulating an exception."""

        def GetStdHandle(self, _: Any) -> int:  # pylint: disable=invalid-name
            """Mocks GetStdHandle."""
            return 42

        def GetConsoleMode(self, *_: Any) -> bool:  # pylint: disable=invalid-name
            """Mocks GetConsoleMode raising an exception."""
            raise OSError("Simulated API failure")

        def SetConsoleMode(self, *_: Any) -> bool:  # pylint: disable=invalid-name
            """Mocks SetConsoleMode."""
            return True

    dummy_ctypes = types.SimpleNamespace(
        windll=types.SimpleNamespace(kernel32=DummyKernel32()),
        c_uint32=lambda: types.SimpleNamespace(value=0),
        byref=lambda x: x,
    )
    sys.modules["ctypes"] = dummy_ctypes  # type: ignore[assignment]
    assert Kolyre.enable_ansi_support() is False


def test_enable_ansi_support_windows_ctypes_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate a successful SetConsoleMode call, enabling ANSI."""
    monkeypatch.setattr(sys, "platform", "win32")

    class DummyKernel32:
        """Mock Kernel32 DLL for a successful API sequence."""

        def GetStdHandle(self, _: Any) -> int:  # pylint: disable=invalid-name
            """Mocks GetStdHandle."""
            return 42

        def GetConsoleMode(self, _: Any, mode: Any) -> bool:  # pylint: disable=invalid-name
            """Mocks GetConsoleMode, setting initial mode value."""
            mode.value = 0
            return True

        def SetConsoleMode(self, _handle: Any, _mode: Any) -> bool:  # pylint: disable=invalid-name
            """Mocks SetConsoleMode returning success."""
            return True

    dummy_ctypes = types.SimpleNamespace(
        windll=types.SimpleNamespace(kernel32=DummyKernel32()),
        c_uint32=lambda: types.SimpleNamespace(value=0),
        byref=lambda x: x,
    )
    sys.modules["ctypes"] = dummy_ctypes  # type: ignore[assignment]
    assert Kolyre.enable_ansi_support() is True


def test_enable_ansi_support_windows_ctypes_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate SetConsoleMode returning False (permission/API failure)."""
    monkeypatch.setattr(sys, "platform", "win32")

    class DummyKernel32:
        """Mock Kernel32 DLL for SetConsoleMode failure."""

        def GetStdHandle(self, _: Any) -> int:  # pylint: disable=invalid-name
            """Mocks GetStdHandle."""
            return 42

        def GetConsoleMode(self, _handle: Any, _mode: Any) -> bool:  # pylint: disable=invalid-name
            """Mocks GetConsoleMode returning success."""
            return True

        def SetConsoleMode(self, _handle: Any, _mode: Any) -> bool:  # pylint: disable=invalid-name
            """Mocks SetConsoleMode returning failure."""
            return False

    dummy_ctypes = types.SimpleNamespace(
        windll=types.SimpleNamespace(kernel32=DummyKernel32()),
        c_uint32=lambda: types.SimpleNamespace(value=0),
        byref=lambda x: x,
    )
    sys.modules["ctypes"] = dummy_ctypes  # type: ignore[assignment]
    assert Kolyre.enable_ansi_support() is False
