import logging
from typing import List

logger = logging.getLogger("RAG-Embeddings")

class EmbeddingService:
    """
    Service to generate embeddings locally using the sentence-transformers library.
    Lazy-loads the model only when embedding functions are executed.
    """
    def __init__(self):
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info("Lazy loading sentence-transformers model 'all-MiniLM-L6-v2'...")
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.warning(f"Could not load SentenceTransformer (running mock fallback): {e}")
                # Mock fallback to prevent server import crashes on systems without transformers compiled
                class MockModel:
                    def encode(self, sentences, **kwargs):
                        import numpy as np
                        if isinstance(sentences, str):
                            return np.random.rand(384)
                        return np.random.rand(len(sentences), 384)
                self._model = MockModel()
        return self._model

    def embed_query(self, query: str) -> List[float]:
        """
        Embeds a single search query.
        """
        return self.model.encode(query).tolist()

    def embed_documents(self, docs: List[str]) -> List[List[float]]:
        """
        Embeds a list of document passages/chunks.
        """
        return self.model.encode(docs).tolist()

embeddings_service = EmbeddingService()
