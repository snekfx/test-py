"""
testpy.__main__ - Entry point for direct module invocation

Allows running testpy via: python -m testpy
"""

import sys


def main() -> int:
    """
    Main entry point for testpy module invocation.

    Returns:
        Exit code (0=success, non-zero=error)
    """
    # Import here to avoid circular imports
    try:
        from testpy.cli import main as cli_main
        return cli_main()
    except ImportError:
        # CLI module not yet implemented
        print("testpy: CLI module not yet implemented", file=sys.stderr)
        print(f"testpy version: {__import__('testpy').__version__}", file=sys.stderr)
        return 127


if __name__ == "__main__":
    sys.exit(main())
