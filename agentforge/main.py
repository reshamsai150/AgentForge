from .llm.client import LLMClient
from .agents.planner import Planner
from .agents.executor import Executor
from .agents.verifier import Verifier
from .schemas import FinalResponse

def run_agent(user_request: str) -> FinalResponse:
    """
    Orchestrates the Planner -> Executor -> Verifier flow.
    """
    client = LLMClient()
    
    # 1. Planning
    planner = Planner(client)
    plan = planner.create_plan(user_request)
    
    # 2. Execution
    executor = Executor()
    results = executor.execute(plan)
    
    # 3. Verification
    verifier = Verifier(client)
    final_response = verifier.verify(user_request, results)
    
    return final_response
