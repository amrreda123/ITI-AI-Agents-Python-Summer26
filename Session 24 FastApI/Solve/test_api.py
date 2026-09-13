import io
import pytest
from fastapi.testclient import TestClient

from main import app, documents

client = TestClient(app)


def setup_function():
    # Reset in-memory database before each test
    documents.clear()
    documents[1] = {
        "id": 1,
        "title": "FastAPI Notes",
        "content": "REST and Validation basics",
        "priority": 1,
    }


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app_name"] == "Documents API"


def test_list_documents():
    response = client.get("/documents")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_document_success():
    response = client.get("/documents/1")
    assert response.status_code == 200
    assert response.json()["title"] == "FastAPI Notes"


def test_get_document_not_found():
    response = client.get("/documents/999")
    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "document_not_found",
            "message": "Document with ID 999 not found",
        }
    }


def test_create_document_success():
    payload = {
        "title": "Docker Guide",
        "content": "Comprehensive Docker notes",
        "priority": 3,
    }
    response = client.post("/documents", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 2
    assert data["title"] == "Docker Guide"
    assert data["priority"] == 3


def test_create_document_validation_error():
    # Invalid: title < 3 chars, priority > 5
    payload = {
        "title": "A",
        "content": "",
        "priority": 10,
    }
    response = client.post("/documents", json=payload)
    assert response.status_code == 422


def test_create_duplicate_title():
    payload = {
        "title": "FastAPI Notes",
        "content": "Duplicate content",
        "priority": 2,
    }
    response = client.post("/documents", json=payload)
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "duplicate_title",
            "message": "A document with this title already exists",
        }
    }


def test_update_document_success():
    payload = {
        "title": "FastAPI Advanced Notes",
        "content": "Pydantic and Uploads",
        "priority": 4,
    }
    response = client.put("/documents/1", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "FastAPI Advanced Notes"


def test_delete_document_success():
    response = client.delete("/documents/1")
    assert response.status_code == 200
    assert response.json() == {"deleted": 1}

    # Verify not found after delete
    response_check = client.get("/documents/1")
    assert response_check.status_code == 404


def test_upload_valid_txt_file():
    file_content = b"Hello, this is a test text file."
    file = io.BytesIO(file_content)
    response = client.post(
        "/documents/upload",
        files={"file": ("sample.txt", file, "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "sample.txt"
    assert data["content_type"] == "text/plain"
    assert data["size"] == len(file_content)


def test_upload_valid_pdf_file():
    file_content = b"%PDF-1.4 test binary dummy pdf content"
    file = io.BytesIO(file_content)
    response = client.post(
        "/documents/upload",
        files={"file": ("report.pdf", file, "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "report.pdf"
    assert data["content_type"] == "application/pdf"
    assert data["size"] == len(file_content)


def test_upload_invalid_file_type():
    file_content = b"<html><body>Not allowed</body></html>"
    file = io.BytesIO(file_content)
    response = client.post(
        "/documents/upload",
        files={"file": ("index.html", file, "text/html")},
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "unsupported_file_type",
            "message": "Only TXT (text/plain) and PDF (application/pdf) files are allowed",
        }
    }


if __name__ == "__main__":
    pytest.main(["-v", __file__])
