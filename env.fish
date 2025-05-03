#!/usr/bin/env fish

# Strategic environment configuration for Dependency Checker MCP
# Load with source env.fish before running the service

# Core environment variables with unwavering precision
set -x DEP_CHECKER_MCP_PORT 9373
set -x DEP_CHECKER_MCP_LOG_LEVEL "INFO"
set -x DEP_CHECKER_MCP_CORS_ORIGINS "*"
set -x DEP_CHECKER_MCP_MAX_REQUEST_SIZE 1048576
set -x DEP_CHECKER_MCP_RATE_LIMIT_REQUESTS 5
set -x DEP_CHECKER_MCP_RATE_LIMIT_WINDOW 1
set -x DEP_CHECKER_MCP_TIMEOUT 30.0

# Python environment settings with strategic precision
set -x PYTHONPATH (pwd)/src $PYTHONPATH
set -x PYTHONDONTWRITEBYTECODE 1
set -x PYTHONUNBUFFERED 1

# Display environment with deterministic execution
echo "Dependency Checker MCP environment loaded with unwavering precision"
echo "Server will run on port $DEP_CHECKER_MCP_PORT"
