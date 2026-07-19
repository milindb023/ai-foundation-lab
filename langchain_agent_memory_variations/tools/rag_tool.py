from langchain.tools import tool

# We will import core.rag dynamically inside the function or reference it safely
# to avoid circular imports.
@tool
def rag_tool(question: str) -> str:
    """Search the uploaded PDF and return relevant context. Use this when the user asks about the uploaded document, resume, policy, notes, or internal knowledge base."""
    print("📚 RAG TOOL CALLED")
    
    from langchain_agent_memory_variations.core import rag
    retriever = rag.get_retriever()
    pdf_path = rag.get_pdf_path()
    
    if not retriever:
        return "RAG database is not initialized. Please configure/build the vector store first."

    docs = retriever.invoke(question)

    if not docs:
        return "No relevant information found in the uploaded PDF."

    formatted_chunks = []
    for i, doc in enumerate(docs, start=1):
        page = doc.metadata.get("page", "unknown")
        source = doc.metadata.get("source", pdf_path or "unknown_pdf")
        formatted_chunks.append(
            f"Chunk {i} | Source: {source} | Page: {page}\n{doc.page_content}"
        )

    return "\n\n".join(formatted_chunks)
