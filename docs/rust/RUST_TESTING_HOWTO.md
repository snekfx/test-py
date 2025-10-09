# Rust Testing: HOWTO Guide (Universal)

**Updated**: 2025-10-09
**Status**: Universal Rust Testing Standard

## Quick Start

```bash
# Check test organization compliance
testpy lint

# View detailed violations (if any)
testpy lint --violations

# Run all tests (validates organization first)
testpy

# Run specific test categories
testpy sanity
testpy smoke
testpy uat

# Module-based testing
testpy sanity math        # Run sanity tests for math module
testpy uat tokens         # Run UAT tests for tokens module

# Display documentation
testpy docs rust-org      # Test organization standard
testpy docs rust-howto    # This guide
testpy docs rust-ux       # Visual testing UX guide
testpy checklist          # Step-by-step setup guide

# Emergency bypass (run despite violations)
testpy --override
```

## Module-Based Testing System

testpy supports **module filtering** that allows targeted testing by category and module for more efficient development workflows.

### Module Testing Syntax

```bash
# General syntax
testpy <category> <module>

# Examples
testpy uat math           # Run all math UAT tests
testpy sanity tokens      # Run all tokens sanity tests
testpy sanity             # Run all sanity tests across modules
testpy uat                # Run all UAT tests across modules

# Run specific test files directly
cargo test --test uat_math -- --nocapture
cargo test --test sanity_tokens
```

### Function Naming Patterns

**RECOMMENDED**: All test functions should follow standardized naming patterns for clarity:

#### UAT Functions
```rust
// Pattern: uat_<module>_<description>()
fn uat_math_basic_demo() { /* Visual demonstration of math basics */ }
fn uat_math_floating_point_demo() { /* Float operations demo */ }
fn uat_tokens_validation_demo() { /* Token validation showcase */ }
fn uat_tokens_parsing_edge_cases() { /* Edge case demonstrations */ }
```

#### SANITY Functions
```rust
// Pattern: sanity_<module>_<description>()
fn sanity_math_basic() { /* Core math functionality tests */ }
fn sanity_math_operations() { /* Mathematical operation tests */ }
fn sanity_tokens_parsing() { /* Token parsing validation */ }
fn sanity_tokens_generation() { /* Token generation tests */ }
```

#### Other Categories
```rust
// UNIT tests
fn unit_<module>_<description>() { /* Fast isolated tests */ }

// SMOKE tests
fn smoke_<module>_<description>() { /* Essential functionality */ }

// INTEGRATION tests (cross-module)
fn integration_<feature>_<description>() { /* Feature-based testing */ }
```

### Benefits of Module-Based Testing

- **Targeted Development**: Test only the module you're working on
- **Faster Feedback**: Skip unrelated test suites during development
- **Better Organization**: Clear separation between module testing categories
- **Easier Debugging**: Isolate issues to specific functional areas
- **Parallel Development**: Teams can work on different modules independently

## Test Organization System

testpy uses a **strict, enforced test organization system** following BashFX Visual Friendliness Principles. All tests must follow the prescribed structure or testpy will report violations.

### Directory Structure (ENFORCED)

```
tests/
├── unit/                    # Fast, isolated module tests (<1s each)
│   └── <module>/           # Example: folder per src module
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
│   └── <feature>.rs        # Tests by feature area (cross-module)
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
├── _adhoc/                  # Experimental tests (outside enforcement)
│   └── *.rs, *.sh          # Temporary/experimental test files
│
├── _archive/                # Deprecated tests (prefixed with _)
│   └── *.rs
│
└── sh/                      # Shell scripts for complex workflows
    └── *.sh
```

### Category Entry Files (tests/*.rs) - REQUIRED

All 9 category entry files in `tests/` root are required:

**Required Files:**
- `sanity.rs` → aggregates all sanity tests
- `smoke.rs` → aggregates all smoke tests
- `unit.rs` → aggregates all unit tests
- `integration.rs` → aggregates all integration tests
- `e2e.rs` → aggregates all e2e tests
- `uat.rs` → aggregates all UAT tests
- `chaos.rs` → aggregates all chaos tests
- `bench.rs` → aggregates all benchmark tests
- `regression.rs` → aggregates all regression tests

**Example Category Entry File** (tests/sanity.rs):
```rust
//! Sanity test category entry point
//!
//! This file aggregates all sanity tests across modules.

// Import from subdirectory (recommended)
#[path = "sanity/math.rs"]
mod math;

#[path = "sanity/tokens.rs"]
mod tokens;

// Or import root-level files
// mod sanity_strings;
```

## Test Runner Commands

### Core Commands

```bash
# Show validation status and run tests
testpy

# Check test organization compliance only
testpy lint

# View detailed violation report
testpy lint --violations

# Run specific category
testpy sanity
testpy smoke
testpy uat

# Module-based testing
testpy <category> <module>
testpy uat math              # Run all math UAT tests
testpy sanity tokens         # Run all tokens sanity tests

# Display documentation
testpy docs rust-org         # Organization standard
testpy docs rust-howto       # This guide
testpy docs rust-ux          # Visual UX guide
testpy docs rust-boxy        # Boxy/rolo usage
testpy checklist             # Setup checklist
```

### Enforcement Modes

```bash
# Standard mode (DEFAULT) - validates before running
testpy

# Override mode - run despite violations with warnings
testpy --override

# Lint only - check compliance without running tests
testpy lint
```

## Test Categories

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

### Required Tests Per Module

**Every module MUST have:**
1. **Sanity tests** - `tests/sanity/<module>.rs`
2. **UAT tests** - `tests/uat/<module>.rs`

Missing either will cause testpy lint violations.

## Visual UAT Testing Pattern

UAT tests should be **simple Rust tests** that output clean, structured text demonstrating functionality.

### Simple UAT Pattern (RECOMMENDED)

```rust
#[test]
fn uat_color_demonstrations() {
    println!("Colors Module UAT");
    println!("==================\n");

    // UAT 1: Basic Color Output
    println!("UAT 1: Basic Color Output");
    println!("  Command: red_text!(\"Error message\")");
    println!("  Expected: Red colored text output");
    println!("  Running...");
    let result = red_text!("Error message");
    println!("  Output: {}", result);
    println!("  ✓ PASS\n");

    // UAT 2: Multiple Color Combinations
    println!("UAT 2: Multiple Color Combinations");
    println!("  Command: green_text!(\"Success\") + yellow_text!(\"Warning\")");
    println!("  Expected: Green text followed by yellow text");
    println!("  Running...");
    println!("  Output: {} {}", green_text!("Success"), yellow_text!("Warning"));
    println!("  ✓ PASS\n");

    // UAT 3: Color with Background
    println!("UAT 3: Color with Background");
    println!("  Command: bg_red!(\"Alert message\")");
    println!("  Expected: Text with red background");
    println!("  Running...");
    println!("  Output: {}", bg_red!("Alert message"));
    println!("  ✓ PASS\n");

    println!("=== UAT Complete ===");
}
```

### UAT Visual Requirements

1. **Clear Test Numbers**: Number each demonstration
2. **Command**: Show the command being demonstrated
3. **Expected**: Describe expected behavior
4. **Running**: Indicate test execution
5. **Output**: Show actual output
6. **STATUS**: Use ✓ PASS, ✗ FAIL, ⚠ SKIP glyphs
7. **Spacing**: Separate demonstrations with blank lines
8. **Summary**: End with completion message

### UAT Multiple Variations Pattern

For testing multiple command variations:

```rust
#[test]
fn uat_param_expansion_variations() {
    println!("Parameter Expansion UAT");
    println!("========================\n");

    let test_cases = vec![
        ("param!(\"HOME\")", "Environment variable expansion"),
        ("param!(\"USER.name\")", "Nested property access"),
        ("param!(\"app.version\", \"1.0.0\")", "Default value fallback"),
    ];

    for (i, (command, description)) in test_cases.iter().enumerate() {
        println!("UAT {}: {}", i + 1, description);
        println!("  Command: {}", command);
        println!("  Expected: {}", description);
        println!("  Running...");

        // Execute the actual command
        let result = match i {
            0 => param!("HOME"),
            1 => param!("USER.name"),
            2 => param!("app.version", "1.0.0"),
            _ => unreachable!(),
        };

        println!("  Output: {}", result);
        println!("  ✓ PASS\n");
    }

    println!("=== UAT Complete ===");
}
```

### Running UAT Tests with Output

```bash
# Run UAT tests with output visible
cargo test --test uat_<module> -- --nocapture

# Or via testpy (if implemented)
testpy uat <module>

# Examples
cargo test --test uat_colors -- --nocapture
cargo test --test uat_math -- --nocapture
```

## Hub Integration Testing

If your project uses **hub** (has `src/deps.rs`), you need lightweight integration tests for each hub package.

### Hub Integration Test Pattern

```rust
// tests/integration/hub_chrono.rs
//! Hub integration test for chrono
//!
//! Lightweight sanity check that hub package is accessible.

#[test]
fn hub_chrono_available() {
    use your_project::deps::chrono::Utc;

    let now = Utc::now();
    assert!(now.timestamp() > 0);

    println!("✓ chrono hub integration working");
}
```

### Detecting Hub Packages

testpy uses blade's cache to detect hub packages:

```bash
# Blade shows hub packages (requires blade installed)
blade deps <your-repo>

# testpy automatically detects via blade cache
testpy lint  # Shows missing hub integration tests
```

### Creating Hub Integration Tests

```bash
# 1. Create integration directory
mkdir -p tests/integration

# 2. Create hub test for each package
cat > tests/integration/hub_chrono.rs << 'EOF'
//! Hub integration test for chrono

#[test]
fn hub_chrono_available() {
    use your_project::deps::chrono;
    // Minimal usage test
}
EOF

# 3. Update integration.rs
echo "#[path = \"integration/hub_chrono.rs\"]" >> tests/integration.rs
echo "mod hub_chrono;" >> tests/integration.rs

# 4. Verify
testpy lint
```

## Cross-Module Integration Testing

### Progressive Enhancement Pattern

Use a **progressive enhancement** approach for cross-module testing:

1. **Pure Module Tests** (sanity): Test modules in isolation
2. **Cross-Module Features** (integration): Test module interactions
3. **Dependency Validation**: Ensure stable core before cross-module work

### Cross-Module Adapter Pattern

Create adapter tests for cross-module functionality:

```rust
// tests/integration/string_math_adapter.rs
use your_project::{string, math};

#[test]
fn integration_string_math_number_formatting() {
    // Generate number with math
    let number = math::calculate(42);

    // Format with string utilities
    let formatted = string::format_number(number);

    assert!(!formatted.is_empty());
}
```

### Feature-Gated Integration Tests

Use feature gates for optional dependencies:

```rust
// tests/integration/string_dev_adapter.rs
#[cfg(feature = "dev-pty")]
use your_project::dev::{PtyOptions, spawn_pty};

#[test]
#[cfg(feature = "dev-pty")]
fn integration_string_dev_pty_output() {
    let mut sess = spawn_pty("echo 'Hello'", &PtyOptions::default())
        .expect("PTY spawn");

    let output = sess.read_for(Duration::from_millis(500))
        .expect("PTY read");

    let processed = your_project::string::to_snake_case(&output.trim());
    assert_eq!(processed, "hello");
}

#[test]
#[cfg(not(feature = "dev-pty"))]
fn integration_string_dev_fallback() {
    // Fallback when feature unavailable
    let processed = your_project::string::to_snake_case("Hello");
    assert_eq!(processed, "hello");
}
```

## Adding New Tests

### 1. Create Test Files

```bash
# Choose organization approach:

# Approach A: Subdirectory organization (recommended)
mkdir -p tests/sanity
mkdir -p tests/uat
touch tests/sanity/new_module.rs
touch tests/uat/new_module.rs

# Approach B: Root-level files
touch tests/sanity_new_module.rs
touch tests/uat_new_module.rs
```

### 2. Update Category Entry Files

```rust
// tests/sanity.rs - add import

// For subdirectory files (Approach A)
#[path = "sanity/new_module.rs"]
mod new_module;

// For root-level files (Approach B)
// mod sanity_new_module;
```

```rust
// tests/uat.rs - add import

#[path = "uat/new_module.rs"]
mod new_module;
```

### 3. Implement Tests

```rust
// tests/sanity/new_module.rs
//! Sanity tests for new_module

#[test]
fn sanity_new_module_basic() {
    use your_project::new_module;

    // Core functionality test
    let result = new_module::basic_operation();
    assert!(result.is_ok());
}

#[test]
fn sanity_new_module_api() {
    // Test public API availability
    use your_project::new_module::*;

    // Verify functions exist and work
    assert!(true);
}
```

```rust
// tests/uat/new_module.rs
//! UAT tests for new_module

#[test]
fn uat_new_module_demonstration() {
    println!("New Module UAT");
    println!("===============\n");

    println!("UAT 1: Basic Functionality");
    println!("  Command: new_module::operation()");
    println!("  Expected: Successful operation");
    println!("  Running...");

    use your_project::new_module;
    let result = new_module::operation();

    println!("  Output: {:?}", result);
    println!("  ✓ PASS\n");

    println!("=== UAT Complete ===");
}
```

### 4. Verify Compliance

```bash
# Check compliance
testpy lint

# Should show 0 violations now

# Run your new tests
testpy sanity new_module
testpy uat new_module

# Or directly with cargo
cargo test --test sanity_new_module
cargo test --test uat_new_module -- --nocapture
```

## Module-Based Development Workflow

### Typical Development Cycle

When working on a specific module:

```bash
# 1. Work on a module (e.g., math)
vim src/math/mod.rs

# 2. Test only that module quickly
testpy sanity math    # Core functionality
testpy uat math       # Visual demonstrations

# Or with cargo directly
cargo test --test sanity_math
cargo test --test uat_math -- --nocapture

# 3. Test related modules if needed
testpy sanity tokens  # If math affects tokens

# 4. Full category testing before commit
testpy sanity        # All sanity tests
testpy uat           # All UAT tests

# 5. Full test suite
testpy
```

### Module Development Best Practices

1. **Start with Sanity**: Write sanity tests first for core functionality
2. **Add UAT Demonstrations**: Create visual tests showing module capabilities
3. **Follow Naming**: Use `<category>_<module>_<description>()` pattern
4. **Test Incrementally**: Test specific modules during development
5. **Validate Organization**: Run `testpy lint` regularly
6. **Full Suite Before Commit**: Run `testpy` before committing

## Configuration via .spec.toml

Customize test enforcement via `.spec.toml`:

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

## Troubleshooting

### Test Organization Violations

```bash
# See all violations with details
testpy lint --violations

# Emergency bypass (shows warnings but runs tests)
testpy --override
```

### Common Issues

1. **Missing category entry files** - Need all 9 .rs files in tests/
   - Solution: Create missing category entry files
   - Quick: `touch tests/{sanity,smoke,unit,integration,e2e,uat,chaos,bench,regression}.rs`

2. **Missing sanity/UAT tests** - Every module needs both
   - Solution: Create tests/sanity/<module>.rs and tests/uat/<module>.rs
   - Update category entry files with module imports

3. **Unauthorized root files** - Only approved patterns in `tests/`
   - Solution: Move to subdirectory or rename to match pattern
   - Or move to `_adhoc/` or `_archive/` if experimental/deprecated

4. **Missing hub integration tests** - Hub packages need integration tests
   - Solution: Create tests/integration/hub_<package>.rs for each package
   - See Hub Integration Testing section above

5. **Invalid directory** - Unknown subdirectory in tests/
   - Solution: Rename to valid category or move to `_adhoc/`
   - Valid: unit, sanity, smoke, integration, e2e, uat, chaos, bench, regression, sh, ceremonies, _adhoc, _archive

### Getting Help

```bash
# Display organization standard
testpy docs rust-org

# Display this guide
testpy docs rust-howto

# Display visual UX guide
testpy docs rust-ux

# Display step-by-step checklist
testpy checklist
```

## Key Principles

1. **Enforced Structure** - testpy validates organization before running tests
2. **Pattern Compliance** - Strict naming and structure requirements
3. **Visual UAT** - Clear demonstrations with hypothesis/expected/actual/status
4. **Progressive Testing** - smoke → sanity → integration → e2e progression
5. **Required Coverage** - Every module needs sanity AND UAT tests
6. **Hub Integration** - Hub packages need lightweight integration tests

## Related Documentation

- **Test Organization**: `testpy docs rust-org` - Complete structure standard
- **Visual UX Guide**: `testpy docs rust-ux` - Visual testing principles
- **Boxy/Rolo Usage**: `testpy docs rust-boxy` - Enhanced ceremony tools
- **Quick Checklist**: `testpy checklist` - Step-by-step setup guide

---

**Remember**: testpy enforces test organization. Tests will show violations if the organization doesn't comply. Use `testpy lint` to check compliance and `testpy lint --violations` for detailed fix instructions.
