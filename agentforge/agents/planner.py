from ..llm.client import LLMClient
from ..llm.prompts import PLANNER_SYSTEM_PROMPT
from ..schemas import Plan

class Planner:
    def __init__(self, client: LLMClient):
        self.client = client

    def create_plan(self, user_request: str) -> Plan:
        """
        Interprets user request and generates a plan of tool steps.
        """
        return self.client.call_with_schema(
            system_prompt=PLANNER_SYSTEM_PROMPT,
            user_prompt=user_request,
            schema=Plan
        )
