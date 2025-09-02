"""
Configuration settings for the AI Agent application.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "AI Agent Project"
    app_version: str = "1.0.0"
    debug: bool = True
    log_level: str = "INFO"
    
    # Azure OpenAI
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str = "2024-02-01"
    azure_openai_deployment_name: str
    
    # FastAPI
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    
    # Streamlit
    streamlit_host: str = "0.0.0.0"
    streamlit_port: int = 8501
    
    # Database
    database_url: str = "sqlite:///./ai_agent.db"
    
    # Optional APIs
    tavily_api_key: Optional[str] = None
    serpapi_key: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8501"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()