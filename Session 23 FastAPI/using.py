from fastapi import FastAPI, Query ,HTTPException, status
app = FastAPI(
    title="My API",
    version="1.0.0",
)
@app.get("/health")
def health_check():
    return {"status": "healthy"}


documents = {
    101: {
        "id": 101,
        "title": "Python Basics",
        "author": "Ahmed",
        "category": "Programming"
    },
    102: {
        "id": 102,
        "title": "Machine Learning Introduction",
        "author": "Sara",
        "category": "AI"
    },
    103: {
        "id": 103,
        "title": "Deep Learning Notes",
        "author": "Omar",
        "category": "AI"
    },
    104: {
        "id": 104,
        "title": "FastAPI Notes",
        "author": "Fatma",
        "category": "Backend"
    },
    105: {
        "id": 105,
        "title": "REST API Guide",
        "author": "Mohamed",
        "category": "Web Development"
    }
}
@app.get("/documents")
def get_documents():
    return list(documents.values())

@app.get("/documents/{document_id}")
def get_document(document_id: int):
    document = documents.get(document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return document

@app.delete("/documents/{document_id}")
def delete_document(document_id: int):
    if document_id in documents:
        del documents[document_id]
        return {"message": "Document deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

@app.get("/documentstitles")
def list_documents(
        q: str | None = Query(default=None, description="Search query for document titles"),
        limit: int = Query(default=10, description="Maximum number of documents to return", ge=1, le=100)
):
    return {"Query": q, "Limit": limit}


@app.get("/documentss")
def list_documents(q: str = None, limit: int = 10):
    items = list(documents.values())
    if q:
        items = [
            doc for doc in items
            if q.lower() in doc["title"].lower()
        ]
    items = items[:limit]
    return {
        "query": q,
        "limit": limit,
        "items": items
    }



# python -m uvicorn main:app --reload
# http://127.0.0.1:8000/docs
