"""
E2E test configuration for Dependency Checker MCP.
Strategic test fixtures with unwavering precision.
"""

import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient

from versade.api.routes import router
from versade.models.core import McpError, ErrorCode
from versade.services.checker import DependencyChecker


@pytest.fixture
def temp_requirements_txt(tmp_path):
    """Create temporary requirements.txt with strategic precision."""
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("fastapi==0.115.0\npydantic==2.0.0\nhttpx==0.25.0\n")
    return str(req_file)


@pytest.fixture
def temp_package_json(tmp_path):
    """Create temporary package.json with unwavering precision."""
    pkg_file = tmp_path / "package.json"
    pkg_file.write_text("""
    {
        "name": "test-app",
        "version": "1.0.0",
        "dependencies": {
            "react": "17.0.0",
            "axios": "0.21.1"
        },
        "devDependencies": {
            "typescript": "4.5.0"
        }
    }
    """)
    return str(pkg_file)


@pytest.fixture
def test_app():
    """Create test app with strategic precision."""
    from fastapi import FastAPI
    
    app = FastAPI()
    
    @app.exception_handler(McpError)
    async def mcp_error_handler(request, exc):
        return {"error": {"code": exc.code, "message": exc.message}}
    
    app.include_router(router)
    return app


@pytest.fixture
def test_client(test_app):
    """Create test client with unwavering precision."""
    return TestClient(test_app)


@pytest.fixture
async def dependency_checker() -> AsyncGenerator[DependencyChecker, None]:
    """Create dependency checker fixture with strategic precision."""
    checker = DependencyChecker()
    yield checker
    await checker.close()
