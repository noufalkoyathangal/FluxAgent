"""
Pydantic response models for the API.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Agent's response to the user")
    conversation_id: str = Field(..., description="Unique conversation identifier")
    status: str = Field(..., description="Processing status (completed, error, etc.)")
    tools_used: List[str] = Field(default_factory=list, description="List of tools used by the agent")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional response metadata")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "response": "Based on my research, artificial intelligence is rapidly evolving...",
                "conversation_id": "conv_123",
                "status": "completed",
                "tools_used": ["web_search", "research"],
                "metadata": {
                    "processing_time": 3.2,
                    "sources_found": 5
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
    }

class StreamResponse(BaseModel):
    """Response model for streaming chat endpoint."""
    type: str = Field(..., description="Type of stream message (message, status, error, complete)")
    content: str = Field(..., description="Stream content")
    conversation_id: Optional[str] = Field(None, description="Conversation identifier")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Stream metadata")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Stream timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "message",
                "content": "I'm searching for information about your query...",
                "conversation_id": "conv_123",
                "metadata": {"node": "research", "step": 1},
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
    }

class AgentStatusResponse(BaseModel):
    """Response model for agent status."""
    agent_type: str = Field(..., description="Type of agent")
    status: str = Field(..., description="Current agent status")
    active_conversations: int = Field(..., description="Number of active conversations")
    total_processed: int = Field(..., description="Total messages processed")
    uptime: str = Field(..., description="Agent uptime")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "agent_type": "research",
                "status": "running",
                "active_conversations": 3,
                "total_processed": 157,
                "uptime": "2h 34m"
            }
        }
    }

class ToolExecutionResponse(BaseModel):
    """Response model for tool execution."""
    tool_name: str = Field(..., description="Name of the executed tool")
    status: str = Field(..., description="Execution status")
    result: Any = Field(..., description="Tool execution result")
    execution_time: float = Field(..., description="Execution time in seconds")
    error_message: Optional[str] = Field(None, description="Error message if execution failed")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "tool_name": "web_search",
                "status": "success",
                "result": "Found 5 relevant articles about AI trends...",
                "execution_time": 1.23,
                "error_message": None
            }
        }
    }

class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history."""
    conversation_id: str = Field(..., description="Conversation identifier")
    messages: List[Dict[str, Any]] = Field(..., description="List of conversation messages")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Conversation metadata")
    created_at: Optional[datetime] = Field(None, description="Conversation creation time")
    last_updated: Optional[datetime] = Field(None, description="Last update time")
    message_count: int = Field(..., description="Total number of messages")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "conversation_id": "conv_123",
                "messages": [
                    {"role": "user", "content": "Hello", "timestamp": "2024-01-15T10:00:00Z"},
                    {"role": "assistant", "content": "Hi! How can I help?", "timestamp": "2024-01-15T10:00:01Z"}
                ],
                "metadata": {"user_id": "user_456", "session_data": {}},
                "created_at": "2024-01-15T10:00:00Z",
                "last_updated": "2024-01-15T10:00:01Z",
                "message_count": 2
            }
        }
    }

class ErrorResponse(BaseModel):
    """Response model for API errors."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "ValidationError",
                "message": "Invalid request parameters",
                "details": {"field": "message", "issue": "Required field missing"},
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
    }

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional health details")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "service": "AI Agent API",
                "version": "1.0.0",
                "timestamp": "2024-01-15T10:30:00Z",
                "details": {
                    "database": "connected",
                    "llm": "operational",
                    "memory_usage": "45%"
                }
            }
        }
    }