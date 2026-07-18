# OpenRouter API & Weather Tool-Calling Workflow

This module is a modular Python implementation of the instructor's Jupyter Colab notebook showing various LLM integration strategies using the OpenRouter API (compatible with the OpenAI Python SDK) and Pydantic validation.

## Directory Structure

```text
weather_workflow/
│
├── .env.example        # Template for API keys configuration
├── README.md           # This documentation file
├── requirements.txt    # Python library requirements
│
├── config.py           # API configuration, key loaders, and OpenAI client setup
├── schemas.py          # Pydantic schemas (ConceptExplanation and WeatherToolInput)
├── tools.py            # External API integrations (OpenWeather) and tool registry
├── workflows.py        # Core workflow loops (basic call, JSON mode, structured outputs, agent tool loop)
└── main.py             # CLI application to run and test all workflows
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
