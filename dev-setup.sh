#!/bin/bash
# Quick development setup for Versade

set -e

echo "🔧 Versade Development Setup"
echo "============================"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Are you in the Versade project directory?"
    exit 1
fi

# Check for uv
if command -v uv >/dev/null 2>&1; then
    echo "✅ Found uv"
    echo "📦 Installing dependencies..."
    uv sync
    
    echo ""
    echo "🎉 Development setup complete!"
    echo ""
    echo "🎯 Quick start:"
    echo "  uv run versade --help           # Show help"
    echo "  uv run versade check requests   # Check packages"
    echo "  uv run versade serve            # Start API server"
    echo "  uv run versade mcp              # Start MCP server"
    echo "  uv run versade setup            # Interactive setup"
    echo ""
    echo "🧪 Test installation:"
    echo "  uv run versade --version"
    echo ""
    
    # Test the installation
    echo "🧪 Testing installation..."
    if uv run versade --version >/dev/null 2>&1; then
        echo "✅ Installation test passed!"
    else
        echo "❌ Installation test failed"
        exit 1
    fi
    
else
    echo "❌ uv not found. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   # or"
    echo "   pip install uv"
    exit 1
fi 