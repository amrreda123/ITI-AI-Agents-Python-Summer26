"""Comprehensive HTTP Contract and Endpoint Verification for SmartDoc AI."""

import io
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from main import app
from schemas import AIAnalysisResponse

client = TestClient(app)


def run_tests():
    print("========================================")
    print(" SmartDoc AI - Complete Contract Tests  ")
    print("========================================")

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print(f"[PASS] GET /health -> Status {res.status_code} ({res.json()})")

    # 2. List documents
    res = client.get("/documents")
    assert res.status_code == 200
    print(f"[PASS] GET /documents -> Status {res.status_code}")

    # 3. Create document (Valid)
    valid_doc = {
        "title": "FastAPI Architecture Notes",
        "content": "FastAPI is a modern web framework for building APIs with Python 3.8+ with automatic OpenAPI and interactive Swagger docs.",
        "priority": 3,
        "description": "Notes on FastAPI core strengths",
    }
    res = client.post("/documents", json=valid_doc)
    assert res.status_code == 201, f"Expected 201, got {res.status_code}"
    doc_data = res.json()
    doc_id = doc_data["id"]
    print(f"[PASS] POST /documents (Valid) -> Status {res.status_code} (Created Doc ID: {doc_id})")

    # 4. Create document (Invalid Body -> 422)
    invalid_doc = {"title": "X", "content": ""}  # Title too short (<3)
    res = client.post("/documents", json=invalid_doc)
    assert res.status_code == 422, f"Expected 422, got {res.status_code}"
    print(f"[PASS] POST /documents (Invalid) -> Status {res.status_code} (Validation Error Handled)")

    # 5. Get document by ID (Existing -> 200)
    res = client.get(f"/documents/{doc_id}")
    assert res.status_code == 200
    assert res.json()["title"] == valid_doc["title"]
    print(f"[PASS] GET /documents/{doc_id} -> Status {res.status_code}")

    # 6. Get document by ID (Missing -> 404)
    res = client.get("/documents/999999")
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"
    print(f"[PASS] GET /documents/999999 -> Status {res.status_code} (404 Not Found Handled)")

    # 7. Upload document (Valid text/plain -> 201)
    file_content = b"AI Agents in Python allow autonomous LLM models to call functions, query databases, and solve multi-step tasks safely."
    files = {"file": ("ai_agents_guide.txt", io.BytesIO(file_content), "text/plain")}
    res = client.post("/documents/upload", files=files)
    assert res.status_code == 201, f"Expected 201, got {res.status_code}"
    uploaded_doc_id = res.json()["id"]
    print(f"[PASS] POST /documents/upload (Valid) -> Status {res.status_code} (Uploaded Doc ID: {uploaded_doc_id})")

    # 8. Upload document (Invalid media type -> 400)
    files_invalid = {"file": ("image.png", io.BytesIO(b"\x89PNG\r\n\x1a\n"), "image/png")}
    res = client.post("/documents/upload", files=files_invalid)
    assert res.status_code == 400, f"Expected 400, got {res.status_code}"
    print(f"[PASS] POST /documents/upload (Invalid MIME) -> Status {res.status_code} (400 Bad Request Handled)")

    # 9. AI Analysis with mocked Gemini service (Verifying contract & DB update)
    print("\n--- Testing Gemini Structured Document Analysis Pipeline ---")
    mock_analysis = AIAnalysisResponse(
        summary="A concise summary of FastAPI features and high performance architecture.",
        key_points=["Modern web framework", "Automatic OpenAPI docs", "Fast async performance"],
        category="technical",
        suggested_priority=3,
    )

    with patch("routes.ai.analyze_document_content", return_value=mock_analysis):
        res = client.post(f"/documents/{doc_id}/analyze")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        analysis = res.json()
        assert analysis["summary"] == mock_analysis.summary
        assert analysis["category"] == "technical"
        assert analysis["suggested_priority"] == 3
        print(f"[PASS] POST /documents/{doc_id}/analyze -> Status {res.status_code}")
        print(f"       Category: {analysis['category']} | Priority: {analysis['suggested_priority']}")
        print(f"       Summary: {analysis['summary']}")

    # Verify that ai_summary was persisted in the database
    res = client.get(f"/documents/{doc_id}")
    assert res.json()["ai_summary"] == mock_analysis.summary
    print(f"[PASS] Verified 'ai_summary' column persistence in SQLite DB.")

    # 10. AI Analysis (Missing Doc -> 404)
    res = client.post("/documents/999999/analyze")
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"
    print(f"[PASS] POST /documents/999999/analyze -> Status {res.status_code} (404 Handled)")

    # 11. AI Read-Only Agent with mocked tool reasoning (POST /agent/ask -> 200)
    print("\n--- Testing Read-Only AI Agent Endpoint & Dispatch Pipeline ---")
    mock_agent_result = {
        "answer": "Based on the stored documents, we have 'FastAPI Architecture Notes' and 'ai_agents_guide'.",
        "steps_taken": 2,
        "tools_called": ["list_documents"],
    }
    with patch("routes.ai.run_agent", return_value=mock_agent_result):
        agent_payload = {"message": "List available documents and summarize them."}
        res = client.post("/agent/ask", json=agent_payload)
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        agent_res = res.json()
        assert agent_res["steps_taken"] == 2
        assert "list_documents" in agent_res["tools_called"]
        print(f"[PASS] POST /agent/ask -> Status {res.status_code}")
        print(f"       Tools Called: {agent_res['tools_called']}")
        print(f"       Steps Taken: {agent_res['steps_taken']}")
        print(f"       Agent Answer:\n       {agent_res['answer']}")

    print("\n=======================================================")
    print(" ALL SMARTDOC AI VERIFICATION CONTRACT TESTS PASSED! [SUCCESS]")
    print("=======================================================")


if __name__ == "__main__":
    run_tests()
