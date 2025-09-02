"""
Web search tool for the AI agent.
"""
import json
import httpx
from typing import Dict, Any, Optional, List
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class WebSearchInput(BaseModel):
    """Input schema for web search tool."""
    query: str = Field(description="Search query to find information on the web")
    max_results: int = Field(default=5, description="Maximum number of search results to return")

class WebSearchTool(BaseTool):
    """Tool for searching the web and returning relevant information."""
    
    name: str = "web_search"
    description: str = """
    Search the web for current information on any topic.
    Use this when you need to find recent information, news, or data that might not be in your training.
    """
    args_schema: type[BaseModel] = WebSearchInput
    
    def _run(self, query: str, max_results: int = 5) -> str:
        """Execute the web search."""
        try:
            # Using DuckDuckGo as a fallback search engine
            return self._duckduckgo_search(query, max_results)
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return f"Web search failed: {str(e)}"
    
    async def _arun(self, query: str, max_results: int = 5) -> str:
        """Async version of the web search."""
        return self._run(query, max_results)
    
    def _duckduckgo_search(self, query: str, max_results: int) -> str:
        """Perform search using DuckDuckGo."""
        try:
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                search_results = list(ddgs.text(query, max_results=max_results))
                
                for result in search_results:
                    results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("body", ""),
                        "link": result.get("href", "")
                    })
            
            # Format results for the agent
            formatted_results = "Web Search Results:\n\n"
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. **{result['title']}**\n"
                formatted_results += f"   {result['snippet']}\n"
                formatted_results += f"   Source: {result['link']}\n\n"
            
            return formatted_results if results else "No search results found."
            
        except ImportError:
            logger.warning("duckduckgo-search not installed, using fallback method")
            return self._fallback_search(query)
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return f"Search failed: {str(e)}"
    
    def _fallback_search(self, query: str) -> str:
        """Fallback search method when DuckDuckGo is not available."""
        return f"Web search for '{query}' is currently unavailable. Please install the duckduckgo-search package or configure an alternative search API."

class TavilySearchTool(BaseTool):
    """Tool for searching the web using Tavily API."""
    
    name: str = "tavily_search"
    description: str = """
    Advanced web search using Tavily API for high-quality, recent information.
    Provides more detailed and accurate results than basic web search.
    """
    args_schema: type[BaseModel] = WebSearchInput
    
    def _run(self, query: str, max_results: int = 5) -> str:
        """Execute Tavily search."""
        if not settings.tavily_api_key:
            return "Tavily API key not configured. Please set TAVILY_API_KEY in your environment."
        
        try:
            url = "https://api.tavily.com/search"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "api_key": settings.tavily_api_key,
                "query": query,
                "search_depth": "advanced",
                "include_answer": True,
                "include_raw_content": False,
                "max_results": max_results
            }
            
            with httpx.Client() as client:
                response = client.post(url, headers=headers, json=data)
                response.raise_for_status()
                
                result = response.json()
                return self._format_tavily_results(result)
                
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            return f"Tavily search failed: {str(e)}"
    
    async def _arun(self, query: str, max_results: int = 5) -> str:
        """Async version of Tavily search."""
        return self._run(query, max_results)
    
    def _format_tavily_results(self, result: Dict[str, Any]) -> str:
        """Format Tavily search results."""
        formatted = "Tavily Search Results:\n\n"
        
        # Add answer if available
        if result.get("answer"):
            formatted += f"**Answer:** {result['answer']}\n\n"
        
        # Add search results
        for i, item in enumerate(result.get("results", []), 1):
            formatted += f"{i}. **{item.get('title', 'No title')}**\n"
            formatted += f"   {item.get('content', 'No content')}\n"
            formatted += f"   Source: {item.get('url', 'No URL')}\n\n"
        
        return formatted

def get_web_search_tools() -> List[BaseTool]:
    """Get available web search tools."""
    tools = [WebSearchTool()]
    
    # Add Tavily if API key is available
    if settings.tavily_api_key:
        tools.append(TavilySearchTool())
    
    return tools