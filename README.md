Theek hai, bina outer box ke seedha likh deta hoon taake copy karne mein confusion na ho:

Tool Calling Agent
A Tool Calling AI Agent powered by Google Gemini 2.5 Flash — understands user queries and automatically calls the right tool (calculator, weather, or date/time) to give accurate, real-time answers. Built with Poetry for clean dependency management.
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
🧰 Available Tools
ToolPurposecalculatoradd / subtract / multiply / divide two numbersget_weathercurrent weather for any city (via wttr.in)get_current_datetimecurrent date, time, and weekday
📁 Project Structure
tool-calling-agent/
├── main.py          # Agent logic + CLI — run this file to start
├── tools.py          # All tools (functions + schemas) in one place
├── pyproject.toml    # Poetry project config + dependencies
├── poetry.lock
├── .env              # Your Gemini API key (never commit this)
└── .gitignore
🚀 Setup

Install Poetry (if you don't have it):
pip install poetry
Clone the repo and install dependencies:
git clone https://github.com/usama-79074/Tool-Calling-Agent.git
cd Tool-Calling-Agent
poetry install
Add your Gemini API key — create a .env file in the project root:
GEMINI_API_KEY=your_gemini_api_key_here
Get a free key at Google AI Studio.
Run the agent:
poetry run python main.py

💬 Example
Enter your query: what is 25 multiplied by 18
🔧 Tool(s) used: calculator
Agent: The answer is 450.
Enter your query: what's the weather in Lahore
🔧 Tool(s) used: get_weather
Agent: It's currently 34°C in Lahore, with clear skies and 30% humidity.
Enter your query: what's today's date
🔧 Tool(s) used: get_current_datetime
Agent: Today is Thursday, 2026-07-16.
➕ Adding a New Tool

In tools.py, write a plain Python function that does the work.
Write a matching google.genai.types.FunctionDeclaration describing its name and parameters.
Add both to TOOL_FUNCTIONS and ALL_DECLARATIONS at the bottom of tools.py.

Gemini will then be able to call it automatically whenever it's relevant to a user's query.
⚙️ Tech Stack

Google Gemini 2.5 Flash — the LLM powering the agent
google-genai — official Python SDK
Poetry — dependency management
Rich — terminal UI
