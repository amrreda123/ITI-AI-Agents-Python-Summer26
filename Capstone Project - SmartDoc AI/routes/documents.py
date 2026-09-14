from fastapi import APIRouter, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from database import engine
from models import Document
from schemas import DocumentCreate, DocumentResponse, DocumentUpdate

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.get(
    "",
    response_model=list[DocumentResponse],
    status_code=status.HTTP_200_OK,
    summary="List all documents",
    description="Retrieve all stored documents from SQLite database.",
)
def list_documents():
    with Session(engine) as db:
        documents = db.query(Document).all()
        return documents


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new document",
    description="Create and persist a new document from JSON body.",
)
def create_document(payload: DocumentCreate):
    with Session(engine) as db:
        doc = Document(
            title=payload.title,
            content=payload.content,
            priority=payload.priority,
            description=payload.description,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get document by ID",
    description="Retrieve a single document by its integer ID.",
    responses={
        404: {"description": "Document not found", "content": {"application/json": {"example": {"detail": "Document not found"}}}}
    },
)
def get_document(document_id: int):
    with Session(engine) as db:
        doc = db.get(Document, document_id)
        if doc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )
        return doc


@router.put(
    "/{document_id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a document",
    description="Update an existing document's fields in SQLite.",
    responses={
        404: {"description": "Document not found", "content": {"application/json": {"example": {"detail": "Document not found"}}}}
    },
)
def update_document(document_id: int, payload: DocumentUpdate):
    with Session(engine) as db:
        doc = db.get(Document, document_id)
        if doc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )

        if payload.title is not None:
            doc.title = payload.title
        if payload.content is not None:
            doc.content = payload.content
        if payload.priority is not None:
            doc.priority = payload.priority
        if payload.description is not None:
            doc.description = payload.description

        db.commit()
        db.refresh(doc)
        return doc


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a document",
    description="Remove a document permanently from SQLite.",
    responses={
        404: {"description": "Document not found", "content": {"application/json": {"example": {"detail": "Document not found"}}}}
    },
)
def delete_document(document_id: int):
    with Session(engine) as db:
        doc = db.get(Document, document_id)
        if doc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )
        db.delete(doc)
        db.commit()
        return {"detail": f"Document {document_id} deleted successfully"}


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a text document",
    description="Accepts text/plain file uploads and extracts content into a new Document.",
    responses={
        400: {"description": "Unsupported media type / Invalid file", "content": {"application/json": {"example": {"detail": "Only text/plain files are supported"}}}}
    },
)
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in ["text/plain", "application/octet-stream"] and not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only text/plain files are supported",
        )

    try:
        raw_bytes = await file.read()
        content = raw_bytes.decode("utf-8")
        if not content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty",
            )
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only valid UTF-8 text/plain files are supported",
        )

    title = file.filename if file.filename else "Uploaded Document"
    if title.endswith(".txt"):
        title = title[:-4]

    with Session(engine) as db:
        doc = Document(
            title=title[:120],
            content=content,
            priority=1,
            description="Uploaded via /documents/upload",
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc
