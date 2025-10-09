# Rust Testing: Visual UX Guide

**Version**: 1.0
**Updated**: 2025-10-09
**Status**: Universal Visual Testing Standard

## Overview

This guide describes **visual friendliness principles** for Rust testing, derived from BashFX v3 architecture. These principles transform tests from simple pass/fail assertions into clear, communicative demonstrations of functionality.

**Core Principle**: Tests should be **proactively communicative** about state, progression, and results.

## Visual Friendliness Principles

### Ceremony With Automation

**Ceremony** provides clear visual demarkation of:
- Important state progression
- Critical warnings and errors
- Helpful visual patterns guiding users through execution

**Ceremony Elements**:
- ASCII banners and headers
- Structured data presentation
- Boxes and visual containers
- Clearly numbered and labeled steps
- Visual summaries with metrics
- Colors and glyphs (✓, ✗, ⚠, ℹ)
- Occasional emojis for state communication

**Balance**: Ceremony enhances communication without overwhelming simple tests.

## UAT Visual Requirements

**User Acceptance Tests (UAT)** must provide visual demonstrations following these patterns:

### Required Structure

```
1. Test Title/Header
2. Test Number (for multiple demonstrations)
3. Hypothesis/Description
4. Expected Behavior
5. Execution Indicator
6. Actual Output
7. STATUS Indicator (PASS/FAIL/SKIP/STUB)
8. Spacing Between Tests
9. Summary/Completion Message
```

### Simple UAT Pattern

```rust
#[test]
fn uat_module_demonstration() {
    println!("Module Name UAT");
    println!("================\n");

    // UAT 1: First demonstration
    println!("UAT 1: Basic Functionality");
    println!("  Hypothesis: Function performs expected operation");
    println!("  Expected: Successful result with valid output");
    println!("  Running...");

    let result = your_function();

    println!("  Actual: {:?}", result);
    assert!(result.is_ok());
    println!("  ✓ PASS\n");

    // UAT 2: Second demonstration
    println!("UAT 2: Edge Case Handling");
    println!("  Hypothesis: Function handles edge cases gracefully");
    println!("  Expected: No panic, error handled properly");
    println!("  Running...");

    let result = your_function_edge_case();

    println!("  Actual: {:?}", result);
    println!("  ✓ PASS\n");

    println!("=== UAT Complete ===");
}
```

## Test Output Structure

### Numbered Tests

Each test in a suite should be clearly numbered:

```
UAT 1: Basic Functionality
UAT 2: Edge Cases
UAT 3: Error Handling
```

**Benefits**:
- Easy to reference specific tests
- Clear progression through suite
- Enables test counting in summaries

### Titled Tests

Each test needs a clear, descriptive title:

```
UAT 1: Parameter Expansion with Defaults
UAT 2: Nested Property Access
UAT 3: Environment Variable Substitution
```

**Good Titles**:
- Describe what is being tested
- Use domain language
- Are concise (< 50 characters)

**Bad Titles**:
- "Test 1", "Test 2" (not descriptive)
- "This test checks if the function works when..." (too verbose)

### STATUS Messages

Use clear, visual STATUS indicators:

| Status | Glyph | Meaning | Color |
|--------|-------|---------|-------|
| **PASS** | ✓ | Test passed successfully | Green |
| **FAIL** | ✗ | Test failed | Red |
| **SKIP** | ⚠ | Test skipped (conditional) | Yellow |
| **STUB** | ℹ | Test not yet implemented | Blue |
| **INVALID** | ⊘ | Test cannot run (env issue) | Purple |

**Example Usage**:
```rust
println!("  ✓ PASS");       // Success
println!("  ✗ FAIL");       // Failure
println!("  ⚠ SKIP");       // Skipped
println!("  ℹ STUB");       // Not implemented
println!("  ⊘ INVALID");    // Environment issue
```

## Glyphs and Symbols

### Standard Glyphs

Recommended glyphs for visual communication:

| Glyph | Meaning | Usage |
|-------|---------|-------|
| ✓ | Check/Pass | Successful test |
| ✗ | X/Fail | Failed test |
| ⚠ | Warning/Delta | Warning or skipped |
| ℹ | Info | Information or stub |
| ⊘ | Invalid/Null | Cannot execute |
| → | Arrow/Next | Progression |
| • | Bullet | List item |
| ─ | Line | Separator |
| │ | Vertical | Box border |
| ┌ ┐ └ ┘ | Corners | Box drawing |

### Emoji Usage (Optional)

Emojis can enhance communication when used sparingly:

| Emoji | Meaning | Usage |
|-------|---------|-------|
| 🎭 | Ceremony | Test ceremony header |
| 📁 | Folder | Test category |
| 🔄 | Running | Test in progress |
| ✅ | Success | Category passed |
| ❌ | Failure | Category failed |
| 📊 | Results | Summary section |
| ⚡ | Fast | Quick test category |
| 🎯 | Target | Specific test focus |

**Note**: Simple ASCII glyphs (✓, ✗) are generally preferred over emojis for better terminal compatibility.

## Formatting Techniques

### Box Drawing

Use box drawing for visual containers:

```
┌─────────────────────────────────┐
│ Test Suite: Module Name         │
├─────────────────────────────────┤
│ Status: Running                 │
│ Tests: 5                        │
└─────────────────────────────────┘
```

**Simple Approach**: Use equals and dashes:
```
=====================================
 Test Suite: Module Name
=====================================
```

### Indentation

Use consistent indentation for hierarchy:

```
Test Category: Sanity
  Test 1: Basic Functionality
    Expected: Success
    Actual: Success
    ✓ PASS

  Test 2: Edge Cases
    Expected: Graceful handling
    Actual: Error handled properly
    ✓ PASS
```

### Spacing

Use blank lines to separate logical sections:

```rust
println!("UAT 1: First Test");
println!("  Running...");
println!("  ✓ PASS\n");          // Blank line after test

println!("UAT 2: Second Test");   // Start next test
println!("  Running...");
println!("  ✓ PASS\n");

println!("=== Complete ===");     // Final summary
```

## Summary Ceremonies

End test suites with visual summaries containing:

1. **Test Metrics**: Total, passed, failed, skipped
2. **Timing Information**: Duration of test run
3. **Failed Test List**: Which tests failed (if any)
4. **Environment Notes**: Any invalid/skipped tests with reasons

### Simple Summary Pattern

```rust
println!("\n=== Test Summary ===");
println!("Total Tests: {}", total);
println!("Passed: {} ✓", passed);
println!("Failed: {} ✗", failed);
println!("Skipped: {} ⚠", skipped);
println!("Success Rate: {:.1}%", (passed as f64 / total as f64) * 100.0);
```

### Detailed Summary Pattern

```rust
println!("\n╔═══════════════════════════════════╗");
println!("║     Test Suite Results            ║");
println!("╠═══════════════════════════════════╣");
println!("║ Category: Sanity                  ║");
println!("║ Duration: 2.3s                    ║");
println!("║                                   ║");
println!("║ Tests Run: 10                     ║");
println!("║ Passed: 9 ✓                       ║");
println!("║ Failed: 1 ✗                       ║");
println!("║ Success Rate: 90.0%               ║");
println!("╚═══════════════════════════════════╝");

if !failed_tests.is_empty() {
    println!("\nFailed Tests:");
    for test in failed_tests {
        println!("  ✗ {}", test);
    }
}
```

## Tool Integration

### When to Use Enhanced Tools

**Simple println!() is sufficient for**:
- Basic UAT demonstrations
- Standard test output
- Development testing
- Small projects

**Use enhanced tools (boxy/rolo) for**:
- Ceremony tests (optional)
- Complex test suites
- Production demonstrations
- Visual emphasis needs

### Tool Reference

For enhanced visual output using boxy and rolo:

```bash
# See tool-specific documentation
testpy docs rust-boxy
```

**Note**: Enhanced tools are **optional**. Simple println!() with proper structure is perfectly acceptable and often preferred for maintainability.

## Example UAT Patterns

### Example 1: Simple Demonstration

```rust
#[test]
fn uat_string_case_conversion() {
    println!("String Case Conversion UAT\n");

    println!("UAT 1: Snake Case Conversion");
    println!("  Command: to_snake_case(\"HelloWorld\")");
    println!("  Expected: \"hello_world\"");

    let result = to_snake_case("HelloWorld");

    println!("  Actual: \"{}\"", result);
    assert_eq!(result, "hello_world");
    println!("  ✓ PASS\n");

    println!("UAT 2: Kebab Case Conversion");
    println!("  Command: to_kebab_case(\"HelloWorld\")");
    println!("  Expected: \"hello-world\"");

    let result = to_kebab_case("HelloWorld");

    println!("  Actual: \"{}\"", result);
    assert_eq!(result, "hello-world");
    println!("  ✓ PASS\n");

    println!("=== UAT Complete ===");
}
```

### Example 2: Multiple Variations

```rust
#[test]
fn uat_color_variations() {
    println!("Color Module UAT\n");

    let colors = vec![
        ("red_text!(\"Error\")", "Red colored text"),
        ("green_text!(\"Success\")", "Green colored text"),
        ("blue_text!(\"Info\")", "Blue colored text"),
        ("yellow_text!(\"Warning\")", "Yellow colored text"),
    ];

    for (i, (command, description)) in colors.iter().enumerate() {
        println!("UAT {}: {}", i + 1, description);
        println!("  Command: {}", command);
        println!("  Expected: Colored ANSI output");
        println!("  Running...");

        let result = match i {
            0 => red_text!("Error"),
            1 => green_text!("Success"),
            2 => blue_text!("Info"),
            3 => yellow_text!("Warning"),
            _ => unreachable!(),
        };

        println!("  Output: {}", result);
        assert!(result.contains("\x1b["));
        println!("  ✓ PASS\n");
    }

    println!("=== All Variations Tested ===");
}
```

### Example 3: Error Handling

```rust
#[test]
fn uat_error_handling() {
    println!("Error Handling UAT\n");

    println!("UAT 1: Invalid Input Handling");
    println!("  Hypothesis: Function rejects invalid input");
    println!("  Expected: Error result, no panic");
    println!("  Running...");

    let result = parse_config("invalid_data");

    println!("  Actual: {:?}", result);
    assert!(result.is_err());
    println!("  ✓ PASS - Error handled gracefully\n");

    println!("UAT 2: Graceful Recovery");
    println!("  Hypothesis: Function provides default on error");
    println!("  Expected: Default value returned");
    println!("  Running...");

    let result = parse_config_or_default("invalid_data");

    println!("  Actual: {:?}", result);
    assert!(result.is_ok());
    println!("  ✓ PASS - Default provided\n");

    println!("=== Error Handling Validated ===");
}
```

### Example 4: Visual Output Demonstration

```rust
#[test]
fn uat_visual_output() {
    println!("Visual Output UAT\n");

    println!("UAT 1: Color Demonstration");
    println!("  The following line should be red:");
    println!("  {}", red_text!("This is an error message"));
    println!("  ✓ PASS (Visual verification)\n");

    println!("UAT 2: Multiple Color Combination");
    println!("  Status indicators:");
    println!("  {} Success message", green_text!("✓"));
    println!("  {} Error message", red_text!("✗"));
    println!("  {} Warning message", yellow_text!("⚠"));
    println!("  ✓ PASS (Visual verification)\n");

    println!("UAT 3: Box Drawing");
    println!("  ┌─────────────────────┐");
    println!("  │ Boxed Content       │");
    println!("  └─────────────────────┘");
    println!("  ✓ PASS (Visual verification)\n");

    println!("=== Visual Output Demonstrated ===");
}
```

## Best Practices

### Do's

✓ **DO** use clear test numbering
✓ **DO** provide hypothesis and expected behavior
✓ **DO** show actual output
✓ **DO** use STATUS glyphs (✓ ✗ ⚠)
✓ **DO** separate tests with blank lines
✓ **DO** provide summary ceremonies
✓ **DO** keep output clean and readable
✓ **DO** use consistent formatting
✓ **DO** make tests self-documenting

### Don'ts

✗ **DON'T** use println!() without structure
✗ **DON'T** skip test numbering in suites
✗ **DON'T** forget STATUS indicators
✗ **DON'T** clutter output with debug info
✗ **DON'T** use inconsistent formatting
✗ **DON'T** skip summaries
✗ **DON'T** assume readers know context
✗ **DON'T** make tests hard to read

## Running Visual Tests

```bash
# Run with output visible (cargo)
cargo test --test uat_module -- --nocapture

# Run via testpy (if implemented)
testpy uat module

# Run all UAT tests
testpy uat
```

## Key Principles Summary

1. **Proactive Communication**: Tests should clearly communicate state and progression
2. **Visual Structure**: Use numbering, titles, indentation, spacing
3. **STATUS Indicators**: Always show pass/fail/skip clearly
4. **Hypothesis → Expected → Actual**: Show the testing thought process
5. **Summaries**: Provide metrics and status at test suite end
6. **Simplicity First**: Start simple (println!), enhance only when needed
7. **Consistency**: Use consistent patterns across all tests
8. **Self-Documentation**: Tests should be readable as documentation

## Related Documentation

- **Test Organization**: `testpy docs rust-org` - Test structure standard
- **Testing HOWTO**: `testpy docs rust-howto` - Complete testing guide
- **Boxy/Rolo Usage**: `testpy docs rust-boxy` - Enhanced visual tools (optional)
- **Quick Checklist**: `testpy checklist` - Setup guide

---

**Remember**: Visual friendliness is about **clear communication**, not fancy graphics. Simple, well-structured println!() output following these patterns is often the best approach.
