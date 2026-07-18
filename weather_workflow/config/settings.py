import os
import getpass
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists (checks current working directory, then the parent directory of this module)
load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

# Model to be used
MODEL_NAME = "openai/gpt-4o-mini"

def get_openrouter_client() -> OpenAI:
    """
    Initializes and returns the OpenAI client configured for OpenRouter.
    Prompts the user for the key if it's not set in the environment.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("\n[Config] OPENROUTER_API_KEY not found in environment or .env file.")
        api_key = getpass.getpass("Enter your OpenRouter API key: ").strip()
        if not api_key:
            raise ValueError("OpenRouter API key cannot be empty.")
        os.environ["OPENROUTER_API_KEY"] = api_key
    
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

def get_openweather_key() -> str:
    """
    Retrieves the OpenWeather API key.
    Prompts the user for the key if it's not set in the environment.
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        print("\n[Config] OPENWEATHER_API_KEY not found in environment or .env file.")
        api_key = getpass.getpass("Enter your OpenWeather API key: ").strip()
        if not api_key:
            raise ValueError("OpenWeather API key cannot be empty.")
        os.environ["OPENWEATHER_API_KEY"] = api_key
    return api_key
