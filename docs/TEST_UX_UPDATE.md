# TEST_UX_UPDATE.md - Testing UX and Documentation Implementation

**Date:** 2025-10-09
**Status:** Planning Document
**Purpose:** Capture comprehensive testing UX improvements and documentation updates for testpy

---

## Overview

This document captures the research, patterns, and implementation plan for enhancing testpy with:
1. Rust testing documentation (universal, not RSB-specific)
2. Visual testing UX guidance
3. Ceremony test support
4. Boxy and rolo integration patterns
5. Brain sync for universal testing protocols

---

## 1. Documentation Structure

### 1.1 Source Documentation Analysis

**RSB Test Documentation Found (5 files, 1,520 lines):**
- `TEST_ORGANIZATION.md` (363 lines) - Test structure standard
- `HOWTO_TEST.md` (766 lines) - Testing guide with examples
- `RSB_TEST_RUNNER.md` (50 lines) - BashFX runner mapping (RSB-specific, skip)
- `RSB_TESTSH_INTEGRATION.md` (148 lines) - Integration procedure (RSB-specific, skip)
- `TEST_HARDENING_SUMMARY.md` (193 lines) - Session report (dated, skip)

**RSB Architecture Docs (ceremony/UX concepts):**
- `BASHFX-v3.md` - Section 4.5: Principle of Visual Friendliness (lines 790-820)
- `RSB_ARCH.md` - Section 4.2: Test Runner and Ceremony (lines 623-667)
- `HOWTO_UPDATE_RSB.md` - Chapters 3-7: Testing framework, patterns, commands

**Additional Resources:**
- Boxy v0.23.0 - `tests/ceremonies/` with 15+ ceremony implementations
- Rolo v0.2 - Table/column formatting tool

### 1.2 Target Documentation for testpy

```
test-py/
├── docs/
│   └── rust/
│       ├── RUST_TEST_ORGANIZATION.md     # From RSB (363 lines) - Universal patterns
│       ├── RUST_TESTING_HOWTO.md         # From RSB (766 lines) - testpy commands
│       ├── RUST_TESTING_UX.md            # NEW: Visual UX for tests (not ceremony-specific)
│       └── RUST_BOXY_ROLO_USAGE.md       # NEW: Boxy + Rolo patterns for tests
```

**Brain Sync Target:**
```
~/repos/docs/brain/dev/procs/testing/rust/
├── RUST_TEST_ORGANIZATION.md
├── RUST_TESTING_HOWTO.md
├── RUST_TESTING_UX.md
└── RUST_BOXY_ROLO_USAGE.md
```

---

## 2. Visual Testing UX Principles

### 2.1 Core Concepts from BashFX

**Visual Friendliness (BASHFX-v3.md:790-820):**
- Ceremony with Automation
- Clear visual demarkation of state progression
- ASCII banners, structured data, boxes
- Numbered steps, visual summaries
- Colors, glyphs, emojis for visual thinkers
- Whitespace for visual parsing

**Testing Suite Ceremony Requirements:**
- Test number + readable label
- STATUS messages: STUB (blue), PASS, FAIL, INVALID (purple)
- Standard glyphs: ✓, ☐, ✗, Δ (warning)
- Summary ceremony with metrics
- Independent tests (one invalid doesn't break others)

### 2.2 UAT Visual Requirements

**UAT tests MUST communicate (human-readable):**
1. **Hypothesis** - What are we testing?
2. **Expectations** - What should happen?
3. **Inputs** - What data/state are we using?
4. **Outcomes** - What actually happened?
5. **Results** - Pass/Fail with clear reasoning

**Implementation patterns:**
- Numbered tests with descriptive titles
- Smart iconography and colors
- Formatted strings for clarity
- Visual separation between steps
- Summary at end

**UAT does NOT require boxy:**
- Simple println! with good formatting works
- Clear hypothesis → expectation → result flow
- Human-readable output is the goal

### 2.3 Ceremony Tests (Optional, Enhanced)

**Ceremonies vs UAT:**
- **UAT:** Required module tests, simple visual output
- **Ceremony:** Optional workflow tests, heavily formatted with boxy/rolo

**When to use ceremonies:**
- A LOT of automation with minor variations
- Complex multi-step workflows
- Integration/e2e scenarios needing progressive disclosure
- Visual celebrations of results/outcomes

**Ceremony characteristics:**
- Top-level, NOT module-specific
- Named by purpose: `ceremony_<name>.sh`
- Shell scripts preferred (easier boxy/rolo integration)
- Located in `tests/ceremonies/` (flat structure)
- Not enforced by testpy validator

### 2.4 Celebrations Concept

**Celebrations:** Results/outcomes display
- "Something is done, here are the sub-results"
- Final results with summary
- Visual emphasis on completion
- Often end of ceremony or test suite

---

## 3. Tool Integration

### 3.1 Boxy (v0.23.0)

**Purpose:** Box drawing with themes, layouts, and formatting

**Key Features for Testing:**
- Theme system: success, error, warning, info
- Title/status/header/footer support
- Layout control (alignment, dividers, padding)
- Param streams for complex layouts
- ANSI color preservation
- Icon decorations

**Basic Usage:**
```bash
echo "Test passed" | boxy --theme success --title "✓ Sanity Test"
echo "Error occurred" | boxy --theme error --title "✗ Test Failed"
```

**Advanced Ceremony:**
```bash
echo "Step 1: Initialize" | boxy --theme info --title "🔧 Setup"
echo "Step 2: Execute" | boxy --theme info --title "⚡ Run"
echo "Summary: 2/2 passed" | boxy --theme success --title "📊 Results"
```

**Param Streams (complex layouts):**
```bash
echo "Body content" | boxy --params "hd='Header'; tl='Title'; st='Status'; h=14"
```

**Reference:**
- `boxy --version` - Check installed version
- `boxy --help` - Full API reference
- Upstream: `~/repos/code/rust/prods/vizo/boxy/tests/ceremonies/`

### 3.2 Rolo (v0.2)

**Purpose:** Tabular and structured text layout

**⚠️ NOTE:** Rolo documentation is being cleaned up/updated (as of 2025-10-09). Verify current API with `rolo --help` and upstream docs.

**Key Features:**
- Column mode (intelligent layout)
- Table mode (CSV formatting)
- ANSI-aware width handling
- Unix pipeline friendly

**Basic Usage (verify with current version):**
```bash
# Simple table
echo -e "Name,Age\nAlice,30\nBob,25" | rolo table

# Column layout
cat data.txt | rolo --cols 2
```

**Integration with Boxy:**
```bash
# Table inside box
echo -e "Col1,Col2\nA,B\nC,D" | rolo table | boxy --title "📊 Results"

# Multiple tables in ceremony
rolo table < data1.csv | boxy --title "Test 1"
rolo table < data2.csv | boxy --title "Test 2"
```

**Reference:**
- Upstream: `~/repos/code/rust/prods/vizo/rolo/`
- Status: v0.2 (in development, documentation cleanup in progress)
- **Always check:** `rolo --help` for current API

### 3.3 Combined Patterns

**UAT with structured data:**
```rust
#[test]
fn strings_uat() {
    println!("🧪 Strings Module UAT");
    println!("═══════════════════════");
    println!();

    println!("Test 1: Snake Case Conversion");
    println!("  Hypothesis: CamelCase → snake_case");
    println!("  Input:      'CamelCase'");
    let result = snake_case!("CamelCase");
    println!("  Output:     {}", result);
    println!("  Expected:   camel_case");
    println!("  Result:     ✓ PASS");
    println!();
}
```

**Ceremony with boxy + rolo:**
```bash
#!/usr/bin/env bash
# ceremony_test_summary.sh

echo "Collecting test results..." | boxy --theme info --title "📊 Test Suite"

# Generate results table
cat > /tmp/results.csv <<EOF
Module,Sanity,UAT,Status
strings,✓,✓,PASS
math,✓,✗,FAIL
colors,✓,✓,PASS
EOF

# Display formatted table
rolo table < /tmp/results.csv | boxy --theme success --title "✅ Test Results"

# Summary
echo -e "Total: 3 modules\nPassed: 2\nFailed: 1" | boxy --theme warning --title "📈 Summary"
```

---

## 4. Test Categories and Structure

### 4.1 Standard Categories (9)

1. **smoke** - Minimal CI tests (<10s total)
2. **sanity** - Core functionality (REQUIRED per module)
3. **unit** - Fast, isolated tests (<1s each)
4. **integration** - Cross-module interaction
5. **e2e** - End-to-end workflows
6. **uat** - User acceptance with visual output (REQUIRED per module)
7. **chaos** - Edge cases, stress tests
8. **bench** - Performance benchmarks
9. **regression** - Long-running historical suites

### 4.2 Ceremony Category (Optional)

**NOT enforced, NOT module-specific**

**Structure:**
- Directory: `tests/ceremonies/`
- Naming: `ceremony_<name>.sh` (shell preferred)
- Also supports: `.rs`, `.py` for special cases

**Purpose:**
- Integration workflows
- E2E scenarios with heavy formatting
- Automated demonstrations
- Result celebrations

**Examples:**
- `ceremony_error_handling.sh` - Error recovery workflow
- `ceremony_integration_flow.sh` - Multi-module integration
- `ceremony_performance.rs` - Benchmark visualization

**Discovery:**
```bash
testpy ceremony list            # List all ceremonies
testpy ceremony run <name>      # Run specific ceremony
testpy ceremony run all         # Run all ceremonies
```

---

## 5. Documentation Content Plan

### 5.1 RUST_TEST_ORGANIZATION.md

**Source:** RSB TEST_ORGANIZATION.md (363 lines)

**Adaptations:**
- Remove RSB-specific references
- Replace `test.sh` with `testpy`
- Generalize for any Rust project using RSB patterns
- Keep all structure/pattern definitions

**Content:**
1. Philosophy (Ceremony with Automation)
2. Directory Structure (9 categories)
3. Naming Patterns (`<category>_<module>.rs`)
4. Wrapper Pattern Requirements
5. Required Tests (sanity + UAT per module)
6. 6 Violation Types
7. Category Definitions
8. **NEW:** Ceremony Tests (optional section)

### 5.2 RUST_TESTING_HOWTO.md

**Source:** RSB HOWTO_TEST.md (766 lines)

**Adaptations:**
- Replace `./bin/test.sh` with `testpy`
- Replace RSB workflows with generic patterns
- Keep examples and best practices

**Content:**
1. Quick Start
2. Module-Based Testing System
3. Test Categories Explained
4. Writing Sanity Tests
5. Writing UAT Tests
6. Test Organization Compliance
7. **NEW:** Ceremony Tests (optional)
8. Common Patterns and Examples

### 5.3 RUST_TESTING_UX.md (NEW)

**Focus:** Visual UX for ALL tests (not just ceremonies)

**Content:**

1. **Visual Friendliness Principles**
   - Clear communication for visual thinkers
   - Progressive disclosure
   - Smart use of colors/glyphs
   - Whitespace for parsing

2. **UAT Visual Requirements**
   - Hypothesis → Expectation → Input → Output → Result
   - Numbered tests with titles
   - STATUS messages (PASS/FAIL/STUB/INVALID)
   - Simple formatting (doesn't require boxy)

3. **Test Output Structure**
   ```
   🧪 Module UAT
   ═══════════════════════

   Test 1: Feature Name
     Hypothesis: What we're testing
     Input:      Test data
     Expected:   What should happen
     Output:     Actual result
     Result:     ✓ PASS / ✗ FAIL

   Summary: 3/3 passed
   ```

4. **Glyphs and Colors**
   - STATUS: ✓ (pass), ✗ (fail), ⚠ (warning), ℹ (info)
   - Progress: numbers, arrows (→), bullets (•)
   - Categories: 🧪 (test), 📊 (summary), 🔧 (setup)

5. **Formatting Techniques**
   - Box drawing (═, ─, │)
   - Indentation for hierarchy
   - Blank lines for separation
   - Aligned columns for readability

6. **Summary Ceremonies**
   - End-of-suite summaries
   - Metrics display
   - Failed test details
   - Timing information

7. **Tool Integration**
   - When to use boxy (see RUST_BOXY_ROLO_USAGE.md)
   - When to use rolo (see RUST_BOXY_ROLO_USAGE.md)
   - Simple println is often sufficient

8. **Examples**
   - Simple UAT (println only)
   - Enhanced UAT (with formatting)
   - Ceremony (boxy + rolo)

### 5.4 RUST_BOXY_ROLO_USAGE.md (NEW)

**Focus:** Boxy and Rolo integration for enhanced visual tests

**Content:**

1. **Tool Overview**
   - Boxy v0.23.0: Box drawing and theming
   - Rolo v0.2: Tabular and structured layout
   - Version checks: `boxy --version`, `rolo --version`
   - API reference: `boxy --help`, `rolo --help`

2. **When to Use These Tools**
   - Ceremonies (complex workflows)
   - Result celebrations (summaries)
   - Integration tests with structured data
   - E2E scenarios with progressive disclosure
   - NOT required for simple UAT tests

3. **Boxy Basics**
   - Themes (success, error, warning, info)
   - Title/status/footer
   - Layout control
   - Icon decorations

4. **Boxy Advanced**
   - Param streams for complex layouts
   - Multi-section ceremonies
   - Progressive disclosure patterns
   - Custom themes for STATUS (purple for INVALID)

5. **Rolo Basics**
   - Table mode (CSV formatting)
   - Column mode (multi-column layout)
   - Pipeline integration

6. **Combined Patterns**
   - Table in box: `rolo table | boxy`
   - Multi-step ceremony with data
   - Test result summaries
   - Celebration patterns

7. **Ceremony Script Templates**
   - Basic ceremony structure
   - Multi-step workflow
   - Result celebration
   - Integration test pattern

8. **Real Examples**
   - From boxy: `~/repos/code/rust/prods/vizo/boxy/tests/ceremonies/`
   - Ceremony runner patterns
   - Batch organization (foundation, intermediate, advanced)

9. **Cross-Reference**
   - For UX principles: RUST_TESTING_UX.md
   - For ceremony structure: RUST_TEST_ORGANIZATION.md

---

## 6. testpy Implementation Plan

### 6.1 Documentation Commands

```bash
# Display docs
testpy docs rust-lint         # RUST_TEST_ORGANIZATION.md (alias: rust-org)
testpy docs rust-howto        # RUST_TESTING_HOWTO.md
testpy docs rust-ux           # RUST_TESTING_UX.md
testpy docs rust-boxy         # RUST_BOXY_ROLO_USAGE.md (alias: rust-tools)

# Sync to brain
testpy sync                   # → ~/repos/docs/brain/dev/procs/testing/rust/
```

### 6.2 Ceremony Commands

```bash
# List ceremonies
testpy ceremony               # Same as 'ceremony list'
testpy ceremony list          # List all ceremony_*.{sh,rs,py}

# Run ceremonies
testpy ceremony run <name>    # Run specific ceremony
testpy ceremony run all       # Run all ceremonies
```

### 6.3 Discovery Logic

```python
def discover_ceremonies(repo_root: Path) -> List[str]:
    """Discover ceremony tests from tests/ceremonies/."""
    ceremony_dir = repo_root / "tests" / "ceremonies"
    if not ceremony_dir.exists():
        return []

    ceremonies = []
    for ext in [".sh", ".rs", ".py"]:
        for file in ceremony_dir.glob(f"ceremony_*{ext}"):
            # Extract name: ceremony_<name>.sh → <name>
            name = file.stem.replace("ceremony_", "")
            ceremonies.append(name)

    return sorted(set(ceremonies))
```

### 6.4 Validator Updates

**NO enforcement for ceremonies:**
- Validator ignores `tests/ceremonies/` directory
- No required ceremony tests
- No violations if absent
- Pattern validation only if present (for consistency)

---

## 7. Milestone and Task Breakdown

### Milestone: M4 - Documentation & Testing UX (TBD story points)

**Story 1: Create Rust Documentation (13 points)**
- Task: Adapt TEST_ORGANIZATION.md → RUST_TEST_ORGANIZATION.md (5 pts)
- Task: Adapt HOWTO_TEST.md → RUST_TESTING_HOWTO.md (5 pts)
- Task: Create RUST_TESTING_UX.md from architecture docs (3 pts)

**Story 2: Create Tool Integration Docs (8 points)**
- Task: Document boxy usage patterns (3 pts)
- Task: Document rolo usage patterns (3 pts)
- Task: Create RUST_BOXY_ROLO_USAGE.md with examples (2 pts)

**Story 3: Implement docs Command (5 points)**
- Task: Add CLI subcommand for docs (2 pts)
- Task: Implement doc display with boxy theming (2 pts)
- Task: Add doc path resolution (1 pt)

**Story 4: Implement sync Command (5 points)**
- Task: Create brain sync function (2 pts)
- Task: Copy docs to ~/repos/docs/brain/dev/procs/testing/rust/ (2 pts)
- Task: Add sync status reporting (1 pt)

**Story 5: Ceremony Support (8 points)**
- Task: Implement ceremony discovery (2 pts)
- Task: Add ceremony CLI commands (list, run) (3 pts)
- Task: Integrate ceremony execution (shell/rust/python) (3 pts)

**Story 6: Testing and Documentation (5 points)**
- Task: Test on RSB project (2 pts)
- Task: Update testpy README with docs/ceremony features (2 pts)
- Task: Create usage examples (1 pt)

**Total: M4 - 44 story points**

---

## 8. Next Steps

1. ✅ Create TEST_UX_UPDATE.md (this document)
2. Update TASKS.txt with M4 milestone breakdown
3. Create RUST_TEST_ORGANIZATION.md (adapt from RSB)
4. Create RUST_TESTING_HOWTO.md (adapt from RSB)
5. Create RUST_TESTING_UX.md (extract from architecture docs)
6. Create RUST_BOXY_ROLO_USAGE.md (document tools)
7. Implement testpy docs command
8. Implement testpy sync command
9. Implement testpy ceremony commands
10. Test on RSB project
11. Update testpy README

---

## 9. Key Decisions and Rationale

**Decision 1: RUST_TESTING_UX.md instead of RUST_CEREMONY_UX.md**
- Rationale: UX principles apply to ALL tests, not just ceremonies
- Focus on visual communication, readability, human understanding
- Ceremonies are one application of these principles

**Decision 2: Ceremony tests are shell-first**
- Rationale: Easier to integrate with boxy/rolo via pipes
- No compilation needed for quick iterations
- Natural for multi-tool orchestration
- Rust compilation can be painful for shell-out scenarios

**Decision 3: Ceremonies are top-level, not module-specific**
- Rationale: Integration/workflow tests aren't tied to single modules
- Purpose-driven naming (what vs where)
- Flat structure for easy discovery

**Decision 4: UAT doesn't require boxy**
- Rationale: Simple formatting with println works fine
- Required tests should be easy to write
- Boxy/rolo are enhancements, not requirements

**Decision 5: Sync to brain/dev/procs/testing/ not brain/dev/proj/tests/**
- Rationale: These are universal testing protocols, not project-specific
- feat.py syncs project metadata to proj/
- testpy syncs universal testing guides to procs/

---

## 10. References

**RSB Documentation:**
- `/home/xnull/repos/code/rust/prods/oodx/rsb/docs/tech/development/TEST_ORGANIZATION.md`
- `/home/xnull/repos/code/rust/prods/oodx/rsb/docs/tech/development/HOWTO_TEST.md`
- `/home/xnull/repos/code/rust/prods/oodx/rsb/docs/tech/development/HOWTO_UPDATE_RSB.md`
- `/home/xnull/repos/code/rust/prods/oodx/rsb/docs/tech/reference/BASHFX-v3.md`
- `/home/xnull/repos/code/rust/prods/oodx/rsb/docs/tech/reference/RSB_ARCH.md`

**Tool Repositories:**
- Boxy: `/home/xnull/repos/code/rust/prods/vizo/boxy/` (v0.23.0)
- Rolo: `/home/xnull/repos/code/rust/prods/vizo/rolo/` (v0.2)

**Boxy Ceremonies:**
- `/home/xnull/repos/code/rust/prods/vizo/boxy/tests/ceremonies/`

---

**Document Status:** Complete - Ready for milestone breakdown in TASKS.txt
**Next Action:** Update TASKS.txt with M4 milestone and begin implementation
