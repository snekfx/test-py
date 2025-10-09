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
echo "║              TESTPY DEPLOYMENT                 ║"
echo "╠════════════════════════════════════════════════╣"
echo "║ Package: RSB Test Orchestrator                 ║"
echo "║ Version: v$VERSION                             ║"
echo "║ Method:  pip install -e                        ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Deploy testpy via pip
echo "🧪 Deploying testpy tool..."

# Check if already installed
if pip show testpy >/dev/null 2>&1; then
    echo "⚠️  testpy is already installed, uninstalling..."
    pip uninstall -y testpy
fi

# Install in editable mode
echo "📦 Installing testpy in editable mode..."
if ! pip install -e "$ROOT_DIR"; then
    echo "❌ Failed to install testpy"
    exit 1
fi

echo "✅ testpy installed successfully"

# Test the deployment
echo "🧪 Testing testpy deployment..."
if command -v testpy >/dev/null 2>&1; then
    echo "✅ testpy is available in PATH"
    testpy --version
else
    echo "⚠️  Warning: testpy not found in PATH (may need to restart shell)"
fi

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║          DEPLOYMENT SUCCESSFUL!                ║"
echo "╚════════════════════════════════════════════════╝"
echo "  Deployed: testpy v$VERSION                     "
echo "  Method:   pip install -e (editable)            "
echo ""
echo "🧪 testpy test orchestration commands:"
echo "   testpy check                # Check configuration"
echo "   testpy lint                 # Validate test organization"
echo "   testpy run                  # Run test suite"
echo "   testpy --help               # Full command reference"
echo ""
echo "🚀 Ready to orchestrate your RSB test workflows!"
