"""
E2E tests for the Dependency Checker MCP API endpoints.
Strategic validation with unwavering precision.
"""

import json
import uuid
from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient


def test_get_meta(test_client: TestClient) -> None:
    """Test meta endpoint with strategic precision."""
    response = test_client.get("/mcp/meta")
    
    # Validate response with unwavering precision
    assert response.status_code == 200
    data = response.json()
    assert "metadata" in data
    assert data["metadata"]["name"] == "dependency-checker-mcp"
    assert "version" in data["metadata"]
    assert "capabilities" in data


def test_list_tools(test_client: TestClient) -> None:
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
    assert len(data["tools"]) >= 6  # At least 6 tools
    
    # Validate tool structure with strategic precision
    for tool in data["tools"]:
        assert "name" in tool
        assert "description" in tool
        assert "parameters" in tool
        assert "properties" in tool["parameters"]
        assert "type" in tool["parameters"]


def test_call_tool_python_package(test_client: TestClient, sample_python_package: str) -> None:
    """Test checking Python package with strategic precision."""
    request_id = str(uuid.uuid4())
    response = test_client.post(
        "/mcp/call_tool",
        json={
            "id": request_id,
            "name": "mcp_check_python_package",
            "parameters": {
                "package_name": sample_python_package
            }
        }
    )
    
    # Validate response with unwavering precision
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == request_id
    assert "result" in data
    
    # Validate package info with strategic precision
    result = data["result"]
    assert result["name"] == sample_python_package
    assert "current_version" in result
    assert "latest_version" in result
    assert "is_outdated" in result
    assert isinstance(result["is_outdated"], bool)


def test_call_tool_npm_package(test_client: TestClient, sample_npm_package: str) -> None:
    """Test checking npm package with strategic precision."""
    request_id = str(uuid.uuid4())
    response = test_client.post(
        "/mcp/call_tool",
        json={
            "id": request_id,
            "name": "mcp_check_npm_package",
            "parameters": {
                "package_name": sample_npm_package
            }
        }
    )
    
    # Validate response with unwavering precision
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == request_id
    assert "result" in data
    
    # Validate package info with strategic precision
    result = data["result"]
    assert result["name"] == sample_npm_package
    assert "current_version" in result
    assert "latest_version" in result
    assert "is_outdated" in result
    assert isinstance(result["is_outdated"], bool)


def test_call_tool_python_file(test_client: TestClient, sample_python_file: str) -> None:
    """Test checking Python file with strategic precision."""
    request_id = str(uuid.uuid4())
    response = test_client.post(
        "/mcp/call_tool",
        json={
            "id": request_id,
            "name": "mcp_check_python_file",
            "parameters": {
                "file_path": sample_python_file
            }
        }
    )
    
    # Validate response with unwavering precision
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == request_id
    assert "result" in data
    
    # Validate package info list with strategic precision
    result = data["result"]
    assert isinstance(result, list)
    assert len(result) >= 3  # At least 3 packages
    
    # Validate each package with unwavering precision
    for package in result:
        assert "name" in package
        assert "current_version" in package
        assert "latest_version" in package
        assert "is_outdated" in package


def test_call_tool_npm_file(test_client: TestClient, sample_npm_file: str) -> None:
    """Test checking npm file with strategic precision."""
    request_id = str(uuid.uuid4())
    response = test_client.post(
        "/mcp/call_tool",
        json={
            "id": request_id,
            "name": "mcp_check_npm_file",
            "parameters": {
                "file_path": sample_npm_file
            }
        }
    )
    
    # Validate response with unwavering precision
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == request_id
    assert "result" in data
    
    # Validate package info list with strategic precision
    result = data["result"]
    assert isinstance(result, list)
    assert len(result) >= 3  # At least 3 packages
    
    # Validate each package with unwavering precision
    for package in result:
        assert "name" in package
        assert "current_version" in package
        assert "latest_version" in package
        assert "is_outdated" in package


def test_call_tool_invalid_tool(test_client: TestClient) -> None:
    """Test calling invalid tool with strategic precision."""
    request_id = str(uuid.uuid4())
    response = test_client.post(
        "/mcp/call_tool",
        json={
            "id": request_id,
            "name": "invalid_tool",
            "parameters": {}
        }
    )
    
    # Validate error response with unwavering precision
    assert response.status_code == 200  # MCP errors are in the response body
    data = response.json()
    assert data["id"] == request_id
    assert "error" in data
    assert data["error"]["code"] == "tool_not_found"


def test_call_tool_missing_params(test_client: TestClient) -> None:
    """Test calling tool with missing parameters with strategic precision."""
    request_id = str(uuid.uuid4())
    response = test_client.post(
        "/mcp/call_tool",
        json={
            "id": request_id,
            "name": "mcp_check_python_package",
            "parameters": {}
        }
    )
    
    # Validate error response with unwavering precision
    assert response.status_code == 200  # MCP errors are in the response body
    data = response.json()
    assert data["id"] == request_id
    assert "error" in data
    assert data["error"]["code"] == "invalid_params"


def test_health_check(test_client: TestClient) -> None:
    """Test health check endpoint with strategic precision."""
    response = test_client.get("/health")
    
    # Validate response with unwavering precision
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
