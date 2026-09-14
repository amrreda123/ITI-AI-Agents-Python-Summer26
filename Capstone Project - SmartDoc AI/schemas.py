from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=120,
        description="Title of the document (3 to 120 characters)"
    )
    content: str = Field(
        min_length=1,
        description="Content of the document"
    )
    priority: int = Field(
        default=1,
        ge=1,
        le=5,
        description="Priority level between 1 and 5 (default: 1)"
    )
    description: str | None = Field(
        default=None,
        max_length=250,
        description="Optional brief description of the document"
    )


class DocumentUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=120,
        description="Updated title of the document"
    )
    content: str | None = Field(
        default=None,
        min_length=1,
        description="Updated content of the document"
    )
    priority: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="Updated priority level (1 to 5)"
    )
    description: str | None = Field(
        default=None,
        max_length=250,
        description="Updated brief description"
    )


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    priority: int
    description: str | None = None
    ai_summary: str | None = None


class AIAnalysisResponse(BaseModel):
    summary: str = Field(description="Short summary of the document")
    key_points: list[str] = Field(description="List of key points extracted from the document")
    category: Literal["technical", "business", "general"] = Field(description="Category of the document")
    suggested_priority: int = Field(description="Suggested priority between 1 and 5", ge=1, le=5)


class AgentAskRequest(BaseModel):
    message: str = Field(min_length=1, description="Question or task for the AI document agent")


class AgentAskResponse(BaseModel):
    answer: str = Field(description="Final grounded response from the agent")
    steps_taken: int = Field(default=0, description="Total steps executed in the agent loop")
    tools_called: list[str] = Field(default_factory=list, description="Names of tools called during execution")
