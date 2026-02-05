# IMPLEMENTATION_PLAN.md

## Phase 1: Core Foundation (0-4 Hours)

### 1.1 Project & Schema Setup
- **Description:** Initialize project structure and define Pydantic models in `schemas.py`.
- **Expected Output:** `schemas.py` containing `Plan`, `Step`, `ToolResult`, and `FinalResponse`.
- **How to verify:** Run `pydantic` validation tests on mock data.
- **Dependencies:** `python-dotenv`, `pydantic`.
- **Estimate:** 1 Hour.

### 1.2 Deterministic Tools
- **Description:** Build `WeatherTool` and `GitHubSearchTool` (Read-only).
- **Expected Output:** Tool functions that return JSON-serializable dictionaries. Executor converts dictionaries into ToolResult models.
- **How to verify:** CLI unit tests for each tool with hardcoded API responses.
- **Dependencies:** `httpx`.
- **Estimate:** 2 Hours.

### 1.3 Tool Registry
- **Description:** Map string keys to tool functions.
- **Expected Output:** Importable registry in `tools/registry.py`.
- **How to verify:** Verify `registry.get("weather")` returns the correct function.
- **Estimate:** 30 Mins.

---

## Phase 2: Agent Implementation (4-12 Hours)

### 2.1 LLM Infrastructure
- **Description:** Standardize LLM client to enforce JSON schema responses with automatic schema validation and one retry on invalid output
- **Expected Output:** `llm/client.py` and structured `llm/prompts.py`.
- **How to verify:** Script that pings LLM and returns a validated `Plan` object.
- **Dependencies:** OpenAI/Gemini API key.
- **Estimate:** 2 Hours.

### 2.2 Planner Agent
- **Description:** LLM-based agent to produce a sequence of tool steps.
- **Expected Output:** `agents/planner.py` returning a `Plan` Pydantic model.
- **How to verify:** Prompt: "Get London weather" -> Expect `Plan` with 1 `Step`.
- **Estimate:** 2 Hours.

### 2.3 Executor (Deterministic)
- **Description:** Logic to loop through a `Plan` and call tools. No LLM allowed.
- **Expected Output:** `agents/executor.py` returning `List[ToolResult]`.
- **How to verify:** Pass a mock `Plan` and confirm it returns `List[ToolResult]`.
- **Estimate:** 1 Hour.

### 2.4 Verifier Agent
- **Description:** LLM-based agent to validate results against user intent.
- **Expected Output:** `agents/verifier.py` returning `FinalResponse` model.
- **How to verify:** Pass successful tool output -> Expect `valid: True`. Pass error -> Expect `valid: False`.
- **Estimate:** 2 Hours.

---

## Phase 3: Integration & CLI (12-20 Hours)

### 3.1 Orchestration
- **Description:** Connect P -> E -> V in `main.py`.
- **Expected Output:** `run_agent(user_input)` function.
- **How to verify:** Full system dry-run from a python script.
- **Estimate:** 2 Hours.

### 3.2 CLI Interface
- **Description:** Build user-facing CLI with `argparse` or `rich`.
- **Expected Output:** `python cli.py "Task description"`.
- **How to verify:** Run command and observe structured, colorized terminal output.
- **Estimate:** 2 Hours.

### 3.3 Error Boundaries
- **Description:** Wrap whole flow in try/except for API/LLM failures.
- **Expected Output:** Graceful failure messages (No tracebacks).
- **Estimate:** 1 Hour.

---

## Phase 4: Final Polish (20-24 Hours)

### 4.1 Demo & Readme
- **Description:** Create a high-quality README and recorded demo path.
- **Estimate:** 2 Hours.

### 4.2 **[STOP HERE FOR SUBMISSION]**
Total Build Time: ~18-20 Hours.

---

# FILE_STRUCTURE.md

```text
agentforge/
â”œâ”€â”€ agents/             # Agent logic
â”‚   â”œâ”€â”€ planner.py      # LLM: Intent -> Plan
â”‚   â”œâ”€â”€ executor.py     # Code: Plan -> List[ToolResult]
â”‚   â””â”€â”€ verifier.py     # LLM: (Intent + Results) -> FinalResponse
â”œâ”€â”€ tools/              # Tool implementations
â”‚   â”œâ”€â”€ weather.py      # Weather API client
â”‚   â”œâ”€â”€ github.py       # GitHub Search client (Read-only)
â”‚   â””â”€â”€ registry.py     # Tool lookup table
â”œâ”€â”€ llm/                # LLM communication
â”‚   â”œâ”€â”€ client.py       # Wrapper for LLM calls with schema enforcement
â”‚   â””â”€â”€ prompts.py      # Distinct system prompts per agent
â”œâ”€â”€ schemas.py          # Pydantic models (Plan, Step, ToolResult, FinalResponse)
â”œâ”€â”€ main.py             # Workflow orchestration
â”œâ”€â”€ cli.py              # CLI entrypoint
â”œâ”€â”€ requirements.txt    # Base dependencies
â””â”€â”€ .env.example        # Configuration template
```

---

# REQUIREMENTS.txt

```text
openai>=1.0.0
httpx>=0.24.0
python-dotenv>=1.0.0
pydantic>=2.0.0
rich>=13.0.0
```

---

# ARCHITECTURE_RULES.md

## Agent Responsibilities
- **Planner (LLM):** Decomposes natural language into a list of specific tool steps. MUST output a `Plan` model.
- **Executor (Python):** Deterministically executes the `Plan`. MUST NOT use LLM. Calls tools and collects results into a `List[ToolResult]`.
- **Verifier (LLM):** Evaluates if the `List[ToolResult]` satisfies the user's original request. MUST output a `FinalResponse` model.

## Tool Contract
- Tools are independent functions.
- Every tool MUST return a dictionary compatible with the `ToolResult` schema.
- Tools MUST be Read-Only and have no persistent side effects.
- Tools must NOT import or depend on Pydantic models (loose coupling).

## Data Flow
1. `User String` -> **Planner** -> `Plan Object`
2. `Plan Object` -> **Executor** -> `List[ToolResult]`
3. `User String` + `List[ToolResult]` -> **Verifier** -> `FinalResponse Object`

## Strict "What NOT to Add"
- NO raw JSON string manipulation (use Pydantic objects).
- NO FastAPI / Flask / Servers.
- NO database or file-based caching.
- NO write operations to GitHub (Read-only search only).
- NO LLM calls inside the Executor or Tools.
