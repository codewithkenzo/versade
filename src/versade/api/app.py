"""
Versade FastAPI Application
Modern HTTP/SSE API for dependency analysis and research.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

import httpx
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from versade.server import check_python_package, check_npm_package, analyze_dependencies

# Configure logging
logger = logging.getLogger("versade.api")

# Global job storage (in production, use Redis or similar)
jobs: Dict[str, Dict[str, Any]] = {}

# FastAPI app
app = FastAPI(
    title="Versade API",
    description="Versatile dependency analysis and research API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class AnalyzeRequest(BaseModel):
    dependencies: List[str] = Field(..., description="List of package names to analyze")
    package_manager: str = Field("pip", description="Package manager (pip, npm)")

class QueueRequest(BaseModel):
    dependencies: List[str] = Field(..., description="List of package names to analyze")
    package_manager: str = Field("pip", description="Package manager (pip, npm)")
    
class BatchResearchRequest(BaseModel):
    queries: List[str] = Field(..., description="List of research queries")
    api_key: Optional[str] = Field(None, description="Perplexity API key (optional if set in env)")
    model: str = Field(
        "sonar-deep-research", 
        description="Perplexity model to use for batch research",
        pattern="^(sonar-deep-research|sonar-reasoning-pro|sonar-reasoning|sonar-pro|sonar|r1-1776)$"
    )
    
class ResearchRequest(BaseModel):
    query: str = Field(..., description="Research question")
    api_key: Optional[str] = Field(None, description="Perplexity API key (optional if set in env)")
    model: str = Field(
        "sonar-pro", 
        description="Perplexity model to use",
        pattern="^(sonar-deep-research|sonar-reasoning-pro|sonar-reasoning|sonar-pro|sonar|r1-1776)$"
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# SSE streaming analysis endpoint
@app.post("/analyze")
async def analyze_stream(request: AnalyzeRequest):
    """
    Analyze dependencies with real-time SSE streaming.
    Returns results as they become available.
    """
    async def event_stream():
        try:
            yield {
                "event": "start",
                "data": json.dumps({
                    "message": f"Starting analysis of {len(request.dependencies)} packages",
                    "total": len(request.dependencies)
                })
            }
            
            for i, dep in enumerate(request.dependencies):
                try:
                    if request.package_manager in ["pip", "poetry"]:
                        result = await check_python_package(dep)
                    elif request.package_manager == "npm":
                        result = await check_npm_package(dep)
                    else:
                        result = {"name": dep, "error": "Unsupported package manager", "success": False}
                    
                    yield {
                        "event": "result",
                        "data": json.dumps({
                            "index": i,
                            "package": dep,
                            "result": result
                        })
                    }
                    
                    # Small delay to prevent overwhelming
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Error analyzing {dep}: {e}")
                    yield {
                        "event": "error",
                        "data": json.dumps({
                            "index": i,
                            "package": dep,
                            "error": str(e)
                        })
                    }
            
            yield {
                "event": "complete",
                "data": json.dumps({"message": "Analysis complete"})
            }
            
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    
    return EventSourceResponse(event_stream())

# Batch job queue endpoint
@app.post("/queue")
async def queue_analysis(request: QueueRequest, background_tasks: BackgroundTasks):
    """
    Queue a batch analysis job.
    Returns a job ID for polling results.
    """
    job_id = str(uuid4())
    jobs[job_id] = {
        "id": job_id,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat(),
        "dependencies": request.dependencies,
        "package_manager": request.package_manager,
        "results": [],
        "progress": 0,
        "total": len(request.dependencies)
    }
    
    background_tasks.add_task(process_batch_job, job_id)
    
    return {"job_id": job_id, "status": "queued"}

# Get job status/results
@app.get("/queue/{job_id}")
async def get_job_status(job_id: str):
    """Get the status and results of a batch job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]

# Research endpoint (Perplexity integration)
@app.post("/research")
async def research_query(request: ResearchRequest):
    """
    Perform deep research using Perplexity API.
    """
    api_key = request.api_key or os.getenv("PERPLEXITY_API_KEY")
    
    if not api_key:
        raise HTTPException(
            status_code=400, 
            detail="Perplexity API key required. Set PERPLEXITY_API_KEY env var or provide in request."
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": request.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful research assistant. Provide comprehensive, accurate information with sources."
                        },
                        {
                            "role": "user",
                            "content": request.query
                        }
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "return_citations": True,
                    "search_domain_filter": ["github.com", "pypi.org", "npmjs.com", "cve.mitre.org"],
                    "return_images": False,
                    "return_related_questions": True
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Perplexity API error: {response.text}"
                )
            
            result = response.json()
            
            return {
                "query": request.query,
                "response": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                "citations": result.get("citations", []),
                "related_questions": result.get("related_questions", []),
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Research request timed out")
    except Exception as e:
        logger.error(f"Research error: {e}")
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")

# Background task for batch processing
async def process_batch_job(job_id: str):
    """Process a batch analysis job in the background."""
    if job_id not in jobs:
        return
    
    job = jobs[job_id]
    job["status"] = "processing"
    job["started_at"] = datetime.utcnow().isoformat()
    
    try:
        results = []
        for i, dep in enumerate(job["dependencies"]):
            try:
                if job["package_manager"] in ["pip", "poetry"]:
                    result = await check_python_package(dep)
                elif job["package_manager"] == "npm":
                    result = await check_npm_package(dep)
                else:
                    result = {"name": dep, "error": "Unsupported package manager", "success": False}
                
                results.append(result)
                job["progress"] = i + 1
                job["results"] = results
                
                # Small delay to prevent overwhelming
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing {dep} in job {job_id}: {e}")
                results.append({"name": dep, "error": str(e), "success": False})
        
        job["status"] = "completed"
        job["completed_at"] = datetime.utcnow().isoformat()
        job["results"] = results
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        job["status"] = "failed"
        job["error"] = str(e)
        job["failed_at"] = datetime.utcnow().isoformat()

# Batch research endpoint
@app.post("/research/batch")
async def batch_research(request: BatchResearchRequest, background_tasks: BackgroundTasks):
    """
    Queue a batch research job.
    Returns a job ID for polling results.
    """
    if request.api_key:
        research_service.api_key = request.api_key
    
    job_id = str(uuid4())
    jobs[job_id] = {
        "id": job_id,
        "type": "research",
        "status": "queued",
        "created_at": datetime.utcnow().isoformat(),
        "queries": request.queries,
        "model": request.model,
        "results": [],
        "progress": 0,
        "total": len(request.queries)
    }
    
    background_tasks.add_task(process_batch_research_job, job_id)
    
    return {"job_id": job_id, "status": "queued", "type": "research"}

# Background task for batch research processing
async def process_batch_research_job(job_id: str):
    """Process a batch research job in the background."""
    if job_id not in jobs:
        return
    
    job = jobs[job_id]
    job["status"] = "processing"
    job["started_at"] = datetime.utcnow().isoformat()
    
    try:
        results = []
        for i, query in enumerate(job["queries"]):
            try:
                result = await research_service.research(query, model=job["model"])
                results.append(result)
                job["progress"] = i + 1
                job["results"] = results
                
                # Small delay to prevent overwhelming the API
                await asyncio.sleep(1.0)
                
            except Exception as e:
                logger.error(f"Error researching '{query}' in job {job_id}: {e}")
                results.append({"query": query, "error": str(e), "success": False})
        
        job["status"] = "completed"
        job["completed_at"] = datetime.utcnow().isoformat()
        job["results"] = results
        
    except Exception as e:
        logger.error(f"Research job {job_id} failed: {e}")
        job["status"] = "failed"
        job["error"] = str(e)
        job["failed_at"] = datetime.utcnow().isoformat()

# List all jobs (for debugging)
@app.get("/queue")
async def list_jobs():
    """List all jobs (for debugging)."""
    return {"jobs": list(jobs.keys()), "total": len(jobs)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 