"""
Simplified Streamlit application for the AI Agent interface.
"""
import streamlit as st
import requests
import json
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
    
    .status-indicator {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .connected { background-color: #e8f5e8; color: #2e7d32; }
    .disconnected { background-color: #ffebee; color: #c62828; }
</style>
""", unsafe_allow_html=True)

# Configuration
API_BASE_URL = "http://localhost:8000"

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
    
    if "api_status" not in st.session_state:
        st.session_state.api_status = None

def check_api_status():
    """Check if the FastAPI backend is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5.0)
        if response.status_code == 200:
            return True, "Connected"
    except Exception as e:
        return False, f"Disconnected: {str(e)}"
    
    return False, "Disconnected"

def send_message_to_api(message: str):
    """Send a message to the FastAPI backend."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/chat",
            json={
                "message": message,
                "conversation_id": st.session_state.conversation_id,
                "user_id": "streamlit_user"
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None

def render_sidebar():
    """Render the sidebar with configuration options."""
    with st.sidebar:
        st.header("🤖 AI Agent Settings")
        
        # API Status
        is_connected, status_msg = check_api_status()
        status_color = "connected" if is_connected else "disconnected"
        status_icon = "🟢" if is_connected else "🔴"
        
        st.markdown(f"""
        <div class="status-indicator {status_color}">
            {status_icon} <strong>API Status:</strong> {status_msg}
        </div>
        """, unsafe_allow_html=True)
        
        if not is_connected:
            st.warning("⚠️ FastAPI backend is not running!")
            st.info("💡 Start the backend with: `uvicorn app.api.main:app --reload`")
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
        
        # Instructions
        st.subheader("ℹ️ How to Use")
        st.markdown("""
        1. **Start Backend**: Run `uvicorn app.api.main:app --reload`
        2. **Type Message**: Enter your message in the chat input below
        3. **Send**: Press Enter or click send
        4. **View Response**: See the AI agent's response
        
        **Example Messages:**
        - "Hello, how are you?"
        - "What can you help me with?"
        - "Tell me about AI agents"
        """)
        
        return is_connected

def render_chat_interface(api_connected):
    """Render the main chat interface."""
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Agent Assistant</h1>
        <p>Powered by LangGraph, Azure OpenAI & FastAPI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display conversation messages
    if st.session_state.messages:
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
    else:
        # Show welcome message when no conversation exists
        st.markdown("""
        <div class="chat-message assistant-message">
            <strong>🤖 Assistant:</strong><br>
            Welcome! I'm your AI Agent Assistant. Type a message below to get started.
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input
    if api_connected:
        # Use chat_input for better UX
        if prompt := st.chat_input("Type your message here..."):
            handle_user_input(prompt)
    else:
        st.error("⚠️ Cannot send messages. API backend is not available.")
        st.info("💡 Please start the FastAPI server first.")

def handle_user_input(user_input: str):
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
        response_data = send_message_to_api(user_input)
    
    if response_data:
        assistant_response = response_data.get("response", "No response generated.")
        
        # Add to session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        # Display assistant response
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 Assistant:</strong><br>
            {assistant_response}
        </div>
        """, unsafe_allow_html=True)
        
        # Show additional info if available
        if response_data.get("tools_used"):
            st.info(f"🛠️ Tools used: {', '.join(response_data['tools_used'])}")
    
    # Force a rerun to update the interface
    st.rerun()

def render_example_queries():
    """Render example queries for users to try."""
    with st.expander("💡 Example Queries to Try"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💬 Basic Conversations:**")
            examples_1 = [
                "Hello, how are you?",
                "What can you help me with?",
                "Tell me about yourself",
                "How do you work?"
            ]
            
            for example in examples_1:
                if st.button(f"📝 {example}", key=f"ex1_{hash(example)}"):
                    st.session_state.example_query = example
        
        with col2:
            st.markdown("**🤔 Questions:**")
            examples_2 = [
                "Explain artificial intelligence",
                "What is machine learning?",
                "How do chatbots work?",
                "Tell me a fun fact"
            ]
            
            for example in examples_2:
                if st.button(f"📝 {example}", key=f"ex2_{hash(example)}"):
                    st.session_state.example_query = example
    
    # Handle example query selection
    if hasattr(st.session_state, 'example_query'):
        handle_user_input(st.session_state.example_query)
        # Clear the example query
        delattr(st.session_state, 'example_query')

def main():
    """Main application runner."""
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and get API connection status
    api_connected = render_sidebar()
    
    # Render main chat interface
    render_chat_interface(api_connected)
    
    # Render example queries if no conversation exists
    if not st.session_state.messages:
        render_example_queries()

if __name__ == "__main__":
    main()