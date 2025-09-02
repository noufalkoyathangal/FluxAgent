"""
Pydantic request models for the API.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User message to process")
    conversation_id: Optional[str] = Field(None, description="Unique conversation identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "What are the latest trends in AI technology?",
                "conversation_id": "conv_123",
                "user_id": "user_456",
                "context": {"source": "web_ui"}
            }
        }
    }

class StreamChatRequest(BaseModel):
    """Request model for streaming chat endpoint."""
    message: str = Field(..., description="User message to process")
    conversation_id: Optional[str] = Field(None, description="Unique conversation identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    stream_type: str = Field(default="all", description="Type of streaming (all, final, steps)")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Research the latest developments in quantum computing",
                "conversation_id": "conv_123",
                "user_id": "user_456",
                "stream_type": "all"
            }
        }
    }

class AgentConfigRequest(BaseModel):
    """Request model for agent configuration."""
    agent_type: str = Field(..., description="Type of agent to configure")
    config: Dict[str, Any] = Field(..., description="Agent configuration parameters")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "agent_type": "research",
                "config": {
                    "max_search_results": 10,
                    "search_depth": "advanced",
                    "include_sources": True
                }
            }
        }
    }

class ToolExecutionRequest(BaseModel):
    """Request model for direct tool execution."""
    tool_name: str = Field(..., description="Name of the tool to execute")
    parameters: Dict[str, Any] = Field(..., description="Tool parameters")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Execution context")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "tool_name": "web_search",
                "parameters": {
                    "query": "latest AI research papers",
                    "max_results": 5
                },
                "context": {"user_id": "user_123"}
            }
        }
    }