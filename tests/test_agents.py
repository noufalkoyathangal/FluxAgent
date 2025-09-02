# ai_agent_project/tests/test_agents.py

import pytest
from app.agents.supervisor_agent import SupervisorAgent
from app.graph.state import AgentState

@pytest.mark.asyncio
async def test_supervisor_decision_respond():
    agent = SupervisorAgent()
    state = AgentState(
        messages=[],
        user_input="Tell me a joke",
        next_action=None, research_data=None, plan=None,
        tools_used=[], tool_results={},
        conversation_id="c1", user_id="u1",
        current_agent="supervisor", workflow_status="in_progress",
        working_memory={}, long_term_memory=None,
        timestamp=None, session_data={}
    )
    updated = await agent.decide_action(state)
    assert updated["next_action"] == "respond"
