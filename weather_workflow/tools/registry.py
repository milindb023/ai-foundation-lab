from typing import Any
from .weather_api import get_current_weather
from ..schemas.weather import WeatherToolInput

AVAILABLE_TOOLS = {
    "get_current_weather": get_current_weather,
}

def execute_tool(tool_name: str, raw_arguments: str) -> dict[str, Any]:
    """
    Routes a tool call from the LLM to the matching python function execution,
    validating the parameters against their Pydantic schemas.
    """
    if tool_name not in AVAILABLE_TOOLS:
        raise ValueError(f"Unknown tool requested: {tool_name}")

    if tool_name == "get_current_weather":
        validated_args = WeatherToolInput.model_validate_json(raw_arguments)
        return AVAILABLE_TOOLS[tool_name](**validated_args.model_dump())

    raise ValueError(f"No executor configured for tool: {tool_name}")
