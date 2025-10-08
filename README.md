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

🚧 **In Development** - Setting up project structure and reference documentation

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

## Installation (Future)

```bash
# From this directory
pip install -e .

# Or use deploy script
./bin/deploy.sh
```

## Usage (Planned)

```bash
# Run all tests
testrs

# Run specific category
testrs sanity
testrs uat

# Run for specific module
testrs sanity --module math

# Validate test organization
testrs lint

# Show violations
testrs lint --violations
```

## Development

### Reference Documentation

**Start here:** [CODE_REFERENCES.md](docs/CODE_REFERENCES.md)

**Key documents:**
- `docs/ref/rsb_test_patterns_analysis.md` - Line-by-line analysis of canonical implementation
- `docs/ref/MODULE_SPEC.md` - RSB module organization spec
- `docs/rust_test_standardization_plan.md` - Standardization strategy

### Implementation Priority

1. Read and understand `docs/CODE_REFERENCES.md`
2. Study `code_ref/rsb_test.sh` (canonical reference)
3. Review `docs/ref/rsb_test_patterns_analysis.md` (documented logic)
4. Implement core modules based on canonical patterns
5. Test against oodx-rsb project

## Contributing

This project is part of the snekfx Python tool ecosystem. Follow RSB standards and reference the canonical oodx-rsb implementation.

## License

MIT License - See LICENSE file
