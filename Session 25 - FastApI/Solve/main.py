from fastapi import FastAPI, HTTPException, Query, status
from sqlalchemy import String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from schemas import DocumentCreate, DocumentResponse

app = FastAPI(
    title="Documents API with SQLite & SQLAlchemy",
    description="Lab 3 - Simple ORM Persistence with SQLite and SQLAlchemy",
    version="3.0.0",
)

# -------------------------------------------------------------------
# 01: SQLite Engine & Declarative Base
# -------------------------------------------------------------------
DATABASE_URL = "sqlite:///documents.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite in multithreaded environments
)


class Base(DeclarativeBase):
    pass


# -------------------------------------------------------------------
# 02: Define the Document ORM Model
# -------------------------------------------------------------------
class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[int] = mapped_column(default=1, nullable=False)


# Automatically create tables if missing
Base.metadata.create_all(engine)


# -------------------------------------------------------------------
# Health Check Endpoint
# -------------------------------------------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "database": "SQLite (documents.db)"}


# -------------------------------------------------------------------
# 03: Read All Documents with Session(engine)
# -------------------------------------------------------------------
@app.get("/documents", response_model=list[DocumentResponse], tags=["Documents"])
def list_documents():
    with Session(engine) as db:
        docs = db.query(Document).all()
        return docs


# -------------------------------------------------------------------
# 04: Create & Read One Document
# -------------------------------------------------------------------
@app.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Documents"],
)
def create_document(payload: DocumentCreate):
    with Session(engine) as db:
        doc = Document(
            title=payload.title,
            content=payload.content,
            priority=payload.priority,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc


@app.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
    tags=["Documents"],
)
def get_document(document_id: int):
    with Session(engine) as db:
        doc = db.get(Document, document_id)
        if doc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found",
            )
        return doc


# -------------------------------------------------------------------
# 05: Update, Delete & Search
# -------------------------------------------------------------------
@app.put(
    "/documents/{document_id}",
    response_model=DocumentResponse,
    tags=["Documents"],
)
def update_document(document_id: int, payload: DocumentCreate):
    with Session(engine) as db:
        doc = db.get(Document, document_id)
        if doc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found",
            )
        doc.title = payload.title
        doc.content = payload.content
        doc.priority = payload.priority
        db.commit()
        db.refresh(doc)
        return doc


@app.delete("/documents/{document_id}", tags=["Documents"])
def delete_document(document_id: int):
    with Session(engine) as db:
        doc = db.get(Document, document_id)
        if doc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found",
            )
        db.delete(doc)
        db.commit()
        return {"message": f"Document {document_id} deleted successfully"}


@app.get("/search", response_model=list[DocumentResponse], tags=["Documents"])
def search_documents(
    q: str | None = Query(default=None, description="Search keyword in title"),
    limit: int = Query(default=20, ge=1, le=100, description="Max results to return"),
):
    with Session(engine) as db:
        query = db.query(Document)
        if q:
            query = query.filter(Document.title.ilike(f"%{q}%"))
        return query.limit(limit).all()
