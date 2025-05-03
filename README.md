# Versa

A versatile dependency version checker and documentation finder, designed to help developers and LLMs find the latest package versions, compatibility information, and documentation URLs.

## Architecture

```
versa/
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
git clone https://github.com/codewithkenzo/versa.git
cd versa

# Install from source
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"

# Install directly from PyPI
pip install versa
```

## Quick Start

```bash
# Run directly
python -m versa

# Or use the installed CLI
versa

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

Versa automatically finds and provides URLs for:

- **Documentation**: Main documentation site for the package
- **API Reference**: API documentation for developers
- **GitHub Repository**: Source code repository
- **Type Hints**: mypy stubs information (for Python packages)

Example response for a Python package:

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

## Environment Variables

- `VERSA_PORT`: Port for the server (default: 9373)
- `VERSA_LOG_LEVEL`: Logging level (default: INFO)
- `VERSA_CORS_ORIGINS`: Comma-separated list of allowed origins (default: *)
- `VERSA_MAX_REQUEST_SIZE`: Maximum request size in bytes (default: 1MB)
- `VERSA_RATE_LIMIT_REQUESTS`: Rate limit requests per window (default: 5)
- `VERSA_RATE_LIMIT_WINDOW`: Rate limit window in seconds (default: 1)
- `VERSA_TIMEOUT`: HTTP request timeout in seconds (default: 30.0)

## Development

```bash
# Run tests
pytest

# Run tests with coverage reporting
pytest --cov=versa

# Run tests with asyncio auto mode (configured in pyproject.toml)
# asyncio_mode = "auto"
# asyncio_default_fixture_loop_scope = "function"

# Run type checking
mypy src

# Run linting
ruff check src
```

## MCP Integration

You can integrate Versa with Windsurf's MCP (Model Control Protocol) system by adding it to your MCP configuration:

```json
{
  "mcpServers": {
    "versa": {
      "command": "python",
      "args": [
        "/path/to/versa/run.py"
      ],
      "env": {
        "VERSA_PORT": "9373",
        "VERSA_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Why Versa?

Versa was created to solve common challenges faced when working with dependencies:

1. **LLM Assistance**: Help LLMs find accurate version and documentation information
2. **Dependency Management**: Quick checks for outdated packages and security issues
3. **Documentation Discovery**: Auto-find relevant documentation links without manual searches
4. **Type Safety**: Identify packages with typing support and locate mypy stubs

The name "Versa" reflects the tool's versatility in handling different package ecosystems and providing useful information for developers.

## License

MIT
