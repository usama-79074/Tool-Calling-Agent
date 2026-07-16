# Tool Calling Agent

A **Tool Calling AI Agent** built with **Google Gemini 2.5 Flash** and **Poetry**. The agent
understands a user's query, decides on its own whether it needs a tool, calls that tool, and uses
the result to give a final, natural-language answer — printing which tool was used along the way.

```
User Query
   ↓
Gemini Agent
   ↓
Tool Selection   (Gemini decides which function to call, if any)
   ↓
Execute Tool     (the matching Python function runs locally)
   ↓
Tool Result
   ↓
Final Response
```

## 🧰 Available Tools

| Tool | Purpose |
|---|---|
| `calculator` | add / subtract / multiply / divide two numbers |
| `get_weather` | current weather for any city (via wttr.in) |
| `get_current_datetime` | current date, time, and weekday |

## 📁 Project Structure

```
tool-calling-agent/
├── main.py          # Agent logic + CLI — run this file to start
├── tools.py          # All tools (functions + schemas) in one place
├── pyproject.toml    # Poetry project config + dependencies
├── poetry.lock
├── .env              # Your Gemini API key (never commit this)
└── .gitignore
```

## 🚀 Setup

1. **Install Poetry** (if you don't have it):
   ```bash
   pip install poetry
   ```

2. **Clone the repo and install dependencies**:
   ```bash
   git clone https://github.com/usama-79074/Tool-Calling-Agent.git
   cd Tool-Calling-Agent
   poetry install
   ```

3. **Add your Gemini API key** — create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).

4. **Run the agent**:
   ```bash
   poetry run python main.py
   ```

## 💬 Example

```
Enter your query: what is 25 multiplied by 18
🔧 Tool(s) used: calculator
Agent: The answer is 450.

Enter your query: what's the weather in Lahore
🔧 Tool(s) used: get_weather
Agent: It's currently 34°C in Lahore, with clear skies and 30% humidity.

Enter your query: what's today's date
🔧 Tool(s) used: get_current_datetime
Agent: Today is Thursday, 2026-07-16.
```

## ➕ Adding a New Tool

1. In `tools.py`, write a plain Python function that does the work.
2. Write a matching `google.genai.types.FunctionDeclaration` describing its name and parameters.
3. Add both to `TOOL_FUNCTIONS` and `ALL_DECLARATIONS` at the bottom of `tools.py`.

Gemini will then be able to call it automatically whenever it's relevant to a user's query.

## ⚙️ Tech Stack

- [Google Gemini 2.5 Flash](https://ai.google.dev/) — the LLM powering the agent
- [google-genai](https://pypi.org/project/google-genai/) — official Python SDK
- [Poetry](https://python-poetry.org/) — dependency management
- [Rich](https://github.com/Textualize/rich) — terminal UI
