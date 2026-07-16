"""main.py — Tool Calling Agent powered by Google Gemini 2.5 Flash.

Run with:
    poetry run python main.py
"""

import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel

from tools import GEMINI_TOOLS, TOOL_FUNCTIONS

MODEL = "gemini-3.5-flash"

SYSTEM_INSTRUCTION = (
    "You are a helpful AI assistant with access to tools (calculator, weather, "
    "and current date/time). Whenever a user's request needs a calculation, "
    "current weather, or the current date/time, you MUST call the appropriate "
    "tool instead of guessing. After receiving the tool's result, give a clear, "
    "concise final answer using that result."
)

MAX_TOOL_ITERATIONS = 5

console = Console()


class ToolCallingAgent:
    """A minimal tool-calling agent powered by Gemini 2.5 Flash."""

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.chat = self.client.chats.create(
            model=MODEL,
            config=types.GenerateContentConfig(
                tools=GEMINI_TOOLS,
                system_instruction=SYSTEM_INSTRUCTION,
            ),
        )

    def run(self, user_message: str):
        """Send a message through the agent, executing any tool calls Gemini requests.

        Returns (final_text, tools_used_list).
        """
        tools_used = []
        response = self.chat.send_message(user_message)

        for _ in range(MAX_TOOL_ITERATIONS):
            function_calls = getattr(response, "function_calls", None)
            if not function_calls:
                break

            function_response_parts = []
            for call in function_calls:
                tool_name = call.name
                tool_args = dict(call.args) if call.args else {}
                tools_used.append(tool_name)

                tool_fn = TOOL_FUNCTIONS.get(tool_name)
                result = (
                    tool_fn(**tool_args)
                    if tool_fn
                    else {"error": f"Unknown tool: {tool_name}"}
                )

                function_response_parts.append(
                    types.Part.from_function_response(name=tool_name, response=result)
                )

            response = self.chat.send_message(function_response_parts)

        return response.text or "", tools_used


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print(
            "[bold red]Error:[/bold red] GEMINI_API_KEY not found in .env file."
        )
        sys.exit(1)

    agent = ToolCallingAgent(api_key=api_key)

    console.print(
        Panel.fit(
            "Tools: calculator, get_weather, get_current_datetime\n"
            "Type your message, or 'exit' to quit.",
            border_style="cyan",
        )
    )

    while True:
        try:
            user_message = console.input("[bold yellow]Enter your query:[/bold yellow] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if not user_message:
            continue
        if user_message.lower() in ("exit", "quit", "q"):
            console.print("[dim]Goodbye![/dim]")
            break

        final_text, tools_used = agent.run(user_message)

        if tools_used:
            tool_list = ", ".join(f"[magenta]{t}[/magenta]" for t in tools_used)
            console.print(f"[bold]🔧 Tool(s) used:[/bold] {tool_list}")

        console.print(f"[bold green]Agent:[/bold green] {final_text}\n")


if __name__ == "__main__":
    main()
