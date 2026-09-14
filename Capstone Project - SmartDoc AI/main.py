import os
from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routes.documents import router as documents_router
from routes.ai import router as ai_router

app = FastAPI(
    title="SmartDoc AI",
    description="Cross-Course Capstone Project integrating FastAPI REST API, SQLite ORM, Alembic Migrations, Gemini Structured Analysis, and Read-Only Tool-Calling AI Agent.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Register API routers
app.include_router(documents_router)
app.include_router(ai_router)

# Mount static assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", summary="Dashboard Web Interface", tags=["frontend"])
def get_dashboard():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Welcome to SmartDoc AI API. Visit /docs for OpenAPI documentation."}


@app.get(
    "/health",
    tags=["health"],
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Returns the operational status and version of the SmartDoc AI service.",
)
def health_check():
    return {
        "status": "ok",
        "service": "SmartDoc AI",
        "version": "1.0.0",
    }
