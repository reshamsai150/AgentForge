from typing import List, Dict, Any
from ..schemas import Plan, ToolResult
from ..tools.registry import get_tool

class Executor:
    def execute(self, plan: Plan) -> List[ToolResult]:
        """
        Executes each step in the plan deterministically.
        Converts tool-returned dictionaries into ToolResult Pydantic models.
        """
        results = []
        for step in plan.tasks:
            tool_func = get_tool(step.tool)
            if not tool_func:
                results.append(ToolResult(
                    tool=step.tool,
                    args=step.args,
                    output=None,
                    success=False,
                    error=f"Tool '{step.tool}' not found in registry."
                ))
                continue
            
            try:
                # Execute tool (which returns a raw dict)
                raw_output = tool_func(**step.args)
                
                # Convert to ToolResult model
                results.append(ToolResult(
                    tool=step.tool,
                    args=step.args,
                    output=raw_output,
                    success=raw_output.get("success", False),
                    error=raw_output.get("error")
                ))
            except Exception as e:
                results.append(ToolResult(
                    tool=step.tool,
                    args=step.args,
                    output=None,
                    success=False,
                    error=str(e)
                ))
        
        return results
