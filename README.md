# Versade

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/codewithkenzo/versade)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![Type Hints](https://img.shields.io/badge/type%20hints-100%25-brightgreen)](https://mypy.readthedocs.io/)
[![AUR](https://img.shields.io/badge/AUR-versade-blue)](https://aur.archlinux.org/packages/versade)

A versatile dependency version checker and documentation finder, designed specifically for LLMs and developers to find the latest package versions, compatibility information, and documentation URLs with unwavering precision.

## Architecture

```
versade/
├── api/         # FastAPI endpoints for version checking
├── models/      # Core data models with full type safety
├── services/    # Dependency checking and documentation services
└── utils/       # Utility functions and configuration
```

## Features

- **Modular Architecture**: Well-organized codebase with clean separation of concerns
- **Complete Type Safety**: 100% type-annotated with mypy validation
- **Comprehensive Testing**: Thorough unit and e2e tests with high coverage
- **FastAPI Server**: Built with FastAPI for efficient, high-performance API
- **Async I/O**: Leverages anyio and asyncio for optimal performance
- **orjson Performance**: Ultra-fast serialization/deserialization with orjson

## Core Capabilities

- **Python Package Validation**: Check Python packages against PyPI for latest versions
- **npm Package Validation**: Validate npm packages against npm registry
- **Documentation URL Retrieval**: Automatically find and provide URLs for:
  - Documentation websites
  - API references
  - GitHub repositories
  - Type hint stubs (mypy)
- **Security Vulnerability Detection**: Identify security vulnerabilities in both Python and npm packages
- **File-Based Dependency Analysis**: Analyze requirements.txt, pyproject.toml, and package.json files
- **mypy Type Checking Integration**: Validate Python code with mypy type checking
- **npm Audit Integration**: Run npm audit for security vulnerability identification

## Installation

Choose your preferred installation method:

### From PyPI

```bash
# Using pip
pip install versade

# Using uv (faster installation)
uv pip install versade

# Using pipx (isolated environment)
pipx install versade
```

### From AUR (Arch Linux)

```bash
# Using yay
yay -S versade

# Using paru
paru -S versade
```

### From Source

```bash
# Clone the repository
git clone https://github.com/codewithkenzo/versade.git
cd versade

# Install from source
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### With Docker

```bash
# Pull from GitHub Container Registry
docker pull ghcr.io/codewithkenzo/versade:latest

# Or build locally
docker build -t versade:latest .

# Run the container
docker run -d -p 9373:9373 --name versade-container versade:latest
```

## Quick Start

```bash
# Run with the CLI (automatically finds an available port if 9373 is busy)
versade

# Specify a custom port
versade --port 9374

# Show available options
versade --help

# The server will be available at http://localhost:9373 (or another available port)
```

## MCP Tools

- `mcp_check_python_package`: Check a Python package for updates, security issues, and documentation URLs
- `mcp_check_npm_package`: Check an npm package for updates, security issues, and documentation URLs
- `mcp_check_python_file`: Check a Python requirements.txt or pyproject.toml file
- `mcp_check_npm_file`: Check a package.json file
- `mcp_run_mypy`: Run mypy type checker on a Python file or directory
- `mcp_run_npm_audit`: Run npm audit on a package.json file

## Documentation URLs

Versade automatically finds and provides URLs for:

- **Documentation**: Main documentation site for the package
- **API Reference**: API documentation for developers
- **GitHub Repository**: Source code repository
- **Type Hints**: mypy stubs information (for Python packages)

### Example response for a Python package:

```json
{
  "name": "fastapi",
  "current_version": "0.115.12",
  "latest_version": "0.115.12",
  "is_outdated": false,
  "homepage": "https://fastapi.tiangolo.com/",
  "description": "FastAPI framework, high performance, easy to learn, fast to code, ready for production",
  "documentation_url": "https://fastapi.tiangolo.com/",
  "api_docs_url": "https://fastapi.tiangolo.com/reference/",
  "github_url": "https://github.com/tiangolo/fastapi",
  "mypy_stub_url": "https://github.com/tiangolo/fastapi/blob/master/fastapi/py.typed"
}
```

### Example response for an npm package:

```json
{
  "name": "react",
  "current_version": "17.0.1",
  "latest_version": "19.1.0",
  "is_outdated": true,
  "homepage": "https://react.dev/",
  "description": "React is a JavaScript library for building user interfaces.",
  "release_date": "2025-03-28T19:59:42.053Z",
  "security_issues": [],
  "documentation_url": "https://react.dev/",
  "api_docs_url": "https://github.com/facebook/react/blob/main/API.md",
  "mypy_stub_url": null,
  "github_url": "https://github.com/facebook/react"
}
```

## Environment Variables

- `VERSADE_PORT`: Port for the server (default: 9373)
- `VERSADE_LOG_LEVEL`: Logging level (default: INFO)
- `VERSADE_CORS_ORIGINS`: Comma-separated list of allowed origins (default: *)
- `VERSADE_MAX_REQUEST_SIZE`: Maximum request size in bytes (default: 1MB)
- `VERSADE_RATE_LIMIT_REQUESTS`: Rate limit requests per window (default: 5)
- `VERSADE_RATE_LIMIT_WINDOW`: Rate limit window in seconds (default: 1)
- `VERSADE_TIMEOUT`: HTTP request timeout in seconds (default: 30.0)

## Development

```bash
# Run tests
pytest

# Run tests with coverage reporting
pytest --cov=versade

# Run tests with asyncio auto mode (configured in pyproject.toml)
# asyncio_mode = "auto"
# asyncio_default_fixture_loop_scope = "function"

# Run type checking
mypy src

# Run linting
ruff check src
```

## MCP Integration

You can integrate Versade with Windsurf's MCP (Model Control Protocol) system by adding it to your MCP configuration. 

### Standard MCP Configuration

```json
{
  "mcpServers": {
    "versade": {
      "command": "versade",
      "env": {
        "VERSADE_PORT": "9373",
        "VERSADE_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Legacy Python Module (for those unfamiliar with Python in MCP configs)

```json
{
  "mcpServers": {
    "versade": {
      "command": "python",
      "args": [
        "-m", "versade"
      ],
      "env": {
        "VERSADE_PORT": "9373",
        "VERSADE_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Why Versade?

Versade was created to solve common challenges faced when working with dependencies:

1. **LLM Assistance**: Help LLMs find accurate version and documentation information
2. **Dependency Management**: Quick checks for outdated packages and security issues
3. **Documentation Discovery**: Auto-find relevant documentation links without manual searches
4. **Type Safety**: Identify packages with typing support and locate mypy stubs

The name "Versade" reflects the tool's versatility in handling different package ecosystems and providing useful information for developers.

## Deployment Guide

### PyPI

```bash
# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

### Arch User Repository (AUR)

```bash
# Clone the AUR package repository
git clone ssh://aur@aur.archlinux.org/python-versade.git
cd python-versade

# Update the PKGBUILD file
# - Update pkgver variable to match the new version
# - Update sha256sums if source files changed
# - Update dependencies if needed

# Generate .SRCINFO file
makepkg --printsrcinfo > .SRCINFO

# Commit and push changes
git add PKGBUILD .SRCINFO
git commit -m "update to version X.Y.Z"
git push
```

### Smithery MCP Registry

```bash
# Log in to Smithery registry
smith login

# Register or update the MCP server
smith mcp publish ./smithery-manifest.json
```

Example `smithery-manifest.json`:

```json
{
  "name": "versade",
  "version": "1.0.0",
  "description": "Versatile dependency version checker and documentation finder for LLM and developer assistance",
  "author": "codewithkenzo",
  "license": "MIT",
  "server": {
    "command": "versade",
    "env": {}
  },
  "schemas": {
    "config": {
      "type": "object",
      "properties": {
        "port": {
          "type": "number",
          "default": 9373
        },
        "log_level": {
          "type": "string",
          "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
          "default": "INFO"
        }
      }
    }
  }
}
```

### mypy Type Stubs

Ensure your package is properly typed:

1. Include `py.typed` marker file in your package
2. Register your type stubs with typeshed or provide inline documentation
3. Submit a PR to DefinitelyTyped/typeshed for community type stubs

## Project History

Versade began as a dependency checker MCP server and has evolved through several phases:

### Phase 1: Initial Implementation
- Built core functionality for checking Python and npm package versions
- Implemented FastAPI endpoints with SSE support
- Created initial unit and integration tests

### Phase 2: Enhancement & Expansion
- Added documentation URL retrieval for Python and npm packages
- Improved error handling and rate limiting
- Enhanced mypy integration for better type safety

### Phase 3: Rebranding & Refinement
- Rebranded from "dependency-checker-mcp" to "Versade"
- Achieved 100% type safety with mypy
- Enhanced Docker support with multi-stage builds
- Expanded test coverage to >90%

### Phase 4: Deployment & Distribution
- Created AUR package for Arch Linux users
- Registered with Smithery MCP Registry
- Published to PyPI with correct type stubs
- Added support for uv/uvx installation

## Project Management

This project is tracked using Linear, with a comprehensive task breakdown and milestone tracking. Our Linear project includes:

- Feature tracking with detailed specifications
- Bug reports with reproduction steps
- Release planning with version milestones
- Integration testing schedules

View our project timeline and roadmap in the [Linear Project](https://linear.app/versade).

## License

MIT

---

<p align="center">Made with ❤️ for LLMs and developers</p>
