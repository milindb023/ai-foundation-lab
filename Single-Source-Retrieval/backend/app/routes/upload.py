from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from ..models import UploadResponse
import uuid

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...), 
    description: Optional[str] = Form(None)
):
    """
    Accepts a single PDF file and description, extracts text,
    creates overlapping chunks, embeds them, and saves to FAISS.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Generate unique document ID
    doc_id = str(uuid.uuid4())
    
    # In real implementation:
    # chunk_count = document_processor.process_pdf(file.file, doc_id, description)
    chunk_count = 37  # Mock count
    
    return UploadResponse(document_id=doc_id, chunk_count=chunk_count)
