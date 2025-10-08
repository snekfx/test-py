"""
Output and display system for testrs.

Provides boxy integration for pretty terminal output with graceful fallback.
"""

import os
import shutil
import subprocess
import sys
from enum import Enum
from typing import Optional


class OutputMode(Enum):
    """Output mode selection."""

    PRETTY = "pretty"  # Use boxy if available
    DATA = "data"      # Plain text, no formatting


class Theme(Enum):
    """Boxy themes for different message types."""

    SUCCESS = "success"   # Green, for successful operations
    WARNING = "warning"   # Yellow, for warnings and violations
    ERROR = "error"       # Red, for errors
    INFO = "info"         # Blue, for informational messages
    MAGIC = "magic"       # Purple, for special displays
    PLAIN = "plain"       # No special formatting


# Global settings
_OUTPUT_MODE = OutputMode.PRETTY
_BOXY_AVAILABLE = None  # Cache boxy availability check


def check_boxy_availability() -> bool:
    """
    Check if boxy is available and working.

    Returns:
        True if boxy is available, False otherwise
    """
    global _BOXY_AVAILABLE

    # Return cached result if already checked
    if _BOXY_AVAILABLE is not None:
        return _BOXY_AVAILABLE

    # Check REPOS_USE_BOXY environment variable (1=disabled, 0=enabled)
    if os.getenv("REPOS_USE_BOXY") == "1":
        _BOXY_AVAILABLE = False
        return False

    # Check if boxy executable exists
    boxy_path = shutil.which("boxy")
    if not boxy_path:
        _BOXY_AVAILABLE = False
        return False

    # Verify boxy works by checking version
    try:
        result = subprocess.run(
            [boxy_path, "--version"],
            capture_output=True,
            timeout=2,
            text=True
        )
        _BOXY_AVAILABLE = result.returncode == 0
        return _BOXY_AVAILABLE
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        _BOXY_AVAILABLE = False
        return False


def set_output_mode(mode: OutputMode):
    """
    Set global output mode.

    Args:
        mode: OutputMode.PRETTY or OutputMode.DATA
    """
    global _OUTPUT_MODE
    _OUTPUT_MODE = mode


def get_output_mode() -> OutputMode:
    """
    Get current output mode.

    Returns:
        Current OutputMode
    """
    return _OUTPUT_MODE


def boxy_display(
    content: str,
    theme: Theme = Theme.PLAIN,
    title: Optional[str] = None,
    width: str = "max",
) -> bool:
    """
    Display content using boxy with fallback to plain output.

    Args:
        content: Content to display
        theme: Boxy theme to use
        title: Optional title for the box
        width: Box width ("max", "80", "100", etc.)

    Returns:
        True if displayed via boxy, False if fallback used
    """
    # Force plain output in DATA mode
    if _OUTPUT_MODE == OutputMode.DATA:
        _plain_output(content, theme.value, title)
        return False

    # Check if boxy is available
    if not check_boxy_availability():
        _plain_output(content, theme.value, title)
        return False

    # Build boxy command
    cmd = ["boxy"]

    if theme != Theme.PLAIN:
        cmd.extend(["--theme", theme.value])

    if title:
        cmd.extend(["--title", title])

    if width:
        cmd.extend(["--width", width])

    # Try to display via boxy
    try:
        result = subprocess.run(
            cmd,
            input=content,
            text=True,
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0:
            # Boxy succeeded, print its output
            print(result.stdout, end="")
            return True
        else:
            # Boxy failed, use fallback
            _plain_output(content, theme.value, title)
            return False

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        _plain_output(content, theme.value, title)
        return False


def _plain_output(content: str, theme: str, title: Optional[str]):
    """
    Plain text fallback output.

    Args:
        content: Content to display
        theme: Theme name (for header)
        title: Optional title
    """
    # Print to stderr for visibility
    if title:
        print(f"[{theme}] {title}", file=sys.stderr)

    print(content, file=sys.stderr)
    print()  # Empty line after content


def success(message: str, title: Optional[str] = None):
    """
    Display success message with green theme.

    Args:
        message: Success message
        title: Optional title
    """
    boxy_display(message, Theme.SUCCESS, title or "✓ Success")


def warning(message: str, title: Optional[str] = None):
    """
    Display warning message with yellow theme.

    Args:
        message: Warning message
        title: Optional title
    """
    boxy_display(message, Theme.WARNING, title or "⚠ Warning")


def error(message: str, title: Optional[str] = None):
    """
    Display error message with red theme.

    Args:
        message: Error message
        title: Optional title
    """
    boxy_display(message, Theme.ERROR, title or "✗ Error")


def info(message: str, title: Optional[str] = None):
    """
    Display informational message with blue theme.

    Args:
        message: Info message
        title: Optional title
    """
    boxy_display(message, Theme.INFO, title or "ℹ Info")


def plain(message: str):
    """
    Display plain message without boxy (always to stdout).

    Args:
        message: Message to print
    """
    print(message)


def print_plain(message: str):
    """
    Print message to stdout in plain mode.

    Respects output mode setting.

    Args:
        message: Message to print
    """
    print(message)


def print_error(message: str):
    """
    Print error message to stderr.

    Args:
        message: Error message
    """
    print(f"testrs: {message}", file=sys.stderr)


def print_debug(message: str):
    """
    Print debug message to stderr if DEBUG mode enabled.

    Args:
        message: Debug message
    """
    if os.getenv("TESTRS_DEBUG") == "1":
        print(f"[DEBUG] {message}", file=sys.stderr)
