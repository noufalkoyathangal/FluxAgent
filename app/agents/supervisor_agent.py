"""
Supervisor agent for coordinating the multi-agent workflow.
"""
from typing import Dict, Any, Literal
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from app.core.llm import llm_manager
from app.graph.state import AgentState
import logging

logger = logging.getLogger(__name__)

class SupervisorAgent:
    """Supervisor agent that coordinates the workflow and decides next actions."""
    
    def __init__(self):
        self.llm = llm_manager.get_non_streaming_llm()
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for the supervisor agent."""
        return """
        You are a Supervisor Agent responsible for coordinating a multi-agent AI system.
        
        Your role is to analyze user requests and decide which agent should handle the task:
        
        Available agents:
        1. RESEARCH - For gathering information, web searches, fact-finding, and analysis
        2. RESPOND - For direct responses that don't require external information
        
        Guidelines for decision making:
        - Use RESEARCH when the user asks for:
          * Current information, news, or recent developments
          * Facts that need verification or sourcing
          * Comparative analysis requiring multiple sources
          * Questions containing words like "latest," "current," "recent," "find," "search"
          * Technical information that benefits from multiple perspectives
        
        - Use RESPOND when:
          * The question can be answered with general knowledge
          * It's a simple explanation or definition
          * It's a creative task like writing or brainstorming
          * It's a personal opinion or advice
          * No external information is needed
        
        Decision format:
        - If research is needed: Return "research"
        - If direct response is sufficient: Return "respond"
        
        Be decisive and clear in your choice. Consider the user's specific needs and the most appropriate workflow.
        """
    
    async def decide_action(self, state: AgentState) -> AgentState:
        """Decide the next action based on the user input and current state."""
        try:
            user_input = state.get("user_input", "")
            logger.info(f"Supervisor analyzing request: {user_input}")
            
            # Create decision prompt
            decision_prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("human", f"""
                Analyze this user request and decide which agent should handle it:
                
                User Request: "{user_input}"
                
                Consider:
                - Does this need current/recent information?
                - Would web search improve the answer?
                - Can this be answered with existing knowledge?
                
                Respond with only one word: "research" or "respond"
                """)
            ])
            
            # Get decision from LLM
            chain = decision_prompt | self.llm
            response = await chain.ainvoke({})
            
            # Extract decision
            decision = response.content.strip().lower()
            
            # Validate and set decision
            if decision in ["research", "respond"]:
                next_action = decision
            else:
                # Default fallback logic
                next_action = self._fallback_decision(user_input)
            
            logger.info(f"Supervisor decision: {next_action}")
            
            # Update state
            updated_state = state.copy()
            updated_state["next_action"] = next_action
            updated_state["current_agent"] = "supervisor"
            
            # Add supervisor reasoning to working memory
            updated_state["working_memory"]["supervisor_decision"] = {
                "decision": next_action,
                "reasoning": f"Analyzed request: '{user_input}' -> {next_action}",
                "user_input": user_input
            }
            
            return updated_state
            
        except Exception as e:
            logger.error(f"Supervisor decision error: {e}")
            # Fallback decision
            updated_state = state.copy()
            updated_state["next_action"] = self._fallback_decision(state.get("user_input", ""))
            updated_state["workflow_status"] = "error"
            return updated_state
    
    def _fallback_decision(self, user_input: str) -> str:
        """Fallback decision logic when LLM fails."""
        # Simple keyword-based fallback
        research_keywords = [
            "search", "find", "research", "latest", "current", "recent", 
            "news", "what is", "information", "data", "statistics",
            "compare", "versus", "vs", "trends", "developments"
        ]
        
        user_lower = user_input.lower()
        
        # Check if any research keywords are present
        for keyword in research_keywords:
            if keyword in user_lower:
                return "research"
        
        # Default to respond for general queries
        return "respond"
    
    def should_continue(self, state: AgentState) -> Literal["research", "respond", "end"]:
        """Determine if the workflow should continue and where to route next."""
        next_action = state.get("next_action")
        workflow_status = state.get("workflow_status", "in_progress")
        
        if workflow_status == "error":
            return "end"
        
        if next_action == "research":
            return "research"
        elif next_action == "respond":
            return "respond"
        else:
            return "end"