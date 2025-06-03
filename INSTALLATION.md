# Versade Installation Guide

This guide covers all installation methods for Versade, from quick development setup to production deployment.

## Quick Start (Recommended)

### 1. Development Setup (Fastest)
```bash
# Clone the repository
git clone https://github.com/versade/versade
cd versade

# Quick setup with script
./dev-setup.sh

# Test installation
uv run versade --help
uv run versade check requests
```

### 2. Automated Installation
```bash
# Use the installation script
python install.py

# Follow the interactive prompts to choose:
# 1. uvx - Global install (PyPI only)
# 2. pipx - Global install 
# 3. pip - System/venv install
# 4. Development - Local setup (recommended)
# 5. Auto-detect - Best method
```

## Detailed Installation Methods

### Method 1: Development (uv) - Recommended for Local Use

**Prerequisites**: Python 3.8+ and uv

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv

# Clone and setup
git clone https://github.com/versade/versade
cd versade
uv sync

# Usage
uv run versade --help
uv run versade check requests numpy
uv run versade serve --port 8000
uv run versade mcp
```

**Pros**: 
- Fast dependency resolution
- Isolated environment
- No global installation conflicts
- Easy development workflow

**Cons**: 
- Requires `uv run` prefix for commands

### Method 2: pipx - Global Isolated Install

**Prerequisites**: Python 3.8+ and pipx

```bash
# Install pipx if not already installed
pip install pipx

# From source (recommended)
git clone https://github.com/versade/versade
cd versade
pipx install -e .

# From PyPI (when published)
pipx install versade

# Usage
versade --help
versade check requests numpy
```

**Pros**: 
- Global command availability
- Isolated from system Python
- Easy to uninstall

**Cons**: 
- Requires pipx installation
- May have dependency conflicts

### Method 3: pip - System/Virtual Environment

**Prerequisites**: Python 3.8+ and pip

```bash
# Recommended: Use virtual environment
python -m venv versade-env
source versade-env/bin/activate  # Linux/Mac
# or
versade-env\Scripts\activate     # Windows

# From source
git clone https://github.com/versade/versade
cd versade
pip install -e .

# From PyPI (when published)
pip install versade

# Usage
versade --help
versade check requests numpy
```

**Pros**: 
- Standard Python installation
- Works everywhere
- No additional tools needed

**Cons**: 
- Can conflict with system packages
- Requires virtual environment management

### Method 4: uvx - Global Install from PyPI

**Prerequisites**: Python 3.8+ and uvx

```bash
# Install uvx if not already installed
pip install uvx

# From PyPI (when published)
uvx install versade

# Or run directly without installing
uvx --from versade versade check requests numpy

# Usage
versade --help
uvx --from versade versade check requests
```

**Pros**: 
- No local installation needed
- Always uses latest version
- Isolated execution

**Cons**: 
- Only works with published packages
- Requires internet for each run
- Slower startup

### Method 5: AUR (Arch Linux)

**Prerequisites**: Arch Linux with AUR helper

```bash
# Install with yay
yay -S versade

# Or with paru
paru -S versade

# Usage
versade --help
versade check requests numpy
```

**Pros**: 
- Native package management
- Automatic updates
- System integration

**Cons**: 
- Arch Linux only
- May lag behind latest version

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Perplexity API key for research features
PERPLEXITY_API_KEY=your_api_key_here

# Log level (DEBUG, INFO, WARNING, ERROR)
VERSADE_LOG_LEVEL=INFO

# MCP transport mode (stdio, sse)
VERSADE_TRANSPORT_MODE=stdio
```

### Interactive Setup

```bash
versade setup
```

This will guide you through:
- API key configuration
- Log level settings
- Transport mode preferences
- Default options

## Verification

Test your installation:

```bash
# Check version
versade --version

# Test package checking
versade check requests

# Test with JSON output
versade check --json numpy pandas

# Test npm packages
versade check --npm express react

# View history
versade history stats

# Test all features
versade test --quick
```

## Troubleshooting

### Common Issues

1. **Command not found**: 
   - For uv: Use `uv run versade` instead of `versade`
   - For pip: Ensure virtual environment is activated
   - For pipx: Run `pipx ensurepath`

2. **Permission errors**:
   - Use virtual environment with pip
   - Use pipx or uvx for isolated installs

3. **Dependency conflicts**:
   - Use pipx or uv for isolation
   - Create fresh virtual environment

4. **API errors**:
   - Set PERPLEXITY_API_KEY environment variable
   - Run `versade setup` for interactive configuration

### Getting Help

```bash
# General help
versade --help

# Command-specific help
versade check --help
versade serve --help
versade research --help

# View configuration
versade setup --force

# Check installation
versade history stats
```

## Uninstallation

### uv (Development)
```bash
# Just delete the project directory
rm -rf versade/
```

### pipx
```bash
pipx uninstall versade
```

### pip
```bash
pip uninstall versade
```

### uvx
```bash
# No uninstall needed (runs isolated)
```

### AUR
```bash
yay -R versade
# or
paru -R versade
```

## Next Steps

After installation:

1. **Configure API keys**: `versade setup`
2. **Test functionality**: `versade check requests`
3. **Start API server**: `versade serve`
4. **Integrate with MCP**: Add to `mcp-config.json`
5. **Explore research**: `versade research "python security"`
6. **View history**: `versade history list`

For more information, see the main [README.md](README.md). 