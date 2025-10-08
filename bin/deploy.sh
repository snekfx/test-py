#!/bin/bash
set -e

# Configuration
TARGET_BIN_DIR="$HOME/.local/bin"

# Resolve repository root from bin/
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Extract version from pyproject.toml or default
VERSION=$(grep -E "^version\s*=" "$ROOT_DIR/pyproject.toml" | head -1 | cut -d'"' -f2 2>/dev/null || echo "0.1.0-dev")

# Display deployment ceremony
echo "╔════════════════════════════════════════════════╗"
echo "║              TESTRS DEPLOYMENT                 ║"
echo "╠════════════════════════════════════════════════╣"
echo "║ Package: RSB Test Orchestrator                 ║"
echo "║ Version: v$VERSION                             ║"
echo "║ Target:  $TARGET_BIN_DIR/                      ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Deploy testrs tool
echo "🧪 Deploying testrs tool..."
mkdir -p "$TARGET_BIN_DIR"

# TODO: Replace with actual main script path once created
# TESTRS_SOURCE="$ROOT_DIR/src/testrs/main.py"
# TESTRS_TARGET="$TARGET_BIN_DIR/testrs"

# For now, create a placeholder
TESTRS_TARGET="$TARGET_BIN_DIR/testrs"

cat > "$TESTRS_TARGET" <<'EOF'
#!/usr/bin/env python3
"""
RSB Test Orchestrator
"""
import sys

def main():
    print("testrs v0.1.0 - RSB Test Orchestrator")
    print("Implementation pending")
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF

if ! chmod +x "$TESTRS_TARGET"; then
    echo "❌ Failed to make testrs executable"
    exit 1
fi

echo "✅ testrs tool deployed to $TESTRS_TARGET"

# Test the deployment
echo "🧪 Testing testrs deployment..."
if command -v testrs >/dev/null 2>&1; then
    echo "✅ testrs is available in PATH"
else
    echo "⚠️  Warning: testrs not found in PATH (may need to restart shell)"
fi

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║          DEPLOYMENT SUCCESSFUL!                ║"
echo "╚════════════════════════════════════════════════╝"
echo "  Deployed: testrs v$VERSION                     "
echo "  Location: $TESTRS_TARGET                       "
echo ""
echo "🧪 testrs test orchestration commands:"
echo "   testrs run                  # Run test suite"
echo "   testrs --help               # Full command reference"
echo ""
echo "🚀 Ready to orchestrate your RSB test workflows!"
