from fastapi import FastAPI
from routes.documents import router as documents_router

app = FastAPI(
    title="Documents API",
    description="SQLite-backed JSON API for documents with Alembic migrations, APIRouter, and interactive documentation.",
    version="1.0.0",
)

# Register routes
app.include_router(documents_router)


@app.get("/health", tags=["health"], summary="Health Check")
def health_check():
    return {"status": "ok", "api_version": "1.0.0"}
