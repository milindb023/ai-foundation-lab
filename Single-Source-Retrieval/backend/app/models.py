from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class UploadResponse(BaseModel):
    document_id: str = Field(description="Unique identifier generated for the indexed document")
    chunk_count: int = Field(description="Number of chunks created and indexed in FAISS")

class Citation(BaseModel):
    chunk_id: str
    text: str
    page_number: Optional[int] = None

class QueryRequest(BaseModel):
    document_id: str
    question: str

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]

class SuggestionsRequest(BaseModel):
    document_id: str

class SuggestionsResponse(BaseModel):
    suggestions: List[str]

class TopicsRequest(BaseModel):
    document_id: str

class TopicsResponse(BaseModel):
    topics: List[str]

class TTSRequest(BaseModel):
    text: str

class EvaluateRequest(BaseModel):
    document_id: str
    question: str
    answer: str

class EvaluateResponse(BaseModel):
    faithfulness: Optional[float] = None
    answer_relevancy: Optional[float] = None
    context_precision: Optional[float] = None
    context_recall: Optional[float] = None
