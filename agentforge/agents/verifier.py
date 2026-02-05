from typing import List
from ..llm.client import LLMClient
from ..llm.prompts import VERIFIER_SYSTEM_PROMPT
from ..schemas import ToolResult, FinalResponse

class Verifier:
    def __init__(self, client: LLMClient):
        self.client = client

    def verify(self, user_request: str, results: List[ToolResult]) -> FinalResponse:
        """
        Evaluates tool results against the original user intent.
        """
        # Construct a context string for the LLM
        context = f"User Request: {user_request}\n\nExecution Results:\n"
        for i, res in enumerate(results):
            context += f"Step {i+1} ({res.tool}): {'Success' if res.success else 'Failure'}\n"
            context += f"Output snippet: {str(res.output)[:500]}\n"
            if res.error:
                context += f"Error: {res.error}\n"
            context += "---\n"

        # Note: We pass the results as part of the model validation in the LLMClient
        # But for the LLM's comprehension, we format the context string.
        # However, call_with_schema expects a Dict and returns the validated object.
        # We'll rely on the LLM to populate the summary and valid flag.
        response = self.client.call_with_schema(
            system_prompt=VERIFIER_SYSTEM_PROMPT,
            user_prompt=context,
            schema=FinalResponse
        )
        
        # Ensure the results list is attached to the final response object
        response.results = results
        return response
