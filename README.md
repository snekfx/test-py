# testrs - RSB Test Orchestrator for Rust Projects

Universal Python-based test runner implementing RSB (Rebel String-Biased) test organization standards.

## ⚠️ Important: Code References

This project uses **oodx-rsb** as the **ONLY** canonical reference for RSB test patterns.

See [CODE_REFERENCES.md](docs/CODE_REFERENCES.md) for detailed source hierarchy and reliability guide.

**TL;DR:**
- ✅ **Reference:** `code_ref/rsb_test.sh` (oodx-rsb - canonical)
- ⚠️ **Architecture only:** `code_ref/testsh` (BashFX - modular example)
- ❌ **Avoid:** Other test.sh files in rust projects (outdated/unreliable)

## Status

✅ **Milestone 1 Complete** - Foundation & Infrastructure (16/16 points)
✅ **Milestone 2 Complete** - Rust Support (28/28 points)

**Current Progress:** 44/133 story points (33%)

**Working Features:**
- ✅ Multi-language configuration system (.spec.toml)
- ✅ Repository detection and validation
- ✅ Rust module discovery (MODULE_SPEC + legacy patterns)
- ✅ Rust test discovery (3 RSB patterns: wrapper, directory, prefixed)
- ✅ Rust test validation (6 violation types)
- ✅ Rust test execution (cargo test with timeout)
- ✅ Beautiful violation reports (boxy integration)
- ✅ CLI with lint, run, check, violations commands
- ✅ Override and enforcement modes

**Next:** Milestone 3 - Multi-Language Support (deferred) or Milestone 5 - Reporting & Polish

## Goals

Create a universal, Python-based test orchestrator that:

1. **Enforces RSB Standards**
   - Test naming patterns: `<category>_<module>.rs`
   - Required tests: sanity + UAT per module
   - Test organization validation
   - MODULE_SPEC compliance

2. **Cross-Platform Support**
   - Works on Linux, macOS, Windows
   - Better than shell for portability
   - Consistent behavior across environments

3. **Easy Integration**
   - Single tool for all Rust projects
   - Configuration-driven
   - Minimal per-project setup

4. **Comprehensive Testing**
   - 9 test categories: sanity, smoke, unit, integration, e2e, uat, chaos, bench, regression
   - Parallel test execution
   - Timeout handling
   - Beautiful reporting

## Project Structure

```
test-py/
├── src/testrs/          # Python package (to be implemented)
├── bin/
│   └── deploy.sh        # Deployment script
├── code_ref/            # Reference implementations (READ-ONLY)
│   ├── rsb_test.sh      # Symlink to canonical oodx-rsb test.sh
│   └── testsh/          # Symlink to BashFX modular architecture
├── docs/
│   ├── CODE_REFERENCES.md            # Source reliability guide
│   ├── rust_test_standardization_plan.md  # Overall strategy
│   └── ref/
│       ├── MODULE_SPEC.md            # RSB module spec
│       ├── rsb_test_patterns_analysis.md  # Canonical logic analysis
│       └── shell_architecture_comparison.md
└── pyproject.toml       # Python package config
```

## Installation

```bash
# Development install
cd /home/xnull/repos/code/python/snekfx/test-py
pip install -e .

# Or use directly with PYTHONPATH
export PYTHONPATH=/home/xnull/repos/code/python/snekfx/test-py/src
python -m testrs --help
```

## Usage

```bash
# Check configuration
testrs check

# Validate test organization (lint)
testrs lint                    # Show summary
testrs lint --violations       # Show detailed report

# Run tests (validates first, then runs cargo test)
testrs run                     # Run all tests
testrs run sanity              # Run sanity category
testrs run --module math       # Run specific module

# Override validation (emergency bypass)
testrs run --override          # Run despite violations
testrs run --skip-enforcement  # Skip validation completely

# Options
testrs --view=data             # Plain output (no boxy)
testrs --timeout 300           # Custom timeout (seconds)
testrs --help                  # Show all options
```

**Example Output:**

```bash
$ testrs lint
⚠ Validation Failed
Found 4 test organization violation(s):

• Naming issues: 0
• Missing sanity tests: 2
• Missing UAT tests: 2
• Missing category entries: 0
• Unauthorized root files: 0
• Invalid directories: 0

Run 'testrs lint --violations' for detailed report
```

## Development

### Architecture

**Implemented Modules:**
- `src/testrs/__init__.py` - Package initialization (46 LOC)
- `src/testrs/__main__.py` - Module entry point (29 LOC)
- `src/testrs/config.py` - Multi-language configuration (351 LOC)
- `src/testrs/repo.py` - Repository detection (288 LOC)
- `src/testrs/output.py` - Boxy integration (264 LOC)
- `src/testrs/cli.py` - CLI interface (383 LOC)
- `src/testrs/discovery.py` - Module/test discovery (307 LOC)
- `src/testrs/validator.py` - Test validation (352 LOC)
- `src/testrs/runner.py` - Test execution (220 LOC)

**Total:** ~2,240 lines of production Python

### Reference Documentation

**Start here:** [CODE_REFERENCES.md](docs/CODE_REFERENCES.md)

**Key documents:**
- `TASKS.txt` - Complete implementation roadmap (133 story points)
- `CONTINUE.md` - Session continuation guide (M2 complete)
- `docs/procs/M2_REVIEW_REPORT.md` - Code review (Grade A-)
- `docs/ref/rsb_test_patterns_analysis.md` - Canonical logic analysis
- `docs/ref/MODULE_SPEC.md` - RSB module organization spec

### Testing

```bash
# Test on RSB project (canonical reference)
cd /home/xnull/repos/code/rust/prods/oodx/rsb
PYTHONPATH=/home/xnull/repos/code/python/snekfx/test-py/src python -m testrs lint

# Expected results:
# - 24 modules discovered
# - 96 test files discovered
# - 4 violations (deps, xcls missing sanity/UAT tests)
```

### Code Quality

**Repairman Review:** Grade A- (93/100)
- Type hints: 100% coverage
- Python 3.8 compatible
- No security vulnerabilities
- Comprehensive error handling
- Production-ready

## Contributing

This project is part of the snekfx Python tool ecosystem. Follow RSB standards and reference the canonical oodx-rsb implementation.

## License

MIT License - See LICENSE file
