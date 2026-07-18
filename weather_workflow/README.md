# OpenRouter API & Weather Tool-Calling Workflow

This module is a modular, enterprise-ready Python implementation of the instructor's Jupyter Colab notebook showing various LLM integration strategies using the OpenRouter API (compatible with the OpenAI Python SDK) and Pydantic validation.

## Directory Structure

To allow for easy future expansion (e.g., adding more LLM tools, new schemas, or configuration sources), the project is structured as a set of nested Python packages:

```text
weather_workflow/
│
├── config/              # Configuration package
│   ├── __init__.py
│   └── settings.py      # Dynamic environment loaders and OpenAI client config
│
├── schemas/             # Pydantic validation schemas
│   ├── __init__.py
│   ├── explanations.py  # ConceptExplanation schema
│   └── weather.py       # WeatherToolInput schema
│
├── tools/               # External APIs and integration utilities
│   ├── __init__.py
│   ├── weather_api.py   # OpenWeather integration and LLM tool description
│   └── registry.py      # Central tool registry router mapping LLM tool actions to python
│
├── core/                # Core workflows package
│   ├── __init__.py
│   └── workflows.py     # Main LLM execution flows (basic, JSON, Structured, Tool-calling)
│
├── .env.example         # Template for API keys configuration
├── .env                 # Local API keys (ignored by git)
├── README.md            # This documentation file
├── requirements.txt     # Python library requirements
└── main.py              # CLI entry point to run workflows interactively
```

## Setup Instructions

### 1. Install Dependencies
Run the following command to install the required libraries (ensure you have activated your virtual environment if using one):

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Copy the `.env.example` file to `.env` in the same directory:

```bash
cp .env.example .env
```

Edit the `.env` file to add your API keys:
* `OPENROUTER_API_KEY`: Get your key from [OpenRouter](https://openrouter.ai/).
* `OPENWEATHER_API_KEY`: Get your key from [OpenWeatherMap](https://openweathermap.org/).

*Note: If the keys are not found in the `.env` file or environment variables, the script will prompt you for them at runtime using a secure input.*

## How to Run

Launch the interactive CLI dashboard:

```bash
python main.py
```

Select a workflow from the menu options:
1. **Basic Call**: Simple concept explanation.
2. **JSON Mode**: Forces valid JSON syntax back from the model.
3. **Structured Output**: Enforces structured Pydantic schema validation at LLM request and app-side verification.
4. **Live Weather Tool Calling**: Full agent loop to ask for weather, call geocoding/weather API, format results, and get final response.
