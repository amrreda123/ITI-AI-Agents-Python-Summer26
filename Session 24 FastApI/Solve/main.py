import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile, status
from fastapi.responses import JSONResponse

from schemas import DocumentCreate, DocumentResponse

# -------------------------------------------------------------------
# 04: Load Environment Configuration (.env)
# -------------------------------------------------------------------
load_dotenv()
APP_NAME = os.getenv("APP_NAME", "Documents API")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "5"))

app = FastAPI(
    title=APP_NAME,
    description="Lab 2 - Hardened Documents REST API with Validation, Uploads & Structured Errors",
    version="2.0.0",
)

# -------------------------------------------------------------------
# 05: Custom Application Error & Global Exception Handler
# -------------------------------------------------------------------
class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


# -------------------------------------------------------------------
# In-Memory Storage
# -------------------------------------------------------------------
documents: dict[int, dict] = {
    1: {
        "id": 1,
        "title": "FastAPI Notes",
        "content": "REST and Validation basics",
        "priority": 1,
    }
}


# -------------------------------------------------------------------
# Health Check Endpoint
# -------------------------------------------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "app_name": APP_NAME}


# -------------------------------------------------------------------
# 01 & 02: Typed Documents CRUD Endpoints with Pydantic Validation
# -------------------------------------------------------------------
@app.get("/documents", response_model=list[DocumentResponse], tags=["Documents"])
def list_documents():
    return list(documents.values())


@app.get("/documents/{document_id}", response_model=DocumentResponse, tags=["Documents"])
def get_document(document_id: int):
    item = documents.get(document_id)
    if item is None:
        raise AppError(
            code="document_not_found",
            message=f"Document with ID {document_id} not found",
            status_code=404,
        )
    return item


@app.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Documents"],
)
def create_document(payload: DocumentCreate):
    # Enforce Business Rule: Unique Title
    for doc in documents.values():
        if doc["title"].lower() == payload.title.lower():
            raise AppError(
                code="duplicate_title",
                message="A document with this title already exists",
                status_code=400,
            )

    new_id = max(documents.keys(), default=0) + 1
    item = {"id": new_id, **payload.model_dump()}
    documents[new_id] = item
    return item


@app.put(
    "/documents/{document_id}",
    response_model=DocumentResponse,
    tags=["Documents"],
)
def update_document(document_id: int, payload: DocumentCreate):
    if document_id not in documents:
        raise AppError(
            code="document_not_found",
            message=f"Document with ID {document_id} not found",
            status_code=404,
        )

    # Check for duplicate title on other documents
    for doc_id, doc in documents.items():
        if doc_id != document_id and doc["title"].lower() == payload.title.lower():
            raise AppError(
                code="duplicate_title",
                message="Another document with this title already exists",
                status_code=400,
            )

    documents[document_id] = {"id": document_id, **payload.model_dump()}
    return documents[document_id]


@app.delete("/documents/{document_id}", tags=["Documents"])
def delete_document(document_id: int):
    if documents.pop(document_id, None) is None:
        raise AppError(
            code="document_not_found",
            message=f"Document with ID {document_id} not found",
            status_code=404,
        )
    return {"deleted": document_id}


@app.get("/search", response_model=list[DocumentResponse], tags=["Documents"])
def search_documents(
    q: str | None = Query(default=None, description="Search keyword for title"),
    limit: int = Query(default=20, ge=1, le=100, description="Max number of results"),
):
    items = list(documents.values())
    if q:
        items = [x for x in items if q.lower() in x.get("title", "").lower()]
    return items[:limit]


# -------------------------------------------------------------------
# 03: File Upload Endpoint
# -------------------------------------------------------------------
@app.post("/documents/upload", tags=["Upload"])
async def upload_document(file: UploadFile = File(...)):
    allowed_types = {"text/plain", "application/pdf"}

    if file.content_type not in allowed_types:
        raise AppError(
            code="unsupported_file_type",
            message="Only TXT (text/plain) and PDF (application/pdf) files are allowed",
            status_code=400,
        )

    content = await file.read()
    max_size_bytes = MAX_UPLOAD_MB * 1024 * 1024

    if len(content) > max_size_bytes:
        raise AppError(
            code="file_too_large",
            message=f"File exceeds maximum allowed size of {MAX_UPLOAD_MB}MB",
            status_code=400,
        )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
    }
