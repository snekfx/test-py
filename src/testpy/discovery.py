"""
Module and test discovery for testpy.

Language-agnostic discovery with per-language implementations.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from testpy.config import Config


@dataclass
class Module:
    """Discovered module information."""

    # Module name (e.g., "math", "com", "global")
    name: str

    # Module file path (e.g., src/math/mod.rs)
    path: Path

    # Language ("rust", "python", "nodejs", "shell")
    language: str

    # Whether module is public (has pub keyword)
    is_public: bool = True


@dataclass
class TestFile:
    """Discovered test file information."""

    # Test file path
    path: Path

    # Test category (sanity, smoke, unit, etc.)
    category: Optional[str] = None

    # Module being tested (e.g., "math")
    module: Optional[str] = None

    # Language
    language: str = "rust"

    # Whether this is a category entry file (e.g., sanity.rs)
    is_category_entry: bool = False


def discover_rust_modules(repo_root: Path, config: Config) -> List[Module]:
    """
    Discover Rust modules from src/ directory.

    Implements MODULE_SPEC pattern: src/module/mod.rs

    Args:
        repo_root: Repository root directory
        config: Configuration with features_root and exclusions

    Returns:
        List of discovered Rust modules
    """
    modules = []
    src_dir = repo_root / config.features_root

    if not src_dir.exists():
        return modules

    # Get exclusion patterns from config
    exclusions = config.rust.exclusions + config.exclude

    # Pattern 1: src/module/mod.rs (MODULE_SPEC standard)
    for mod_rs in src_dir.glob("*/mod.rs"):
        module_name = mod_rs.parent.name

        # Apply exclusion patterns
        if _is_excluded(module_name, exclusions):
            continue

        modules.append(
            Module(
                name=module_name,
                path=mod_rs,
                language="rust",
                is_public=_check_rust_public(mod_rs),
            )
        )

    # Pattern 2: src/module.rs (legacy, optional - not in exclusions)
    # Only if explicitly enabled or found in older projects
    for module_rs in src_dir.glob("*.rs"):
        module_name = module_rs.stem

        # Skip lib.rs and main.rs (always excluded)
        if module_name in ["lib", "main"]:
            continue

        # Apply exclusion patterns
        if _is_excluded(module_name, exclusions):
            continue

        # Only add if not already found as mod.rs
        if not any(m.name == module_name for m in modules):
            modules.append(
                Module(
                    name=module_name,
                    path=module_rs,
                    language="rust",
                    is_public=_check_rust_public(module_rs),
                )
            )

    return sorted(modules, key=lambda m: m.name)


def discover_rust_tests(repo_root: Path, config: Config) -> List[TestFile]:
    """
    Discover Rust test files in tests/ directory.

    Supports three patterns:
    1. Wrapper style: tests/sanity_math.rs
    2. Directory style: tests/sanity/math.rs
    3. Prefixed style: tests/sanity/sanity_math.rs

    Args:
        repo_root: Repository root directory
        config: Configuration with test_root

    Returns:
        List of discovered test files
    """
    tests = []
    test_dir = repo_root / config.test_root

    if not test_dir.exists():
        return tests

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

    # Pattern 1 & 3: tests/*.rs files (wrappers and category entries)
    for test_file in test_dir.glob("*.rs"):
        basename = test_file.stem

        # Skip excluded patterns (_*, dev_*)
        if basename.startswith("_") or basename.startswith("dev_"):
            continue

        # Check if it's a category entry file (e.g., sanity.rs)
        if basename in valid_categories:
            tests.append(
                TestFile(
                    path=test_file,
                    category=basename,
                    module=None,
                    language="rust",
                    is_category_entry=True,
                )
            )
            continue

        # Try to parse category_module pattern
        parts = basename.split("_", 1)
        if len(parts) == 2:
            category, module = parts
            if category in valid_categories:
                tests.append(
                    TestFile(
                        path=test_file,
                        category=category,
                        module=module,
                        language="rust",
                        is_category_entry=False,
                    )
                )

    # Pattern 2: tests/<category>/*.rs files
    for category in valid_categories:
        category_dir = test_dir / category
        if not category_dir.exists():
            continue

        for test_file in category_dir.glob("*.rs"):
            basename = test_file.stem

            # Skip excluded patterns
            if basename.startswith("_") or basename.startswith("dev_"):
                continue

            # Module name is the file stem (might be prefixed or not)
            # Handle prefixed style: sanity/sanity_math.rs
            if basename.startswith(f"{category}_"):
                module = basename[len(category) + 1 :]
            else:
                # Directory style: sanity/math.rs
                module = basename

            tests.append(
                TestFile(
                    path=test_file,
                    category=category,
                    module=module,
                    language="rust",
                    is_category_entry=False,
                )
            )

    return sorted(tests, key=lambda t: (t.category or "", t.module or ""))


def _is_excluded(name: str, exclusions: List[str]) -> bool:
    """
    Check if module name matches exclusion patterns.

    Args:
        name: Module name to check
        exclusions: List of exclusion patterns

    Returns:
        True if excluded, False otherwise
    """
    for pattern in exclusions:
        # Simple wildcard matching
        if pattern.endswith("*"):
            prefix = pattern[:-1]
            if name.startswith(prefix):
                # Special case: 'dev' itself is NOT excluded, only dev_*
                if pattern == "dev_*" and name == "dev":
                    continue
                return True
        elif pattern.startswith("*"):
            suffix = pattern[1:]
            if name.endswith(suffix):
                return True
        elif pattern == name:
            return True

    return False


def _check_rust_public(module_path: Path) -> bool:
    """
    Check if Rust module has pub keyword (is public).

    Simple heuristic: check if file contains 'pub ' keyword.

    Args:
        module_path: Path to Rust module file

    Returns:
        True if module appears to be public
    """
    try:
        content = module_path.read_text()
        # Simple check: does file contain 'pub '?
        return "pub " in content or "pub(" in content
    except Exception:
        # Default to True if can't read
        return True


def find_test_for_module(
    module: Module, tests: List[TestFile], category: str
) -> Optional[TestFile]:
    """
    Find test file for a specific module and category.

    Args:
        module: Module to find test for
        tests: List of discovered tests
        category: Test category (e.g., "sanity", "uat")

    Returns:
        TestFile if found, None otherwise
    """
    for test in tests:
        if test.category == category and test.module == module.name:
            return test
    return None


def get_category_entry_file(tests: List[TestFile], category: str) -> Optional[TestFile]:
    """
    Get category entry file for a category.

    Args:
        tests: List of discovered tests
        category: Category name (e.g., "sanity")

    Returns:
        TestFile if category entry exists, None otherwise
    """
    for test in tests:
        if test.is_category_entry and test.category == category:
            return test
    return None
