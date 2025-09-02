# ai_agent_project/app/utils/memory.py

from langgraph.checkpoint.memory import MemorySaver

# Expose a global memory saver for the workflow
memory_saver = MemorySaver()
