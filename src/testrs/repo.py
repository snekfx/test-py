"""
Repository detection and validation for testrs.

Detects project type, validates requirements, and provides repository context.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from testrs.config import Config, create_default_config, load_config, validate_config


@dataclass
class RepoContext:
    """
    Repository context with detected project information.

    Provides validated repository information including:
    - Repository root (contains .git)
    - Project configuration
    - Detected languages
    - Primary language
    """

    # Repository root directory (contains .git)
    root: Path

    # Loaded or default configuration
    config: Config

    # Detected languages
    languages: List[str]

    # Primary language (by file count)
    primary_language: str

    # Validation errors (empty if valid)
    errors: List[str]

    @property
    def is_valid(self) -> bool:
        """Check if repository context is valid (no errors)."""
        return len(self.errors) == 0


def find_repo_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Find repository root by walking up directory tree.

    Looks for .git directory or manifest files (Cargo.toml, pyproject.toml, etc.)

    Args:
        start_path: Starting directory (defaults to current directory)

    Returns:
        Repository root Path if found, None otherwise
    """
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()

    # Walk up directory tree
    for parent in [current] + list(current.parents):
        # Primary indicator: .git directory
        if (parent / ".git").exists():
            return parent

        # Secondary indicators: project manifest files
        manifest_files = [
            "Cargo.toml",
            "pyproject.toml",
            "package.json",
            "setup.py",
        ]

        if any((parent / f).exists() for f in manifest_files):
            return parent

    return None


def detect_primary_language(repo_root: Path, languages: List[str]) -> str:
    """
    Detect primary language by counting source files.

    Args:
        repo_root: Repository root directory
        languages: List of languages to consider

    Returns:
        Primary language name (e.g., "rust", "python")
    """
    if not languages:
        return "rust"  # Default

    if len(languages) == 1:
        return languages[0]

    # Count files by extension for each language
    counts = {}

    for lang in languages:
        if lang == "rust":
            count = len(list(repo_root.glob("**/*.rs")))
            counts[lang] = count
        elif lang == "python":
            count = len(list(repo_root.glob("**/*.py")))
            counts[lang] = count
        elif lang == "nodejs":
            js_count = len(list(repo_root.glob("**/*.js")))
            ts_count = len(list(repo_root.glob("**/*.ts")))
            counts[lang] = js_count + ts_count
        elif lang == "shell":
            count = len(list(repo_root.glob("**/*.sh")))
            counts[lang] = count

    # Return language with highest count
    if counts:
        return max(counts.items(), key=lambda x: x[1])[0]

    return languages[0]  # Fallback to first language


def create_repo_context(start_path: Optional[Path] = None) -> RepoContext:
    """
    Create repository context from current or specified directory.

    Performs complete repository detection, configuration loading, and validation.

    Args:
        start_path: Starting directory (defaults to current directory)

    Returns:
        RepoContext with all information

    Raises:
        RuntimeError: If not in a valid repository
    """
    # Find repository root
    repo_root = find_repo_root(start_path)

    if repo_root is None:
        raise RuntimeError(
            "Not in a repository. testrs requires a git repository or project with manifest files."
        )

    # Load or create configuration
    config = load_config(repo_root)

    if config is None:
        # No .spec.toml found, create default config
        config = create_default_config(repo_root)

    # Validate configuration
    errors = validate_config(config, repo_root)

    # Detect primary language
    primary_lang = detect_primary_language(repo_root, config.languages)

    return RepoContext(
        root=repo_root,
        config=config,
        languages=config.languages,
        primary_language=primary_lang,
        errors=errors,
    )


def validate_language_requirements(repo_root: Path, language: str) -> List[str]:
    """
    Validate language-specific requirements.

    Args:
        repo_root: Repository root directory
        language: Language to validate ("rust", "python", "nodejs", "shell")

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    if language == "rust":
        if not (repo_root / "Cargo.toml").exists():
            errors.append("Rust language requires Cargo.toml in repository root")

        # Check for src/ directory
        if not (repo_root / "src").exists():
            errors.append("Rust language expects src/ directory")

    elif language == "python":
        manifests = ["pyproject.toml", "setup.py", "setup.cfg"]
        if not any((repo_root / f).exists() for f in manifests):
            errors.append(
                f"Python language requires one of: {', '.join(manifests)}"
            )

        # Check for src/ or package directory
        src_dir = repo_root / "src"
        if not src_dir.exists():
            # Look for any Python packages in root
            py_packages = list(repo_root.glob("*/__init__.py"))
            if not py_packages:
                errors.append("Python project expects src/ directory or package in root")

    elif language == "nodejs":
        if not (repo_root / "package.json").exists():
            errors.append("Node.js language requires package.json in repository root")

    elif language == "shell":
        # Shell is flexible - just needs test scripts
        # No strict requirements beyond tests/ directory
        pass

    return errors


def get_manifest_project_name(repo_root: Path) -> Optional[str]:
    """
    Get project name from manifest files.

    Tries in order: Cargo.toml, pyproject.toml, package.json

    Args:
        repo_root: Repository root directory

    Returns:
        Project name if found, None otherwise
    """
    # Try Cargo.toml
    cargo_toml = repo_root / "Cargo.toml"
    if cargo_toml.exists():
        try:
            import sys
            if sys.version_info >= (3, 11):
                import tomllib
            else:
                try:
                    import tomli as tomllib
                except ImportError:
                    tomllib = None

            if tomllib:
                with open(cargo_toml, "rb") as f:
                    data = tomllib.load(f)
                    package_name = data.get("package", {}).get("name")
                    if package_name:
                        return package_name
        except Exception:
            pass

    # Try pyproject.toml
    pyproject_toml = repo_root / "pyproject.toml"
    if pyproject_toml.exists():
        try:
            import sys
            if sys.version_info >= (3, 11):
                import tomllib
            else:
                try:
                    import tomli as tomllib
                except ImportError:
                    tomllib = None

            if tomllib:
                with open(pyproject_toml, "rb") as f:
                    data = tomllib.load(f)
                    project_name = data.get("project", {}).get("name")
                    if project_name:
                        return project_name
        except Exception:
            pass

    # Try package.json
    package_json = repo_root / "package.json"
    if package_json.exists():
        try:
            import json
            with open(package_json) as f:
                data = json.load(f)
                name = data.get("name")
                if name:
                    return name
        except Exception:
            pass

    return None
