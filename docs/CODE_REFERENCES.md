# Code References & Source Reliability

**Created:** 2025-10-08

## ⚠️ IMPORTANT: Source Reference Hierarchy

### Canonical Reference (PRIMARY)
**Location:** `code_ref/rsb_test.sh` → `/home/xnull/repos/code/rust/prods/oodx/rsb/bin/test.sh`

This is the **ONLY AUTHORITATIVE** test.sh implementation for RSB patterns.

- ✅ Fully implements MODULE_SPEC integration
- ✅ Correct test organization enforcement
- ✅ Up-to-date with RSB standards
- ✅ Reference for all test validation logic

**Use this for:**
- Test organization rules
- Validation logic
- Category enforcement
- MODULE_SPEC integration
- Error messages and reporting
- Configuration patterns

### Architectural Reference (SECONDARY)
**Location:** `code_ref/testsh` → `/home/xnull/repos/code/shell/bashfx/fx-testsh/`

This demonstrates modular shell architecture **ONLY**.

- ✅ Good example of BashFX v3 build system
- ✅ Shows modular code organization
- ⚠️ **NOT reliable for RSB test patterns**
- ⚠️ **May have outdated or incorrect implementation**

**Use this for:**
- Understanding modular build approach
- Seeing parts/ directory structure
- Learning BashFX build system patterns
- Architectural inspiration ONLY

**DO NOT use for:**
- ❌ Test validation logic
- ❌ MODULE_SPEC patterns
- ❌ RSB enforcement rules
- ❌ Feature implementation reference

---

## Other test.sh Files in Rust Projects

### ⚠️ WARNING: Inconsistent Implementations

Many Rust projects have `bin/test.sh` files, but they are **NOT reliable references**:

**Projects with test.sh based on boxy's version:**
- vizo/boxy
- vizo/rolo
- skull/cage
- skull/padlock
- meteor/meteordb
- servo/kick
- Others...

**Problems with these:**
- Based on older boxy test.sh implementation
- Did not receive proper updates
- May have incorrect MODULE_SPEC integration
- Enforcement logic may be outdated
- Not aligned with current RSB standards

**Status:** These are project runners, not reference implementations.

---

## Reference Documentation

### Primary Documentation Sources

1. **RSB Test Patterns Analysis**
   - Location: `docs/ref/rsb_test_patterns_analysis.md`
   - Source: Analysis of oodx-rsb test.sh
   - Content: Line-by-line breakdown of canonical implementation

2. **MODULE_SPEC v3**
   - Location: `docs/ref/MODULE_SPEC.md`
   - Source: oodx-rsb reference spec
   - Content: Official module organization requirements

3. **Standardization Plan**
   - Location: `docs/rust_test_standardization_plan.md`
   - Content: Strategy for universal test implementation

### Secondary Documentation

4. **Shell Architecture Comparison**
   - Location: `docs/ref/shell_architecture_comparison.md`
   - Content: Monolithic vs modular approaches
   - **Note:** Architectural reference only

---

## Implementation Guidelines

### When Building testrs (this project):

#### ✅ DO Reference:
1. **oodx-rsb test.sh** (`code_ref/rsb_test.sh`)
   - Test organization validation logic
   - Category enforcement rules
   - MODULE_SPEC integration
   - Error messages and warnings
   - Configuration options

2. **RSB Test Patterns Analysis** (`docs/ref/rsb_test_patterns_analysis.md`)
   - Documented line-by-line logic
   - Code snippets with line numbers
   - Validation rules

3. **MODULE_SPEC v3** (`docs/ref/MODULE_SPEC.md`)
   - Official spec for module organization
   - Required test structure

#### ⚠️ Reference Carefully:
1. **BashFX testsh** (`code_ref/testsh`)
   - Modular architecture patterns ONLY
   - Build system approach
   - **Ignore specific test logic**

#### ❌ DO NOT Reference:
1. **Other rust project test.sh files**
   - Outdated implementations
   - Unreliable patterns
   - May contradict RSB standards

---

## Verification Checklist

When implementing testrs features, verify against canonical source:

- [ ] Check logic against `code_ref/rsb_test.sh` (oodx-rsb)
- [ ] Verify line numbers in `docs/ref/rsb_test_patterns_analysis.md`
- [ ] Confirm MODULE_SPEC alignment with `docs/ref/MODULE_SPEC.md`
- [ ] Cross-reference with standardization plan
- [ ] Test against oodx-rsb project as validation

**Never:**
- [ ] ~~Copy logic from boxy-based test.sh files~~
- [ ] ~~Trust bashfx testsh for RSB patterns~~
- [ ] ~~Assume all test.sh files are equivalent~~

---

## Quick Reference Summary

| Source | Purpose | Reliability | Use For |
|--------|---------|-------------|---------|
| **oodx-rsb test.sh** | Canonical RSB implementation | ⭐⭐⭐⭐⭐ | Everything |
| **RSB analysis docs** | Documented reference | ⭐⭐⭐⭐⭐ | Implementation guide |
| **MODULE_SPEC v3** | Official specification | ⭐⭐⭐⭐⭐ | Requirements |
| **BashFX testsh** | Modular architecture example | ⭐⭐⭐ | Architecture only |
| **Boxy-based test.sh** | Legacy project runners | ⭐ | ❌ Avoid |

---

## Contact & Updates

**Maintainer:** testrs project team
**Canonical Source:** `/home/xnull/repos/code/rust/prods/oodx/rsb/`
**Last Verified:** 2025-10-08

**Note:** If RSB test.sh is updated, this project must sync with those changes.
