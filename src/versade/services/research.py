"""
Research service for Perplexity API integration.
Provides deep research capabilities for dependency analysis.
"""

import logging
import os
from typing import Dict, List, Optional

import httpx

logger = logging.getLogger("versade.services.research")


class PerplexityResearchService:
    """
    Service for conducting research using Perplexity API.
    
    Available models:
    - sonar-deep-research (128k) - Best for comprehensive research
    - sonar-reasoning-pro (128k) - Advanced reasoning capabilities  
    - sonar-reasoning (128k) - Standard reasoning
    - sonar-pro (200k) - High-quality with large context
    - sonar (128k) - Standard model
    - r1-1776 (128k) - Specialized model
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the research service."""
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        self.base_url = "https://api.perplexity.ai/chat/completions"
        
    async def research(
        self, 
        query: str, 
        model: str = "sonar-pro",
        max_tokens: int = 1000,
        temperature: float = 0.2
    ) -> Dict:
        """
        Conduct research using Perplexity API.
        
        Args:
            query: The research question
            model: The Perplexity model to use
            max_tokens: Maximum tokens in response
            temperature: Response creativity (0.0-1.0)
            
        Returns:
            Dictionary containing research results
            
        Raises:
            ValueError: If API key is missing
            httpx.HTTPError: If API request fails
        """
        if not self.api_key:
            raise ValueError("Perplexity API key required. Set PERPLEXITY_API_KEY env var.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful research assistant specializing in software dependencies, security, and package management. Provide comprehensive, accurate information with sources."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "return_citations": True,
            "search_domain_filter": [
                "github.com", 
                "pypi.org", 
                "npmjs.com", 
                "cve.mitre.org",
                "snyk.io",
                "security.snyk.io"
            ],
            "return_images": False,
            "return_related_questions": True
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            return {
                "query": query,
                "response": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                "citations": result.get("citations", []),
                "related_questions": result.get("related_questions", []),
                "model": model,
                "usage": result.get("usage", {})
            }
    
    async def research_package_security(self, package_name: str, package_manager: str = "pip") -> Dict:
        """
        Research security information for a specific package.
        
        Args:
            package_name: Name of the package
            package_manager: Package manager (pip, npm)
            
        Returns:
            Security research results
        """
        query = f"""
        Research the security status of the {package_manager} package '{package_name}':
        
        1. Are there any known security vulnerabilities (CVEs)?
        2. What is the maintenance status and activity level?
        3. Are there any security best practices for using this package?
        4. Are there any safer alternatives if security concerns exist?
        5. What is the package's reputation in the community?
        
        Please provide specific, actionable information with sources.
        """
        
        return await self.research(query)
    
    async def research_dependency_update(self, package_name: str, current_version: str, latest_version: str) -> Dict:
        """
        Research the implications of updating a dependency.
        
        Args:
            package_name: Name of the package
            current_version: Current version
            latest_version: Latest available version
            
        Returns:
            Update research results
        """
        query = f"""
        Research updating the package '{package_name}' from version {current_version} to {latest_version}:
        
        1. What are the breaking changes between these versions?
        2. Are there any security fixes in the newer version?
        3. What is the migration effort required?
        4. Are there any known issues with the latest version?
        5. What testing should be done before updating?
        
        Please provide specific guidance for this version upgrade.
        """
        
        return await self.research(query)


# Global instance for easy access
research_service = PerplexityResearchService() 