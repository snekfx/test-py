# Rust Test Organization Checklist

**A step-by-step guide to setting up proper test organization for Rust projects**

This checklist walks you through setting up comprehensive test coverage following RSB test organization standards. Use `testpy checklist` to display this guide.

---

## Quick Validation

Before starting, check your current status:

```bash
testpy lint
```

This will show you exactly what needs to be fixed. Follow the checklist below to address each violation type.

---

## 📋 Checklist Overview

- [ ] **Step 1**: Set up test directory structure
- [ ] **Step 2**: Create category entry files
- [ ] **Step 3**: Add sanity tests for all modules
- [ ] **Step 4**: Add UAT tests for all modules
- [ ] **Step 5**: Add hub integration tests (if using hub)
- [ ] **Step 6**: Fix naming violations
- [ ] **Step 7**: Clean up unauthorized files
- [ ] **Step 8**: Validate and run tests

---

## Step 1: Set Up Test Directory Structure

### Recommended Structure: Category Directories

**Preferred approach** - organize tests in category folders:

```
your-project/
├── src/
│   ├── module1/mod.rs
│   └── module2/mod.rs
└── tests/
    ├── sanity.rs          # Category entry file
    ├── uat.rs             # Category entry file
    ├── unit.rs            # Category entry file
    ├── ...                # Other category entries
    ├── sanity/            # Category directory
    │   ├── module1.rs     # Per-module tests
    │   └── module2.rs
    ├── uat/               # Category directory
    │   ├── module1.rs
    │   └── module2.rs
    └── unit/
        ├── module1.rs
        └── module2.rs
```

**Alternative: Root-level wrappers** (for simpler projects)

You can also put test files directly in `tests/` as `tests/sanity_module.rs` instead of `tests/sanity/module.rs`. Both patterns work, but directory organization scales better.

### Create tests/ directory

```bash
mkdir -p tests
```

### Task Checklist

- [ ] Created `tests/` directory
- [ ] Understand 9 test categories (sanity, smoke, unit, integration, e2e, uat, chaos, bench, regression)
- [ ] Understand naming pattern: `<category>_<module>.rs`

---

## Step 2: Create Category Entry Files

Category entry files aggregate tests across all modules for a given category.

### Required Categories

All 9 category entry files are required:

1. **sanity.rs** - Core functionality tests
2. **smoke.rs** - Quick health checks
3. **unit.rs** - Individual component tests
4. **integration.rs** - Module interaction tests
5. **e2e.rs** - End-to-end workflow tests
6. **uat.rs** - User acceptance/visual tests
7. **chaos.rs** - Stress and chaos testing
8. **bench.rs** - Performance benchmarks
9. **regression.rs** - Regression prevention tests

### Template: Category Entry File

Create each category entry file (e.g., `tests/sanity.rs`):

```rust
//! Sanity test category entry point
//!
//! This file aggregates all sanity tests across modules.

// Import sanity tests for each module
mod sanity_module1;
mod sanity_module2;
// Add more as you create them
```

### Quick Creation Script

```bash
cd tests

# Create all category entry files
for category in sanity smoke unit integration e2e uat chaos bench regression; do
  cat > "${category}.rs" << 'EOF'
//! CATEGORY test category entry point
//!
//! This file aggregates all CATEGORY tests across modules.

// Import CATEGORY tests for each module
// mod CATEGORY_modulename;
EOF
  sed -i "s/CATEGORY/${category}/g" "${category}.rs"
done
```

### Task Checklist

- [ ] Created `tests/sanity.rs`
- [ ] Created `tests/smoke.rs`
- [ ] Created `tests/unit.rs`
- [ ] Created `tests/integration.rs`
- [ ] Created `tests/e2e.rs`
- [ ] Created `tests/uat.rs`
- [ ] Created `tests/chaos.rs`
- [ ] Created `tests/bench.rs`
- [ ] Created `tests/regression.rs`

---

## Step 3: Add Sanity Tests for All Modules

**Every module requires sanity tests** - these verify core functionality works.

### Find Your Modules

```bash
# List modules detected by testpy
testpy lint --violations | grep "Module '"
```

### Template: Sanity Test

**Recommended**: Create `tests/sanity/<module>.rs` in the category directory.

Alternatively, you can use `tests/sanity_<module>.rs` in the root.

```rust
//! Sanity tests for <module> module
//!
//! These tests verify core functionality works correctly.

#[test]
fn <module>_basic_functionality() {
    // Import your module
    use your_project::<module>;

    // Test basic operation
    let result = <module>::basic_operation();
    assert!(result.is_ok());
}

#[test]
fn <module>_core_api_available() {
    // Verify public API is accessible
    use your_project::<module>::*;

    // Test public functions/types exist
    // Add actual tests here
}
```

### Example: Sanity Test for `math` Module

```rust
//! Sanity tests for math module

#[test]
fn math_addition_works() {
    use myproject::math::add;
    assert_eq!(add(2, 2), 4);
}

#[test]
fn math_subtraction_works() {
    use myproject::math::subtract;
    assert_eq!(subtract(5, 3), 2);
}
```

### Update Category Entry File

Add to `tests/sanity.rs`:

```rust
#[path = "sanity/<module>.rs"]
mod <module>;
```

This imports `tests/sanity/<module>.rs` into the sanity test suite.

### Task Checklist

- [ ] Identified all modules needing sanity tests
- [ ] Created `tests/sanity_<module>.rs` for each module
- [ ] Added `mod sanity_<module>;` to `tests/sanity.rs`
- [ ] Verified tests compile: `cargo test --test sanity_<module>`

---

## Step 4: Add UAT Tests for All Modules

**Every module requires UAT tests** - these provide visual demonstrations and user acceptance validation.

### Purpose of UAT Tests

UAT tests should:
- Demonstrate module functionality visually
- Show expected vs actual results
- Be readable and informative
- Use STATUS messages (✓ PASS, ✗ FAIL)

### Template: UAT Test

For each module, create `tests/uat_<module>.rs`:

```rust
//! UAT tests for <module> module
//!
//! User acceptance tests with visual output.

#[test]
fn uat_<module>_demonstration() {
    println!("\n=== <Module> Module UAT ===\n");

    // Test 1: Basic functionality
    println!("Test 1: Basic Functionality");
    println!("  Hypothesis: Module performs expected operation");

    use your_project::<module>;
    let result = <module>::operation();

    println!("  Expected: Success");
    println!("  Actual: {:?}", result);

    assert!(result.is_ok());
    println!("  ✓ PASS: Basic functionality works\n");

    // Test 2: Edge cases
    println!("Test 2: Edge Case Handling");
    // Add more visual tests...

    println!("=== All UAT Tests Passed ===\n");
}
```

### Example: UAT Test for `math` Module

```rust
//! UAT tests for math module

#[test]
fn uat_math_operations() {
    println!("\n=== Math Module UAT ===\n");

    use myproject::math::{add, subtract, multiply, divide};

    // Test 1: Addition
    println!("Test 1: Addition");
    let result = add(10, 5);
    println!("  10 + 5 = {}", result);
    assert_eq!(result, 15);
    println!("  ✓ PASS\n");

    // Test 2: Division with edge case
    println!("Test 2: Division (with zero check)");
    let result = divide(10.0, 2.0);
    println!("  10.0 / 2.0 = {}", result);
    assert_eq!(result, 5.0);
    println!("  ✓ PASS\n");

    println!("=== Math UAT Complete ===\n");
}
```

### Update Category Entry File

Add to `tests/uat.rs`:

```rust
mod uat_<module>;
```

### Task Checklist

- [ ] Created `tests/uat_<module>.rs` for each module
- [ ] Added visual output with STATUS messages
- [ ] Added `mod uat_<module>;` to `tests/uat.rs`
- [ ] Verified tests run: `cargo test --test uat_<module> -- --nocapture`

---

## Step 5: Add Hub Integration Tests (if using hub)

**If your project uses hub** (has `src/deps.rs`), you need integration tests for each hub package.

### Check if You Need Hub Tests

```bash
testpy lint | grep "Missing hub integration tests"
```

### Find Hub Packages

```bash
blade deps | grep "hub"
```

### Template: Hub Integration Test

For each hub package, create `tests/integration/hub_<package>.rs`:

```rust
//! Hub integration test for <package>
//!
//! Lightweight sanity check that hub package is accessible.

#[test]
fn hub_<package>_available() {
    // Import the package via your project's hub re-export
    use your_project::deps::<package>;

    // Basic usage test (minimal, just verify it works)
    // Example for chrono:
    // let now = <package>::Utc::now();
    // assert!(now.timestamp() > 0);

    // Add minimal usage test here
}
```

### Example: Hub Integration Test for `chrono`

```rust
//! Hub integration test for chrono

#[test]
fn hub_chrono_available() {
    use myproject::deps::chrono::Utc;

    let now = Utc::now();
    assert!(now.timestamp() > 0);

    println!("✓ chrono hub integration working");
}
```

### Create Integration Directory

```bash
mkdir -p tests/integration
```

### Update Integration Entry File

Add to `tests/integration.rs`:

```rust
mod hub_<package>;
```

### Task Checklist

- [ ] Checked if project uses hub (`src/deps.rs` exists)
- [ ] Created `tests/integration/` directory
- [ ] Created `tests/integration/hub_<package>.rs` for each package
- [ ] Added `mod hub_<package>;` to `tests/integration.rs`
- [ ] Verified: `cargo test --test integration`

---

## Step 6: Fix Naming Violations

Files must follow the pattern: `<category>_<module>.rs`

### Valid Categories

- sanity
- smoke
- unit
- integration
- e2e
- uat
- chaos
- bench
- regression

### Check for Naming Violations

```bash
testpy lint --violations | grep "NAMING VIOLATIONS" -A 20
```

### Fix Naming Violations

Rename files to match pattern:

```bash
# Example: Wrong name → Correct name
mv tests/test_math.rs tests/sanity_math.rs
mv tests/math_test.rs tests/unit_math.rs
mv tests/foo.rs tests/sanity_foo.rs  # Choose appropriate category
```

### Task Checklist

- [ ] Identified all naming violations
- [ ] Renamed files to `<category>_<module>.rs` pattern
- [ ] Updated imports in category entry files
- [ ] Verified: `testpy lint` shows 0 naming issues

---

## Step 7: Clean Up Unauthorized Files

### What Files Are Allowed in `tests/`?

**Root level (`tests/*.rs`)**:
- Category entry files: `sanity.rs`, `smoke.rs`, etc.
- Module test wrappers: `<category>_<module>.rs`
- Files starting with `_` or `dev_` (excluded by convention)

**Subdirectories**:
- Valid categories: `tests/sanity/`, `tests/unit/`, etc.
- Special directories: `tests/sh/`, `tests/_archive/`, `tests/_adhoc/`
- Optional: `tests/ceremonies/` (not enforced)

### Check for Unauthorized Files

```bash
testpy lint --violations | grep "UNAUTHORIZED ROOT FILES" -A 20
```

### Fix Unauthorized Files

Move or rename unauthorized files:

```bash
# Option 1: Rename to match pattern
mv tests/helper.rs tests/sanity_helper.rs

# Option 2: Move to archive (if old/unused)
mkdir -p tests/_archive
mv tests/old_test.rs tests/_archive/

# Option 3: Move to adhoc (if experimental)
mkdir -p tests/_adhoc
mv tests/experiment.rs tests/_adhoc/

# Option 4: Move to appropriate subdirectory
mv tests/util.rs tests/unit/util.rs
```

### Task Checklist

- [ ] Identified all unauthorized root files
- [ ] Renamed, moved, or archived each file
- [ ] Verified: `testpy lint` shows 0 unauthorized root files

---

## Step 8: Validate and Run Tests

### Final Validation

```bash
# Check for any remaining violations
testpy lint

# View detailed report if needed
testpy lint --violations
```

### Expected Output (Success)

```
✓ Validation Passed

No test organization violations found!

Project: your-project
Language: rust
Test root: tests
```

### Run Your Tests

```bash
# Run all tests
testpy

# Run specific category
testpy sanity

# Run specific module
testpy sanity math

# Run with override (if you need to bypass temporarily)
testpy --override
```

### Task Checklist

- [ ] `testpy lint` shows 0 violations
- [ ] All sanity tests pass: `cargo test --test sanity`
- [ ] All UAT tests pass: `cargo test --test uat`
- [ ] All category entry files compile
- [ ] Hub integration tests pass (if applicable)

---

## 🎯 Common Issues & Solutions

### "Module 'X' missing sanity tests"

**Solution**: Create `tests/sanity_X.rs` with basic functionality tests.

```bash
# Template
cat > tests/sanity_X.rs << 'EOF'
//! Sanity tests for X module

#[test]
fn X_basic_test() {
    use your_project::X;
    // Add test here
}
EOF

# Update tests/sanity.rs
echo "mod sanity_X;" >> tests/sanity.rs
```

### "Module 'X' missing UAT tests"

**Solution**: Create `tests/uat_X.rs` with visual demonstration tests.

```bash
# Template
cat > tests/uat_X.rs << 'EOF'
//! UAT tests for X module

#[test]
fn uat_X_demonstration() {
    println!("\n=== X Module UAT ===\n");
    use your_project::X;
    // Add visual test here
    println!("\n=== UAT Complete ===\n");
}
EOF

# Update tests/uat.rs
echo "mod uat_X;" >> tests/uat.rs
```

### "Missing category entry file: Y"

**Solution**: Create `tests/Y.rs` category entry file.

```bash
cat > tests/Y.rs << 'EOF'
//! Y test category entry point

// Add module imports as you create tests:
// mod Y_modulename;
EOF
```

### "Invalid directory: tests/foo/"

**Solution**: Rename directory to valid category or move to `_archive/`.

```bash
# Option 1: Rename to valid category
mv tests/foo/ tests/unit/

# Option 2: Archive if unused
mv tests/foo/ tests/_archive/
```

### "Hub package 'X' missing integration test"

**Solution**: Create `tests/integration/hub_X.rs`.

```bash
mkdir -p tests/integration

cat > tests/integration/hub_X.rs << 'EOF'
//! Hub integration test for X

#[test]
fn hub_X_available() {
    use your_project::deps::X;
    // Add minimal usage test
}
EOF

# Update tests/integration.rs
echo "mod hub_X;" >> tests/integration.rs
```

---

## 📚 Reference Commands

```bash
# Check test organization
testpy lint

# View detailed violations
testpy lint --violations

# Run all tests
testpy

# Run specific category
testpy sanity

# Run specific module tests
testpy sanity math

# Run with override (bypass validation)
testpy --override

# View documentation
testpy docs rust-org          # Test organization guide
testpy docs rust-howto        # Testing how-to guide
testpy docs rust-ux           # Visual testing UX guide
testpy docs checklist         # This checklist
```

---

## 🚀 Next Steps

Once your tests are organized:

1. **Set up CI/CD**: Add `testpy` to your CI pipeline
2. **Enhance UAT tests**: Add boxy/rolo for beautiful output
3. **Add ceremonies**: Create optional ceremony tests in `tests/ceremonies/`
4. **Document**: Update your project's README with test commands

### Learn More

- `testpy docs rust-org` - Complete test organization standard
- `testpy docs rust-howto` - Detailed testing guide with examples
- `testpy docs rust-ux` - Visual testing UX principles

---

**Generated by testpy - Universal Test Orchestrator**
