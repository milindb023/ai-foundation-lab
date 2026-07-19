from langchain.agents import create_agent
from langchain_agent_memory_variations.tools import search_tool, weather_tool, rag_tool

# Initialize the tools list
tools = [search_tool, weather_tool, rag_tool]

# Define the system prompt instruction for the agent
system_prompt = """
You are a helpful AI class-demo assistant.

You have access to three tools:

1. search_tool:
   Use for latest news, current facts, recent information, or external web knowledge.

2. weather_tool:
   Use for current weather, temperature, humidity, wind, or rain questions.

3. rag_tool:
   Use for questions about the uploaded PDF or private document.

Rules:
- If the user asks about the uploaded document, use rag_tool.
- If the user asks about weather, use weather_tool.
- If the user asks about latest/current information, use search_tool.
- If a question needs multiple tools, use multiple tools.
- Always give a clear final answer.
- Mention which tool(s) you used at the end.
"""

def get_agent(llm):
    """Creates and returns the LangChain agent instance."""
    print("🤖 Constructing LangChain tool-calling agent...")
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )
