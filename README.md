# AgentForge

Local AI Operations Assistant with Planner -> Executor -> Verifier architecture.

## 🚀 Setup Instructions

### 1. Prerequisite: Python 3.10+
Ensure you have Python installed.

### 2. Install Dependencies
```bash
pip install -r agentforge/requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and add your API keys.
```bash
cp agentforge/.env.example .env
```
Add these keys:
- `OPENAI_API_KEY`: For Planner and Verifier agents.
- `WEATHER_API_KEY`: From OpenWeatherMap.
- `GITHUB_TOKEN`: GitHub Personal Access Token (Read-only search permissions).

## 🛠️ How to Run

Run the assistant using the CLI module:

```bash
python -m agentforge.cli "What is the weather in London and search for popular rust repositories?"
```

## 🏗️ Architecture

- **Planner (LLM)**: Decomposes task into tool steps.
- **Executor (Python)**: Deterministic execution of steps (ZERO LLM calls).
- **Verifier (LLM)**: Validates results against original intent.

## 🛠️ Tools Available
- **Weather**: Current weather data.
- **GitHub Search**: Search for repositories (Read-only).
