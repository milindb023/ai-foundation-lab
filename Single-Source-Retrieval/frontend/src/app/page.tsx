"use client";

import React, { useState } from "react";
import { UploadZone } from "../components/UploadZone";
import { ChatInterface } from "../components/ChatInterface";
import { Sparkles, FileText, ArrowLeft, BrainCircuit } from "lucide-react";

export default function HomePage() {
  const [docId, setDocId] = useState<string | null>(null);
  const [chunkCount, setChunkCount] = useState<number>(0);
  const [filename, setFilename] = useState<string>("");

  const handleUploadSuccess = (id: string, count: number, name: string) => {
    setDocId(id);
    setChunkCount(count);
    setFilename(name);
  };

  const handleReset = () => {
    setDocId(null);
    setChunkCount(0);
    setFilename("");
  };

  return (
    <main className="relative min-h-screen flex flex-col items-center justify-center py-12 px-4 bg-slate-950 overflow-hidden">
      {/* Premium background glowing radial blobs */}
      <div className="absolute top-[-15%] left-[-15%] w-[60%] h-[60%] rounded-full bg-emerald-500/5 blur-[150px] pointer-events-none" />
      <div className="absolute bottom-[-15%] right-[-15%] w-[60%] h-[60%] rounded-full bg-blue-600/5 blur-[150px] pointer-events-none" />

      {/* Header section */}
      <div className="w-full max-w-4xl flex flex-col items-center mb-10 text-center z-10">
        <div className="flex items-center gap-2.5 mb-3 px-3 py-1 rounded-full border border-slate-800 bg-slate-900/30 text-slate-300 text-xs font-medium shadow-inner animate-pulse">
          <BrainCircuit className="h-4 w-4 text-emerald-500" />
          <span>Next-Generation Document Intelligence</span>
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl text-transparent bg-clip-text bg-gradient-to-r from-slate-100 via-slate-200 to-slate-400">
          Single Source Retrieval
        </h1>
        <p className="text-md text-slate-400 max-w-md mt-3 leading-relaxed">
          Upload a document and ask natural language questions with page citations and answer validation.
        </p>
      </div>

      {/* Main interactive cards switcher */}
      <div className="w-full z-10 flex flex-col items-center">
        {!docId ? (
          <UploadZone onUploadSuccess={handleUploadSuccess} />
        ) : (
          <div className="w-full space-y-4">
            <div className="w-full max-w-4xl mx-auto flex items-center justify-between px-2">
              <button
                onClick={handleReset}
                className="flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
              >
                <ArrowLeft className="h-3.5 w-3.5" />
                <span>Upload a different PDF</span>
              </button>
              
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <FileText className="h-3.5 w-3.5 text-emerald-500" />
                <span>Indexed {chunkCount} chunks</span>
              </div>
            </div>
            
            <ChatInterface documentId={docId} filename={filename} />
          </div>
        )}
      </div>

      {/* Footer bar */}
      <div className="w-full max-w-4xl text-center text-xs text-slate-600 mt-16 z-10">
        <p>© 2026 Single-Source-Retrieval Capstone Reference Template. Powered by local embeddings & Gemini.</p>
      </div>
    </main>
  );
}
