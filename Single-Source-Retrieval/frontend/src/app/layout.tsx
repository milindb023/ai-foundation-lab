import React from "react";
import "../index.css"; // Assumed styling location for Tailwind directives

export const metadata = {
  title: "Single Source QA Assistant",
  description: "Retrieval-Augmented Generation (RAG) assistant for PDF documents.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100 min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
