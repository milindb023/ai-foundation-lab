from fastapi import APIRouter
from ..models import EvaluateRequest, EvaluateResponse

router = APIRouter()

@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_rag(request: EvaluateRequest):
    """
    Triggers a RAGAS metrics evaluation for the generated answer and retrieved context,
    logging the results to a local JSONL log file.
    """
    # In real implementation:
    # scores = evaluator.calculate_ragas_scores(request.document_id, request.question, request.answer)
    
    mock_scores = EvaluateResponse(
        faithfulness=0.92,
        answer_relevancy=0.88,
        context_precision=0.85,
        context_recall=0.89
    )
    
    # In real implementation:
    # evaluator.log_eval_to_jsonl(request.question, request.answer, mock_scores)
    
    return mock_scores
