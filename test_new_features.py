#!/usr/bin/env python3
"""
Test script for new Versade features.
Tests CLI, API, and research functionality.
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

import httpx


async def test_cli_check():
    """Test the new CLI check command."""
    print("🧪 Testing CLI check command...")
    
    try:
        # Test Python package check
        result = subprocess.run(
            ["uv", "run", "python", "-m", "versade.cli", "check", "requests", "--json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            print(f"✅ CLI check works: {data[0]['name']} v{data[0]['version']}")
            return True
        else:
            print(f"❌ CLI check failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ CLI check error: {e}")
        return False


async def test_api_server():
    """Test the FastAPI server endpoints."""
    print("🧪 Testing FastAPI server...")
    
    # Start server in background
    server_process = None
    try:
        server_process = subprocess.Popen(
            ["uv", "run", "python", "-m", "versade.api.app"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        await asyncio.sleep(3)
        
        async with httpx.AsyncClient() as client:
            # Test health endpoint
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✅ Health endpoint works")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
            
            # Test queue endpoint
            response = await client.post(
                "http://localhost:8000/queue",
                json={
                    "dependencies": ["requests"],
                    "package_manager": "pip"
                }
            )
            
            if response.status_code == 200:
                job_data = response.json()
                job_id = job_data["job_id"]
                print(f"✅ Queue endpoint works: job {job_id}")
                
                # Wait a bit and check job status
                await asyncio.sleep(2)
                response = await client.get(f"http://localhost:8000/queue/{job_id}")
                if response.status_code == 200:
                    job_status = response.json()
                    print(f"✅ Job status endpoint works: {job_status['status']}")
                    return True
                else:
                    print(f"❌ Job status failed: {response.status_code}")
                    return False
            else:
                print(f"❌ Queue endpoint failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ API server error: {e}")
        return False
    finally:
        if server_process:
            server_process.terminate()
            server_process.wait()


async def test_mcp_server():
    """Test the MCP server stdio mode."""
    print("🧪 Testing MCP server...")
    
    try:
        # Test MCP server initialization
        process = subprocess.Popen(
            ["uv", "run", "python", "-m", "versade.cli", "mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read response with timeout
        try:
            output = process.stdout.readline()
            if output:
                response = json.loads(output.strip())
                if "result" in response:
                    print("✅ MCP server initialization works")
                    return True
                else:
                    print(f"❌ MCP server init failed: {response}")
                    return False
            else:
                print("❌ MCP server no response")
                return False
        except json.JSONDecodeError as e:
            print(f"❌ MCP server JSON error: {e}")
            return False
        finally:
            process.terminate()
            process.wait()
            
    except Exception as e:
        print(f"❌ MCP server error: {e}")
        return False


async def test_research_service():
    """Test the research service (without API key)."""
    print("🧪 Testing research service...")
    
    try:
        from versade.services.research import PerplexityResearchService
        
        # Test without API key (should raise ValueError)
        service = PerplexityResearchService()
        
        try:
            await service.research("test query")
            print("❌ Research service should require API key")
            return False
        except ValueError as e:
            if "API key required" in str(e):
                print("✅ Research service correctly requires API key")
                return True
            else:
                print(f"❌ Unexpected error: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Research service error: {e}")
        return False


async def main():
    """Run all tests."""
    print("🚀 Testing new Versade features...\n")
    
    tests = [
        ("CLI Check", test_cli_check),
        ("API Server", test_api_server),
        ("MCP Server", test_mcp_server),
        ("Research Service", test_research_service),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Testing: {name}")
        print('='*50)
        
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main())) 