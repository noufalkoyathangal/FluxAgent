"""
Minimal FastAPI main application file.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# Simple settings without pydantic-settings
import os
from dotenv import load_dotenv

load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="AI Agent Project",
    version="1.0.0",
    description="An intelligent AI agent system built with LangGraph, FastAPI, and Azure OpenAI"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8501", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AI Agent Project",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Agent Project",
        "version": "1.0.0"
    }

@app.post("/api/v1/chat")
async def chat_endpoint(message: dict):
    """Simple chat endpoint."""
    user_message = message.get("message", "")
    
    return {
        "response": f"Echo: {user_message}",
        "conversation_id": message.get("conversation_id", "default"),
        "status": "completed",
        "tools_used": [],
        "metadata": {}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)