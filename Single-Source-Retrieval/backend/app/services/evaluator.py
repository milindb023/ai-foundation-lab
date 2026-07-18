import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from ..config import settings

logger = logging.getLogger("RAG-Evaluator")

class EvaluatorService:
    """
    Calculates RAGAS evaluation metrics for generated answers relative to context and logs them to JSONL.
    """
    def __init__(self):
        self.log_path = settings.EVAL_LOG_PATH

    def calculate_ragas_scores(self, doc_id: str, question: str, answer: str, context: List[str]) -> Dict[str, float]:
        """
        Invokes RAGAS evaluation framework to score answer quality.
        """
        logger.info(f"Computing RAGAS evaluation for RAG query...")
        
        # Real logic steps:
        # 1. Format the question, generated answer, and context into a Dataset.
        # 2. Call ragas.evaluate(dataset, metrics=[faithfulness, answer_relevancy, ...]).
        # 3. Return parsed float score values.
        
        # Mock scores returned for the template execution
        mock_scores = {
            "faithfulness": 0.92,
            "answer_relevancy": 0.88,
            "context_precision": 0.85,
            "context_recall": 0.89
        }
        return mock_scores

    def log_eval_to_jsonl(self, question: str, answer: str, scores: Dict[str, float]):
        """
        Appends metrics evaluation results to a local JSONL log database.
        """
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "question": question,
            "answer_preview": answer[:60] + "..." if len(answer) > 60 else answer,
            "metrics": scores
        }
        
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
            logger.info(f"Evaluation logs successfully appended to {self.log_path}")
        except Exception as e:
            logger.error(f"Failed to log RAGAS evaluation to JSONL: {e}")

evaluator_service = EvaluatorService()
