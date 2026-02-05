import sys
import os
import warnings

# Suppress Gemini deprecation warnings early
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

from dotenv import load_dotenv

# Ensure the root directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    load_dotenv()
    
    # Handle the "one command" requirement 
    # If no args are passed, provide a default demo task
    if len(sys.argv) < 2:
        task = "What is the weather in London?"
        print(f"No task provided. Running default demo: '{task}'")
    else:
        task = " ".join(sys.argv[1:])

    from agentforge.cli import run_with_task
    run_with_task(task)

if __name__ == "__main__":
    main()
