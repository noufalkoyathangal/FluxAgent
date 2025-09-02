"""
LangGraph workflow definition for the AI agent system.
"""
from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.graph.state import AgentState
from app.agents.research_agent import ResearchAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.core.llm import llm_manager
import logging

logger = logging.getLogger(__name__)

class AgentWorkflow:
    """Main workflow orchestrator using LangGraph."""
    
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.supervisor_agent = SupervisorAgent()
        self.memory = MemorySaver()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        # Create the state graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("research", self._research_node)
        workflow.add_node("respond", self._respond_node)
        
        # Set entry point
        workflow.set_entry_point("supervisor")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "supervisor",
            self._route_supervisor,
            {
                "research": "research",
                "respond": "respond",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "research",
            self._route_after_research,
            {
                "respond": "respond",
                "end": END
            }
        )
        
        # Response node always ends
        workflow.add_edge("respond", END)
        
        # Compile the graph with memory
        return workflow.compile(checkpointer=self.memory)
    
    async def _supervisor_node(self, state: AgentState) -> AgentState:
        """Supervisor node that decides the next action."""
        try:
            logger.info("Supervisor node activated")
            return await self.supervisor_agent.decide_action(state)
        except Exception as e:
            logger.error(f"Supervisor node error: {e}")
            state["workflow_status"] = "error"
            state["messages"].append({
                "role": "assistant",
                "content": f"Supervisor error: {str(e)}"
            })
            return state
    
    async def _research_node(self, state: AgentState) -> AgentState:
        """Research node for information gathering."""
        try:
            logger.info("Research node activated")
            return await self.research_agent.research(state)
        except Exception as e:
            logger.error(f"Research node error: {e}")
            state["workflow_status"] = "error"
            state["messages"].append({
                "role": "assistant", 
                "content": f"Research error: {str(e)}"
            })
            return state
    
    async def _respond_node(self, state: AgentState) -> AgentState:
        """Final response node."""
        try:
            logger.info("Response node activated")
            
            # Generate final response based on research and context
            if state.get("research_data"):
                # Use research data to generate response
                synthesis = state["research_data"].get("synthesis", "")
                if synthesis:
                    state["messages"].append({
                        "role": "assistant",
                        "content": synthesis
                    })
            else:
                # Generate direct response
                llm = llm_manager.llm
                user_input = state.get("user_input", "")
                
                response = await llm.ainvoke([
                    {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses."},
                    {"role": "user", "content": user_input}
                ])
                
                state["messages"].append({
                    "role": "assistant",
                    "content": response.content
                })
            
            state["workflow_status"] = "completed"
            state["current_agent"] = "respond"
            
            logger.info("Response generated successfully")
            return state
            
        except Exception as e:
            logger.error(f"Response node error: {e}")
            state["workflow_status"] = "error"
            state["messages"].append({
                "role": "assistant",
                "content": f"Response generation error: {str(e)}"
            })
            return state
    
    def _route_supervisor(self, state: AgentState) -> Literal["research", "respond", "end"]:
        """Route after supervisor decision."""
        next_action = state.get("next_action", "respond")
        
        if next_action == "research":
            return "research"
        elif next_action == "respond":
            return "respond"
        else:
            return "end"
    
    def _route_after_research(self, state: AgentState) -> Literal["respond", "end"]:
        """Route after research completion."""
        if state.get("workflow_status") == "error":
            return "end"
        return "respond"
    
    async def process_message(self, user_input: str, conversation_id: str = "default", user_id: str = "default") -> Dict[str, Any]:
        """Process a user message through the workflow."""
        try:
            # Initialize state
            initial_state = AgentState(
                messages=[{"role": "user", "content": user_input}],
                user_input=user_input,
                next_action=None,
                research_data=None,
                plan=None,
                tools_used=[],
                tool_results={},
                conversation_id=conversation_id,
                user_id=user_id,
                current_agent="supervisor",
                workflow_status="in_progress",
                working_memory={},
                long_term_memory=None,
                timestamp=None,
                session_data={}
            )
            
            # Configure the graph run
            config = {
                "configurable": {
                    "thread_id": conversation_id,
                    "user_id": user_id
                }
            }
            
            # Run the graph
            final_state = await self.graph.ainvoke(initial_state, config)
            
            # Extract response
            messages = final_state.get("messages", [])
            latest_message = messages[-1] if messages else {"content": "No response generated"}
            
            return {
                "response": latest_message.get("content", ""),
                "status": final_state.get("workflow_status", "completed"),
                "tools_used": final_state.get("tools_used", []),
                "research_data": final_state.get("research_data"),
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            logger.error(f"Workflow processing error: {e}")
            return {
                "response": f"Workflow error: {str(e)}",
                "status": "error",
                "tools_used": [],
                "research_data": None,
                "conversation_id": conversation_id
            }
    
    async def stream_process_message(self, user_input: str, conversation_id: str = "default", user_id: str = "default"):
        """Stream process a user message through the workflow."""
        try:
            # Initialize state
            initial_state = AgentState(
                messages=[{"role": "user", "content": user_input}],
                user_input=user_input,
                next_action=None,
                research_data=None,
                plan=None,
                tools_used=[],
                tool_results={},
                conversation_id=conversation_id,
                user_id=user_id,
                current_agent="supervisor",
                workflow_status="in_progress",
                working_memory={},
                long_term_memory=None,
                timestamp=None,
                session_data={}
            )
            
            # Configure the graph run
            config = {
                "configurable": {
                    "thread_id": conversation_id,
                    "user_id": user_id
                }
            }
            
            # Stream the graph execution
            async for chunk in self.graph.astream(initial_state, config):
                yield chunk
                
        except Exception as e:
            logger.error(f"Workflow streaming error: {e}")
            yield {"error": str(e)}

# Global workflow instance
workflow = AgentWorkflow()