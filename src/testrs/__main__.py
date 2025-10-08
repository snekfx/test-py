"""
testrs.__main__ - Entry point for direct module invocation

Allows running testrs via: python -m testrs
"""

import sys


def main() -> int:
    """
    Main entry point for testrs module invocation.

    Returns:
        Exit code (0=success, non-zero=error)
    """
    # Import here to avoid circular imports
    try:
        from testrs.cli import main as cli_main
        return cli_main()
    except ImportError:
        # CLI module not yet implemented
        print("testrs: CLI module not yet implemented", file=sys.stderr)
        print(f"testrs version: {__import__('testrs').__version__}", file=sys.stderr)
        return 127


if __name__ == "__main__":
    sys.exit(main())
