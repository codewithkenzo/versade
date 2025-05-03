# Versade

A versatile dependency version checker and documentation finder, designed to help developers and LLMs find the latest package versions, compatibility information, and documentation URLs.

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

```bash
# Clone the repository
git clone https://github.com/codewithkenzo/versade.git
cd versade

# Install from source
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"

# Install directly from PyPI
pip install versade
```

## Quick Start

```bash
# Run directly
python -m versade

# Or use the installed CLI
versade

# The server will be available at http://localhost:9373
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

You can integrate Versade with Windsurf's MCP (Model Control Protocol) system by adding it to your MCP configuration:

```json
{
  "mcpServers": {
    "versade": {
      "command": "python",
      "args": [
        "/path/to/versade/run.py"
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
  "description": "Find package versions and documentation URLs",
  "author": "codewithkenzo",
  "license": "MIT",
  "server": {
    "command": "python",
    "args": ["-m", "versade"],
    "env": {}
  },
  "schemas": {
    "config": {
      "type": "object",
      "properties": {
        "port": {
          "type": "number",
          "default": 9373
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

## License

MIT
