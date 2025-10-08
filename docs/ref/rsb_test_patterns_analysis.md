# RSB Test Organization Patterns - Technical Analysis

**Document Version:** 1.0
**Source:** `/home/xnull/repos/code/rust/prods/oodx/rsb/bin/test.sh` (1561 lines)
**Analysis Date:** 2025-10-08
**Analyst:** Rust Repairman

---

## Executive Summary

The RSB test.sh script enforces a strict, BASHFX-aligned test organization framework with:
- **8 required test categories** (sanity, smoke, unit, integration, e2e, uat, chaos, bench, regression)
- **Mandatory naming patterns** for test files: `<category>_<module>.rs`
- **Required sanity and UAT tests** for every module (except excluded patterns)
- **Three enforcement modes**: strict (default), override (warnings), skip (disabled)
- **Full MODULE_SPEC integration** for discovering modules requiring tests

---

## Test Directory Structure Requirements

### Approved Root Test Directory Layout

**Location:** `tests/` directory at project root

**Required Category Entry Files** (lines 122, 224-228):
```bash
# Each category MUST have an entry file (either .rs OR .sh)
required_category_entries=(sanity smoke unit integration e2e uat chaos bench regression)
```

Each entry file serves as a **category orchestrator** that includes/imports all module-specific tests for that category.

**Valid Test Directories** (lines 273-276):
```bash
# Valid subdirectories under tests/
valid_directories: unit/ sanity/ smoke/ integration/ e2e/ uat/ chaos/ bench/ regression/ sh/ _archive/ _adhoc/
```

**Special Directories:**
- `tests/_archive/` - Archived/legacy tests (excluded from validation)
- `tests/_adhoc/` - Experimental tests (excluded from validation, run via `test.sh adhoc`)
- `tests/sh/` - Shell-based test scripts

---

## Test File Naming Patterns

### Wrapper File Pattern (lines 136-152)

**Required Pattern:**
```regex
^(unit|sanity|smoke|integration|e2e|uat|chaos|bench|regression)(_[a-z_]+)?$
```

**Valid Examples:**
- `sanity_math.rs` - Sanity tests for math module
- `uat_global.rs` - UAT tests for global module
- `unit_string.rs` - Unit tests for string module
- `sanity.rs` - Category orchestrator (no module suffix)

**Invalid Examples:**
- `math_sanity.rs` - ❌ Wrong order (module before category)
- `SanityMath.rs` - ❌ Wrong case (must be lowercase)
- `sanity-math.rs` - ❌ Wrong separator (must be underscore)
- `test_math.rs` - ❌ Invalid category name

**Code Reference (lines 148-151):**
```bash
# Check naming pattern
if [[ ! "$basename" =~ ^($valid_categories)(_[a-z_]+)?$ ]]; then
    naming_violations+=("$file")
fi
```

### Exclusion Patterns (lines 142-146)

Files **excluded from validation**:
```bash
# Skip excluded test files (starting with _ or dev_)
[[ "$basename" =~ ^(_|dev_) ]] && continue

# Skip archive files
[[ "$basename" =~ ^_ ]] && continue
```

**Excluded file prefixes:**
- `_*.rs` - Archived or work-in-progress tests
- `dev_*.rs` - Development/experimental tests

---

## Required Test Categories Per Module

### Mandatory Tests for Each Module

**Sanity Tests** (lines 186-215):
- **Required:** Every module MUST have sanity tests
- **Purpose:** Core functionality validation (fast, reliable, essential)
- **Patterns checked** (3 acceptable locations):
  1. `tests/sanity_<module>.rs` (root wrapper)
  2. `tests/sanity/<module>.rs` (subdirectory)
  3. `tests/sanity/sanity_<module>.rs` (subdirectory with prefix)

**UAT Tests** (lines 217-221):
- **Required:** Every module MUST have UAT tests
- **Purpose:** User Acceptance Tests with visual ceremony/demonstrations
- **Patterns checked** (3 acceptable locations):
  1. `tests/uat_<module>.rs` (root wrapper)
  2. `tests/uat/<module>.rs` (subdirectory)
  3. `tests/uat/uat_<module>.rs` (subdirectory with prefix)

**Code Reference (lines 212-215):**
```bash
# Check for sanity test existence (3 patterns: wrapper, direct, or prefixed in folder)
if [[ ! -f "tests/sanity_${module_name}.rs" && ! -f "tests/sanity/${module_name}.rs" && ! -f "tests/sanity/sanity_${module_name}.rs" ]]; then
    missing_sanity_violations+=("$module_name")
fi
```

### Module Discovery Pattern (lines 202-221)

**How modules are discovered:**
```bash
# Pattern: src/module/mod.rs files (directory modules)
for module_dir in src/*/; do
    [[ ! -d "$module_dir" ]] && continue
    [[ ! -f "${module_dir}mod.rs" ]] && continue

    module_name=$(basename "$module_dir")

    # Skip excluded modules
    is_excluded_module "$module_name" && continue

    # Check for sanity test existence...
    # Check for UAT test existence...
done
```

**Note:** Direct `src/module.rs` files are **currently disabled** during MODULE_SPEC migration (lines 187-200):
```bash
# Pattern 1: src/module.rs files (direct module files) - COMMENTED OUT DURING MODULE_SPEC MIGRATION
# TODO: Re-enable once legacy .rs files are migrated to MODULE_SPEC
# for module_file in src/*.rs; do
#     ...
# done
```

---

## Module Exclusion Patterns

### Excluded Modules (lines 159-169)

Modules **NOT requiring tests**:
```bash
local excluded_patterns=(
    "_*"           # Not ready/WIP modules
    "dev_*"        # Experimental modules (but 'dev' itself is real)
    "prelude*"     # Re-export modules
    "dummy_*"      # Test helper modules
    "lib"          # Library entry point
    "main"         # Binary entry point
    "macros"       # Legacy module (pending MODULE_SPEC migration)
    "streamable"   # Legacy module (pending MODULE_SPEC migration)
    "xcls"         # Legacy module (pending MODULE_SPEC migration)
)
```

**Special Case (lines 176-180):**
```bash
# Special case: 'dev' itself is not excluded, only dev_*
if [[ "$pattern" == "dev_*" && "$module" == "dev" ]]; then
    return 1  # Not excluded
fi
```

### Exclusion Logic Function (lines 172-184)

```bash
# Function to check if module should be excluded
is_excluded_module() {
    local module="$1"
    for pattern in "${excluded_patterns[@]}"; do
        if [[ "$module" == $pattern ]]; then
            # Special case: 'dev' itself is not excluded, only dev_*
            if [[ "$pattern" == "dev_*" && "$module" == "dev" ]]; then
                return 1  # Not excluded
            fi
            return 0  # Excluded
        fi
    done
    return 1  # Not excluded
}
```

---

## Test Function Naming Requirements

### UAT Function Naming (lines 660-661)

**Required Pattern:**
```rust
uat_<module>_<description>()
```

**Examples:**
```rust
#[test]
fn uat_math_basic_demo() { ... }

#[test]
fn uat_math_integer_operations_demo() { ... }

#[test]
fn uat_global_clear_demo() { ... }
```

**Observed in:** `/home/xnull/repos/code/rust/prods/oodx/rsb/tests/uat/math.rs:8, 52`

### SANITY Function Naming (lines 661-662)

**Required Pattern:**
```rust
sanity_<module>_<description>()
```

**Examples:**
```rust
#[test]
fn test_basic_arithmetic_operations() { ... }  // Generic test functions also allowed

#[test]
fn test_integer_operations() { ... }

#[test]
fn test_base_conversions() { ... }
```

**Note:** While the script documents the `sanity_<module>_<description>` pattern, actual test files use standard Rust `test_*` naming. The requirement is for **file-level organization**, not function naming enforcement.

---

## Validation Logic and Error Detection

### Violation Categories (lines 112-118)

The script tracks **6 violation types**:
```bash
local naming_violations=()                      # Files not matching <category>_<module>.rs
local missing_sanity_violations=()              # Modules without sanity tests
local missing_uat_violations=()                 # Modules without UAT tests
local directory_violations=()                   # Invalid test directories
local missing_category_entry_violations=()      # Missing category orchestrator files
local unauthorized_root_violations=()           # Files in tests/ root not following rules
```

### Validation Entry Point (lines 111-467)

**Function:** `validate_test_structure()`

**Execution Logic:**
1. Skip if `SKIP_ENFORCEMENT=true` (line 124-126)
2. Show warning if `OVERRIDE_MODE=true` (line 129-131)
3. Check wrapper naming patterns (lines 136-152)
4. Check for required sanity/UAT tests per module (lines 186-221)
5. Check for category entry files (lines 224-228)
6. Check for unauthorized root files (lines 231-265)
7. Check for invalid directories (lines 268-277)
8. Calculate total violations (line 280)
9. Report violations based on mode (lines 283-464)

### Enforcement Modes (lines 403-451)

**1. STRICT MODE (default)** - Lines 403-424:
```bash
if [[ "$STRICT_MODE" == "true" && "$OVERRIDE_MODE" != "true" ]]; then
    # HARD FAIL: Tests cannot run with violations in strict mode
    boxy_display "$error_text" "error" "❌ Test Organization Violations"
    exit 1
fi
```
- **Behavior:** Block test execution with exit code 1
- **Enabled by:** `--strict` flag (default: true, line 512)

**2. OVERRIDE MODE** - Lines 425-439:
```bash
elif [[ "$OVERRIDE_MODE" == "true" ]]; then
    # OVERRIDE MODE: Show violations but continue with warning
    boxy_display "$override_text" "warning" "⚠️  Organization Violations (Override Active)"
fi
```
- **Behavior:** Show warnings but allow tests to run
- **Enabled by:** `--override` flag (lines 543-547)
- **Shows warning banner** via `show_override_warning()` (lines 92-107)

**3. PERMISSIVE MODE** - Lines 440-451:
```bash
else
    # PERMISSIVE MODE: Just warn
    echo "⚠️  Test structure warnings ($total_violations total):"
    echo "   • Naming issues: ${#naming_violations[@]}"
    ...
fi
```
- **Behavior:** Show simple console warnings only
- **Enabled by:** Setting `STRICT_MODE=false` without `--override`

**4. SKIP ENFORCEMENT** - Lines 538-542:
```bash
--skip-enforcement)
    SKIP_ENFORCEMENT="true"
    STRICT_MODE="false"
    shift 1
    ;;
```
- **Behavior:** Completely disable all validation
- **Enabled by:** `--skip-enforcement` flag

---

## Violation Reporting

### Detailed Violations Report (lines 286-401)

**Triggered by:** `--violations` flag (lines 548-551)

**Report Sections:**
1. **Naming Violations** (lines 292-305)
   - Issue: Files don't follow `<category>_<module>.rs` pattern
   - Fix: Rename files to match pattern

2. **Missing Sanity Tests** (lines 308-320)
   - Issue: Modules without required sanity tests
   - Fix: Create `tests/sanity_<module>.rs` for each module

3. **Missing UAT Tests** (lines 323-335)
   - Issue: Modules without required UAT/ceremony tests
   - Fix: Create `tests/uat_<module>.rs` with visual demonstrations

4. **Missing Category Entry Files** (lines 338-350)
   - Issue: Missing category orchestrator files
   - Fix: Create category entry files (e.g., `tests/smoke.rs`)

5. **Unauthorized Root Files** (lines 353-365)
   - Issue: Files in `tests/` root that don't follow rules
   - Fix: Rename, move to `_adhoc/`, or move to `_archive/`

6. **Invalid Directories** (lines 368-380)
   - Issue: Test directories not matching approved organization
   - Fix: Move to approved categories or rename to `_archive/`

**Example Error Message (lines 295-303):**
```
🏷️  NAMING VIOLATIONS (3 files)
────────────────────────────────────────────────────────
Issue: Test wrapper files don't follow naming pattern
Required: <category>_<module>.rs (e.g., sanity_com.rs, uat_math.rs)
Valid categories: unit, sanity, smoke, integration, e2e, uat, chaos, bench

  1. tests/math_sanity.rs
  2. tests/test_global.rs
  3. tests/SanityColors.rs

Fix: Rename files to match pattern (e.g., com_sanity.rs → sanity_com.rs)
```

---

## MODULE_SPEC Integration Points

### Module Discovery from MODULE_SPEC (lines 202-221)

The script integrates with MODULE_SPEC by:

1. **Discovering modules via directory structure:**
   ```bash
   for module_dir in src/*/; do
       [[ ! -d "$module_dir" ]] && continue
       [[ ! -f "${module_dir}mod.rs" ]] && continue

       module_name=$(basename "$module_dir")
       # ... validation logic
   done
   ```

2. **Respecting MODULE_SPEC exclusion patterns** (lines 159-169)

3. **Deferring legacy module checks** (lines 187-200):
   ```bash
   # Pattern 1: src/module.rs files (direct module files) - COMMENTED OUT DURING MODULE_SPEC MIGRATION
   # TODO: Re-enable once legacy .rs files are migrated to MODULE_SPEC
   ```

4. **Enforcing MODULE_SPEC requirements:**
   - Every MODULE_SPEC module MUST have sanity tests
   - Every MODULE_SPEC module MUST have UAT tests
   - Legacy modules marked in exclusions (macros, streamable, xcls)

### MODULE_SPEC Documentation Reference

**File:** `/home/xnull/repos/code/rust/prods/oodx/rsb/docs/tech/development/MODULE_SPEC.md`

**Relevant Section (lines 61-62):**
```markdown
- **REQUIRED:** Create sanity and UAT tests for new modules or tests will be blocked.
```

**Module Layout Enforcement:**
- Script validates that `src/<module>/mod.rs` exists (line 205)
- Excludes modules matching MODULE_SPEC exclusion patterns
- Requires test files matching module names

---

## Configuration Options and Overrides

### Environment Variables

**Test Timeout Configuration (lines 41-42):**
```bash
# Default to 10 minutes if not provided; override via RSB_TEST_TIMEOUT (in seconds)
local secs="${RSB_TEST_TIMEOUT:-600}"
```

**Documentation Path Overrides (lines 12-17):**
```bash
DOCS_BASE_DIR="${RSB_DOCS_BASE_DIR:-$PROJECT_ROOT/docs}"
DOCS_DEV_DIR="${RSB_DOCS_DEV_DIR:-$DOCS_BASE_DIR/tech/development}"
DOCS_FEATURES_DIR="${RSB_DOCS_FEATURES_DIR:-$DOCS_BASE_DIR/tech/features}"
DOCS_REFERENCE_DIR="${RSB_DOCS_REFERENCE_DIR:-$DOCS_BASE_DIR/tech/reference}"
```

### Command-Line Flags

**Enforcement Control (lines 518-557):**
```bash
--verbose, -v           # Enable verbose test output (VERBOSE_MODE=true)
--quick                 # Force quick mode (default, QUICK_MODE=true)
--comprehensive, --full # Run full test suite (COMPREHENSIVE_MODE=true)
--strict                # Fail on violations (default, STRICT_MODE=true)
--skip-enforcement      # Disable validation entirely (SKIP_ENFORCEMENT=true)
--override              # Run despite violations with warnings (OVERRIDE_MODE=true)
--violations            # Show detailed violation report and exit (VIOLATIONS_MODE=true)
```

**Flag Parsing (lines 518-557):**
```bash
while [[ $# -gt 0 ]]; do
    case "$1" in
        --verbose|-v)
            VERBOSE_MODE="true"
            shift 1
            ;;
        --strict)
            STRICT_MODE="true"
            shift 1
            ;;
        --override)
            OVERRIDE_MODE="true"
            STRICT_MODE="false"
            shift 1
            ;;
        # ... more cases
    esac
done
```

### Default Configuration (lines 509-516)

```bash
VERBOSE_MODE="false"
QUICK_MODE="true"      # Default to quick mode
COMPREHENSIVE_MODE="false"
STRICT_MODE="true"     # Default to strict - tests fail if disorganized
SKIP_ENFORCEMENT="false"
OVERRIDE_MODE="false"
VIOLATIONS_MODE="false"
```

---

## Test Execution Integration

### Pre-Execution Validation (lines 1214-1218)

**All test runs validate structure first:**
```bash
case "${1:-status}" in
    "run")
        # Validate structure before running tests (unless skipped)
        if [[ "$SKIP_ENFORCEMENT" != "true" ]]; then
            validate_test_structure
        fi
        run_test "$2" "$3"
        ;;
```

### Module-Specific Test Filtering (lines 927-959)

**New feature: Run tests by module:**
```bash
run_module_tests() {
    local category="$1"
    local module="$2"

    case "$category" in
        "uat")
            ctest test --test uat uat_${module}_ -- --nocapture
            ;;
        "sanity")
            ctest test --test sanity sanity_${module}_ -- --nocapture
            ;;
    esac
}
```

**Usage:**
```bash
./bin/test.sh run uat math       # Run all math UAT tests
./bin/test.sh run sanity tokens  # Run all tokens sanity tests
```

---

## Category Orchestrator Pattern

### Implementation Example

**File:** `tests/sanity.rs` (Category orchestrator)

**Pattern (lines 1-169 of sanity.rs):**
```rust
// Category orchestrator: sanity tests
// This file includes all sanity test modules for category-level execution

#[path = "sanity/baseline.rs"]
mod baseline;

#[path = "sanity/bash.rs"]
mod bash;

#[path = "sanity/com.rs"]
mod com;

#[path = "sanity/core.rs"]
mod core;

// ... more module imports

#[cfg(feature = "object")]
#[path = "sanity/object.rs"]
mod object;

// NEW: Math module subdirectory
#[path = "sanity/math/basic.rs"]
mod math_basic;

#[path = "sanity/math/integers.rs"]
mod math_integers;

// ... more submodule imports
```

**Purpose:**
- Single entry point for all sanity tests
- Enables running entire category: `cargo test --test sanity`
- Maintains organization while allowing granular imports
- Supports feature-gated modules

---

## Special Test Directories

### Adhoc Tests (lines 809-924)

**Directory:** `tests/_adhoc/`

**Purpose:** Experimental/temporary tests excluded from validation

**Commands:**
```bash
./bin/test.sh adhoc <test_name>     # Run specific adhoc test
./bin/test.sh list-adhoc            # List all adhoc tests
```

**Discovery Logic (lines 820-825):**
```bash
# Find .rs and .sh files in _adhoc directory
while IFS= read -r -d '' file; do
    local basename
    basename="$(basename "$file")"
    adhoc_tests+=("$basename")
done < <(find "$adhoc_dir" -maxdepth 1 \( -name "*.rs" -o -name "*.sh" \) -print0 | sort -z)
```

**Execution (lines 901-923):**
- `.rs` files: Execute via `cargo test --test "_adhoc_$test_basename"`
- `.sh` files: Execute via `bash "$test_file"`

### Archive Directory

**Directory:** `tests/_archive/`

**Purpose:** Archived/obsolete tests

**Treatment:**
- Excluded from naming validation (lines 142-146)
- Not discovered or run automatically
- Preserved for historical reference

---

## Zero Violations Achievement

### Success Message (lines 453-464)

**When all violations are resolved:**
```bash
# 🎉 ZERO VIOLATIONS ACHIEVED! 🎉
local celebration_text="🎉 ZERO TEST VIOLATIONS ACHIEVED! 🎉

Test framework status: FULLY COMPLIANT

The RSB test ecosystem is now perfectly organized and ready for
comprehensive validation across all modules and categories.

🏆 Outstanding work achieving complete test compliance! 🏆"

boxy_display "$celebration_text" "success" "🎯 RSB TEST ORGANIZATION: PERFECT COMPLIANCE"
```

---

## Boxy Integration

### Pretty Output System (lines 19-86)

**Boxy Detection (lines 19-27):**
```bash
# Try to find boxy for pretty output (optional)
BOXY=""
if command -v boxy >/dev/null 2>&1; then
    BOXY="boxy"
elif [[ -f "./target/release/boxy" ]]; then
    BOXY="./target/release/boxy"
elif [[ -f "../boxy/target/release/boxy" ]]; then
    BOXY="../boxy/target/release/boxy"
fi
```

**Centralized Display Function (lines 64-86):**
```bash
boxy_display() {
    local content="$1"
    local theme="$2"    # info, success, warning, error, magic
    local title="$3"
    local width="${4:-max}"

    if command -v boxy >/dev/null 2>&1; then
        local args=()
        [[ -n "$theme" ]] && args+=(--theme "$theme")
        [[ -n "$title" ]] && args+=(--title "$title")
        [[ -n "$width" ]] && args+=(--width "$width")

        local boxy_status=0
        set +e
        printf '%s\n' "$content" | boxy "${args[@]}"
        boxy_status=$?
        set -e
        [[ $boxy_status -ne 0 ]] && boxy_stderr_fallback "$content" "$title" "$theme"
    else
        boxy_stderr_fallback "$content" "$title" "$theme"
    fi
}
```

**Themes Used:**
- `info` - Documentation, help text, lists
- `success` - Test execution, zero violations
- `warning` - Override mode, violations
- `error` - Strict mode blocks
- `magic` - Special effects (line 88)

---

## Lint and Report Commands

### Lint Mode (lines 470-478)

**Command:** `./bin/test.sh lint`

**Purpose:** Check compliance only (no test execution)

```bash
lint_tests() {
    echo "🧹 Linting test organization..."
    echo

    STRICT_MODE="true"  # Always strict in lint mode
    validate_test_structure

    echo "✅ Test organization lint completed"
}
```

**Behavior:**
- Forces strict mode
- Runs validation logic
- Exits with error code if violations found
- Ideal for CI/CD pipelines

### Report Mode (lines 481-505)

**Command:** `./bin/test.sh report`

**Purpose:** Generate test organization statistics

```bash
report_tests() {
    echo "📊 Test Organization Report"
    echo "=========================="
    echo

    # Count tests by category
    local categories=(unit sanity smoke integration e2e uat chaos bench)

    for category in "${categories[@]}"; do
        local count=$(find tests -name "${category}_*.rs" -o -name "${category}.rs" 2>/dev/null | wc -l)
        echo "$category: $count test files"
    done

    echo
    echo "Test directories:"
    for dir in tests/*/; do
        [[ ! -d "$dir" ]] && continue
        local dir_name=$(basename "$dir")
        local file_count=$(find "$dir" -name "*.rs" 2>/dev/null | wc -l)
        echo "  $dir_name/: $file_count files"
    done

    echo
    validate_test_structure
}
```

**Output Example:**
```
📊 Test Organization Report
==========================

sanity: 15 test files
smoke: 1 test files
unit: 8 test files
integration: 3 test files
e2e: 1 test files
uat: 12 test files
chaos: 2 test files
bench: 1 test files

Test directories:
  sanity/: 45 files
  uat/: 32 files
  unit/: 28 files
  integration/: 8 files
  ...

🔍 Validating test structure...
✅ Test organization is compliant
```

---

## Test Category Definitions

### Category Specifications (lines 643-651)

**From help text:**

| Category      | Purpose                                              | Timing       | Required |
|---------------|------------------------------------------------------|--------------|----------|
| `sanity`      | Core functionality validation (essential baseline)   | Fast         | YES      |
| `smoke`       | Minimal CI tests (<10s total)                        | Very Fast    | NO       |
| `unit`        | Fast, isolated module tests                          | Fast         | NO       |
| `integration` | Cross-module interaction tests                       | Medium       | NO       |
| `e2e`         | End-to-end user workflow tests                       | Slow         | NO       |
| `uat`         | User Acceptance Tests with visual ceremony           | Medium/Slow  | YES      |
| `chaos`       | Edge cases, stress tests, property tests             | Variable     | NO       |
| `bench`       | Performance benchmarks                               | Slow         | NO       |
| `regression`  | Tests for previously broken functionality            | Variable     | NO       |

**Valid Categories Regex (line 121):**
```bash
local valid_categories="unit|sanity|smoke|integration|e2e|uat|chaos|bench|regression"
```

---

## TODOs and Commented Sections

### Deferred Module Tests (lines 37-43 of sanity.rs)

```rust
// TEMP: logging sanity test not yet created - deferred per user request
// #[path = "sanity/logging.rs"]
// mod logging;

// TEMP: streams sanity test not yet created - deferred per user request
// #[path = "sanity/streams.rs"]
// mod streams;
```

**Status:** Temporarily deferred by user request

### Legacy Module Migration (lines 187-200)

```bash
# Pattern 1: src/module.rs files (direct module files) - COMMENTED OUT DURING MODULE_SPEC MIGRATION
# TODO: Re-enable once legacy .rs files are migrated to MODULE_SPEC
# for module_file in src/*.rs; do
#     [[ ! -f "$module_file" ]] && continue
#     module_name=$(basename "$module_file" .rs)
#
#     # Skip excluded modules
#     is_excluded_module "$module_name" && continue
#
#     # Check for sanity test existence (3 patterns: wrapper, direct, or prefixed in folder)
#     if [[ ! -f "tests/sanity_${module_name}.rs" && ! -f "tests/sanity/${module_name}.rs" && ! -f "tests/sanity/sanity_${module_name}.rs" ]]; then
#         missing_sanity_violations+=("$module_name")
#     fi
# done
```

**Status:** Disabled during MODULE_SPEC v3 migration
**Action Required:** Re-enable after all `src/*.rs` files migrated to `src/*/mod.rs` structure

### Archived Token Module (lines 84-86 of sanity.rs)

```rust
// TEMP: Tokens module archived, being replaced with meteor
// #[path = "sanity/tokens/basic.rs"]
// mod tokens_basic;
```

**Status:** Module archived, being replaced with meteor module

---

## Quick Reference Commands

### Common Usage Patterns

```bash
# Run all tests with validation (strict mode - default)
./bin/test.sh run sanity

# Run specific module tests
./bin/test.sh run uat math           # All math UAT tests
./bin/test.sh run sanity global      # All global sanity tests

# Validation and reporting
./bin/test.sh lint                   # Check compliance only
./bin/test.sh report                 # Generate statistics report
./bin/test.sh --violations           # Show detailed violations

# Override modes
./bin/test.sh --override run sanity  # Run with warnings
./bin/test.sh --skip-enforcement run sanity  # No validation

# Adhoc tests
./bin/test.sh adhoc my_test          # Run experimental test
./bin/test.sh list-adhoc             # List experimental tests

# Documentation
./bin/test.sh docs org               # Show test organization docs
./bin/test.sh docs howto             # Show testing guide
./bin/test.sh docs modules           # Show MODULE_SPEC
```

---

## Compliance Checklist

Use this checklist to ensure test organization compliance:

- [ ] Every module in `src/*/mod.rs` has corresponding sanity tests
- [ ] Every module in `src/*/mod.rs` has corresponding UAT tests
- [ ] All test files follow `<category>_<module>.rs` naming pattern
- [ ] All 9 category entry files exist: `sanity.rs`, `smoke.rs`, `unit.rs`, `integration.rs`, `e2e.rs`, `uat.rs`, `chaos.rs`, `bench.rs`, `regression.rs`
- [ ] No unauthorized files in `tests/` root (move to `_adhoc/` or `_archive/`)
- [ ] Only valid directories exist under `tests/`
- [ ] Category orchestrator files import all module tests
- [ ] Test functions follow naming conventions (for UAT: `uat_<module>_<description>`)
- [ ] Legacy modules marked in exclusion patterns
- [ ] Experimental tests moved to `tests/_adhoc/`
- [ ] `./bin/test.sh lint` runs without errors

---

## Architecture Alignment

This test organization enforces:

1. **BASHFX Alignment** - Mentioned throughout script as guiding framework
2. **MODULE_SPEC v3** - Direct integration with module discovery
3. **Progressive Enhancement** - Feature-gated tests, staged rollout
4. **Zero-Tolerance** - Strict mode prevents technical debt accumulation
5. **Escape Hatches** - Override and skip modes for emergencies
6. **Developer Experience** - Clear error messages, helpful suggestions

---

## Summary Statistics

**Source File Analysis:**
- **Total Lines:** 1561
- **Validation Function:** 357 lines (lines 111-467)
- **Configuration Variables:** 4 (environment overrides)
- **Command-Line Flags:** 7 (control enforcement behavior)
- **Valid Test Categories:** 9
- **Required Categories:** 2 (sanity, uat)
- **Module Exclusion Patterns:** 9
- **Violation Types Tracked:** 6
- **Enforcement Modes:** 4 (strict, override, permissive, skip)

---

## File Paths Referenced

**Script Location:**
- `/home/xnull/repos/code/rust/prods/oodx/rsb/bin/test.sh`

**Documentation Paths (configurable):**
- `$DOCS_BASE_DIR` (default: `docs/`)
- `$DOCS_DEV_DIR` (default: `docs/tech/development/`)
- `$DOCS_FEATURES_DIR` (default: `docs/tech/features/`)
- `$DOCS_REFERENCE_DIR` (default: `docs/tech/reference/`)

**Key Documentation Files:**
- `docs/tech/development/MODULE_SPEC.md` - Module organization specification
- `docs/tech/development/TEST_ORGANIZATION.md` - Test requirements
- `docs/tech/development/HOWTO_TEST.md` - Testing guide

**Test Directories:**
- `tests/` - Root test directory
- `tests/sanity/` - Sanity test modules
- `tests/uat/` - UAT test modules
- `tests/_adhoc/` - Experimental tests
- `tests/_archive/` - Archived tests

---

## Recommendations for Stakeholders

1. **Enable CI/CD Integration:** Run `./bin/test.sh lint` in CI pipeline to enforce compliance
2. **Complete MODULE_SPEC Migration:** Re-enable `src/*.rs` validation after migration (line 187)
3. **Create Missing Tests:** Address deferred modules (logging, streams)
4. **Document Exclusions:** Update MODULE_SPEC when adding new excluded patterns
5. **Monitor Override Usage:** Track `--override` flag usage to prevent abuse
6. **Enforce Strict Mode:** Keep `STRICT_MODE=true` as default to prevent regression

---

**End of Report**
