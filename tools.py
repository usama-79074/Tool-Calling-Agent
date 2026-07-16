"""tools.py — All tools available to the agent, in one place.

Each tool has:
  1. A plain Python function that does the actual work.
  2. A google.genai FunctionDeclaration describing it to Gemini.

To add a new tool: write a function, write its FunctionDeclaration, then add
both to TOOL_FUNCTIONS and ALL_DECLARATIONS at the bottom of this file.
"""

from datetime import datetime

import requests
from google.genai import types

# ---------------------------------------------------------------------------
# Tool 1: Calculator
# ---------------------------------------------------------------------------


def calculator(operation: str, a: float, b: float) -> dict:
    """Perform a basic arithmetic operation on two numbers."""
    operation = operation.lower().strip()

    if operation in ("add", "addition", "+"):
        result = a + b
    elif operation in ("subtract", "subtraction", "-"):
        result = a - b
    elif operation in ("multiply", "multiplication", "*", "x"):
        result = a * b
    elif operation in ("divide", "division", "/"):
        if b == 0:
            return {"error": "Division by zero is not allowed."}
        result = a / b
    else:
        return {"error": f"Unsupported operation: {operation}"}

    return {"operation": operation, "a": a, "b": b, "result": result}


calculator_declaration = types.FunctionDeclaration(
    name="calculator",
    description=(
        "Perform a basic arithmetic operation (add, subtract, multiply, divide) "
        "on two numbers. Use this whenever the user asks for a calculation."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "operation": types.Schema(
                type=types.Type.STRING,
                description="The arithmetic operation to perform.",
                enum=["add", "subtract", "multiply", "divide"],
            ),
            "a": types.Schema(type=types.Type.NUMBER, description="The first number."),
            "b": types.Schema(type=types.Type.NUMBER, description="The second number."),
        },
        required=["operation", "a", "b"],
    ),
)

# ---------------------------------------------------------------------------
# Tool 2: Weather
# ---------------------------------------------------------------------------


def get_weather(city: str) -> dict:
    """Fetch the current weather for a given city using the free wttr.in API."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]
        return {
            "city": city,
            "temperature_c": current["temp_C"],
            "feels_like_c": current["FeelsLikeC"],
            "description": current["weatherDesc"][0]["value"],
            "humidity": current["humidity"],
        }
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Could not fetch weather for '{city}': {exc}"}


weather_declaration = types.FunctionDeclaration(
    name="get_weather",
    description=(
        "Get the current real-world weather (temperature, conditions, humidity) "
        "for a given city. Use this whenever the user asks about the weather."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "city": types.Schema(
                type=types.Type.STRING,
                description="The city to get the weather for, e.g. 'Lahore'.",
            ),
        },
        required=["city"],
    ),
)

# ---------------------------------------------------------------------------
# Tool 3: Current date/time
# ---------------------------------------------------------------------------


def get_current_datetime() -> dict:
    """Get the current date, time, and day of the week (server local time)."""
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": now.strftime("%A"),
    }


datetime_declaration = types.FunctionDeclaration(
    name="get_current_datetime",
    description=(
        "Get the current date, time, and day of the week. Use this whenever the "
        "user asks what the date, time, or day today is."
    ),
    parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
)

# ---------------------------------------------------------------------------
# Registry — everything the agent needs to know about the tools
# ---------------------------------------------------------------------------

TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_weather": get_weather,
    "get_current_datetime": get_current_datetime,
}

ALL_DECLARATIONS = [calculator_declaration, weather_declaration, datetime_declaration]

GEMINI_TOOLS = [types.Tool(function_declarations=ALL_DECLARATIONS)]
