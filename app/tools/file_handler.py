# ai_agent_project/app/tools/file_handler.py

import os
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class FileHandlerInput(BaseModel):
    filename: str = Field(..., description="Name of the file")
    content: str = Field(..., description="Content to write")

class FileHandlerTool(BaseTool):
    name = "file_handler"
    description = "Read/write files on the server"

    args_schema = FileHandlerInput

    def _run(self, filename: str, content: str) -> str:
        with open(filename, "w") as f:
            f.write(content)
        return f"File {filename} saved."

    async def _arun(self, filename: str, content: str) -> str:
        return self._run(filename, content)
