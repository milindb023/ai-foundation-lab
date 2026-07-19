import os
import getpass
from dotenv import load_dotenv

# Path to the workspace/project level .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path)

def get_env_var_or_prompt(var_name: str, display_name: str) -> str:
    """Gets an environment variable or prompts the user for it if missing."""
    val = os.environ.get(var_name)
    if not val:
        print(f"\n🔑 {display_name} ({var_name}) not found in environment.")
        val = getpass.getpass(f"Enter {display_name}: ").strip()
        if not val:
            raise ValueError(f"{display_name} cannot be empty.")
        os.environ[var_name] = val
    return val

def initialize_llm(model_name: str = "openai/gpt-4o-mini", temperature: float = 0.2):
    """Initializes and returns ChatOpenRouter LLM."""
    api_key = get_env_var_or_prompt("OPENROUTER_API_KEY", "OpenRouter API Key")
    
    # Try importing from langchain_openrouter, fallback to standard ChatOpenAI with custom base_url
    try:
        from langchain_openrouter import ChatOpenRouter
        return ChatOpenRouter(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
    except ImportError:
        # Fallback to standard ChatOpenAI pointing to OpenRouter endpoint
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1"
        )
