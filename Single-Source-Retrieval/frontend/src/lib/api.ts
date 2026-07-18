import { Citation, EvaluationMetrics } from "../types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function uploadDocument(file: File): Promise<{ document_id: string; chunk_count: number }> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/api/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Upload failed");
  }
  return res.json();
}

export async function queryRAG(document_id: string, question: string): Promise<{ answer: string; citations: Citation[] }> {
  const res = await fetch(`${API_BASE}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id, question }),
  });

  if (!res.ok) {
    throw new Error("RAG Query request failed");
  }
  return res.json();
}

export async function getSuggestions(document_id: string): Promise<string[]> {
  const res = await fetch(`${API_BASE}/api/suggestions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id }),
  });

  if (!res.ok) {
    throw new Error("Suggestions fetch failed");
  }
  const data = await res.json();
  return data.suggestions;
}

export async function getTopics(document_id: string): Promise<string[]> {
  const res = await fetch(`${API_BASE}/api/topics`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id }),
  });

  if (!res.ok) {
    throw new Error("Topics extraction request failed");
  }
  const data = await res.json();
  return data.topics;
}

export async function textToSpeech(text: string): Promise<Blob> {
  const res = await fetch(`${API_BASE}/api/tts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    throw new Error("Audio synthesis request failed");
  }
  return res.blob();
}

export async function evaluateAnswer(
  document_id: string, 
  question: string, 
  answer: string
): Promise<EvaluationMetrics> {
  const res = await fetch(`${API_BASE}/api/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id, question, answer }),
  });

  if (!res.ok) {
    throw new Error("RAGAS quality score evaluation failed");
  }
  return res.json();
}
