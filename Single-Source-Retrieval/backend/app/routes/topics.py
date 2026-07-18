from fastapi import APIRouter
from ..models import TopicsRequest, TopicsResponse

router = APIRouter()

@router.post("/topics", response_model=TopicsResponse)
async def get_topics(request: TopicsRequest):
    """
    Extracts the key topics/themes from the indexed document content.
    """
    mock_topics = [
        "Problem Framing & Scope",
        "RAG Pipeline Architecture",
        "Local Embeddings & FAISS",
        "TTS/STT Speech I/O",
        "RAGAS Evaluation"
    ]
    return TopicsResponse(topics=mock_topics)
