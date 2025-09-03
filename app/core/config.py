"""
Configuration settings for the AI Agent application.
"""
import os
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # Application
        self.app_name: str = os.getenv("APP_NAME", "AI Agent Project")
        self.app_version: str = os.getenv("APP_VERSION", "1.0.0")
        self.debug: bool = os.getenv("DEBUG", "True").lower() == "true"
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Azure OpenAI - Required
        self.azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
        self.azure_openai_deployment_name: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
        
        # FastAPI
        self.fastapi_host: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
        self.fastapi_port: int = int(os.getenv("FASTAPI_PORT", "8000"))
        
        # Streamlit
        self.streamlit_host: str = os.getenv("STREAMLIT_HOST", "0.0.0.0")
        self.streamlit_port: int = int(os.getenv("STREAMLIT_PORT", "8501"))
        
        # Database
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./ai_agent.db")
        
        # Optional APIs
        self.tavily_api_key: Optional[str] = os.getenv("TAVILY_API_KEY")
        self.serpapi_key: Optional[str] = os.getenv("SERPAPI_KEY")
        
        # Security
        self.secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8501")
        self.cors_origins: List[str] = [origin.strip() for origin in cors_origins_str.split(",")]
    
    def validate_azure_config(self) -> bool:
        """Validate that required Azure OpenAI configuration is present."""
        return bool(
            self.azure_openai_api_key and 
            self.azure_openai_endpoint and 
            self.azure_openai_deployment_name
        )

# Global settings instance
settings = Settings()