# ai_agent_project/ui/components/sidebar.py

import streamlit as st
import httpx

def render_sidebar(api_url, convo_id, user_id):
    st.sidebar.header("🤖 AI Agent Settings")
    status = "🟢 Connected" if httpx.get(f"{api_url}/health").status_code == 200 else "🔴 Disconnected"
    st.sidebar.markdown(f"**API Status:** {status}")
    st.sidebar.markdown("---")
    if st.sidebar.button("🆕 New Conversation"):
        st.session_state.messages = []
        st.session_state.conversation_id = user_id  # or new uuid
        st.experimental_rerun()
    return st.sidebar.checkbox("Enable Streaming", value=True)
