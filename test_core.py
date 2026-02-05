from agentforge.main import run_agent
import json
import os

try:
    print("Starting AgentForge Test Run...")
    response = run_agent("What is the weather in London?")
    
    print("\n--- Final Response ---")
    print(f"Valid: {response.valid}")
    print(f"Summary: {response.summary}")
    print("\n--- Tool Results ---")
    for res in response.results:
        print(f"Tool: {res.tool}")
        print(f"Success: {res.success}")
        print(f"Output: {json.dumps(res.output, indent=2)}")
        if res.error:
            print(f"Error: {res.error}")
        print("-" * 20)

except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
