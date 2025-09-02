# ai_agent_project/app/tools/calculator.py

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(..., description="Mathematical expression to evaluate")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluate a mathematical expression"

    args_schema = CalculatorInput

    def _run(self, expression: str) -> str:
        try:
            result = eval(expression, {}, {})
            return str(result)
        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, expression: str) -> str:
        return self._run(expression)
