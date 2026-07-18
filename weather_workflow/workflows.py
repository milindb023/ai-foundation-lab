import json
from pydantic import ValidationError
from .config import get_openrouter_client, MODEL_NAME
from .schemas import ConceptExplanation
from .tools import weather_tool_definition, execute_tool

def run_basic_call(prompt: str) -> str:
    """
    1. Basic OpenRouter API call: Requests a basic explanation.
    """
    client = get_openrouter_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI instructor. Explain concepts simply.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        top_p=0.9,
        max_tokens=300
    )
    return response.choices[0].message.content or ""


def run_json_mode(prompt: str) -> dict:
    """
    2. JSON-mode response: Guarantees that the output matches valid JSON syntax.
    """
    client = get_openrouter_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "Return only a valid JSON object. "
                    "Include the keys topic, explanation, and examples."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    json_text = response.choices[0].message.content or "{}"
    return json.loads(json_text)


def run_structured_output(prompt: str) -> ConceptExplanation:
    """
    3. Structured output using a Pydantic-generated JSON Schema:
       Enforces field names, types, and ranges directly during generation.
    """
    client = get_openrouter_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are an AI instructor. Follow the supplied JSON schema exactly.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "concept_explanation",
                "strict": True,
                "schema": ConceptExplanation.model_json_schema(),
            },
        },
        temperature=0,
    )
    structured_text = response.choices[0].message.content or "{}"
    return ConceptExplanation.model_validate_json(structured_text)


def run_weather_workflow(question: str) -> str:
    """
    4. Tool calling workflow using a live weather tool:
       Implements the full agentic loop (Prompt -> LLM Decides -> Execute -> LLM Final response).
    """
    client = get_openrouter_client()
    messages = [
        {
            "role": "system",
            "content": "Use the weather tool for current weather questions."
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # First LLM call
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=[weather_tool_definition],
        tool_choice="auto",
        temperature=0
    )

    assistant_message = response.choices[0].message

    # If no tool is needed, return the normal answer
    if not assistant_message.tool_calls:
        return assistant_message.content or ""

    # Get tool call details
    tool_call = assistant_message.tool_calls[0]
    raw_args = tool_call.function.arguments
    tool_name = tool_call.function.name

    print(f"\n[Workflow] LLM selected tool: {tool_name}")
    print(f"[Workflow] Arguments: {raw_args}")

    # Execute tool locally via router
    tool_result = execute_tool(tool_name, raw_args)
    print(f"[Workflow] Tool result: {tool_result}")

    # Add tool invocation and results back into the context
    messages.append(assistant_message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(tool_result)
    })

    # Second LLM call for final natural-language answer
    print("[Workflow] Requesting final answer from LLM...")
    final_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=[weather_tool_definition],
        temperature=0
    )

    return final_response.choices[0].message.content or ""
