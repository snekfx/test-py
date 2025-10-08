"""
testrs - Universal test orchestrator for multi-language projects

A Python-based test orchestrator that enforces test organization standards
across Rust, Python, Node.js, and shell script projects.

Supports:
- Rust: cargo test integration
- Python: pytest/unittest integration
- Node.js: npm/jest/mocha integration
- Shell: direct script execution

Key features:
- 9 test categories: sanity, smoke, unit, integration, e2e, uat, chaos, bench, regression
- Test structure validation and enforcement
- Multi-language module discovery
- Parallel test execution
- Beautiful reporting via boxy integration
"""

import sys
import importlib.metadata


def get_version() -> str:
    """
    Get version from package metadata.

    Returns:
        Version string (e.g., "0.1.0")
    """
    try:
        return importlib.metadata.version("testrs")
    except importlib.metadata.PackageNotFoundError:
        # Fallback during development
        return "0.1.0-dev"


__version__ = get_version()
__author__ = "snekfx"

# Package metadata
__all__ = [
    "__version__",
    "__author__",
]
