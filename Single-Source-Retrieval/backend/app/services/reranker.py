import logging
from typing import List, Dict, Any

logger = logging.getLogger("RAG-Reranker")

class RerankerService:
    """
    Service to re-rank retrieved documents locally using a Cross-Encoder.
    Lazy-loads the model only when re-ranking functions are executed.
    """
    def __init__(self):
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info("Lazy loading CrossEncoder model 'ms-marco-MiniLM-L-6-v2'...")
            try:
                from sentence_transformers import CrossEncoder
                self._model = CrossEncoder("ms-marco-MiniLM-L-6-v2")
                logger.info("Cross-Encoder loaded successfully.")
            except Exception as e:
                logger.warning(f"Could not load CrossEncoder (running mock fallback): {e}")
                # Mock fallback
                class MockEncoder:
                    def predict(self, pairs):
                        import numpy as np
                        # Return scores between 0 and 1
                        return np.random.rand(len(pairs)).tolist()
                self._model = MockEncoder()
        return self._model

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Re-ranks a list of documents relative to a query.
        Each document is expected to have a 'text' key.
        """
        if not documents:
            return []
            
        pairs = [[query, doc["text"]] for doc in documents]
        scores = self.model.predict(pairs)
        
        # Attach scores to documents
        for idx, score in enumerate(scores):
            documents[idx]["rerank_score"] = float(score)
            
        # Sort documents descending by score
        documents.sort(key=lambda x: x["rerank_score"], reverse=True)
        return documents[:top_k]

reranker_service = RerankerService()
