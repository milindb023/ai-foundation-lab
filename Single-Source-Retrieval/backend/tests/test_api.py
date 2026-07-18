from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Checks that the health endpoint returns status ok.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_upload_pdf():
    """
    Checks PDF uploading validations.
    """
    # Send non-PDF file
    bad_response = client.post(
        "/api/upload",
        files={"file": ("test.txt", b"dummy plain text", "text/plain")}
    )
    assert bad_response.status_code == 400
    
    # Send PDF file
    response = client.post(
        "/api/upload",
        files={"file": ("test.pdf", b"%PDF-1.4 mock pdf header bytes", "application/pdf")},
        data={"description": "Test doc upload"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "document_id" in json_data
    assert "chunk_count" in json_data
    assert json_data["chunk_count"] > 0

def test_query_rag():
    """
    Validates RAG query endpoint response fields.
    """
    response = client.post(
        "/api/query",
        json={"document_id": "mock_id", "question": "What is FAISS?"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "answer" in json_data
    assert "citations" in json_data
    assert len(json_data["citations"]) > 0

def test_topics():
    """
    Verifies topics extraction.
    """
    response = client.post(
        "/api/topics",
        json={"document_id": "mock_id"}
    )
    assert response.status_code == 200
    assert "topics" in response.json()

def test_suggestions():
    """
    Verifies question recommendations.
    """
    response = client.post(
        "/api/suggestions",
        json={"document_id": "mock_id"}
    )
    assert response.status_code == 200
    assert "suggestions" in response.json()

def test_tts():
    """
    Verifies TTS output response streaming headers.
    """
    response = client.post(
        "/api/tts",
        json={"text": "Hello world"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
