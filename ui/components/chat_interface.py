# ai_agent_project/ui/components/chat_interface.py

import streamlit as st

def render_chat(messages):
    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
              <strong>🧑 You:</strong><br>{msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
              <strong>🤖 Assistant:</strong><br>{msg["content"]}
            </div>
            """, unsafe_allow_html=True)
