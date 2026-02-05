# AgentForge

AgentForge is a local AI Operations Assistant built on a multi-agent orchestrated architecture. It decomposes complex user requests into actionable tool calls, executes them against real-world APIs, and validates the final output against the original user intent.

## 🚀 One-Command Execution
Run the system with a single command:
```bash
python run.py "What is the weather in London?"
```

---

## 🏗 Architecture
AgentForge uses a deterministic orchestration pattern with three distinct agents:

1.  **Planner (LLM)**: Analyzes user input and decomposes it into a list of specific tool-based steps.
2.  **Executor (Python)**: A purely deterministic agent that executes the plan sequence. It has **ZERO LLM calls**, ensuring predictable tool behavior and no hallucination during execution.
3.  **Verifier (LLM)**: Takes the tool outputs and the original request to verify satisfaction and generate a natural language summary.

**Communication**: All agents and tools communicate using strictly enforced **Pydantic schemas**. There is no raw JSON parsing in the core logic.

---

## 🛠 Integrated APIs
- **Google Gemini (LLM Backend)**: Powers the Planner and Verifier (using the Free Tier).
- **OpenWeatherMap**: Fetches real-time weather data for any city.
- **GitHub Search API**: Real-time read-only repository search.

---

## 📋 Setup & Installation

### 1. Requirements
- Python 3.10+
- Internet access for API calls

### 2. Install Dependencies
```bash
pip install -r agentforge/requirements.txt
```

### 3. Environment Configuration
Copy the template and add your keys:
```bash
cp agentforge/.env.example .env
```

**Required Variables in `.env`:**
- `GEMINI_API_KEY`: Get from [Google AI Studio](https://aistudio.google.com/app/apikey).
- `WEATHER_API_KEY`: Get from [OpenWeatherMap](https://home.openweathermap.org/api_keys).
- `GITHUB_TOKEN`: GitHub Personal Access Token (Classic) with `repo` scope.

---

## 💡 Example Prompts
- `"What is the weather in New York?"`
- `"Find the top 5 Python machine learning repositories on GitHub."`
- `"Check the weather in Tokyo and find top research papers repositories on GitHub."`

---

## ⚠️ Limitations & Tradeoffs
- **Stateless**: The system does not maintain history between requests (no memory).
- **Read-Only**: The GitHub tool is restricted to search; it cannot modify code or create issues.
- **Single-Turn**: If a plan fails, the executor does not attempt to "re-plan" mid-flight (Agentic loop is simple for reliability).
- **Local Execution**: Runs entirely as a CLI tool; no web UI or persistent database is included to minimize latency and architectural complexity for this 24-hour build.

---

## 📂 Project Structure
- `agentforge/`
  - `agents/`: Planner, Executor, and Verifier implementations.
  - `tools/`: Deterministic code for Weather and GitHub APIs.
  - `llm/`: Gemini client with schema enforcement.
  - `schemas.py`: Central Pydantic models.
  - `main.py`: Core orchestration logic.
  - `cli.py`: User interface layer.
- `run.py`: Simplified entry point.
