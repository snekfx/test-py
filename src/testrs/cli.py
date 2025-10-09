"""
CLI interface for testrs.

Command-line argument parsing and command routing.
"""

import argparse
import sys
from pathlib import Path

from testrs import __version__
from testrs.output import OutputMode, set_output_mode, print_error, info


def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser for testrs CLI.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="testrs",
        description="Universal test orchestrator for multi-language projects",
        epilog="For more information, see: https://github.com/snekfx/test-py",
    )

    # Version
    parser.add_argument(
        "--version",
        action="version",
        version=f"testrs {__version__}",
    )

    # Global options
    parser.add_argument(
        "--view",
        choices=["pretty", "data"],
        default="pretty",
        help="Output mode: pretty (boxy) or data (plain)",
    )

    parser.add_argument(
        "--no-boxy",
        action="store_true",
        help="Disable boxy output (same as --view=data)",
    )

    parser.add_argument(
        "--override",
        action="store_true",
        help="Override validation enforcement (run tests despite violations)",
    )

    parser.add_argument(
        "--skip-enforcement",
        action="store_true",
        help="Skip test organization enforcement completely",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        metavar="SECS",
        help="Test timeout in seconds (default: 600)",
    )

    parser.add_argument(
        "--parallel",
        type=int,
        metavar="N",
        help="Number of parallel test workers (default: CPU count)",
    )

    parser.add_argument(
        "--language",
        choices=["rust", "python", "nodejs", "shell"],
        help="Filter tests by language",
    )

    # Subcommands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        required=False,
    )

    # run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run tests (default command)",
    )
    run_parser.add_argument(
        "category",
        nargs="?",
        choices=["sanity", "smoke", "unit", "integration", "e2e", "uat", "chaos", "bench", "regression"],
        help="Test category to run (runs all if not specified)",
    )
    run_parser.add_argument(
        "module",
        nargs="?",
        help="Specific module to test",
    )

    # lint command
    lint_parser = subparsers.add_parser(
        "lint",
        help="Validate test organization without running tests",
    )
    lint_parser.add_argument(
        "--violations",
        action="store_true",
        help="Show detailed violation report",
    )

    # violations command (alias for lint --violations)
    violations_parser = subparsers.add_parser(
        "violations",
        help="Show detailed test organization violations",
    )

    # check command
    check_parser = subparsers.add_parser(
        "check",
        help="Validate configuration and requirements",
    )
    check_parser.add_argument(
        "--missing-docs",
        action="store_true",
        help="Report missing documentation",
    )

    # docs command
    docs_parser = subparsers.add_parser(
        "docs",
        help="Display documentation",
    )
    docs_parser.add_argument(
        "feature",
        nargs="?",
        help="Feature to display (shows MODULE_SPEC if not specified)",
    )

    return parser


def cmd_run(args: argparse.Namespace) -> int:
    """
    Run tests command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0=success, 1=violations, 2=test failures)
    """
    from testrs.repo import create_repo_context
    from testrs.validator import validate_rust_tests, format_violation_report
    from testrs.runner import run_rust_tests
    from testrs.output import warning, error, success, info

    try:
        ctx = create_repo_context()

        # Validate test organization first (unless --skip-enforcement)
        if not args.skip_enforcement:
            violations = validate_rust_tests(ctx.root, ctx.config)

            if not violations.is_valid():
                report = format_violation_report(violations, ctx.root)
                warning(report, "⚠ Test Organization Violations")

                if not args.override:
                    error(
                        f"Found {violations.total()} test organization violation(s).\n\n"
                        "Fix violations or use --override to run anyway.",
                        title="✗ Validation Failed"
                    )
                    return 1
                else:
                    warning(
                        "Running tests despite violations (--override mode)",
                        title="⚠ Override Mode"
                    )

        # Run tests
        timeout = args.timeout or ctx.config.rust.timeout
        category = getattr(args, 'category', None)
        module = getattr(args, 'module', None)

        info(f"Running Rust tests... (timeout: {timeout}s)")

        result = run_rust_tests(ctx.root, category, module, timeout)

        if result.success:
            success(
                f"Tests passed!\n\n"
                f"Passed: {result.passed}\n"
                f"Failed: {result.failed}\n"
                f"Ignored: {result.ignored}\n"
                f"Duration: {result.duration:.2f}s",
                title="✓ Test Results"
            )
            return 0
        else:
            error(
                f"Tests failed!\n\n"
                f"Passed: {result.passed}\n"
                f"Failed: {result.failed}\n"
                f"Ignored: {result.ignored}\n"
                f"Duration: {result.duration:.2f}s\n\n"
                f"Exit code: {result.exit_code}",
                title="✗ Test Results"
            )
            return 2

    except RuntimeError as e:
        print_error(str(e))
        return 127


def cmd_lint(args: argparse.Namespace) -> int:
    """
    Lint test organization command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0=valid, 1=violations found)
    """
    from testrs.repo import create_repo_context
    from testrs.validator import validate_rust_tests, format_violation_report, get_violation_summary
    from testrs.output import warning, success, info

    try:
        ctx = create_repo_context()

        # Validate test organization
        violations = validate_rust_tests(ctx.root, ctx.config)

        if violations.is_valid():
            success(
                f"No test organization violations found!\n\n"
                f"Project: {ctx.config.project_name or ctx.root.name}\n"
                f"Language: {ctx.primary_language}\n"
                f"Test root: {ctx.config.test_root}",
                title="✓ Validation Passed"
            )
            return 0
        else:
            # Show detailed report if --violations flag set
            if getattr(args, 'violations', False):
                report = format_violation_report(violations, ctx.root)
                warning(report, "⚠ Test Organization Violations")
            else:
                # Show summary only
                summary = get_violation_summary(violations)
                summary_text = (
                    f"Found {summary['total']} test organization violation(s):\n\n"
                    f"• Naming issues: {summary['naming']}\n"
                    f"• Missing sanity tests: {summary['missing_sanity']}\n"
                    f"• Missing UAT tests: {summary['missing_uat']}\n"
                    f"• Missing category entries: {summary['missing_category_entries']}\n"
                    f"• Unauthorized root files: {summary['unauthorized_root']}\n"
                    f"• Invalid directories: {summary['invalid_directories']}\n\n"
                    f"Run 'testrs lint --violations' for detailed report"
                )
                warning(summary_text, "⚠ Validation Failed")

            return 1

    except RuntimeError as e:
        print_error(str(e))
        return 127


def cmd_violations(args: argparse.Namespace) -> int:
    """
    Show violations command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0=no violations, 1=violations found)
    """
    # Just call lint with --violations
    args.violations = True
    return cmd_lint(args)


def cmd_check(args: argparse.Namespace) -> int:
    """
    Check configuration command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0=valid, 127=errors)
    """
    from testrs.repo import create_repo_context
    from testrs.output import success, error

    try:
        ctx = create_repo_context()

        if ctx.is_valid:
            success(
                f"Configuration valid!\n\n"
                f"Project: {ctx.config.project_name or ctx.root.name}\n"
                f"Languages: {', '.join(ctx.languages)}\n"
                f"Primary: {ctx.primary_language}\n"
                f"Test root: {ctx.config.test_root}\n"
                f"Features root: {ctx.config.features_root}",
                title="✓ Configuration Check"
            )
            return 0
        else:
            error(
                f"Configuration has {len(ctx.errors)} error(s):\n\n" +
                "\n".join(f"  • {err}" for err in ctx.errors),
                title="✗ Configuration Errors"
            )
            return 127

    except RuntimeError as e:
        print_error(str(e))
        return 127


def cmd_docs(args: argparse.Namespace) -> int:
    """
    Display documentation command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0=success)
    """
    info("Documentation display not yet implemented\n\nComing in Milestone 5!")
    return 127


def main() -> int:
    """
    Main entry point for testrs CLI.

    Returns:
        Exit code (0=success, non-zero=error)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Set output mode
    if args.no_boxy or args.view == "data":
        set_output_mode(OutputMode.DATA)
    else:
        set_output_mode(OutputMode.PRETTY)

    # Route to command handler
    command = args.command or "run"  # Default to run if no command specified

    if command == "run":
        return cmd_run(args)
    elif command == "lint":
        return cmd_lint(args)
    elif command == "violations":
        return cmd_violations(args)
    elif command == "check":
        return cmd_check(args)
    elif command == "docs":
        return cmd_docs(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
