# ai_agent_project/tests/test_graph.py

import pytest
from app.graph.workflow import workflow

@pytest.mark.asyncio
async def test_workflow_simple():
    res = await workflow.process_message("Hello", conversation_id="t1", user_id="u1")
    assert "response" in res
    assert res["status"] in ("completed", "error")
