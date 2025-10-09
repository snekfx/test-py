"""
Test organization validation for testpy.

Enforces RSB test organization standards with categorized violation reporting.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from testpy.config import Config
from testpy.discovery import Module, TestFile, discover_rust_modules, discover_rust_tests


@dataclass
class Violations:
    """Categorized test organization violations."""

    # Naming violations: files don't follow <category>_<module>.rs pattern
    naming: List[str] = field(default_factory=list)

    # Missing sanity tests: modules without sanity tests
    missing_sanity: List[str] = field(default_factory=list)

    # Missing UAT tests: modules without UAT tests
    missing_uat: List[str] = field(default_factory=list)

    # Missing category entry files: no sanity.rs, smoke.rs, etc.
    missing_category_entries: List[str] = field(default_factory=list)

    # Unauthorized root files: tests/foo.rs doesn't match pattern
    unauthorized_root: List[str] = field(default_factory=list)

    # Invalid directories: tests/foo/ is not a valid category
    invalid_directories: List[str] = field(default_factory=list)

    # Missing hub integration tests: hub packages without integration tests
    missing_hub_integration: List[str] = field(default_factory=list)

    def total(self) -> int:
        """Get total violation count."""
        return (
            len(self.naming)
            + len(self.missing_sanity)
            + len(self.missing_uat)
            + len(self.missing_category_entries)
            + len(self.unauthorized_root)
            + len(self.invalid_directories)
            + len(self.missing_hub_integration)
        )

    def is_valid(self) -> bool:
        """Check if there are no violations."""
        return self.total() == 0


def validate_rust_tests(repo_root: Path, config: Config) -> Violations:
    """
    Validate Rust test organization against RSB standards.

    Checks:
    1. Test naming patterns: <category>_<module>.rs
    2. Required tests: sanity + UAT per module
    3. Category entry files: sanity.rs, smoke.rs, etc.
    4. Unauthorized root files
    5. Invalid test directories

    Args:
        repo_root: Repository root directory
        config: Configuration

    Returns:
        Violations object with categorized violations
    """
    violations = Violations()

    # Discover modules and tests
    modules = discover_rust_modules(repo_root, config)
    tests = discover_rust_tests(repo_root, config)

    # Valid categories
    valid_categories = {
        "sanity",
        "smoke",
        "unit",
        "integration",
        "e2e",
        "uat",
        "chaos",
        "bench",
        "regression",
    }

    # Required category entry files
    required_category_entries = list(valid_categories)

    test_dir = repo_root / config.test_root

    # Check 1: Naming violations (tests/*.rs files with wrong pattern)
    if test_dir.exists():
        for test_file in test_dir.glob("*.rs"):
            basename = test_file.stem

            # Skip excluded patterns
            if basename.startswith("_") or basename.startswith("dev_"):
                continue

            # Check if it's a valid category entry
            if basename in valid_categories:
                continue

            # Check if it matches <category>_<module> pattern
            parts = basename.split("_", 1)
            if len(parts) != 2:
                violations.naming.append(str(test_file.relative_to(repo_root)))
                continue

            category, module = parts
            if category not in valid_categories:
                violations.naming.append(str(test_file.relative_to(repo_root)))

    # Check 2: Missing sanity tests per module
    for module in modules:
        # Check for sanity test in any of the 3 patterns
        has_sanity = any(
            t.category == "sanity" and t.module == module.name for t in tests
        )

        if not has_sanity:
            violations.missing_sanity.append(module.name)

    # Check 3: Missing UAT tests per module
    for module in modules:
        # Check for UAT test in any of the 3 patterns
        has_uat = any(t.category == "uat" and t.module == module.name for t in tests)

        if not has_uat:
            violations.missing_uat.append(module.name)

    # Check 4: Missing category entry files
    category_entries_found = {t.category for t in tests if t.is_category_entry}

    for category in required_category_entries:
        if category not in category_entries_found:
            # Also check if .sh version exists
            sh_file = test_dir / f"{category}.sh"
            if not sh_file.exists():
                violations.missing_category_entries.append(category)

    # Check 5: Unauthorized root files (tests/*.rs or tests/*.sh not matching rules)
    if test_dir.exists():
        for test_file in list(test_dir.glob("*.rs")) + list(test_dir.glob("*.sh")):
            basename = test_file.stem

            # Skip excluded patterns
            if basename.startswith("_") or basename.startswith("dev_"):
                continue

            # Check if it's a category entry
            if basename in valid_categories:
                continue

            # Check if it's a valid <category>_<module> pattern
            parts = basename.split("_", 1)
            is_valid = False

            if len(parts) == 2:
                category, module = parts
                if category in valid_categories:
                    is_valid = True

            if not is_valid:
                violations.unauthorized_root.append(
                    str(test_file.relative_to(repo_root))
                )

    # Check 6: Invalid test directories
    if test_dir.exists():
        for subdir in test_dir.iterdir():
            if not subdir.is_dir():
                continue

            dir_name = subdir.name

            # Valid directories: categories, sh, _archive, _adhoc
            valid_dirs = valid_categories | {"sh", "_archive", "_adhoc"}

            if dir_name not in valid_dirs:
                violations.invalid_directories.append(
                    str(subdir.relative_to(repo_root))
                )

    # Validation 6: Check for hub integration tests (optional)
    violations.missing_hub_integration = validate_hub_integration_tests(repo_root)

    return violations


def get_violation_summary(violations: Violations) -> Dict[str, int]:
    """
    Get violation summary with counts per type.

    Args:
        violations: Violations object

    Returns:
        Dict mapping violation type to count
    """
    return {
        "naming": len(violations.naming),
        "missing_sanity": len(violations.missing_sanity),
        "missing_uat": len(violations.missing_uat),
        "missing_category_entries": len(violations.missing_category_entries),
        "unauthorized_root": len(violations.unauthorized_root),
        "invalid_directories": len(violations.invalid_directories),
        "missing_hub_integration": len(violations.missing_hub_integration),
        "total": violations.total(),
    }


def format_violation_report(violations: Violations, repo_root: Path) -> str:
    """
    Format detailed violation report for display.

    Args:
        violations: Violations to report
        repo_root: Repository root for relative paths

    Returns:
        Formatted report string
    """
    lines = []

    lines.append(f"📋 Test Organization Violations Report ({violations.total()} total)")
    lines.append("=" * 80)
    lines.append("")

    # Naming violations
    if violations.naming:
        lines.append(f"🏷️  NAMING VIOLATIONS ({len(violations.naming)} files)")
        lines.append("-" * 80)
        lines.append("Issue: Test wrapper files don't follow naming pattern")
        lines.append(
            "Required: <category>_<module>.rs (e.g., sanity_com.rs, uat_math.rs)"
        )
        lines.append(
            "Valid categories: unit, sanity, smoke, integration, e2e, uat, chaos, bench"
        )
        lines.append("")
        for i, file in enumerate(violations.naming, 1):
            lines.append(f"  {i:3d}. {file}")
        lines.append("")
        lines.append(
            "Fix: Rename files to match pattern (e.g., com_sanity.rs → sanity_com.rs)"
        )
        lines.append("")

    # Missing sanity tests
    if violations.missing_sanity:
        lines.append(
            f"🚨 MISSING SANITY TESTS ({len(violations.missing_sanity)} modules)"
        )
        lines.append("-" * 80)
        lines.append("Issue: Modules without required sanity tests")
        lines.append("Required: Every module must have sanity tests for core functionality")
        lines.append("")
        for i, module in enumerate(violations.missing_sanity, 1):
            lines.append(f"  {i:3d}. Module '{module}' (create: tests/sanity_{module}.rs)")
        lines.append("")
        lines.append("Fix: Create sanity test files for each module")
        lines.append("")

    # Missing UAT tests
    if violations.missing_uat:
        lines.append(f"🎭 MISSING UAT TESTS ({len(violations.missing_uat)} modules)")
        lines.append("-" * 80)
        lines.append("Issue: Modules without required visual UAT/ceremony tests")
        lines.append(
            "Required: Every module must have UAT tests for visual demonstrations"
        )
        lines.append("")
        for i, module in enumerate(violations.missing_uat, 1):
            lines.append(f"  {i:3d}. Module '{module}' (create: tests/uat_{module}.rs)")
        lines.append("")
        lines.append("Fix: Create UAT test files with visual demonstrations for each module")
        lines.append("")

    # Missing category entries
    if violations.missing_category_entries:
        lines.append(
            f"📋 MISSING CATEGORY ENTRY FILES ({len(violations.missing_category_entries)} categories)"
        )
        lines.append("-" * 80)
        lines.append("Issue: Missing category-level test orchestrators")
        lines.append(
            "Required: Each category needs an entry file (e.g., smoke.rs, unit.rs)"
        )
        lines.append("")
        for i, category in enumerate(violations.missing_category_entries, 1):
            lines.append(f"  {i:3d}. Category '{category}' (create: tests/{category}.rs)")
        lines.append("")
        lines.append("Fix: Create category entry files for cross-module integration tests")
        lines.append("")

    # Unauthorized root files
    if violations.unauthorized_root:
        lines.append(
            f"🚫 UNAUTHORIZED ROOT FILES ({len(violations.unauthorized_root)} files)"
        )
        lines.append("-" * 80)
        lines.append("Issue: Files in tests/ root that don't follow organization rules")
        lines.append("Allowed: <category>.rs or <category>_<module>.rs only")
        lines.append("")
        for i, file in enumerate(violations.unauthorized_root, 1):
            lines.append(f"  {i:3d}. {file}")
        lines.append("")
        lines.append(
            "Fix: Rename to pattern, move to tests/_adhoc/, or move to tests/_archive/"
        )
        lines.append("")

    # Invalid directories
    if violations.invalid_directories:
        lines.append(
            f"📁 INVALID DIRECTORIES ({len(violations.invalid_directories)} directories)"
        )
        lines.append("-" * 80)
        lines.append("Issue: Test directories don't match approved organization")
        lines.append(
            "Valid: unit/, sanity/, smoke/, integration/, e2e/, uat/, chaos/, bench/, regression/, sh/, _archive/, _adhoc/"
        )
        lines.append("")
        for i, dir_path in enumerate(violations.invalid_directories, 1):
            lines.append(f"  {i:3d}. {dir_path}")
        lines.append("")
        lines.append(
            "Fix: Move tests to approved category directories or rename to _archive/"
        )
        lines.append("")

    # Missing hub integration tests
    if violations.missing_hub_integration:
        lines.append(
            f"🔌 MISSING HUB INTEGRATION TESTS ({len(violations.missing_hub_integration)} packages)"
        )
        lines.append("-" * 80)
        lines.append("Issue: Hub packages missing integration tests")
        lines.append("Pattern: tests/integration/hub_<package>.rs")
        lines.append("Purpose: Lightweight sanity check that hub package is accessible")
        lines.append("")
        for i, package in enumerate(violations.missing_hub_integration, 1):
            lines.append(f"  {i:3d}. {package}")
            lines.append(f"       Expected: tests/integration/hub_{package}.rs")
        lines.append("")
        lines.append("Fix: Create hub integration tests for each package:")
        lines.append("  // tests/integration/hub_chrono.rs")
        lines.append("  #[test]")
        lines.append("  fn hub_chrono_available() {")
        lines.append("      use myproject::deps::chrono::Utc;")
        lines.append("      let now = Utc::now();")
        lines.append("      assert!(now.timestamp() > 0);")
        lines.append("  }")
        lines.append("")

    # Summary
    summary = get_violation_summary(violations)
    lines.append("VIOLATION SUMMARY & FIXES")
    lines.append("")
    lines.append(f"Total Violations: {summary['total']}")
    lines.append(f"• Naming issues: {summary['naming']}")
    lines.append(f"• Missing sanity tests: {summary['missing_sanity']}")
    lines.append(f"• Missing UAT tests: {summary['missing_uat']}")
    lines.append(f"• Missing category entries: {summary['missing_category_entries']}")
    lines.append(f"• Unauthorized root files: {summary['unauthorized_root']}")
    lines.append(f"• Invalid directories: {summary['invalid_directories']}")
    lines.append(f"• Missing hub integration tests: {summary['missing_hub_integration']}")
    lines.append("")
    lines.append("QUICK FIXES:")
    lines.append("• Run 'testpy lint --violations' for detailed analysis")
    lines.append("• Use 'testpy --override' for emergency bypass")
    lines.append("• Follow naming pattern: <category>_<module>.rs")
    lines.append("• Create missing sanity tests for all modules")

    return "\n".join(lines)


def get_hub_packages() -> List[str]:
    """
    Get list of hub packages from blade cache.

    Parses ~/.local/data/snek/blade/deps_cache.tsv to extract
    packages from the hub repo (dependency reexports).

    Returns:
        List of hub package names (e.g., ["chrono", "serde", "regex"])
        Empty list if blade cache not found or hub repo not detected
    """
    cache_file = Path.home() / ".local/data/snek/blade/deps_cache.tsv"

    if not cache_file.exists():
        return []  # Blade cache not generated yet

    packages = []
    hub_repo_id = None

    try:
        with open(cache_file, "r") as f:
            for line in f:
                parts = line.strip().split("\t")

                if len(parts) < 2:
                    continue

                # Find hub repo line: has "hub" name and "Cargo.toml" in path
                if parts[1] == "hub" and "Cargo.toml" in line:
                    hub_repo_id = parts[0]
                    continue

                # If we found hub repo, collect its dependencies
                if hub_repo_id and parts[0].startswith(hub_repo_id):
                    # Dependency lines: <id> <repo_id> <package> <version> ...
                    if len(parts) >= 3 and parts[0] != hub_repo_id:
                        package_name = parts[2]
                        packages.append(package_name)
                    # Stop when we hit next repo (different prefix)
                    elif not parts[0].startswith(hub_repo_id):
                        break

    except Exception:
        # Silently fail - hub validation is optional
        return []

    return sorted(set(packages))


def has_hub_usage(repo_root: Path) -> bool:
    """
    Check if repository uses hub (dependency reexports).

    Args:
        repo_root: Repository root directory

    Returns:
        True if repo has src/deps.rs (hub usage indicator)
    """
    deps_file = repo_root / "src" / "deps.rs"
    return deps_file.exists()


def validate_hub_integration_tests(repo_root: Path) -> List[str]:
    """
    Validate that hub packages have integration tests.

    For projects using hub (dependency reexports), checks that each
    hub package has a corresponding integration test file following
    the pattern: tests/integration/hub_<package>.rs

    Args:
        repo_root: Repository root directory

    Returns:
        List of hub packages missing integration tests
    """
    # Skip if project doesn't use hub
    if not has_hub_usage(repo_root):
        return []

    hub_packages = get_hub_packages()
    if not hub_packages:
        return []  # No hub packages found or blade cache unavailable

    missing = []
    integration_dir = repo_root / "tests" / "integration"

    for package in hub_packages:
        # Expected test file: tests/integration/hub_<package>.rs
        test_file = integration_dir / f"hub_{package}.rs"
        if not test_file.exists():
            missing.append(package)

    return missing
