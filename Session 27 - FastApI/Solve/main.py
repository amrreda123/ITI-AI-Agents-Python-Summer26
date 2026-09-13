from fastapi import FastAPI
from routes.documents import router as documents_router

app = FastAPI(
    title="Documents API",
    description="Capstone delivery of SQLite-backed JSON REST API with APIRouter, Alembic, and full HTTP testing.",
    version="1.0.0",
)

# Include router
app.include_router(documents_router)


@app.get("/health", tags=["health"], summary="Health Check")
def health_check():
    return {"status": "ok", "api_version": "1.0.0"}
