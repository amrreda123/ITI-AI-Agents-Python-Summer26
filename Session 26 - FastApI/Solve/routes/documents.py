from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import engine
from models import Document
from schemas import DocumentCreate, DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.get(
    "",
    response_model=list[DocumentResponse],
    summary="List all documents",
    description="Retrieve all stored documents from the SQLite database.",
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
    description="Create a new document and persist it in the SQLite database.",
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
    summary="Get one document by ID",
    description="Retrieve a single document by its primary key ID.",
    responses={
        404: {
            "description": "Document not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Document not found"}
                }
            },
        }
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
    summary="Update an existing document",
    description="Update title, content, priority, or description of a document.",
    responses={
        404: {
            "description": "Document not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Document not found"}
                }
            },
        }
    },
)
def update_document(document_id: int, payload: DocumentCreate):
    with Session(engine) as db:
        doc = db.get(Document, document_id)
        if doc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )
        doc.title = payload.title
        doc.content = payload.content
        doc.priority = payload.priority
        doc.description = payload.description
        db.commit()
        db.refresh(doc)
        return doc


@router.delete(
    "/{document_id}",
    summary="Delete a document",
    description="Delete a document permanently from the SQLite database.",
    responses={
        404: {
            "description": "Document not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Document not found"}
                }
            },
        }
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
        return {"message": "Document deleted"}
