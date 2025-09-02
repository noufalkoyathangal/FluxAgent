"""
Main Streamlit application for the AI Agent interface.
"""
import streamlit as st
import httpx
import json
import asyncio
from typing import Dict, Any, Optional
import time
import uuid

# Page configuration
st.set_page_config(
    page_title="AI Agent Assistant", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
    }
    
    .agent-status {
        background-color: #fff3e0;
        border: 1px solid #ff9800;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .tools-used {
        background-color: #f3e5f5;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

class AIAgentUI:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = str(uuid.uuid4())
        
        if "user_id" not in st.session_state:
            st.session_state.user_id = "streamlit_user"
        
        if "api_status" not in st.session_state:
            st.session_state.api_status = None
    
    def check_api_status(self) -> bool:
        """Check if the FastAPI backend is running."""
        try:
            response = httpx.get(f"{API_BASE_URL.replace('/api/v1', '')}/health", timeout=5.0)
            if response.status_code == 200:
                st.session_state.api_status = "connected"
                return True
        except Exception:
            pass
        
        st.session_state.api_status = "disconnected"
        return False
    
    def send_message(self, message: str, use_streaming: bool = False) -> Optional[Dict[str, Any]]:
        """Send a message to the AI agent API."""
        try:
            if use_streaming:
                return self.send_streaming_message(message)
            else:
                response = httpx.post(
                    f"{API_BASE_URL}/chat",
                    json={
                        "message": message,
                        "conversation_id": st.session_state.conversation_id,
                        "user_id": st.session_state.user_id
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
                    return None
        
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None
    
    def send_streaming_message(self, message: str):
        """Send a streaming message to the AI agent API."""
        try:
            with httpx.stream(
                "POST",
                f"{API_BASE_URL}/chat/stream",
                json={
                    "message": message,
                    "conversation_id": st.session_state.conversation_id,
                    "user_id": st.session_state.user_id,
                    "stream_type": "all"
                },
                timeout=60.0
            ) as response:
                if response.status_code == 200:
                    # Create a placeholder for streaming content
                    placeholder = st.empty()
                    full_response = ""
                    
                    for line in response.iter_lines():
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])  # Remove "data: " prefix
                                
                                if data.get("type") == "message":
                                    content = data.get("content", "")
                                    if content:
                                        full_response = content
                                        placeholder.markdown(f"**Assistant:** {full_response}")
                                
                                elif data.get("type") == "status":
                                    status_content = data.get("content", "")
                                    if status_content:
                                        with st.container():
                                            st.markdown(f'<div class="agent-status">🔄 {status_content}</div>', unsafe_allow_html=True)
                                
                                elif data.get("type") == "complete":
                                    break
                                
                                elif data.get("type") == "error":
                                    st.error(f"Agent Error: {data.get('content', 'Unknown error')}")
                                    return None
                            
                            except json.JSONDecodeError:
                                continue
                    
                    # Clear the placeholder and return the final response
                    placeholder.empty()
                    return {"response": full_response, "status": "completed"}
                
                else:
                    st.error(f"Streaming API Error: {response.status_code}")
                    return None
        
        except Exception as e:
            st.error(f"Streaming error: {str(e)}")
            return None
    
    def render_sidebar(self):
        """Render the sidebar with configuration options."""
        with st.sidebar:
            st.header("🤖 AI Agent Settings")
            
            # API Status
            api_connected = self.check_api_status()
            status_color = "🟢" if api_connected else "🔴"
            status_text = "Connected" if api_connected else "Disconnected"
            st.markdown(f"**API Status:** {status_color} {status_text}")
            
            if not api_connected:
                st.warning("FastAPI backend is not running. Please start the server first.")
                if st.button("🔄 Refresh Status"):
                    st.rerun()
            
            st.divider()
            
            # Conversation Settings
            st.subheader("💬 Conversation")
            
            # Display current conversation ID
            st.text(f"ID: {st.session_state.conversation_id[:8]}...")
            
            # New conversation button
            if st.button("🆕 New Conversation"):
                st.session_state.messages = []
                st.session_state.conversation_id = str(uuid.uuid4())
                st.rerun()
            
            # Clear history button
            if st.button("🗑️ Clear History"):
                st.session_state.messages = []
                st.rerun()
            
            st.divider()
            
            # Agent Settings
            st.subheader("⚙️ Agent Options")
            
            # Streaming toggle
            use_streaming = st.checkbox("Enable Streaming", value=True, 
                                      help="Show agent processing steps in real-time")
            
            # Model temperature (placeholder for future enhancement)
            temperature = st.slider("Response Creativity", 0.0, 1.0, 0.1, 0.1,
                                  help="Higher values make responses more creative")
            
            # Max tokens (placeholder for future enhancement)
            max_tokens = st.slider("Max Response Length", 100, 4000, 2000, 100)
            
            st.divider()
            
            # Agent Information
            st.subheader("ℹ️ About")
            st.markdown("""
            This AI Agent uses:
            - **LangGraph** for workflow orchestration
            - **Azure OpenAI** for language processing
            - **FastAPI** for backend services
            - **Streamlit** for the user interface
            
            The agent can:
            - 🔍 Search the web for current information
            - 🧠 Conduct research and analysis
            - 💬 Maintain conversation context
            - 🛠️ Use multiple specialized tools
            """)
            
            return {
                "use_streaming": use_streaming,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "api_connected": api_connected
            }
    
    def render_chat_interface(self, settings: Dict[str, Any]):
        """Render the main chat interface."""
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>🤖 AI Agent Assistant</h1>
            <p>Powered by LangGraph, Azure OpenAI & FastAPI</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display conversation messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>🧑 You:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            
            elif message["role"] == "assistant":
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Assistant:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
                
                # Show tools used if available
                if "tools_used" in message and message["tools_used"]:
                    tools_list = ", ".join(message["tools_used"])
                    st.markdown(f"""
                    <div class="tools-used">
                        🛠️ <strong>Tools used:</strong> {tools_list}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        if settings["api_connected"]:
            # Use chat_input for better UX
            if prompt := st.chat_input("Ask me anything..."):
                self.handle_user_input(prompt, settings)
        else:
            st.error("⚠️ Cannot send messages. API backend is not available.")
            st.info("💡 Please start the FastAPI server by running: `python -m uvicorn app.api.main:app --reload`")
    
    def handle_user_input(self, user_input: str, settings: Dict[str, Any]):
        """Handle user input and get agent response."""
        # Add user message to session state
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input
        })
        
        # Show user message immediately
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🧑 You:</strong><br>
            {user_input}
        </div>
        """, unsafe_allow_html=True)
        
        # Get agent response
        with st.spinner("🤖 Agent is thinking..."):
            response_data = self.send_message(user_input, settings["use_streaming"])
        
        if response_data:
            assistant_message = {
                "role": "assistant",
                "content": response_data.get("response", "No response generated."),
                "tools_used": response_data.get("tools_used", []),
                "status": response_data.get("status", "unknown")
            }
            
            # Add to session state
            st.session_state.messages.append(assistant_message)
            
            # Display assistant response
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Assistant:</strong><br>
                {assistant_message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Show tools used
            if assistant_message["tools_used"]:
                tools_list = ", ".join(assistant_message["tools_used"])
                st.markdown(f"""
                <div class="tools-used">
                    🛠️ <strong>Tools used:</strong> {tools_list}
                </div>
                """, unsafe_allow_html=True)
        
        # Force a rerun to update the interface
        st.rerun()
    
    def render_example_queries(self):
        """Render example queries for users to try."""
        with st.expander("💡 Example Queries to Try"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔍 Research & Analysis:**")
                example_queries_1 = [
                    "What are the latest trends in artificial intelligence?",
                    "Research the current state of quantum computing",
                    "Find information about sustainable energy solutions",
                    "What are the recent developments in space exploration?"
                ]
                
                for query in example_queries_1:
                    if st.button(f"📝 {query}", key=f"example1_{hash(query)}"):
                        st.session_state.example_query = query
            
            with col2:
                st.markdown("**💡 General Questions:**")
                example_queries_2 = [
                    "Explain machine learning in simple terms",
                    "How does blockchain technology work?",
                    "What are the benefits of renewable energy?",
                    "Compare different programming languages"
                ]
                
                for query in example_queries_2:
                    if st.button(f"📝 {query}", key=f"example2_{hash(query)}"):
                        st.session_state.example_query = query
        
        # Handle example query selection
        if hasattr(st.session_state, 'example_query'):
            settings = {
                "use_streaming": True,
                "temperature": 0.1,
                "max_tokens": 2000,
                "api_connected": self.check_api_status()
            }
            
            if settings["api_connected"]:
                self.handle_user_input(st.session_state.example_query, settings)
            
            # Clear the example query
            delattr(st.session_state, 'example_query')
    
    def run(self):
        """Main application runner."""
        # Render sidebar and get settings
        settings = self.render_sidebar()
        
        # Render main chat interface
        self.render_chat_interface(settings)
        
        # Render example queries
        if not st.session_state.messages:
            self.render_example_queries()

def main():
    """Main function to run the Streamlit app."""
    app = AIAgentUI()
    app.run()

if __name__ == "__main__":
    main()