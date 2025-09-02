"""
Graph state definition for LangGraph workflow.
"""
from typing import Annotated, Dict, List, Optional, Any
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    State structure for the agent workflow.
    
    This defines what information is passed between nodes in the graph.
    """
    # Conversation messages
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Current user input
    user_input: str
    
    # Agent decision making
    next_action: Optional[str]
    
    # Research and planning data
    research_data: Optional[Dict[str, Any]]
    plan: Optional[List[str]]
    
    # Tool usage tracking
    tools_used: List[str]
    tool_results: Dict[str, Any]
    
    # Conversation context
    conversation_id: Optional[str]
    user_id: Optional[str]
    
    # Agent state management
    current_agent: str
    workflow_status: str  # "in_progress", "completed", "error"
    
    # Memory and context
    working_memory: Dict[str, Any]
    long_term_memory: Optional[Dict[str, Any]]
    
    # Metadata
    timestamp: Optional[str]
    session_data: Dict[str, Any]

class ConversationState:
    """Helper class for managing conversation state."""
    
    def __init__(self, conversation_id: str, user_id: str = "default"):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.messages: List[BaseMessage] = []
        self.metadata: Dict[str, Any] = {}
    
    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)
    
    def add_human_message(self, content: str) -> None:
        """Add a human message to the conversation."""
        self.add_message(HumanMessage(content=content))
    
    def add_ai_message(self, content: str) -> None:
        """Add an AI message to the conversation."""
        self.add_message(AIMessage(content=content))
    
    def get_messages(self) -> List[BaseMessage]:
        """Get all messages in the conversation."""
        return self.messages
    
    def clear_messages(self) -> None:
        """Clear all messages in the conversation."""
        self.messages = []
    
    def to_agent_state(self, **kwargs) -> AgentState:
        """Convert to AgentState format."""
        return AgentState(
            messages=self.messages,
            user_input=kwargs.get("user_input", ""),
            next_action=kwargs.get("next_action"),
            research_data=kwargs.get("research_data"),
            plan=kwargs.get("plan"),
            tools_used=kwargs.get("tools_used", []),
            tool_results=kwargs.get("tool_results", {}),
            conversation_id=self.conversation_id,
            user_id=self.user_id,
            current_agent=kwargs.get("current_agent", "supervisor"),
            workflow_status=kwargs.get("workflow_status", "in_progress"),
            working_memory=kwargs.get("working_memory", {}),
            long_term_memory=kwargs.get("long_term_memory"),
            timestamp=kwargs.get("timestamp"),
            session_data=kwargs.get("session_data", {})
        )