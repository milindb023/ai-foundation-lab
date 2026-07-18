from fastapi import APIRouter
from ..models import QueryRequest, QueryResponse, Citation

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """
    Submits a user question, retrieves the top-k matches from FAISS,
    re-ranks them, passes the text to the LLM, and returns the grounded answer with citations.
    """
    # In real implementation:
    # answer, citations = rag_pipeline.execute_rag(request.document_id, request.question)
    
    # Mock data
    mock_citations = [
        Citation(
            chunk_id="chunk_101", 
            text="Single-document RAG indices are stored in local FAISS databases to avoid costs.",
            page_number=2
        ),
        Citation(
            chunk_id="chunk_105", 
            text="The evaluation pipeline uses RAGAS to compute faithfulness and recall.",
            page_number=6
        )
    ]
    
    mock_answer = (
        "According to page 2, the single-document RAG indices are stored in local FAISS databases "
        "to avoid costs. Additionally, as described on page 6, RAGAS is used in the evaluation "
        "pipeline to compute metrics such as faithfulness and recall."
    )
    
    return QueryResponse(answer=mock_answer, citations=mock_citations)
