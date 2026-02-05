from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Step(BaseModel):
    tool: str = Field(..., description="The name of the tool to be called")
    args: Dict[str, Any] = Field(default_factory=dict, description="Arguments to pass to the tool")

class Plan(BaseModel):
    tasks: List[Step] = Field(..., description="A list of steps to execute to satisfy the user request")

class ToolResult(BaseModel):
    tool: str
    args: Dict[str, Any]
    output: Any
    success: bool
    error: Optional[str] = None

class FinalResponse(BaseModel):
    valid: bool = Field(..., description="Whether the tool results successfully satisfied the user intent")
    summary: str = Field(..., description="A concise natural language summary of the results")
    results: List[ToolResult] = Field(..., description="The structured results from the executor")
