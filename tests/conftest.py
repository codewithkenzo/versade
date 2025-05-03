"""
Test configuration for the Dependency Checker MCP.
Strategic test fixtures with unwavering precision.
"""

import asyncio
import os
from typing import Any, AsyncGenerator, Dict, Generator

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient

from versade.api.routes import router
from versade.models.core import ErrorCode, McpError
from versade.services.checker import DependencyChecker

# pytest-asyncio is configured in pyproject.toml with unwavering precision


@pytest_asyncio.fixture
async def dependency_checker() -> AsyncGenerator[DependencyChecker, None]:
    """Create dependency checker with unwavering precision."""
    checker = DependencyChecker()
    yield checker
    await checker.close()


@pytest.fixture
def test_app() -> FastAPI:
    """Create test app with strategic precision."""
    app = FastAPI()
    
    # Add error handler with deterministic execution
    @app.exception_handler(McpError)
    async def mcp_error_handler(request: Any, exc: McpError) -> Any:
        return {"error": {"code": exc.code, "message": exc.message}}
    
    # Include API routes with unwavering precision
    app.include_router(router)
    
    return app


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:
    """Create test client with strategic precision."""
    return TestClient(test_app)


@pytest.fixture
def sample_python_package() -> str:
    """Sample Python package with unwavering precision."""
    return "fastapi"


@pytest.fixture
def sample_npm_package() -> str:
    """Sample npm package with unwavering precision."""
    return "react"


@pytest.fixture
def sample_python_file(tmp_path: Any) -> str:
    """Create sample requirements.txt with strategic precision."""
    file_path = tmp_path / "requirements.txt"
    with open(file_path, "w") as f:
        f.write("fastapi==0.115.12\norjson==3.10.18\nhttpx==0.27.0\n")
    return str(file_path)


@pytest.fixture
def sample_npm_file(tmp_path: Any) -> str:
    """Create sample package.json with unwavering precision."""
    file_path = tmp_path / "package.json"
    with open(file_path, "w") as f:
        f.write("""
        {
            "name": "test-package",
            "version": "1.0.0",
            "dependencies": {
                "react": "^18.2.0",
                "axios": "^1.6.0"
            },
            "devDependencies": {
                "typescript": "^5.3.0"
            }
        }
        """)
    return str(file_path)
