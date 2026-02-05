# AgentForge

AgentForge is a local AI Operations Assistant that uses a multi-agent architecture:

Planner → Executor → Verifier

It converts natural language tasks into tool calls, executes real APIs (GitHub + Weather), and returns structured validated results.

## Requirements

Python 3.10+

API keys for:
- OpenAI or Groq
- OpenWeather
- GitHub (read-only)

## Setup

### Clone:
```bash
git clone https://github.com/reshamsai150/AgentForge.git
cd AgentForge
```

### Install:
```bash
pip install -r requirements.txt
```

### Configure:
```bash
cp agentforge/.env.example .env
```
Add your keys inside `.env`.

## Run

Example:
```bash
python -m agentforge.cli "What is the weather in London?"
```

Multi-tool example:
```bash
python -m agentforge.cli "Find top 3 GenAI repos and check weather in Hyderabad"
```

## Architecture

- **Planner (LLM)**: Generates structured Plan
- **Executor (Python only)**: Executes tools deterministically (ZERO LLM calls)
- **Verifier (LLM)**: Validates results and summarizes

All communication uses Pydantic schemas. No raw JSON parsing.

## Project Structure
```text
agentforge/
  agents/
  tools/
  llm/
  schemas.py
  main.py
  cli.py
```

## Notes
- Runs locally only
- No database
- No web server
- Read-only APIs
- Built for 24-hour GenAI intern assignment
