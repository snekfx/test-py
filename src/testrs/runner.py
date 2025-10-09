"""
Test execution runner for testrs.

Executes tests with timeout support and captures results.
"""

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Tuple


@dataclass
class TestResult:
    """Test execution result."""

    passed: int
    failed: int
    ignored: int
    total: int
    duration: float
    output: str
    exit_code: int

    @property
    def success(self) -> bool:
        """Check if tests passed (exit code 0)."""
        return self.exit_code == 0


def find_timeout_command() -> Optional[str]:
    """
    Find timeout command (timeout or gtimeout).

    Returns:
        Path to timeout command, or None if not available
    """
    # Try GNU timeout first
    timeout_path = shutil.which("timeout")
    if timeout_path:
        return timeout_path

    # Try gtimeout (macOS/BSD)
    gtimeout_path = shutil.which("gtimeout")
    if gtimeout_path:
        return gtimeout_path

    return None


def parse_cargo_test_output(output: str) -> Tuple[int, int, int]:
    """
    Parse cargo test output for test counts.

    Args:
        output: Cargo test output string

    Returns:
        Tuple of (passed, failed, ignored) counts
    """
    passed = 0
    failed = 0
    ignored = 0

    # Look for summary line: "test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out"
    summary_pattern = r"test result:.*?(\d+) passed.*?(\d+) failed.*?(\d+) ignored"
    match = re.search(summary_pattern, output)

    if match:
        passed = int(match.group(1))
        failed = int(match.group(2))
        ignored = int(match.group(3))

    return passed, failed, ignored


def run_cargo_test(
    repo_root: Path,
    category: Optional[str] = None,
    module: Optional[str] = None,
    timeout: int = 600,
) -> TestResult:
    """
    Run cargo test with optional filtering and timeout.

    Args:
        repo_root: Repository root directory
        category: Optional category filter (e.g., "sanity")
        module: Optional module filter (e.g., "math")
        timeout: Timeout in seconds (default 600)

    Returns:
        TestResult with execution results
    """
    # Build cargo test command
    cmd = ["cargo", "test"]

    # Add filtering
    if category and module:
        # Both category and module: cargo test --test sanity_math
        cmd.extend(["--test", f"{category}_{module}"])
    elif category:
        # Category only: run all tests for that category
        # Note: cargo test doesn't support wildcards, so we run without --test
        # and filter by test name pattern instead
        cmd.append(category)
    elif module:
        # Module only: run all tests for that module
        cmd.append(module)

    # Find timeout command
    timeout_bin = find_timeout_command()

    # Prepare final command with timeout wrapper
    if timeout_bin:
        # Use timeout command wrapper
        final_cmd = [timeout_bin, f"{timeout}s"] + cmd
    else:
        # No timeout wrapper available, use subprocess timeout
        final_cmd = cmd

    # Execute command
    try:
        result = subprocess.run(
            final_cmd,
            cwd=repo_root,
            capture_output=True,
            timeout=timeout if not timeout_bin else None,  # Only use subprocess timeout if no timeout bin
            text=True,
        )

        # Parse output for test counts
        combined_output = result.stdout + result.stderr
        passed, failed, ignored = parse_cargo_test_output(combined_output)
        total = passed + failed + ignored

        # Extract duration if available
        duration = 0.0
        duration_pattern = r"finished in ([\d.]+)s"
        duration_match = re.search(duration_pattern, combined_output)
        if duration_match:
            duration = float(duration_match.group(1))

        return TestResult(
            passed=passed,
            failed=failed,
            ignored=ignored,
            total=total,
            duration=duration,
            output=combined_output,
            exit_code=result.returncode,
        )

    except subprocess.TimeoutExpired as e:
        # Timeout occurred
        output = ""
        if e.stdout:
            output += e.stdout if isinstance(e.stdout, str) else e.stdout.decode('utf-8', errors='replace')
        if e.stderr:
            output += e.stderr if isinstance(e.stderr, str) else e.stderr.decode('utf-8', errors='replace')

        return TestResult(
            passed=0,
            failed=0,
            ignored=0,
            total=0,
            duration=float(timeout),
            output=output + f"\n\nTest execution timed out after {timeout} seconds",
            exit_code=124,  # Standard timeout exit code
        )

    except FileNotFoundError:
        # cargo not found
        return TestResult(
            passed=0,
            failed=0,
            ignored=0,
            total=0,
            duration=0.0,
            output="Error: cargo command not found. Is Rust installed?",
            exit_code=127,
        )

    except Exception as e:
        # Unexpected error
        return TestResult(
            passed=0,
            failed=0,
            ignored=0,
            total=0,
            duration=0.0,
            output=f"Error executing cargo test: {e}",
            exit_code=1,
        )


def run_rust_tests(
    repo_root: Path,
    category: Optional[str] = None,
    module: Optional[str] = None,
    timeout: int = 600,
) -> TestResult:
    """
    Run Rust tests with cargo.

    This is the main entry point for Rust test execution.

    Args:
        repo_root: Repository root directory
        category: Optional category filter (e.g., "sanity", "uat")
        module: Optional module filter (e.g., "math", "com")
        timeout: Timeout in seconds (default 600)

    Returns:
        TestResult with execution results
    """
    return run_cargo_test(repo_root, category, module, timeout)
