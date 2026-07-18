import React, { useState, useEffect, useRef } from "react";
import { Send, Mic, Volume2, Sparkles, BookOpen, BarChart3, AlertCircle, Loader2 } from "lucide-react";
import { Message, Citation, EvaluationMetrics } from "../types";
import { queryRAG, getSuggestions, evaluateAnswer } from "../lib/api";
import { useSpeechRecognition } from "../hooks/useSpeechRecognition";
import { useTextToSpeech } from "../hooks/useTextToSpeech";

interface ChatInterfaceProps {
  documentId: string;
  filename: string;
}

export function ChatInterface({ documentId, filename }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [evaluations, setEvaluations] = useState<Record<string, EvaluationMetrics>>({});
  const [isEvaluating, setIsEvaluating] = useState<Record<string, boolean>>({});

  const chatEndRef = useRef<HTMLDivElement>(null);
  
  const { isListening, transcript, startListening, isSupported: isSpeechSupported } = useSpeechRecognition();
  const { speak, isPlaying: isTtsPlaying, stop: stopTts } = useTextToSpeech();

  // Scroll to bottom on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // Load starter question suggestions
  useEffect(() => {
    async function loadSuggestions() {
      try {
        const list = await getSuggestions(documentId);
        setSuggestions(list);
      } catch (err) {
        console.error("Error loading suggestions:", err);
      }
    }
    loadSuggestions();
  }, [documentId]);

  // Handle Speech-to-Text transcript changes
  useEffect(() => {
    if (transcript) {
      setInput(transcript);
    }
  }, [transcript]);

  const handleSend = async (text: string) => {
    if (!text.trim() || isLoading) return;

    const userMessage: Message = {
      id: Math.random().toString(),
      sender: "user",
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await queryRAG(documentId, text);
      
      const botMessage: Message = {
        id: Math.random().toString(),
        sender: "bot",
        text: response.answer,
        citations: response.citations,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const errorMessage: Message = {
        id: Math.random().toString(),
        sender: "bot",
        text: "Sorry, I encountered an error searching the document. Please verify the connection.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEvaluate = async (messageId: string, text: string) => {
    const userMessage = [...messages].reverse().find(m => m.sender === "user");
    if (!userMessage) return;

    setIsEvaluating(prev => ({ ...prev, [messageId]: true }));
    try {
      const metrics = await evaluateAnswer(documentId, userMessage.text, text);
      setEvaluations(prev => ({ ...prev, [messageId]: metrics }));
    } catch (err) {
      console.error("Evaluation error:", err);
    } finally {
      setIsEvaluating(prev => ({ ...prev, [messageId]: false }));
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto flex flex-col h-[600px] rounded-2xl border border-slate-800 bg-slate-950/40 backdrop-blur-xl shadow-2xl overflow-hidden">
      {/* Header bar */}
      <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/40">
        <div>
          <h2 className="text-md font-semibold text-slate-100 flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-emerald-500" />
            <span>Chatting with Document</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5 max-w-[280px] sm:max-w-md truncate">
            Active: {filename}
          </p>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-950/30 border border-emerald-800/40 text-emerald-400 text-xs">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Indexed in FAISS</span>
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-track-transparent scrollbar-thumb-slate-800">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-slate-400 space-y-4">
            <Sparkles className="h-10 w-10 text-emerald-500 animate-pulse" />
            <p className="text-sm font-medium">Ask anything about this document to get started</p>
          </div>
        )}
        
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"} animate-in fade-in-50 duration-300`}>
            <div className={`flex flex-col max-w-[85%] sm:max-w-[75%] rounded-2xl px-5 py-4 ${
              msg.sender === "user" 
                ? "bg-emerald-500 text-slate-950 rounded-tr-none shadow-[0_4px_15px_rgba(16,185,129,0.15)]" 
                : "bg-slate-900/60 text-slate-200 border border-slate-800/80 rounded-tl-none shadow-md"
            }`}>
              {/* Text content */}
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.text}</p>
              
              {/* Citations block */}
              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-4 pt-3 border-t border-slate-800/60">
                  <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block mb-2">Sources referenced:</span>
                  <div className="grid grid-cols-1 gap-2">
                    {msg.citations.map((cit, idx) => (
                      <div key={idx} className="text-xs p-2 rounded bg-slate-950/50 border border-slate-800/40 flex items-start gap-2">
                        <span className="px-1.5 py-0.5 rounded bg-emerald-950/50 border border-emerald-800/30 text-emerald-400 text-[10px] font-semibold mt-0.5">
                          Page {cit.page_number || "N/A"}
                        </span>
                        <p className="text-slate-300 leading-tight italic">"{cit.text}"</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* RAGAS Metrics block */}
              {evaluations[msg.id] && (
                <div className="mt-3 pt-3 border-t border-slate-800/60 grid grid-cols-2 gap-2 text-xs p-2 rounded bg-slate-950/40 border border-slate-800/40 text-slate-300">
                  <div className="flex justify-between">
                    <span>Faithfulness:</span>
                    <span className="font-semibold text-emerald-400">{evaluations[msg.id].faithfulness}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Relevancy:</span>
                    <span className="font-semibold text-emerald-400">{evaluations[msg.id].answer_relevancy}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Precision:</span>
                    <span className="font-semibold text-emerald-400">{evaluations[msg.id].context_precision}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Recall:</span>
                    <span className="font-semibold text-emerald-400">{evaluations[msg.id].context_recall || "N/A"}</span>
                  </div>
                </div>
              )}

              {/* Action buttons (Bot only) */}
              {msg.sender === "bot" && (
                <div className="mt-3 flex items-center justify-end gap-3 text-slate-400 border-t border-slate-800/30 pt-2 text-[11px]">
                  <button 
                    onClick={() => speak(msg.text)} 
                    className="hover:text-slate-200 transition-colors flex items-center gap-1"
                  >
                    <Volume2 className="h-3.5 w-3.5" />
                    <span>Speak</span>
                  </button>
                  <button 
                    onClick={() => handleEvaluate(msg.id, msg.text)} 
                    disabled={isEvaluating[msg.id]}
                    className="hover:text-slate-200 transition-colors flex items-center gap-1"
                  >
                    {isEvaluating[msg.id] ? (
                      <Loader2 className="h-3 w-3 animate-spin" />
                    ) : (
                      <BarChart3 className="h-3.5 w-3.5" />
                    )}
                    <span>Score with RAGAS</span>
                  </button>
                  <span className="text-[10px] text-slate-500 self-end ml-auto">{msg.timestamp}</span>
                </div>
              )}
              {msg.sender === "user" && (
                <span className="text-[9px] text-emerald-950/70 text-right mt-1.5 block">{msg.timestamp}</span>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-900/40 text-slate-400 border border-slate-800/60 rounded-2xl rounded-tl-none px-5 py-4 flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin text-emerald-500" />
              <span className="text-xs">Searching documents & generating answer...</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Suggested questions */}
      {suggestions.length > 0 && !isLoading && (
        <div className="px-6 py-2 bg-slate-900/20 border-t border-slate-800/40 flex items-center gap-2 overflow-x-auto no-scrollbar">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider whitespace-nowrap">Suggested:</span>
          {suggestions.map((sug, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(sug)}
              className="text-xs px-3 py-1 rounded-full border border-slate-800 bg-slate-950/40 hover:bg-slate-900 text-slate-300 hover:text-slate-200 whitespace-nowrap transition-all duration-200"
            >
              {sug}
            </button>
          ))}
        </div>
      )}

      {/* Input panel */}
      <div className="p-4 border-t border-slate-800 bg-slate-900/40 flex items-center gap-2">
        <button
          onClick={startListening}
          className={`p-3 rounded-xl border border-slate-800 bg-slate-950/60 hover:bg-slate-900 transition-all ${
            isListening ? "text-emerald-500 border-emerald-800 shadow-[0_0_15px_rgba(16,185,129,0.1)]" : "text-slate-400"
          }`}
          title="Speak Question"
        >
          <Mic className={`h-5 w-5 ${isListening ? "animate-pulse" : ""}`} />
        </button>
        
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend(input)}
          placeholder={isListening ? "Listening..." : "Ask a question about the document..."}
          disabled={isLoading || isListening}
          className="flex-1 px-4 py-3 rounded-xl bg-slate-950/60 border border-slate-800 text-slate-200 text-sm focus:outline-none focus:border-slate-700 placeholder-slate-500"
        />

        <button
          onClick={() => handleSend(input)}
          disabled={!input.trim() || isLoading || isListening}
          className="p-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-medium transition-colors shadow-md disabled:bg-slate-800 disabled:text-slate-500 disabled:shadow-none"
        >
          <Send className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
}
