"""
Research agent for gathering and analyzing information.
"""
from typing import Dict, List, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.core.llm import llm_manager
from app.tools.web_search import get_web_search_tools
from app.graph.state import AgentState
import logging

logger = logging.getLogger(__name__)

class ResearchAgent:
    """Agent specialized in research and information gathering."""
    
    def __init__(self):
        self.llm = llm_manager.llm
        self.tools = get_web_search_tools()
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for the research agent."""
        return """
        You are a Research Agent, an expert at gathering, analyzing, and synthesizing information.
        
        Your responsibilities:
        1. Conduct thorough research on given topics
        2. Use web search tools to find current and relevant information
        3. Analyze and synthesize information from multiple sources
        4. Present findings in a clear, organized manner
        5. Identify reliable sources and fact-check information
        
        Guidelines:
        - Always use web search tools for current information
        - Cross-reference information from multiple sources when possible
        - Clearly distinguish between facts and opinions
        - Cite sources when presenting information
        - Be thorough but concise in your research
        - Flag any conflicting information you find
        
        You have access to the following tools: {tools}
        
        When conducting research:
        1. Break down complex topics into specific search queries
        2. Search for the most recent and reliable information
        3. Look for multiple perspectives on controversial topics
        4. Summarize findings with proper attribution
        """
    
    async def research(self, state: AgentState) -> AgentState:
        """Conduct research based on the current state and user query."""
        try:
            user_query = state["user_input"]
            logger.info(f"Research agent processing query: {user_query}")
            
            # Create the research prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt.format(
                    tools=", ".join([tool.name for tool in self.tools])
                )),
                MessagesPlaceholder(variable_name="messages"),
                ("human", f"Please research the following topic: {user_query}")
            ])
            
            # Bind tools to the LLM
            llm_with_tools = self.llm.bind_tools(self.tools)
            
            # Create the research chain
            research_chain = prompt | llm_with_tools
            
            # Execute research
            messages = state.get("messages", [])
            response = await research_chain.ainvoke({"messages": messages})
            
            # Process tool calls if any
            research_results = []
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    
                    # Find and execute the tool
                    for tool in self.tools:
                        if tool.name == tool_name:
                            try:
                                result = await tool._arun(**tool_args)
                                research_results.append({
                                    "tool": tool_name,
                                    "query": tool_args,
                                    "result": result
                                })
                                logger.info(f"Tool {tool_name} executed successfully")
                            except Exception as e:
                                logger.error(f"Tool {tool_name} failed: {e}")
                                research_results.append({
                                    "tool": tool_name,
                                    "query": tool_args,
                                    "error": str(e)
                                })
                            break
            
            # Synthesize research results
            synthesis_prompt = self._create_synthesis_prompt(user_query, research_results)
            synthesis_response = await self.llm.ainvoke([
                SystemMessage(content="You are an expert research analyst. Synthesize the following research results into a comprehensive and well-organized response."),
                HumanMessage(content=synthesis_prompt)
            ])
            
            # Update state
            updated_state = state.copy()
            updated_state["research_data"] = {
                "query": user_query,
                "raw_results": research_results,
                "synthesis": synthesis_response.content
            }
            updated_state["messages"].append(AIMessage(content=synthesis_response.content))
            updated_state["tools_used"].extend([result.get("tool", "") for result in research_results])
            updated_state["current_agent"] = "research"
            
            logger.info("Research completed successfully")
            return updated_state
            
        except Exception as e:
            logger.error(f"Research agent error: {e}")
            error_message = f"Research failed: {str(e)}"
            
            updated_state = state.copy()
            updated_state["messages"].append(AIMessage(content=error_message))
            updated_state["workflow_status"] = "error"
            return updated_state
    
    def _create_synthesis_prompt(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Create a prompt for synthesizing research results."""
        prompt = f"Original Query: {query}\n\nResearch Results:\n\n"
        
        for i, result in enumerate(results, 1):
            if "error" in result:
                prompt += f"Result {i}: Error - {result['error']}\n\n"
            else:
                prompt += f"Result {i} (Tool: {result['tool']}):\n"
                prompt += f"Query: {result['query']}\n"
                prompt += f"Result: {result['result']}\n\n"
        
        prompt += """
        Please provide a comprehensive synthesis of the research results above. Include:
        1. A clear summary of the key findings
        2. Analysis of any patterns or trends
        3. Identification of reliable sources
        4. Any conflicting information found
        5. Actionable insights or recommendations
        6. Areas where further research might be needed
        
        Format your response in a clear, well-structured manner with proper citations where applicable.
        """
        
        return prompt
    
    def should_research(self, state: AgentState) -> bool:
        """Determine if research is needed based on the current state."""
        user_input = state.get("user_input", "").lower()
        
        # Keywords that suggest research is needed
        research_keywords = [
            "search", "find", "research", "information", "latest", "current",
            "recent", "news", "data", "statistics", "facts", "what is",
            "how to", "explain", "tell me about", "learn", "discover"
        ]
        
        return any(keyword in user_input for keyword in research_keywords)