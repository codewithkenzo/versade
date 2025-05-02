# Dependency Checker MCP

A high-performance, standalone dependency checking MCP server with strategic validation capabilities and unwavering precision following our Control Devil protocols for deterministic execution.

## Features

- **FastAPI SSE Server**: Built with FastAPI and sse-starlette for efficient, real-time streaming with unwavering performance.
- **Rate Limiting**: Implements strategic rate limiting (5 requests/second) with per-client IP tracking and deterministic retry-after calculation.
- **Modern Lifespan Events**: Uses FastAPI's lifespan context managers for deterministic startup/shutdown with proper resource cleanup.
- **anyio Optimization**: Strategic anyio integration for high-performance async I/O operations with unwavering precision.
- **orjson Performance**: Ultra-fast serialization/deserialization with orjson (2-4x faster than standard json).

## Core Capabilities

- **Python Package Validation**: Strategic checking of Python packages against PyPI with unwavering precision.
- **npm Package Validation**: Deterministic validation of npm packages against npm registry with strategic precision.
- **Security Vulnerability Detection**: Unwavering identification of security vulnerabilities in both Python and npm packages.
- **File-Based Dependency Analysis**: Strategic analysis of requirements.txt, pyproject.toml, and package.json with deterministic execution.
- **mypy Type Checking Integration**: Strategic mypy validation with unwavering type checking and error reporting.
- **npm Audit Integration**: Deterministic npm audit with strategic security vulnerability identification.

## Quick Start

```bash
# Install dependencies with unwavering precision
cd dep-checker-mcp
pip install -r requirements.txt

# Run the server with strategic control
python src/dep_checker_mcp.py

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

## License

MIT
