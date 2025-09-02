"""
Chat API routes for the AI agent system.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional
import json
import asyncio
import logging

from app.api.models.requests import ChatRequest, StreamChatRequest
from app.api.models.responses import ChatResponse, StreamResponse
from app.graph.workflow import workflow

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message through the AI agent workflow.
    
    This endpoint processes user messages and returns a complete response
    after the agent workflow completes.
    """
    try:
        logger.info(f"Processing chat request for conversation: {request.conversation_id}")
        
        # Process the message through the workflow
        result = await workflow.process_message(
            user_input=request.message,
            conversation_id=request.conversation_id or "default",
            user_id=request.user_id or "default"
        )
        
        response = ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            status=result["status"],
            tools_used=result.get("tools_used", []),
            metadata={
                "research_data": result.get("research_data"),
                "processing_time": None  # You can add timing if needed
            }
        )
        
        logger.info(f"Chat request processed successfully: {request.conversation_id}")
        return response
        
    except Exception as e:
        logger.error(f"Chat processing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/stream")
async def stream_chat(request: StreamChatRequest):
    """
    Stream a chat conversation through the AI agent workflow.
    
    This endpoint provides real-time streaming of the agent's processing steps.
    """
    try:
        logger.info(f"Starting stream chat for conversation: {request.conversation_id}")
        
        async def generate_stream():
            try:
                async for chunk in workflow.stream_process_message(
                    user_input=request.message,
                    conversation_id=request.conversation_id or "default",
                    user_id=request.user_id or "default"
                ):
                    # Format the chunk for SSE
                    if isinstance(chunk, dict):
                        if "error" in chunk:
                            stream_response = StreamResponse(
                                type="error",
                                content=chunk["error"],
                                conversation_id=request.conversation_id
                            )
                        else:
                            # Extract the current node and its output
                            node_name = list(chunk.keys())[0] if chunk else "unknown"
                            node_data = chunk.get(node_name, {})
                            
                            # Determine the content type
                            if "messages" in node_data:
                                messages = node_data["messages"]
                                if messages and isinstance(messages[-1], dict):
                                    content = messages[-1].get("content", "")
                                    stream_response = StreamResponse(
                                        type="message",
                                        content=content,
                                        conversation_id=request.conversation_id,
                                        metadata={
                                            "node": node_name,
                                            "status": node_data.get("workflow_status", "processing")
                                        }
                                    )
                                else:
                                    continue
                            else:
                                stream_response = StreamResponse(
                                    type="status",
                                    content=f"Processing with {node_name}...",
                                    conversation_id=request.conversation_id,
                                    metadata={"node": node_name}
                                )
                        
                        # Send the formatted response
                        yield f"data: {stream_response.model_dump_json()}\n\n"
                
                # Send completion signal
                completion_response = StreamResponse(
                    type="complete",
                    content="",
                    conversation_id=request.conversation_id
                )
                yield f"data: {completion_response.model_dump_json()}\n\n"
                
            except Exception as e:
                logger.error(f"Stream generation error: {e}", exc_info=True)
                error_response = StreamResponse(
                    type="error",
                    content=str(e),
                    conversation_id=request.conversation_id
                )
                yield f"data: {error_response.model_dump_json()}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            }
        )
        
    except Exception as e:
        logger.error(f"Stream chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history/{conversation_id}")
async def get_chat_history(conversation_id: str):
    """
    Get chat history for a specific conversation.
    
    Note: This is a placeholder. In a real application, you would
    retrieve this from a database or the workflow's memory system.
    """
    try:
        # This would typically fetch from a database
        # For now, return a placeholder response
        return {
            "conversation_id": conversation_id,
            "messages": [],
            "metadata": {
                "created_at": None,
                "last_updated": None,
                "message_count": 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching chat history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/chat/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete a conversation and its history.
    
    Note: This is a placeholder. In a real application, you would
    delete from a database and clear the workflow's memory.
    """
    try:
        # This would typically delete from a database
        # and clear memory checkpoints
        logger.info(f"Deleting conversation: {conversation_id}")
        
        return {
            "message": f"Conversation {conversation_id} deleted successfully",
            "conversation_id": conversation_id
        }
        
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))