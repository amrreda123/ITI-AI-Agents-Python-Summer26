import logging
from typing import Any
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from google import genai
from google.genai import types

from database import engine
from models import Document
from settings import settings

logger = logging.getLogger("smartdoc.agent_service")

# --- Tool Validation Schemas ---
class GetDocumentSchema(BaseModel):
    document_id: int = Field(gt=0, description="The positive integer ID of the document")


class SearchDocumentsSchema(BaseModel):
    query: str = Field(min_length=1, description="Keywords to search in document titles and contents")


# --- Tool Implementations (Strictly Read-Only) ---
def list_documents() -> list[dict[str, Any]]:
    """List all available documents with id, title, and priority."""
    with Session(engine) as db:
        docs = db.query(Document).all()
        return [
            {"id": doc.id, "title": doc.title, "priority": doc.priority}
            for doc in docs
        ]


def get_document(document_id: int) -> dict[str, Any]:
    """Retrieve full details of a specific document by its ID."""
    with Session(engine) as db:
        doc = db.get(Document, document_id)
        if not doc:
            return {"error": "Not Found", "message": f"Document with ID {document_id} was not found."}
        return {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "priority": doc.priority,
            "description": doc.description,
            "ai_summary": doc.ai_summary,
        }


def search_documents(query: str) -> list[dict[str, Any]]:
    """Search for documents containing the query string in title or content."""
    clean_query = query.strip().lower()
    with Session(engine) as db:
        docs = db.query(Document).all()
        matched = []
        for doc in docs:
            if clean_query in doc.title.lower() or (doc.content and clean_query in doc.content.lower()):
                matched.append({
                    "id": doc.id,
                    "title": doc.title,
                    "priority": doc.priority,
                    "description": doc.description,
                })
        return matched


# Whitelist Registry
REGISTRY: dict[str, dict[str, Any]] = {
    "list_documents": {
        "func": list_documents,
        "schema": None,
    },
    "get_document": {
        "func": get_document,
        "schema": GetDocumentSchema,
    },
    "search_documents": {
        "func": search_documents,
        "schema": SearchDocumentsSchema,
    },
}

MAX_STEPS = 5


def execute_safe_tool(tool_name: str, raw_args: dict[str, Any]) -> dict[str, Any]:
    if tool_name not in REGISTRY:
        logger.warning(f"Unauthorized tool execution attempt: {tool_name}")
        return {"error": "Unauthorized", "message": f"Tool '{tool_name}' is not allowed."}

    tool_info = REGISTRY[tool_name]
    func = tool_info["func"]
    schema = tool_info["schema"]

    try:
        if schema:
            validated = schema(**raw_args).model_dump()
            result = func(**validated)
        else:
            result = func()
        logger.info(f"Tool execution succeeded: {tool_name}")
        return {"result": result}
    except ValidationError as val_err:
        logger.warning(f"Tool validation error for {tool_name}: {val_err}")
        return {"error": "Invalid Arguments", "message": "Supplied tool parameters are invalid."}
    except Exception as err:
        logger.error(f"Internal tool error during {tool_name}: {type(err).__name__}")
        return {"error": "Execution Failure", "message": "Failed to query document store safely."}


def run_agent(user_message: str) -> dict[str, Any]:
    api_key = settings.GEMINI_API_KEY
    if not api_key or api_key == "replace_me":
        raise ValueError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    system_instruction = (
        "You are SmartDoc AI, a helpful and secure document assistant. "
        "You can inspect stored documents using only your read-only tools: "
        "list_documents, get_document, and search_documents. "
        "Base all your answers strictly on data returned by the tools. "
        "Never invent document contents or answer from external unverified sources."
    )

    tools_for_gemini = [list_documents, get_document, search_documents]
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=tools_for_gemini,
        temperature=0.1,
    )

    chat = client.chats.create(model=settings.GEMINI_MODEL, config=config)

    tools_called = []
    current_message: Any = user_message
    final_answer = ""
    steps_taken = 0

    for step in range(1, MAX_STEPS + 1):
        steps_taken = step
        try:
            response = chat.send_message(current_message)
        except Exception as api_err:
            logger.error(f"Gemini agent communication error: {api_err}")
            raise RuntimeError("Upstream AI Agent service error.")

        # Check for function calls
        if not response.function_calls:
            final_answer = response.text or "I processed your request but have no further details."
            break

        # Execute proposed function calls safely
        function_responses = []
        for call in response.function_calls:
            tool_name = call.name
            raw_args = dict(call.args) if call.args else {}
            tools_called.append(tool_name)

            observation = execute_safe_tool(tool_name, raw_args)
            function_responses.append(
                types.Part.from_function_response(
                    name=tool_name,
                    response=observation,
                )
            )

        current_message = function_responses
    else:
        final_answer = "Maximum reasoning steps reached without final conclusion."

    return {
        "answer": final_answer,
        "steps_taken": steps_taken,
        "tools_called": tools_called,
    }
