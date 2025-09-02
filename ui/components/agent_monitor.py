# ai_agent_project/ui/components/agent_monitor.py

import streamlit as st

def render_agent_status(status):
    st.markdown(f"""
    <div class="agent-status">
      🔄 <strong>Status:</strong> {status}
    </div>
    """, unsafe_allow_html=True)
