import os
from langchain.tools import tool
from langchain_community.utilities import SerpAPIWrapper

@tool
def search_tool(query: str) -> str:
    """Search Google for current information using SerpAPI. Use this for latest news, recent facts, current events, or anything that may have changed recently."""
    print("🔎 SERPAPI SEARCH TOOL CALLED")
    serpapi_key = os.environ.get("SERPAPI_API_KEY")
    if not serpapi_key:
        return "SERPAPI_API_KEY is missing. Please set the API key first."
    search = SerpAPIWrapper(serpapi_api_key=serpapi_key)
    return search.run(query)
