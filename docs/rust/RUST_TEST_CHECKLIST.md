# Rust Test Organization Checklist

**Quick reference for setting up RSB-compliant test organization**

⚠️ **IMPORTANT**: The `testpy` linter enforces this organization. Tests will not run until all violations are fixed. Use `testpy lint --violations` to see what needs fixing.

---

## Quick Start

```bash
# Check current status
testpy lint

# View detailed violations
testpy lint --violations

# See detailed examples and templates
testpy docs rust-howto
```

---

## 📋 Per-Module Checklist

**Run this checklist every time you create a new module:**

### For Each New Module

- [ ] **Module created** in `src/<module>/mod.rs`
- [ ] **Sanity test created** in `tests/sanity/<module>.rs`
  - Tests core functionality works
  - Imported in `tests/sanity.rs`
- [ ] **UAT test created** in `tests/uat/<module>.rs`
  - Visual demonstration with STATUS messages (✓ PASS, ✗ FAIL)
  - Imported in `tests/uat.rs`
- [ ] **Tests compile**: `cargo test --test sanity` and `cargo test --test uat`
- [ ] **Validation passes**: `testpy lint` shows 0 violations

**See detailed templates**: `testpy docs rust-howto`

---

## 🏗️ Initial Project Setup Checklist

**Run this once when setting up test organization:**

### Step 1: Directory Structure

- [ ] Created `tests/` directory
- [ ] Created category directories:
  ```bash
  mkdir -p tests/{sanity,smoke,unit,integration,e2e,uat,chaos,bench,regression}
  ```

**Recommended structure**: `tests/<category>/<module>.rs`

### Step 2: Category Entry Files

Create all 9 category entry files in `tests/`:

- [ ] `sanity.rs` - Core functionality tests
- [ ] `smoke.rs` - Quick health checks
- [ ] `unit.rs` - Individual component tests
- [ ] `integration.rs` - Module interaction tests
- [ ] `e2e.rs` - End-to-end workflows
- [ ] `uat.rs` - User acceptance/visual tests
- [ ] `chaos.rs` - Stress and chaos testing
- [ ] `bench.rs` - Performance benchmarks
- [ ] `regression.rs` - Regression prevention

**Quick creation**:
```bash
cd tests
for cat in sanity smoke unit integration e2e uat chaos bench regression; do
  echo "//! ${cat^} test category entry point" > ${cat}.rs
done
```

### Step 3: Module Tests

For each module in `src/`:

- [ ] Add sanity test: `tests/sanity/<module>.rs`
- [ ] Add UAT test: `tests/uat/<module>.rs`
- [ ] Update `tests/sanity.rs` to import module
- [ ] Update `tests/uat.rs` to import module

**See templates**: `testpy docs rust-howto`

### Step 4: Hub Integration Tests (if using hub)

If your project has `src/deps.rs`:

- [ ] Created `tests/integration/` directory
- [ ] For each hub package, created `tests/integration/hub_<package>.rs`
- [ ] Updated `tests/integration.rs` to import hub tests

**Find hub packages**: `blade deps | grep hub`

### Step 5: Validation

- [ ] Run `testpy lint` - should show 0 violations
- [ ] All tests compile: `cargo test --lib`
- [ ] All category tests run: `cargo test --test sanity`, etc.

---

## 🔧 Fixing Violations

Run `testpy lint --violations` to see detailed issues.

### Common Violations & Fixes

| Violation | Fix |
|-----------|-----|
| **Naming issues** | Rename to `<category>_<module>.rs` or move to `tests/<category>/<module>.rs` |
| **Missing sanity tests** | Create `tests/sanity/<module>.rs` for each module |
| **Missing UAT tests** | Create `tests/uat/<module>.rs` for each module |
| **Missing category entries** | Create `tests/<category>.rs` entry files |
| **Unauthorized root files** | Move to `tests/_archive/` or rename to valid pattern |
| **Invalid directories** | Rename to valid category or move to `tests/_archive/` |
| **Missing hub integration** | Create `tests/integration/hub_<package>.rs` for each hub package |

**Detailed examples**: `testpy docs rust-howto`

---

## 📐 Valid Test Organization

### Required Patterns

**Category directories** (recommended):
```
tests/
├── sanity.rs              # Category entry
├── sanity/
│   ├── module1.rs         # Module tests
│   └── module2.rs
├── uat.rs                 # Category entry
├── uat/
│   ├── module1.rs
│   └── module2.rs
...
```

**Root-level wrappers** (alternative):
```
tests/
├── sanity.rs              # Category entry
├── sanity_module1.rs      # Module wrapper
├── sanity_module2.rs
├── uat.rs                 # Category entry
├── uat_module1.rs
├── uat_module2.rs
...
```

### Valid Categories

Only these 9 categories are allowed:
- `sanity`, `smoke`, `unit`, `integration`, `e2e`, `uat`, `chaos`, `bench`, `regression`

### Valid Directories

- `tests/<category>/` - One of the 9 valid categories
- `tests/sh/` - Shell scripts
- `tests/ceremonies/` - Optional ceremony tests (not enforced)
- `tests/_archive/` - Archived tests
- `tests/_adhoc/` - Experimental tests

**Files starting with `_` or `dev_` are automatically excluded.**

---

## 🎯 Required Tests Per Module

Every module in `src/` must have:

1. ✅ **Sanity tests** - Core functionality works
2. ✅ **UAT tests** - Visual demonstration with output

**No exceptions.** The linter enforces this.

If you need to exclude a module temporarily:
```toml
# .spec.toml
[tests]
exclude = ["legacy_module"]
```

---

## 📚 Getting Help

```bash
# View this checklist
testpy checklist

# View detailed testing guide with templates
testpy docs rust-howto

# View test organization standard
testpy docs rust-org

# View visual testing UX guide
testpy docs rust-ux

# Check for violations
testpy lint --violations
```

---

## 🚀 Quick Commands

```bash
# Validate test organization
testpy lint

# Run all tests
testpy

# Run specific category
testpy sanity

# Run specific module
testpy sanity math

# Emergency bypass (not recommended)
testpy --override
```

---

## ⚠️ Linter Enforcement

**The `testpy` linter is strict and non-negotiable:**

- ❌ Tests will NOT run if violations exist
- ❌ Naming patterns must be exact
- ❌ All modules must have sanity + UAT tests
- ❌ All 9 category entry files are required
- ❌ No unauthorized files in `tests/` root

**Only option**: Fix the violations or use `--override` (strongly discouraged).

---

**For detailed templates, examples, and explanations, see:**
- `testpy docs rust-howto` - Complete testing guide
- `testpy docs rust-org` - Test organization standard

**Generated by testpy - Universal Test Orchestrator**
