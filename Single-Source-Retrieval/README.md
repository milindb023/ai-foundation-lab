# Single-Source-Retrieval (RAG-based QA Assistant)

A Retrieval-Augmented Generation (RAG) full-stack web application that allows users to upload a single PDF document and ask questions about its content. The application retrieves context from the document using local embeddings and FAISS search, re-ranks the chunks, and uses a hosted LLM to generate answers grounded in the source, complete with cited page numbers.

## Features
* **Single PDF Upload**: Index document up to 50MB.
* **Semantic Vector Search**: Sentence-Transformers embeddings stored in FAISS locally.
* **Re-Ranking**: Local Cross-Encoder model to improve top search result relevancy.
* **OpenRouter LLM Integration**: Grounded completions generated using Gemini 2.5 Flash.
* **Suggestions & Topics**: Extract primary themes and suggest starter questions.
* **Speech Capabilities**: Speech-to-Text questions input and Text-to-Speech answer output.
* **Metrics & Evaluation**: Automated RAGAS evaluation (faithfulness, relevancy, recall).

## Tech Stack
* **Frontend**: Next.js (App Router), React, Tailwind CSS, Lucide Icons.
* **Backend**: FastAPI, LangChain, FAISS, Sentence-Transformers.
* **DevOps**: Docker, Docker Compose, GitHub Actions.

## Directory Structure
```text
Single-Source-Retrieval/
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── routes/           # API routes (upload, query, suggestions, topics, etc.)
│   │   ├── services/         # Services (FAISS processor, embeddings, rag_pipeline, etc.)
│   │   ├── utils/            # General helpers (retry, etc.)
│   │   ├── main.py           # FastAPI server entry point
│   │   ├── config.py         # Config and environment manager
│   │   └── models.py         # Request/response validation schemas
│   ├── tests/                # Pytest tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/              # App router layouts and pages
│   │   ├── components/       # Interface components (UploadZone, ChatInterface)
│   │   ├── hooks/            # TTS and speech hooks
│   │   ├── lib/              # API Client helpers
│   │   └── types/            # TypeScript type declarations
│   └── Dockerfile
├── .github/workflows/        # CI workflows
└── docker-compose.yml
```

## Running the Application

### Using Docker Compose
1. Copy the environment template in backend:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Open `backend/.env` and specify your `OPENROUTER_API_KEY`.
3. Launch the stack:
   ```bash
   docker-compose up --build
   ```
4. Access the applications:
   * **Frontend**: `http://localhost:3000`
   * **Backend Documentation (Swagger)**: `http://localhost:8000/docs`
