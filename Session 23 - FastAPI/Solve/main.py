from fastapi import FastAPI, HTTPException, Query, status

app = FastAPI(
    title="Documents API",
    description="Lab 1 - JSON-Only Documents REST API with in-memory CRUD operations",
    version="1.0.0"
)

# -------------------------------------------------------------------
# Exercise 01: Health Endpoint
# -------------------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# -------------------------------------------------------------------
# Exercise 02: Build the In-Memory Resource
# -------------------------------------------------------------------
from fastapi import HTTPException

documents = {
    1: {"id": 1, "title": "FastAPI Notes", "content": "REST basics"}
}

@app.get("/documents")
def list_documents():
    return {"items": list(documents.values())}

@app.get("/documents/{document_id}")
def get_document(document_id: int):
    item = documents.get(document_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return item

# -------------------------------------------------------------------
# Exercise 03: POST - Create Document
# -------------------------------------------------------------------
@app.post("/documents", status_code=status.HTTP_201_CREATED)
def create_document(payload: dict):
    new_id = max(documents.keys(), default=0) + 1
    item = {"id": new_id, **payload}
    documents[new_id] = item
    return item


# -------------------------------------------------------------------
# Exercise 04: PUT - DELETE
# -------------------------------------------------------------------
@app.put("/documents/{document_id}")
def update_document(document_id: int, payload: dict):
    if document_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    documents[document_id] = {"id": document_id, **payload}
    return documents[document_id]

@app.delete("/documents/{document_id}")
def delete_document(document_id: int):
    if documents.pop(document_id, None) is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"deleted": document_id}

# -------------------------------------------------------------------
# Exercise 05: Query Parameters & Client Testing
# -------------------------------------------------------------------
@app.get("/search")
def search_documents(
    q: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
):
    items = list(documents.values())
    if q:
        items = [x for x in items if q.lower() in x.get("title", "").lower()]
    return {"items": items[:limit]}

