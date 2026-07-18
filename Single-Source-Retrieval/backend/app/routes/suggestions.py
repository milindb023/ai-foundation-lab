from fastapi import APIRouter
from ..models import SuggestionsRequest, SuggestionsResponse

router = APIRouter()

@router.post("/suggestions", response_model=SuggestionsResponse)
async def get_suggestions(request: SuggestionsRequest):
    """
    Generates follow-up question suggestions to guide user exploration of the PDF.
    """
    mock_suggestions = [
        "What is the scope of the Single-Source-Retrieval project?",
        "Which embeddings are run offline without API costs?",
        "Explain the quantitative evaluation metrics used."
    ]
    return SuggestionsResponse(suggestions=mock_suggestions)
