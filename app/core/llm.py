"""
LLM initialization and configuration for Azure OpenAI.
"""
from langchain_openai import AzureChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMManager:
    """Manages LLM instances and configurations."""
    
    def __init__(self):
        self._llm: BaseChatModel = None
        self._initialize_llm()
    
    def _initialize_llm(self) -> None:
        """Initialize Azure OpenAI LLM instance."""
        try:
            self._llm = AzureChatOpenAI(
                api_key=settings.azure_openai_api_key,
                azure_endpoint=settings.azure_openai_endpoint,
                api_version=settings.azure_openai_api_version,
                azure_deployment=settings.azure_openai_deployment_name,
                temperature=0.1,
                max_tokens=4000,
                streaming=True,
                verbose=settings.debug
            )
            logger.info("Azure OpenAI LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI LLM: {e}")
            raise
    
    @property
    def llm(self) -> BaseChatModel:
        """Get the LLM instance."""
        if self._llm is None:
            self._initialize_llm()
        return self._llm
    
    def get_streaming_llm(self, temperature: float = 0.1) -> BaseChatModel:
        """Get a streaming LLM with custom temperature."""
        return AzureChatOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
            azure_deployment=settings.azure_openai_deployment_name,
            temperature=temperature,
            max_tokens=4000,
            streaming=True,
            verbose=settings.debug
        )
    
    def get_non_streaming_llm(self, temperature: float = 0.1) -> BaseChatModel:
        """Get a non-streaming LLM with custom temperature."""
        return AzureChatOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
            azure_deployment=settings.azure_openai_deployment_name,
            temperature=temperature,
            max_tokens=4000,
            streaming=False,
            verbose=settings.debug
        )

# Global LLM manager instance
llm_manager = LLMManager()