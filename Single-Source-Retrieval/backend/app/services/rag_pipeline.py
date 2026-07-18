import logging
from typing import Tuple, List, Dict, Any
from ..models import Citation
from .embeddings import embeddings_service
from .reranker import reranker_service
from ..config import settings
from openai import OpenAI

logger = logging.getLogger("RAG-Pipeline")

class RAGPipeline:
    """
    Orchestrates the entire QA generation pipeline: query embedding, vector database 
    context retrieval, Cross-Encoder reranking, and grounded LLM prompt generation.
    """
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=settings.OPENROUTER_API_KEY
            )
        return self._client

    def execute_rag(self, doc_id: str, question: str) -> Tuple[str, List[Citation]]:
        """
        Executes query retrieval, ranking, context formatting, and LLM text generation.
        """
        logger.info(f"Running RAG pipeline for doc {doc_id} and question: '{question}'")
        
        # 1. Embed user query using local sentence-transformers
        query_vector = embeddings_service.embed_query(question)
        
        # 2. Retrieve top matching chunks from local FAISS index
        # Real logic: index = FAISS.load_local(f"{settings.FAISS_INDEX_PATH}/{doc_id}", embeddings_service)
        # docs = index.similarity_search_by_vector(query_vector, k=5)
        
        # Mock retrieval chunks
        retrieved_docs = [
            {
                "chunk_id": "chunk_101", 
                "text": "Single-document RAG indices are stored in local FAISS databases to avoid costs.",
                "page_number": 2
            },
            {
                "chunk_id": "chunk_105", 
                "text": "The evaluation pipeline uses RAGAS to compute faithfulness and recall.",
                "page_number": 6
            },
            {
                "chunk_id": "chunk_110", 
                "text": "The Next.js frontend connects to the FastAPI backend dynamically.",
                "page_number": 10
            }
        ]
        
        # 3. Re-rank retrieved items with Cross-Encoder to push best chunks to the top
        reranked_docs = reranker_service.rerank(question, retrieved_docs, top_k=2)
        
        # 4. Generate schemas list citations
        citations = [
            Citation(
                chunk_id=doc["chunk_id"], 
                text=doc["text"], 
                page_number=doc["page_number"]
            )
            for doc in reranked_docs
        ]
        
        # 5. Build system prompt
        context = "\n---\n".join([doc["text"] for doc in reranked_docs])
        
        # 6. Call Gemini model via OpenRouter
        if not settings.OPENROUTER_API_KEY:
            logger.warning("OPENROUTER_API_KEY is missing. Returning mock grounded completion.")
            mock_answer = (
                "According to page 2, the single-document RAG indices are stored in local FAISS databases "
                "to avoid costs. Additionally, as described on page 6, RAGAS is used in the evaluation "
                "pipeline to compute metrics such as faithfulness and recall."
            )
            return mock_answer, citations

        try:
            prompt = f"Grounded Context Info:\n{context}\n\nUser Question: {question}\n\nAnswer the question strictly using the provided context."
            response = self.client.chat.completions.create(
                model="google/gemini-2.5-flash",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful QA assistant. Answer user questions using only the provided facts. Do not hallucinate."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            answer = response.choices[0].message.content or "No response generated."
            return answer, citations
        except Exception as e:
            logger.error(f"Error calling LLM generation: {e}")
            return f"Failed to generate answer due to model request error: {e}", citations

rag_pipeline = RAGPipeline()
