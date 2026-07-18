import React, { useState, DragEvent } from "react";
import { Upload, FileText, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
import { uploadDocument } from "../lib/api";

interface UploadZoneProps {
  onUploadSuccess: (docId: string, chunkCount: number, filename: string) => void;
}

export function UploadZone({ onUploadSuccess }: UploadZoneProps) {
  const [dragActive, setDragActive] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  const handleDrag = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const processFile = async (file: File) => {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Only PDF files are supported.");
      return;
    }
    setError(null);
    setIsUploading(true);
    setStatus("Reading PDF and extracting content...");
    
    try {
      const response = await uploadDocument(file);
      setStatus("Embedding and indexing FAISS vectors...");
      onUploadSuccess(response.document_id, response.chunk_count, file.name);
      setStatus("Success!");
    } catch (err: any) {
      setError(err.message || "Failed to upload document");
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = async (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      await processFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      await processFile(e.target.files[0]);
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto">
      <div
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        className={`relative border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center transition-all duration-300 backdrop-blur-xl ${
          dragActive 
            ? "border-emerald-500 bg-emerald-950/20 shadow-[0_0_20px_rgba(16,185,129,0.15)]" 
            : "border-slate-800 bg-slate-950/40 hover:border-slate-700 shadow-xl"
        }`}
      >
        <input
          type="file"
          id="pdf-upload"
          accept=".pdf"
          className="hidden"
          onChange={handleFileInput}
          disabled={isUploading}
        />
        
        <div className={`p-4 rounded-full bg-slate-900 border mb-4 transition-transform duration-300 ${dragActive ? "scale-110 border-emerald-500 text-emerald-500" : "border-slate-800 text-slate-400"}`}>
          {isUploading ? (
            <Loader2 className="h-8 w-8 animate-spin text-emerald-500" />
          ) : (
            <Upload className="h-8 w-8" />
          )}
        </div>

        <h3 className="text-lg font-medium text-slate-200 mb-2">
          {isUploading ? "Uploading Document..." : "Drag and drop your PDF here"}
        </h3>
        
        <p className="text-sm text-slate-400 text-center mb-6 max-w-xs">
          {isUploading ? status : "Upload a PDF up to 50MB. We'll chunk and generate local embeddings automatically."}
        </p>

        {!isUploading && (
          <label
            htmlFor="pdf-upload"
            className="px-6 py-2.5 rounded-lg bg-emerald-500 text-slate-950 text-sm font-semibold hover:bg-emerald-400 transition-colors shadow-[0_4px_14px_rgba(16,185,129,0.3)] hover:shadow-[0_4px_20px_rgba(16,185,129,0.4)] cursor-pointer"
          >
            Select PDF File
          </label>
        )}

        {error && (
          <div className="absolute -bottom-16 left-0 right-0 flex items-center gap-2 p-3 bg-red-950/30 border border-red-800/40 rounded-xl text-red-400 text-sm shadow-md animate-in fade-in slide-in-from-bottom-2">
            <AlertCircle className="h-5 w-5 shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </div>
    </div>
  );
}
