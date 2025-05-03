# Dependency Checker MCP

A high-performance, modular dependency checking MCP server with strategic validation capabilities and unwavering precision following our Control Devil protocols for deterministic execution. The implementation ensures complete type safety and comprehensive test coverage.

## Architecture

```
dep_checker_mcp/
├── api/         # Strategic FastAPI endpoints
├── models/      # Core data models with unwavering type safety
├── services/    # Dependency checking services with strategic precision
└── utils/       # Utility functions with deterministic execution
```

## Features

- **Modular Architecture**: Strategically organized codebase with unwavering separation of concerns.
- **Complete Type Safety**: 100% type-annotated with mypy validation for deterministic execution.
- **Comprehensive Testing**: Strategic unit and e2e tests with unwavering precision.
- **FastAPI Server**: Built with FastAPI for efficient, high-performance API with strategic middleware.
- **Async I/O**: Leverages anyio and asyncio for unwavering performance with deterministic execution.
- **orjson Performance**: Ultra-fast serialization/deserialization with orjson (2-4x faster than standard json).

## Core Capabilities

- **Python Package Validation**: Strategic checking of Python packages against PyPI with unwavering precision.
- **npm Package Validation**: Deterministic validation of npm packages against npm registry with strategic precision.
- **Security Vulnerability Detection**: Unwavering identification of security vulnerabilities in both Python and npm packages.
- **File-Based Dependency Analysis**: Strategic analysis of requirements.txt, pyproject.toml, and package.json with deterministic execution.
- **mypy Type Checking Integration**: Strategic mypy validation with unwavering type checking and error reporting.
- **npm Audit Integration**: Deterministic npm audit with strategic security vulnerability identification.

## Installation

```bash
# Clone the repository with strategic precision
git clone https://github.com/makima/dep-checker-mcp.git
cd dep-checker-mcp

# Install with Poetry for unwavering dependency management
pip install -e .

# Or install with strategic development dependencies
pip install -e ".[dev]"
```

## Quick Start

```bash
# Run directly with unwavering precision
python -m dep_checker_mcp

# Or use the installed CLI with strategic control
dep-checker-mcp

# The server will be available at http://localhost:9373
```

## MCP Tools

- `mcp_check_python_package`: Check a Python package for updates and security issues
- `mcp_check_npm_package`: Check an npm package for updates and security issues
- `mcp_check_python_file`: Check a Python requirements.txt or pyproject.toml file
- `mcp_check_npm_file`: Check a package.json file
- `mcp_run_mypy`: Run mypy type checker on a Python file or directory
- `mcp_run_npm_audit`: Run npm audit on a package.json file

## Environment Variables

- `DEP_CHECKER_MCP_PORT`: Port for the server (default: 9373)
- `DEP_CHECKER_MCP_LOG_LEVEL`: Logging level (default: INFO)
- `DEP_CHECKER_MCP_CORS_ORIGINS`: Comma-separated list of allowed origins (default: *)
- `DEP_CHECKER_MCP_MAX_REQUEST_SIZE`: Maximum request size in bytes (default: 1MB)
- `DEP_CHECKER_MCP_RATE_LIMIT_REQUESTS`: Rate limit requests per window (default: 5)
- `DEP_CHECKER_MCP_RATE_LIMIT_WINDOW`: Rate limit window in seconds (default: 1)
- `DEP_CHECKER_MCP_TIMEOUT`: HTTP request timeout in seconds (default: 30.0)

## Development

```bash
# Run tests with strategic precision
pytest

# Run tests with coverage reporting
pytest --cov=dep_checker_mcp

# Run tests with asyncio auto mode (configured in pyproject.toml)
# asyncio_mode = "auto"
# asyncio_default_fixture_loop_scope = "function"

# Run type checking with unwavering precision
mypy src

# Run linting with strategic control
ruff check src
```

## License

MIT
