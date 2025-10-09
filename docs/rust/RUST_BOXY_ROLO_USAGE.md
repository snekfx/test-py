# Rust Testing: Boxy & Rolo Usage Guide

**Version**: 1.0
**Updated**: 2025-10-09
**Status**: Optional Enhancement Tools

## Overview

This guide describes **boxy** and **rolo** - optional command-line tools for enhanced visual ceremony in Rust testing. These tools are **NOT REQUIRED** for standard testing but provide professional visual output for ceremony tests and demonstrations.

**Important**: Simple println!() following visual UX principles (see `testpy docs rust-ux`) is sufficient for most testing needs. Use these tools only for:
- Ceremony tests (`tests/ceremonies/`)
- Complex demonstrations
- Production showcases
- Visual emphasis requirements

## Tool Versions

- **boxy**: v0.23.0+ (Visual box drawing and theming)
- **rolo**: v0.2+ (Table formatting - docs being cleaned up)

## When to Use These Tools

### Use Boxy/Rolo For:
- Ceremony tests in `tests/ceremonies/`
- Visual demonstrations for stakeholders
- Complex multi-step workflows
- Test suite summaries
- CI/CD visual reports

### Do NOT Use For:
- Regular UAT tests (use println! instead)
- Sanity tests
- Unit tests
- Integration tests
- Tests that need frequent updates

**Reason**: Boxy/rolo add complexity. Keep standard tests simple and maintainable.

## Boxy Basics

### What is Boxy?

Boxy is a command-line tool that creates visual boxes with theming support. It wraps text content in formatted boxes with titles, borders, and color themes.

### Installation

```bash
# Install via cargo
cargo install boxy

# Or via your project's hub (if available)
# boxy is typically available through Rust package managers
```

### Basic Usage

```bash
# Simple box
echo "Hello, World!" | boxy

# With title
echo "Content here" | boxy --title "My Title"

# With theme
echo "Success message" | boxy --theme success

# Custom width
echo "Content" | boxy --width 80

# Border styles
echo "Content" | boxy --style rounded
echo "Content" | boxy --style thick
echo "Content" | boxy --style ascii
```

### Available Themes

| Theme | Purpose | Color Scheme |
|-------|---------|--------------|
| `info` | Informational | Blue/Cyan |
| `success` | Success messages | Green |
| `warning` | Warnings | Yellow/Orange |
| `error` | Errors | Red |
| `magic` | Special/Highlight | Purple/Magenta |
| `plain` | No color | Default terminal |

### Boxy Examples

#### Example 1: Simple Information Box

```bash
echo "This is important information." | boxy --theme info --title "Notice"
```

Output:
```
┌─[ Notice ]──────────────────────┐
│ This is important information. │
└─────────────────────────────────┘
```

#### Example 2: Success Message

```bash
echo "All tests passed successfully!" | boxy --theme success --title "✓ Test Results"
```

#### Example 3: Multi-line Content

```bash
cat << 'EOF' | boxy --theme info --title "Test Summary"
Total Tests: 10
Passed: 10
Failed: 0
Duration: 2.3s
EOF
```

### Boxy in Shell Scripts

```bash
#!/usr/bin/env bash
# Simple ceremony using boxy

# Header
echo "Test Suite: Module Name" | boxy --theme magic --title "🎭 Test Ceremony"

# Test execution
echo "Running tests..." | boxy --theme info

# Results
cat << 'EOF' | boxy --theme success --title "✅ Results"
Tests Run: 5
All Passed: ✓
Duration: 1.2s
EOF
```

### Nested Boxy Pattern

For complex layouts, nest boxy calls:

```bash
# Inner box
inner=$(echo "Inner content" | boxy --theme info --style ascii --width 60)

# Outer box
echo "$inner" | boxy --theme magic --style rounded --width max --title "Ceremony"
```

## Boxy Advanced

### Progressive Disclosure

Build output incrementally:

```bash
#!/usr/bin/env bash

ceremony_content=""

# Section 1
section1=$(cat << 'EOF' | boxy --theme info --style ascii --width 70
Test 1: Basic Functionality
Status: ✓ PASS
Duration: 0.1s
EOF
)
ceremony_content+="$section1"$'\n\n'

# Section 2
section2=$(cat << 'EOF' | boxy --theme success --style ascii --width 70
Test 2: Edge Cases
Status: ✓ PASS
Duration: 0.2s
EOF
)
ceremony_content+="$section2"$'\n\n'

# Final container
echo "$ceremony_content" | boxy --style rounded --width max --title "Test Ceremony"
```

### Parameter Streams

Pass multiple parameters:

```bash
# Using heredoc with parameters
cat << EOF | boxy --theme info --title "Configuration"
Project: $(basename $PWD)
Tests: $test_count
Duration: ${duration}s
EOF
```

### Conditional Theming

Choose theme based on results:

```bash
if [[ $failures -eq 0 ]]; then
    theme="success"
    title="✓ All Tests Passed"
else
    theme="error"
    title="✗ ${failures} Test(s) Failed"
fi

echo "$summary" | boxy --theme $theme --title "$title"
```

## Rolo Basics

### What is Rolo?

**Note**: Rolo v0.2 documentation is being cleaned up. Use with caution for new projects.

Rolo is a table formatting tool for command-line output. It formats data in columns or rows with alignment and styling.

### Installation

```bash
# Install via cargo (when available)
cargo install rolo

# Or check project's hub
```

### Basic Usage

```bash
# Simple table from TSV
echo -e "Name\tStatus\tTime\nTest1\tPASS\t0.1s\nTest2\tPASS\t0.2s" | rolo

# Column mode
echo -e "Col1\nCol2\nCol3" | rolo --mode column

# Custom delimiter
cat data.csv | rolo --delimiter ","
```

### Rolo Example

```bash
#!/usr/bin/env bash

# Build test results table
cat << 'EOF' | rolo --mode table
Test Name	Status	Duration
sanity_math	PASS	0.15s
sanity_tokens	PASS	0.23s
sanity_strings	PASS	0.11s
uat_math	PASS	1.20s
uat_tokens	PASS	0.95s
EOF
```

Output:
```
Test Name        Status    Duration
─────────────────────────────────────
sanity_math      PASS      0.15s
sanity_tokens    PASS      0.23s
sanity_strings   PASS      0.11s
uat_math         PASS      1.20s
uat_tokens       PASS      0.95s
```

## Combined Patterns

### Table in Box

Combine rolo and boxy for formatted tables in boxes:

```bash
# Generate table
table=$(cat << 'EOF' | rolo --mode table
Module	Sanity	UAT	Status
math	✓	✓	Complete
tokens	✓	✓	Complete
strings	✓	✗	Missing UAT
EOF
)

# Wrap in box
echo "$table" | boxy --theme info --title "Test Coverage"
```

### Multi-Step Ceremony

```bash
#!/usr/bin/env bash

# Step 1: Discovery
discovery=$(cat << 'EOF' | boxy --theme info --title "Step 1: Discovery"
Discovering test modules...
Found: 5 modules
EOF
)

# Step 2: Execution
execution=$(cat << 'EOF' | boxy --theme info --title "Step 2: Execution"
Running tests...
Progress: 5/5 complete
EOF
)

# Step 3: Results
results=$(cat << 'EOF' | rolo --mode table
Module	Tests	Passed	Failed
math	5	5	0
tokens	3	3	0
strings	4	4	0
EOF
)

results_box=$(echo "$results" | boxy --theme success --title "Step 3: Results")

# Complete ceremony
cat << EOF | boxy --style thick --width max --title "🎭 Test Ceremony"

$discovery

$execution

$results_box

EOF
```

## Ceremony Script Templates

### Template 1: Simple Test Ceremony

```bash
#!/usr/bin/env bash
# tests/ceremonies/ceremony_simple.sh

set -euo pipefail

# Configuration
TITLE="Module Test Ceremony"
CATEGORY="sanity"
MODULE="math"

# Header
echo "Running $CATEGORY tests for $MODULE module" | \
    boxy --theme magic --title "🎭 $TITLE"

# Run tests
output=$(cargo test --test "${CATEGORY}_${MODULE}" 2>&1 || true)

# Determine result
if echo "$output" | grep -q "test result: ok"; then
    theme="success"
    status="✓ PASSED"
else
    theme="error"
    status="✗ FAILED"
fi

# Display results
echo "$output" | boxy --theme "$theme" --title "$status"
```

### Template 2: Multi-Module Ceremony

```bash
#!/usr/bin/env bash
# tests/ceremonies/ceremony_multi.sh

set -euo pipefail

modules=("math" "tokens" "strings")
results=()

# Header
echo "Multi-Module Test Ceremony" | boxy --theme magic --title "🎭 Ceremony"

# Test each module
for module in "${modules[@]}"; do
    echo "Testing $module..." | boxy --theme info

    if cargo test --test "sanity_$module" >/dev/null 2>&1; then
        results+=("$module\t✓ PASS")
    else
        results+=("$module\t✗ FAIL")
    fi
done

# Summary table
printf "Module\tStatus\n" > /tmp/results.tsv
printf "%s\n" "${results[@]}" >> /tmp/results.tsv

cat /tmp/results.tsv | rolo --mode table | \
    boxy --theme success --title "📊 Results"

rm /tmp/results.tsv
```

### Template 3: UAT Showcase

```bash
#!/usr/bin/env bash
# tests/ceremonies/ceremony_uat_showcase.sh

set -euo pipefail

MODULE="$1"
: "${MODULE:?Usage: $0 <module>}"

# Title
echo "UAT Showcase for $MODULE" | \
    boxy --theme magic --title "🎭 User Acceptance Testing"

# Run UAT with output
output=$(cargo test --test "uat_$MODULE" -- --nocapture 2>&1 || true)

# Parse and display
if echo "$output" | grep -q "test result: ok"; then
    # Extract test output
    test_output=$(echo "$output" | sed -n '/running.*test/,/test result:/p')

    echo "$test_output" | boxy --theme success --title "✓ $MODULE UAT Results"
else
    echo "$output" | boxy --theme error --title "✗ UAT Failed"
fi
```

## Integration with testpy

### Future testpy Ceremony Support

testpy may add ceremony command support in the future:

```bash
# Future syntax (not yet implemented)
testpy ceremony list          # List available ceremonies
testpy ceremony <name>        # Run specific ceremony
testpy ceremony welcome       # Run welcome ceremony
```

### Current Approach

For now, run ceremony scripts directly:

```bash
# Make ceremony executable
chmod +x tests/ceremonies/ceremony_simple.sh

# Run it
./tests/ceremonies/ceremony_simple.sh

# Or via bash
bash tests/ceremonies/ceremony_simple.sh math
```

## Best Practices

### Do's

✓ **DO** use for ceremonies only, not regular tests
✓ **DO** provide fallback when tools unavailable
✓ **DO** keep ceremony scripts maintainable
✓ **DO** document ceremony purpose
✓ **DO** use appropriate themes
✓ **DO** test ceremony scripts regularly

### Don'ts

✗ **DON'T** use in standard UAT tests
✗ **DON'T** make ceremonies required for CI
✗ **DON'T** over-engineer simple tests
✗ **DON'T** forget graceful degradation
✗ **DON'T** assume tools are installed

## Fallback Pattern

Always provide fallback when tools unavailable:

```bash
#!/usr/bin/env bash

# Check for boxy
if command -v boxy >/dev/null 2>&1; then
    # Use boxy
    echo "$content" | boxy --theme success --title "$title"
else
    # Fallback to simple output
    echo "=== $title ==="
    echo "$content"
    echo "==============="
fi
```

## Tool API Reference

### Boxy Command Reference

```bash
boxy [OPTIONS]

Options:
  --title <TITLE>         Set box title
  --theme <THEME>         Set color theme (info, success, warning, error, magic, plain)
  --style <STYLE>         Set border style (rounded, thick, thin, ascii, double)
  --width <WIDTH>         Set box width (number or 'max')
  --padding <PADDING>     Set internal padding (default: 1)
  --align <ALIGN>         Text alignment (left, center, right)
  --help                  Show help message
```

### Rolo Command Reference

**Note**: Rolo v0.2 API is being updated. Check documentation for current options.

```bash
rolo [OPTIONS]

Options:
  --mode <MODE>           Display mode (table, column, row)
  --delimiter <DELIM>     Field delimiter (default: tab)
  --header                First line is header
  --align <ALIGN>         Column alignment
  --help                  Show help message
```

## Real-World Examples

See these projects for ceremony examples:
- **boxy upstream**: Example ceremonies in boxy's own test suite
- **RSB**: `tests/ceremonies/` directory (if available)

## Related Documentation

- **Visual UX Guide**: `testpy docs rust-ux` - Core visual principles (use this first!)
- **Test Organization**: `testpy docs rust-org` - Test structure standard
- **Testing HOWTO**: `testpy docs rust-howto` - Complete testing guide

---

**Remember**: These tools are **optional enhancements**. Start with simple println!() following visual UX principles. Add boxy/rolo only when you need professional ceremony output for demonstrations or complex reporting.
