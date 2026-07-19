# LangChain Agent & RAG Memory Variations Platform

A modular, production-ready Python command-line utility derived from the Jupyter notebook `Langchain_search_weather_rag_agent_memory_variations.ipynb`. This project demonstrates a smart tool-calling assistant with support for Google Search (SerpAPI), current weather reports (OpenWeatherMap API), internal document lookup (PDF RAG), and three state-of-the-art context window management variations.

---

## 🏗️ Project Architecture & Layout

The project follows clean software design principles separating configuration, tools, core agent pipelines, and user execution endpoints:

```
langchain_agent_memory_variations/
├── .env.example              # Template configuration keys
├── README.md                 # Project guide & instructions
├── requirements.txt          # Python package requirements
├── main.py                   # CLI interactive application wrapper
├── config/
│   ├── __init__.py           # Package indicator
│   └── settings.py           # Loads env vars & initializes LLM
├── core/
│   ├── __init__.py           # Package indicator
│   ├── agent.py              # System prompt and LangChain agent setup
│   ├── memory.py             # Memory wrapper logic (Variations 1, 2, 3)
│   └── rag.py                # PDF Loader, Embeddings, FAISS vector store
└── tools/
    ├── __init__.py           # Exports agent tools
    ├── search.py             # Google Search (SerpAPI) Integration
    ├── weather.py            # OpenWeatherMap API Integration
    └── rag_tool.py           # Retriever interaction for document queries
```

---

## ⚙️ Configuration Setup

1. Copy `.env.example` to `.env` in the project root:
   ```bash
   cp .env.example .env
   ```
2. Populate the `.env` file with your credentials:
   - `OPENROUTER_API_KEY`: API Key for accessing Chat LLMs (default `openai/gpt-4o-mini`).
   - `SERPAPI_API_KEY`: Google search wrapper credentials.
   - `OPENWEATHER_API_KEY`: OpenWeatherMap credentials.

*Note: If these keys are not loaded, the application will interactively prompt you for them at startup.*

---

## 🧠 Memory Variations Supported

1. **Complete History**: Retains the entire conversation log. This offers the best context but consumes more tokens as the conversation grows.
2. **Sliding Window (Last 10)**: Sends only the latest 10 messages (including tool requests and output blocks), restricting context window sizes.
3. **Summary Window**: Keeps the last 10 messages unchanged, but compresses older historical messages using a dynamic LLM summary update loop.

---

## 🚀 Running the Terminal Application

1. Open your terminal in the root workspace.
2. Activate your virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the interactive CLI:
   ```bash
   python main.py
   ```
4. Enter the path to any local PDF file you'd like to index (e.g. `d:\sample.pdf`), select a memory mode, and start typing your queries!
5. Use `/clear` to reset dialogue memory and `/exit` to shut down the console.
