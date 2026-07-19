from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Module level state
_retriever = None
_pdf_path = None

def get_retriever():
    """Gets the initialized retriever."""
    return _retriever

def get_pdf_path():
    """Gets the path of the loaded PDF file."""
    return _pdf_path

def build_vectorstore(pdf_path: str):
    """Loads a PDF, splits text, computes embeddings, and builds a FAISS vector store."""
    global _retriever, _pdf_path
    
    print(f"📖 Loading PDF from: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("✂️ Splitting document into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    
    print(f"Total pages loaded: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")

    print("🧠 Generating HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)...")
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("🗄️ Indexing documents in FAISS...")
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    _retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    _pdf_path = pdf_path
    
    print("✅ FAISS vector store created successfully!")
    return _retriever
