# Rust Project Test Standardization Plan
**Created:** 2025-10-08
**Context:** Aligning all Rust projects with RSB test.sh paradigm, MODULE_SPEC, and feat.py

---

## Executive Summary

### Current State (Validated - Excluding Archives/Historical)
- **Total live projects:** 23 (excluded: bak/, _dev, _archive, ___ patterns)
- **Projects with test.sh:** 9 (39%)
- **Projects with feat.py:** 2 (9%)
- **Projects with MODULE_SPEC:** 7 (30%)
- **Projects with all three:** 2 (oodx-rsb, skull-cage)

### Reference Implementation
**oodx-rsb** serves as the canonical reference with:
- test.sh (1,561 lines)
- feat.py (comprehensive)
- MODULE_SPEC v3

---

## Key Findings

### 1. test.sh Analysis

#### RSB Version (~/repos/code/rust/prods/oodx/rsb/bin/test.sh)
- **Size:** 1,561 lines
- **Architecture:** Monolithic bash script
- **Key Features:**
  - Test category enforcement (sanity, smoke, unit, integration, e2e, uat, chaos, bench)
  - Strict test organization validation (`validate_test_structure`)
  - MODULE_SPEC aware module discovery
  - Boxy integration for pretty output
  - Timeout wrapper for cargo tests
  - Documentation integration
  - Override modes for emergency situations

#### BashFX Version (~/repos/code/shell/bashfx/fx-testsh/test.sh)
- **Size:** 1,583 lines (generated from 1,551 lines of parts)
- **Architecture:** BashFX v3 modular build system
- **Parts Structure:**
  - 16 modular parts files (01_header → 99_main)
  - build.sh assembles parts into final script
  - Only 32 lines of overhead from build process (2%)

**Key Modules (Actual Sizes):**
- `01_header.sh` - 10 lines
- `10_constants.sh` - 46 lines (configuration and flags)
- `20_bootstrap.sh` - 46 lines (environment setup)
- `30_boxy.sh` - 41 lines (output formatting)
- `40_execution.sh` - 142 lines (core test execution)
- `50_lanes.sh` - 375 lines (parallel test running)
- `60_docs.sh` - 135 lines (documentation)
- `70_org.sh` - 282 lines (test organization validation)
- `80_commands.sh` - 278 lines (CLI commands)
- `90_options.sh` - 65 lines (option parsing)
- `99_main.sh` - 23 lines (entry point)

### 2. Complexity Analysis: Shell vs Python

**Question:** Is test.sh too complex for shell?

**Findings:**
- Both versions are ~1,500 lines total
- BashFX modular approach adds minimal overhead (2%)
- Largest individual module is only 375 lines (lanes)
- Core logic in RSB is monolithic but manageable
- BashFX proves shell CAN be well-organized at this scale

**Recommendation - REVISED:**
- **Shell is viable** with proper modular architecture
- BashFX approach demonstrates clean separation of concerns
- Each module is digestible (largest = 375 lines)
- However, **Python still has advantages**:
  1. Better cross-platform support (Windows)
  2. Easier to test the tool itself
  3. Better data structures for complex validation
  4. Can leverage existing feat.py integration
  5. Lower barrier for contributors unfamiliar with shell

**Decision:** Either approach is technically sound. Choose based on:
- Team familiarity (shell vs Python)
- Deployment preferences (no deps vs pip install)
- Maintenance strategy (who owns it long-term)

---

## Project Inventory Matrix

```
Project              test.sh  feat.py  MODULE_SPEC  Priority  Notes
──────────────────────────────────────────────────────────────────────
oodx-rsb             YES      YES      YES          Reference  ✨
skull-cage           YES      YES      YES          Complete   ✨
──────────────────────────────────────────────────────────────────────
meteor-meteordb      YES      NO       YES          High
skull-ignite         YES      NO       YES          High
vizo-boxy            YES      NO       YES          High
pronto-prontodb      YES      NO       YES          High
──────────────────────────────────────────────────────────────────────
oodx-asc100          YES      NO       NO           Medium
oodx-xstream         YES      NO       NO           Medium
servo-kick           YES      NO       NO           Medium
skull-padlock        YES      NO       NO           Medium
vizo-rolo            YES      NO       NO           Medium
──────────────────────────────────────────────────────────────────────
oodx-meteor          NO       NO       YES          Medium
oodx-object          NO       NO       YES          Medium
──────────────────────────────────────────────────────────────────────
meteor-chunker       NO       NO       NO           Low
meteor-jsonm         NO       NO       NO           Low
oodx-forge           NO       NO       NO           Low
oodx-hub             NO       NO       NO           Low
oodx-lingo           NO       NO       NO           Low
oodx-syntax          NO       NO       NO           Low
oodx-toolbox         NO       NO       NO           Low
servo-nox            NO       NO       NO           Low
servo-porty          NO       NO       NO           Low
servo-sox            NO       NO       NO           Low
vizo-buddy           NO       NO       NO           Low
vizo-crayon          NO       NO       NO           Low
vizo-jynx            NO       NO       NO           Low
vizo-room            NO       NO       NO           Low
```

**Note:** Historical/archive projects excluded (bak/, _dev, _archive, ___ patterns)

---

## Recommended Solution Architecture

### Option A: Universal Python Test Runner (RECOMMENDED)

Create `testrs.py` (or `rsb-test`) as a universal test orchestrator:

```
~/repos/code/rust/_tools/testrs/
├── testrs.py              # Main CLI entry point
├── pyproject.toml         # Python project config
├── src/
│   └── testrs/
│       ├── __init__.py
│       ├── cli.py         # CLI interface
│       ├── config.py      # Configuration loading
│       ├── discovery.py   # Test/module discovery
│       ├── runner.py      # Test execution
│       ├── validator.py   # MODULE_SPEC validation
│       ├── reporter.py    # Test reporting
│       └── feat.py        # Integrate with feat.py
└── templates/
    ├── test_template.py
    └── MODULE_SPEC.md
```

**Benefits:**
1. Single source of truth for all Rust projects
2. Can be installed via pip/pipx
3. Extensible plugin architecture
4. Better error messages and debugging
5. Cross-platform (Windows support)
6. Can integrate with feat.py seamlessly
7. Easier to test the tester itself

### Option B: BashFX Modular Shell (Alternative)

Enhance fx-testsh with RSB-specific patterns:
- Keep modular architecture
- Add RSB/MODULE_SPEC awareness
- Create installable package
- Maintain shell simplicity

**Benefits:**
1. No Python dependency
2. Familiar to shell developers
3. Already modular
4. Can use existing BashFX patterns

**Drawbacks:**
1. Shell limitations (error handling, data structures)
2. Platform compatibility issues
3. Harder to test
4. 12K+ lines in org.sh is concerning

---

## Implementation Strategy

### Phase 1: Foundation (Week 1-2)
1. **Decision Point:** Python vs Enhanced Shell
   - Review both implementations with team
   - Consider project constraints (dependencies, team skills)
   - Make architectural decision

2. **Create Universal Tool Scaffold**
   - Set up project structure
   - Establish core interfaces
   - Define configuration schema

3. **Extract Common Patterns**
   - Analyze RSB test.sh for core logic
   - Document test organization rules
   - Define MODULE_SPEC requirements

### Phase 2: Core Implementation (Week 3-4)
1. **Test Discovery & Validation**
   - MODULE_SPEC parser
   - Test structure validator
   - Module discovery logic

2. **Test Runner**
   - Cargo test integration
   - Category-based execution
   - Parallel test support
   - Timeout handling

3. **Documentation Integration**
   - feat.py integration
   - Auto-doc generation
   - Test report generation

### Phase 3: Migration Tools (Week 5)
1. **Migration Script**
   - Detect existing test.sh
   - Generate project config
   - Validate MODULE_SPEC compliance

2. **Template Generation**
   - Generate test.sh wrapper
   - Create missing test stubs
   - Generate MODULE_SPEC if missing

### Phase 4: Rollout (Week 6-8)
1. **Pilot Projects** (2-3 projects)
   - High priority projects with test.sh but no feat.py
   - Validate tool functionality
   - Gather feedback

2. **Gradual Rollout**
   - Medium priority: Add feat.py + MODULE_SPEC
   - Low priority: Complete implementation
   - Legacy: Update to new standard

---

## Key Questions to Answer

### 1. Python vs Shell Decision (UPDATED WITH CORRECT DATA)
**Your Feedback Needed:**
- Team Python proficiency?
- Acceptable to add Python dependency?
- Performance concerns?
- Installation/distribution preferences?

**New Context:**
- BashFX proves shell IS viable at this scale (largest module = 375 lines)
- Modular approach keeps complexity manageable
- Shell = zero dependencies, familiar to devs
- Python = better testing, cross-platform, integration with feat.py

### 2. Module Spec Enforcement
**Your Feedback Needed:**
- Strict enforcement from day 1?
- Grace period for migration?
- Exclusion patterns needed?

### 3. feat.py Integration
**Current feat.py location:** `~/repos/code/python/snekfx/feat-py/feat.py`

**Options:**
1. Keep separate, integrate via CLI
2. Bundle into universal test tool
3. Rewrite in same language as test tool

### 4. Distribution Model
**Options:**
1. Central repo with symlinks to projects
2. Installable tool (pip/cargo install)
3. Copy-paste per project
4. Git submodule

---

## Immediate Next Steps

### 1. Review This Plan
- Validate findings
- Confirm priorities
- Make architectural decisions

### 2. Create Proof of Concept
- Build minimal Python version OR
- Enhance bashfx version with RSB patterns

### 3. Pilot on 1-2 Projects
- Test integration
- Validate patterns
- Iterate on design

---

## Standards to Enforce

### 1. Directory Structure (MODULE_SPEC v3)
```
<project>/
├── bin/
│   ├── test.sh          # Wrapper calling universal tool
│   └── feat.py          # Feature documentation
├── docs/
│   ├── proc/            # ROADMAP, TASKS
│   ├── ref/             # Concepts, patterns
│   │   └── rsb/
│   │       └── MODULE_SPEC.md
│   └── feats/           # FEATURES_<name>.md
├── src/
│   ├── lib.rs
│   ├── prelude.rs
│   ├── deps.rs
│   └── <pkg>/
│       └── <module>/    # Individual modules
└── tests/
    ├── sanity/          # Core validation
    ├── smoke/           # Minimal CI
    ├── unit/            # Isolated tests
    ├── integration/     # Cross-module
    ├── e2e/             # End-to-end
    ├── uat/             # User acceptance
    ├── chaos/           # Edge cases
    └── bench/           # Performance
```

### 2. Test Naming Conventions
- Test files: `<category>_<module>.rs`
- Test functions: `<category>_<module>_<description>()`
- Required: sanity + uat per module

### 3. Documentation Requirements
- MODULE_SPEC.md in docs/ref/rsb/
- feat.py for API surface documentation
- Auto-generated feature docs in docs/feats/

---

## Risk Assessment

### High Risk
- **Disruption to existing workflows** - Mitigate: gradual rollout
- **Tool complexity** - Mitigate: start simple, iterate
- **Adoption resistance** - Mitigate: pilot with volunteers

### Medium Risk
- **Maintenance burden** - Mitigate: automated tests for the tester
- **Configuration drift** - Mitigate: validation tools
- **Documentation lag** - Mitigate: automated doc generation

### Low Risk
- **Performance impact** - Modern tools are fast enough
- **Platform compatibility** - Python/Rust are cross-platform

---

## Success Metrics

1. **Coverage:** % of projects with complete tooling
2. **Compliance:** % of projects passing MODULE_SPEC validation
3. **Adoption:** # of projects actively using universal tool
4. **Quality:** Test failure detection rate
5. **Velocity:** Time to run full test suite

---

## Recommendations

### Immediate (This Week)
1. ✅ **Validate findings** (DONE - this document)
2. **Make Python vs Shell decision**
3. **Review MODULE_SPEC v3** for any needed updates
4. **Identify pilot projects** (recommend: meteor-meteordb, skull-ignite)

### Short Term (Next 2 Weeks)
1. **Build POC** of chosen architecture
2. **Test on pilot project**
3. **Iterate based on feedback**
4. **Document usage patterns**

### Long Term (Next 2 Months)
1. **Roll out to high-priority projects** (4 projects)
2. **Roll out to medium-priority projects** (8 projects)
3. **Create migration guide for low-priority**
4. **Establish maintenance process**

---

## Open Questions for Discussion

1. **Should test.sh be Python-based or stay in shell?**
   - Consider: maintenance, portability, team skills

2. **Where should the universal tool live?**
   - Option A: `~/repos/code/rust/_tools/testrs/`
   - Option B: `~/repos/code/python/snekfx/testrs/`
   - Option C: Separate dedicated repo

3. **How strict should MODULE_SPEC enforcement be?**
   - Blocking vs warning
   - Grace period for legacy projects

4. **Should feat.py be integrated or remain separate?**
   - Pros of integration: single tool
   - Cons: increased complexity

5. **Installation mechanism preference?**
   - pip install (Python)
   - cargo install (Rust)
   - Shell script installer
   - Manual symlinks

---

**Status:** AWAITING REVIEW AND ARCHITECTURAL DECISIONS

**Next Action:** User feedback on Python vs Shell and pilot project selection
