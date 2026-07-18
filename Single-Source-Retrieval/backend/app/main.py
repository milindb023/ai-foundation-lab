from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .config import settings
from .routes import upload, query, suggestions, topics, tts, evaluate

# Setup basic log formatters
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("RAG-API")

app = FastAPI(
    title="Single Source Retrieval API",
    description="FastAPI Backend for single-document RAG Q&A Assistant.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware configuration for cross-origin resource requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Route registers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(suggestions.router, prefix="/api", tags=["Suggestions"])
app.include_router(topics.router, prefix="/api", tags=["Topics"])
app.include_router(tts.router, prefix="/api", tags=["TTS"])
app.include_router(evaluate.router, prefix="/api", tags=["Evaluate"])

@app.get("/health", tags=["Health"])
def health_check():
    """
    Service health check monitoring endpoint.
    """
    logger.debug("Health status requested.")
    return {"status": "ok"}
