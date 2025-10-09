# Rust Test Organization Standard

**Version**: 1.0 (Universal Rust Testing)
**Updated**: 2025-10-09
**Status**: Implementation Ready

## Philosophy

This organization standard implements **BashFX v3 Visual Friendliness Principles** with **Ceremony with Automation** for Rust projects, ensuring predictable test structure that scales from simple utilities to complex systems.

**Core Tenets**:
- **Ceremony is Encouraged**: Tests should provide clear visual progression and status
- **Pattern Enforcement**: testpy validates naming and structure compliance
- **Visual UAT**: User Acceptance Tests should demonstrate outputs with ceremony
- **Progressive Testing**: smoke → sanity → integration → e2e → chaos progression

## Directory Structure (ENFORCED)

```
tests/
├── unit/                    # Fast, isolated module tests (<1s each)
│   └── <module>/           # One folder per src module
│       └── *.rs            # Test files
│
├── sanity/                  # Core functionality validation (REQUIRED)
│   └── <module>.rs         # One file per module, comprehensive coverage
│
├── smoke/                   # Minimal CI tests (<10s total runtime)
│   └── core.rs             # Essential functionality only
│   └── <module>.rs         # Optional module smoke tests
│
├── integration/             # Cross-module interaction tests
│   └── <feature>.rs        # Tests by feature area (not module)
│   └── hub_<package>.rs    # Hub integration tests (if using hub)
│
├── e2e/                     # End-to-end user workflow tests
│   └── <workflow>.rs       # Complete user scenarios
│
├── uat/                     # User Acceptance Tests (VISUAL CEREMONY)
│   └── <module>.rs         # Visual demonstrations per module
│
├── chaos/                   # Edge cases, stress tests, property tests
│   └── <module>/           # Module-specific chaos tests
│       └── *.rs
│
├── bench/                   # Performance benchmarks
│   └── <module>.rs         # Module benchmarks
│
├── regression/              # Regression prevention tests
│   └── <issue>.rs          # Tests for previously fixed bugs
│
├── ceremonies/              # Optional ceremony tests (not enforced)
│   └── ceremony_*.{rs,sh}  # Visual demonstrations
│
├── _adhoc/                  # Experimental tests (outside enforcement)
│   └── *.rs                # Temporary/experimental test files
│
├── _archive/                # Deprecated tests (prefixed with _)
│   └── *.rs
│
└── sh/                      # Shell scripts for complex workflows
    └── *.sh
```

## Naming Convention (STRICT ENFORCEMENT)

### Category Entry Files (tests/*.rs)

**REQUIRED PATTERN**: `<category>.rs` - one per category

**Required Category Entry Files** (all 9 must exist):
- `sanity.rs` - Aggregates all sanity tests
- `smoke.rs` - Aggregates all smoke tests
- `unit.rs` - Aggregates all unit tests
- `integration.rs` - Aggregates all integration tests
- `e2e.rs` - Aggregates all e2e tests
- `uat.rs` - Aggregates all UAT tests
- `chaos.rs` - Aggregates all chaos tests
- `bench.rs` - Aggregates all benchmark tests
- `regression.rs` - Aggregates all regression tests

### Module Test Files

**REQUIRED PATTERN**: `<category>_<module>.rs` or organized in subdirectories

**Valid Examples**:
- Root level: `tests/sanity_com.rs` → test file for com module
- Subdirectory: `tests/sanity/com.rs` → test file in sanity/ directory
- Both patterns work, but directory organization scales better

**Category Entry File Content**:
```rust
//! Sanity test category entry point
//!
//! This file aggregates all sanity tests across modules.

// Import tests - use #[path] for subdirectory organization
#[path = "sanity/module1.rs"]
mod module1;

#[path = "sanity/module2.rs"]
mod module2;

// Or simple mod statements for root-level files
// mod sanity_module3;
```

**Invalid Examples** (testpy will reject):
- `com_sanity.rs` (wrong order - category must come first)
- `features_com.rs` (use standard category like `unit_com.rs`)
- `test_com.rs` (non-standard category)
- `random_name.rs` (no pattern match)

### Category Definitions

| Category | Purpose | Max Runtime | Requirements |
|----------|---------|-------------|--------------|
| **sanity** | Core functionality validation | <30s total | **REQUIRED** for every module |
| **smoke** | Minimal CI tests | <10s total | Essential functionality only |
| **unit** | Fast, isolated tests per module | <1s each | One test per function/component |
| **integration** | Cross-module interactions | <60s total | Feature-based organization |
| **e2e** | Complete user workflows | <300s total | Real-world scenarios |
| **uat** | Visual demonstrations | No limit | **REQUIRED** for every module |
| **chaos** | Edge cases, stress tests | No limit | Property/fuzz testing |
| **bench** | Performance benchmarks | No limit | Baseline measurements |
| **regression** | Bug prevention tests | <60s total | One test per fixed bug |

### Hub Integration Tests

**If your project uses hub** (has `src/deps.rs`), you need integration tests for each hub package:

**Pattern**: `tests/integration/hub_<package>.rs`

**Example**:
```rust
//! Hub integration test for chrono
//!
//! Lightweight sanity check that hub package is accessible.

#[test]
fn hub_chrono_available() {
    use your_project::deps::chrono::Utc;

    let now = Utc::now();
    assert!(now.timestamp() > 0);
}
```

## Visual UAT Testing Requirements

UAT tests should be **demonstrative** - show actual outputs and behaviors.

### Simple UAT Pattern (Recommended)

```rust
#[test]
fn uat_color_demonstrations() {
    println!("Colors Module UAT");
    println!("==================\n");

    // Test 1: Basic functionality
    println!("Test 1: Basic Color Output");
    println!("  Hypothesis: red_text!() produces red colored output");
    println!("  Expected: Red ANSI escape codes applied");

    let result = red_text!("Error message");
    println!("  Actual: {}", result);
    assert!(result.contains("\x1b["));
    println!("  ✓ PASS\n");

    // Test 2: Color combinations
    println!("Test 2: Multiple Colors");
    println!("  Hypothesis: Multiple colors work together");
    println!("  Expected: Independent color application");

    let green = green_text!("Success");
    let yellow = yellow_text!("Warning");
    println!("  Actual: {} {}", green, yellow);
    println!("  ✓ PASS\n");

    println!("=== UAT Complete ===");
}
```

### UAT Visual Requirements

1. **Clear Test Numbers**: Number each test clearly
2. **Hypothesis**: State what you're testing
3. **Expected**: Describe expected behavior
4. **Actual**: Show actual output
5. **STATUS**: Use ✓ PASS, ✗ FAIL, ⚠ SKIP glyphs
6. **Spacing**: Separate tests with blank lines
7. **Summary**: End with summary message

## testpy Pattern Enforcement

### Enforcement Modes

```bash
# Standard run (with enforcement)
testpy

# Check compliance only
testpy lint

# View detailed violations
testpy lint --violations

# Emergency bypass (run despite violations)
testpy --override
```

### Validation Rules

testpy **validates**:

1. **Category Entry Files**: All 9 category .rs files must exist
2. **Naming Pattern**: Test files follow `<category>_<module>.rs` or subdirectory organization
3. **Category Validity**: Only approved categories (9 standard)
4. **Required Tests**: Every module has sanity AND UAT tests
5. **File Organization**: Tests in correct subdirectories
6. **Hub Integration**: Hub packages have integration tests (if using hub)
7. **Unauthorized Files**: Only valid patterns in tests/ root

### Violation Types

testpy reports 7 types of violations:

1. **missing_category_entry**: Missing required category .rs file
2. **missing_sanity_tests**: Module lacks sanity tests
3. **missing_uat_tests**: Module lacks UAT tests
4. **invalid_directory**: Unauthorized subdirectory in tests/
5. **unauthorized_root_file**: File in tests/ root doesn't match pattern
6. **naming_violation**: File doesn't follow naming convention
7. **missing_hub_integration**: Hub package lacks integration test

## Migration Strategy

### Phase 1: Initial Setup
1. Create `tests/` directory
2. Create all 9 category entry files (`sanity.rs`, `smoke.rs`, etc.)
3. Add `.spec.toml` with exclusions if needed

### Phase 2: Organize Tests
4. Decide: root-level or subdirectory organization
5. Move/rename existing tests to proper categories
6. Update category entry files with module imports
7. Run `testpy lint` to check compliance

### Phase 3: Add Required Tests
8. Create sanity tests for every module
9. Create UAT tests for every module
10. Add hub integration tests if using hub
11. Verify: `testpy lint` shows zero violations

### Phase 4: Enhancement (Optional)
12. Add ceremony tests in `tests/ceremonies/`
13. Enhance UAT tests with better visuals
14. Add regression tests for bug fixes
15. Set up CI integration with testpy

## Usage Examples

### Running Tests

```bash
# Run all tests (validates organization first)
testpy

# Run specific category
testpy sanity
testpy uat

# Run specific module tests
testpy sanity math
testpy uat tokens

# Check organization compliance
testpy lint

# View detailed violations
testpy lint --violations

# Display test organization docs
testpy docs rust-org
testpy docs rust-howto
testpy docs checklist

# Display this checklist
testpy checklist
```

### Adding New Module Tests

```bash
# 1. Create test files (choose one approach)

# Approach A: Subdirectory organization (recommended)
mkdir -p tests/sanity
mkdir -p tests/uat
touch tests/sanity/new_module.rs
touch tests/uat/new_module.rs

# Approach B: Root-level files
touch tests/sanity_new_module.rs
touch tests/uat_new_module.rs

# 2. Update category entry files
# Add to tests/sanity.rs:
#[path = "sanity/new_module.rs"]
mod new_module;

# Add to tests/uat.rs:
#[path = "uat/new_module.rs"]
mod new_module;

# 3. Verify compliance
testpy lint

# 4. Run tests
testpy sanity new_module
testpy uat new_module
```

## Ceremony Tests (Optional)

Ceremony tests are **optional** visual demonstrations that showcase project capabilities. They are NOT enforced by testpy.

### Ceremony Directory Structure

```
tests/ceremonies/
├── ceremony_welcome.rs      # Welcome demonstration
├── ceremony_quickstart.sh   # Quick start guide
└── ceremony_features.rs     # Feature showcase
```

### Running Ceremonies

If your project implements ceremony support:

```bash
# List available ceremonies
testpy ceremony

# Run specific ceremony
testpy ceremony welcome
testpy ceremony quickstart
```

**Note**: Ceremony support is a future testpy feature. For now, place ceremony tests in `tests/ceremonies/` - testpy will ignore this directory.

## Configuration via .spec.toml

Projects can customize test enforcement via `.spec.toml`:

```toml
# .spec.toml
[project]
name = "your-project"
language = "rust"

[tests]
# Exclude specific modules from test requirements
exclude = [
    "xcls",      # Internal utilities
    "macros",    # Macro definitions
    "streamable" # Generated code
]

[rust]
# Additional source exclusions (for module discovery)
exclusions = [
    "_*",
    "dev_*",
    "prelude*",
    "dummy_*",
    "lib.rs",
    "main.rs",
    "deps.rs",   # Hub re-exports
    "hub.rs"     # Hub utilities
]
```

## Compliance Checklist

Use this checklist to verify your test organization:

- [ ] All 9 category entry files exist (`sanity.rs`, `smoke.rs`, etc.)
- [ ] Every module has sanity tests
- [ ] Every module has UAT tests
- [ ] UAT tests include visual ceremony (hypothesis/expected/actual/status)
- [ ] Hub packages have integration tests (if using hub)
- [ ] All test files follow naming pattern
- [ ] No unauthorized files in tests/ root
- [ ] `testpy lint` shows zero violations
- [ ] Tests run successfully: `testpy`

## Benefits

### Predictability
- Know exactly where to find/add tests
- Consistent structure across all Rust projects
- Clear progression from quick to comprehensive testing

### Scalability
- Works for any Rust project size
- Enforced patterns prevent drift
- Directory organization scales to hundreds of modules

### CI/Development Workflow
- Fast smoke tests for rapid feedback
- Progressive testing levels
- Visual UAT for human verification
- Automated compliance checking via testpy lint

### Universal Standard
- Same organization works for all Rust projects
- Team members can switch projects easily
- Tooling (testpy) works everywhere
- Documentation applies universally

## Related Documentation

- **Testing HOWTO**: `testpy docs rust-howto` - Complete testing guide
- **Visual UX Guide**: `testpy docs rust-ux` - Visual testing principles
- **Boxy/Rolo Usage**: `testpy docs rust-boxy` - Enhanced ceremony tools
- **Quick Checklist**: `testpy checklist` - Step-by-step setup guide

---

This organization transforms testing from an ad-hoc collection of files into a structured, enforceable system that provides clear progression from basic validation to comprehensive verification while maintaining the visual communication standards essential to professional software development.
