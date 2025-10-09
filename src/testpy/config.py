"""
Configuration management for testpy.

Loads and validates .spec.toml configuration files with multi-language support.
Provides fallback chains: .spec.toml → language manifest → sensible defaults
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

# TOML parsing: Python 3.11+ has tomllib, older versions need tomli
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore


@dataclass
class LanguageConfig:
    """Configuration for a specific language."""

    # Test file patterns for this language
    test_patterns: List[str] = field(default_factory=list)

    # Module file patterns for this language
    module_patterns: List[str] = field(default_factory=list)

    # Exclusion patterns specific to this language
    exclusions: List[str] = field(default_factory=list)

    # Test runner command template (e.g., "cargo test", "pytest")
    runner_cmd: Optional[str] = None

    # Test timeout in seconds
    timeout: int = 600

    # Runner-specific options
    runner_options: Dict[str, str] = field(default_factory=dict)


@dataclass
class Config:
    """
    Main configuration for testpy.

    Loaded from .spec.toml with language-specific sections.
    """

    # Project metadata
    project_name: Optional[str] = None

    # Active languages (e.g., ["rust", "python", "nodejs", "shell"])
    languages: List[str] = field(default_factory=lambda: ["rust"])

    # Test organization
    test_root: str = "tests"

    # Features root (for module discovery)
    features_root: str = "src"

    # Global exclusion patterns
    exclude: List[str] = field(default_factory=list)

    # Per-language configuration
    rust: LanguageConfig = field(default_factory=LanguageConfig)
    python: LanguageConfig = field(default_factory=LanguageConfig)
    nodejs: LanguageConfig = field(default_factory=LanguageConfig)
    shell: LanguageConfig = field(default_factory=LanguageConfig)

    # Source file path
    source_file: Optional[Path] = None

    def __post_init__(self):
        """Apply language-specific defaults after initialization."""
        self._apply_defaults()

    def _apply_defaults(self):
        """Apply sensible defaults for each language."""

        # Rust defaults
        if not self.rust.test_patterns:
            self.rust.test_patterns = [
                "tests/*.rs",
                "tests/**/*.rs",
            ]
        if not self.rust.module_patterns:
            self.rust.module_patterns = [
                "src/*/mod.rs",      # MODULE_SPEC pattern
                "src/*.rs",          # Legacy pattern (optional)
            ]
        if not self.rust.exclusions:
            self.rust.exclusions = [
                "_*",
                "dev_*",
                "prelude*",
                "dummy_*",
                "lib.rs",
                "main.rs",
            ]
        if not self.rust.runner_cmd:
            self.rust.runner_cmd = "cargo test"

        # Python defaults
        if not self.python.test_patterns:
            self.python.test_patterns = [
                "tests/test_*.py",
                "tests/*_test.py",
                "tests/**/*_test.py",
            ]
        if not self.python.module_patterns:
            self.python.module_patterns = [
                "src/*/__init__.py",  # Package pattern
                "src/*.py",           # Module pattern
                "*/__init__.py",      # Flat layout
                "*.py",               # Flat layout modules
            ]
        if not self.python.exclusions:
            self.python.exclusions = [
                "__pycache__",
                "*.pyc",
                "_*",
                "dev_*",
                "test_*",
                "conftest.py",
            ]
        if not self.python.runner_cmd:
            self.python.runner_cmd = "pytest"

        # Node.js defaults
        if not self.nodejs.test_patterns:
            self.nodejs.test_patterns = [
                "tests/*.test.js",
                "tests/*.spec.js",
                "tests/**/*.test.js",
                "__tests__/**/*.js",
            ]
        if not self.nodejs.module_patterns:
            self.nodejs.module_patterns = [
                "src/**/*.js",
                "src/**/*.ts",
                "lib/**/*.js",
            ]
        if not self.nodejs.exclusions:
            self.nodejs.exclusions = [
                "node_modules",
                "dist",
                "build",
                "_*",
                "dev_*",
                "*.test.js",
                "*.spec.js",
            ]
        if not self.nodejs.runner_cmd:
            self.nodejs.runner_cmd = "npm test"

        # Shell defaults
        if not self.shell.test_patterns:
            self.shell.test_patterns = [
                "tests/*.sh",
                "tests/**/*.sh",
                "tests/sh/*.sh",
            ]
        if not self.shell.module_patterns:
            self.shell.module_patterns = [
                "bin/*.sh",
                "scripts/*.sh",
                "src/**/*.sh",
            ]
        if not self.shell.exclusions:
            self.shell.exclusions = [
                "_*",
                "dev_*",
                "*.bak",
            ]
        if not self.shell.runner_cmd:
            self.shell.runner_cmd = "bash"


def load_config(repo_root: Path) -> Optional[Config]:
    """
    Load configuration from .spec.toml.

    Args:
        repo_root: Repository root directory

    Returns:
        Config object if .spec.toml found, None otherwise
    """
    spec_path = repo_root / ".spec.toml"

    if not spec_path.exists():
        return None

    if tomllib is None:
        raise RuntimeError(
            "TOML parsing not available. Install tomli: pip install tomli"
        )

    with open(spec_path, "rb") as f:
        data = tomllib.load(f)

    # Check for [tests] section (new format)
    # Fallback to top-level config (legacy format)
    tests_section = data.get("tests", {})

    # Extract main config
    # Priority: [tests] section > top-level (for backward compatibility)
    config = Config(
        project_name=data.get("project_name"),
        languages=data.get("languages", ["rust"]),
        test_root=tests_section.get("test_root", data.get("test_root", "tests")),
        features_root=data.get("features_root", "src"),
        exclude=tests_section.get("exclude", data.get("exclude", [])),
        source_file=spec_path,
    )

    # Load language-specific sections
    # Priority: [tests.rust] > [rust] (backward compatibility)
    if "rust" in tests_section:
        config.rust = _load_lang_config(tests_section["rust"])
    elif "rust" in data:
        config.rust = _load_lang_config(data["rust"])

    if "python" in tests_section:
        config.python = _load_lang_config(tests_section["python"])
    elif "python" in data:
        config.python = _load_lang_config(data["python"])

    if "nodejs" in tests_section:
        config.nodejs = _load_lang_config(tests_section["nodejs"])
    elif "nodejs" in data:
        config.nodejs = _load_lang_config(data["nodejs"])

    if "shell" in tests_section:
        config.shell = _load_lang_config(tests_section["shell"])
    elif "shell" in data:
        config.shell = _load_lang_config(data["shell"])

    # Apply defaults after loading
    config._apply_defaults()

    return config


def _load_lang_config(data: Dict) -> LanguageConfig:
    """Load language-specific configuration from TOML data."""
    return LanguageConfig(
        test_patterns=data.get("test_patterns", []),
        module_patterns=data.get("module_patterns", []),
        exclusions=data.get("exclusions", []),
        runner_cmd=data.get("runner_cmd"),
        timeout=data.get("timeout", 600),
        runner_options=data.get("runner_options", {}),
    )


def detect_languages(repo_root: Path) -> List[str]:
    """
    Detect project languages from manifest files.

    Fallback chain when .spec.toml doesn't specify languages.

    Args:
        repo_root: Repository root directory

    Returns:
        List of detected languages (e.g., ["rust", "python"])
    """
    languages = []

    # Rust: Cargo.toml
    if (repo_root / "Cargo.toml").exists():
        languages.append("rust")

    # Python: pyproject.toml, setup.py, or setup.cfg
    if any((repo_root / f).exists() for f in ["pyproject.toml", "setup.py", "setup.cfg"]):
        languages.append("python")

    # Node.js: package.json
    if (repo_root / "package.json").exists():
        languages.append("nodejs")

    # Shell: tests/ directory with .sh files
    tests_dir = repo_root / "tests"
    if tests_dir.exists() and list(tests_dir.glob("**/*.sh")):
        languages.append("shell")

    return languages if languages else ["rust"]  # Default to Rust


def create_default_config(repo_root: Path, languages: Optional[List[str]] = None) -> Config:
    """
    Create a default configuration.

    Args:
        repo_root: Repository root directory
        languages: Languages to configure (auto-detected if None)

    Returns:
        Config with sensible defaults
    """
    if languages is None:
        languages = detect_languages(repo_root)

    return Config(
        project_name=repo_root.name,
        languages=languages,
        test_root="tests",
        features_root="src",
    )


def validate_config(config: Config, repo_root: Path) -> List[str]:
    """
    Validate configuration against project requirements.

    Args:
        config: Configuration to validate
        repo_root: Repository root directory

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    # Validate languages
    valid_languages = {"rust", "python", "nodejs", "shell"}
    for lang in config.languages:
        if lang not in valid_languages:
            errors.append(f"Invalid language: {lang}. Valid: {', '.join(valid_languages)}")

    # Rust-specific validation
    if "rust" in config.languages:
        if not (repo_root / "Cargo.toml").exists():
            errors.append("Rust language configured but Cargo.toml not found")

    # Python-specific validation
    if "python" in config.languages:
        manifests = ["pyproject.toml", "setup.py", "setup.cfg"]
        if not any((repo_root / f).exists() for f in manifests):
            errors.append(
                f"Python language configured but no manifest found (need one of: {', '.join(manifests)})"
            )

    # Node.js-specific validation
    if "nodejs" in config.languages:
        if not (repo_root / "package.json").exists():
            errors.append("Node.js language configured but package.json not found")

    # Validate test_root exists
    test_dir = repo_root / config.test_root
    if not test_dir.exists():
        errors.append(f"Test directory not found: {config.test_root}")

    # Validate features_root exists
    features_dir = repo_root / config.features_root
    if not features_dir.exists():
        errors.append(f"Features directory not found: {config.features_root}")

    return errors
