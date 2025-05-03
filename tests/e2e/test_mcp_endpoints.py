"""
E2E tests for Dependency Checker MCP endpoints.
Strategic validation with unwavering precision.
"""

import json
import uuid
from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient

from dep_checker_mcp.models.core import ErrorCode


@pytest.mark.e2e
def test_meta_endpoint(test_client: TestClient) -> None:
    """Test meta endpoint with strategic precision."""
    response = test_client.get("/mcp/meta")
    
    # Validate response with unwavering precision
    assert response.status_code == 200
    data = response.json()
    assert "metadata" in data
    assert data["metadata"]["name"] == "dependency-checker-mcp"
    assert "version" in data["metadata"]
    assert "capabilities" in data


@pytest.mark.e2e
def test_list_tools_endpoint(test_client: TestClient) -> None:
    """Test list_tools endpoint with strategic precision."""
    request_id = str(uuid.uuid4())
    
    response = test_client.post(
        "/mcp/list_tools",
        json={"id": request_id}
    )
    
    # Validate response with unwavering precision
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == request_id
    assert "tools" in data
    tools = data["tools"]
    
    # Verify all required tools with strategic precision
    tool_names = [tool["name"] for tool in tools]
    assert "mcp_check_python_package" in tool_names
    assert "mcp_check_npm_package" in tool_names
    assert "mcp_check_python_file" in tool_names
    assert "mcp_check_npm_file" in tool_names
    assert "mcp_run_mypy" in tool_names
    assert "mcp_run_npm_audit" in tool_names
    
    # Verify parameters with unwavering precision
    for tool in tools:
        assert "parameters" in tool
        assert "properties" in tool["parameters"]
        assert "type" in tool["parameters"]


@pytest.mark.e2e
def test_call_tool_invalid_name(test_client: TestClient) -> None:
    """Test call_tool with invalid tool name with strategic precision."""
    request_id = str(uuid.uuid4())
    
    response = test_client.post(
        "/mcp/call_tool",
        json={
            "id": request_id,
            "name": "invalid_tool_name",
            "parameters": {}
        }
    )
    
    # Validate error response with unwavering precision
    assert response.status_code == 200  # MCP protocol returns 200 with error in body
    data = response.json()
    assert data["id"] == request_id
    assert "error" in data
    assert data["error"]["code"] == ErrorCode.TOOL_NOT_FOUND


@pytest.mark.e2e
def test_health_endpoint(test_client: TestClient) -> None:
    """Test health endpoint with strategic precision."""
    response = test_client.get("/health")
    
    # Validate response with unwavering precision
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.e2e
def test_call_tool_missing_parameters(test_client: TestClient) -> None:
    """Test call_tool with missing parameters with strategic precision."""
    request_id = str(uuid.uuid4())
    
    response = test_client.post(
        "/mcp/call_tool",
        json={
            "id": request_id,
            "name": "mcp_check_python_package",
            "parameters": {}  # Missing required package_name
        }
    )
    
    # Validate error response with unwavering precision
    assert response.status_code == 200  # MCP protocol returns 200 with error in body
    data = response.json()
    assert data["id"] == request_id
    assert "error" in data
    assert data["error"]["code"] == ErrorCode.INVALID_PARAMS
