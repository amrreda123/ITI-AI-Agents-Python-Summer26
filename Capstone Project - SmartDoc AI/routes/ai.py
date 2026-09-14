import logging
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from database import engine
from models import Document
from schemas import AIAnalysisResponse, AgentAskRequest, AgentAskResponse
from services.gemini_service import analyze_document_content
from services.agent_service import run_agent

logger = logging.getLogger("smartdoc.routes.ai")

router = APIRouter(tags=["ai"])


@router.post(
    "/documents/{document_id}/analyze",
    response_model=AIAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze a document with Gemini AI",
    description="Loads a document from SQLite, extracts structured summary and classification using Gemini, and saves summary in ai_summary.",
    responses={
        404: {"description": "Document not found", "content": {"application/json": {"example": {"detail": "Document not found"}}}},
        500: {"description": "AI analysis failure", "content": {"application/json": {"example": {"detail": "Upstream AI analysis service is currently unavailable."}}}},
    },
)
def analyze_document(document_id: int):
    with Session(engine) as db:
        doc = db.get(Document, document_id)
        if doc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )

        try:
            analysis_result = analyze_document_content(doc.content)
        except RuntimeError as err:
            logger.error(f"Error during AI analysis for document {document_id}: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err),
            )
        except Exception as err:
            logger.error(f"Unexpected error analyzing document {document_id}: {type(err).__name__}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to analyze document with AI.",
            )

        doc.ai_summary = analysis_result.summary
        db.commit()
        db.refresh(doc)

        return analysis_result


@router.post(
    "/agent/ask",
    response_model=AgentAskResponse,
    status_code=status.HTTP_200_OK,
    summary="Query the Read-Only Document AI Agent",
    description="Interact with an autonomous AI agent equipped with read-only tools to search and inspect documents.",
    responses={
        500: {"description": "Agent execution failure", "content": {"application/json": {"example": {"detail": "AI Agent service encounter an issue."}}}},
    },
)
def ask_agent(payload: AgentAskRequest):
    try:
        agent_output = run_agent(payload.message)
        return AgentAskResponse(
            answer=agent_output["answer"],
            steps_taken=agent_output["steps_taken"],
            tools_called=agent_output["tools_called"],
        )
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(val_err),
        )
    except Exception as err:
        logger.error(f"Agent execution error: {type(err).__name__}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI Agent service encountered an unexpected issue.",
        )
