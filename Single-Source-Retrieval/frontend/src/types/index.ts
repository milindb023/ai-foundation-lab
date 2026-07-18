export interface Citation {
  chunk_id: string;
  text: string;
  page_number?: number;
}

export interface Message {
  id: string;
  sender: "user" | "bot";
  text: string;
  citations?: Citation[];
  timestamp: string;
}

export interface EvaluationMetrics {
  faithfulness?: number;
  answer_relevancy?: number;
  context_precision?: number;
  context_recall?: number;
}
