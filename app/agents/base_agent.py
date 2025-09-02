# ai_agent_project/app/agents/base_agent.py

from abc import ABC, abstractmethod
from app.graph.state import AgentState

class BaseAgent(ABC):
    """Abstract base class for all agents."""
    @abstractmethod
    async def run(self, state: AgentState) -> AgentState:
        pass
