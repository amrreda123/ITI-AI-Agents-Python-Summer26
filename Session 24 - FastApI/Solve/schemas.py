from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=120,
        description="Title of the document (3 to 120 characters)"
    )
    content: str = Field(
        min_length=1,
        description="Content of the document (at least 1 character)"
    )
    priority: int = Field(
        default=1,
        ge=1,
        le=5,
        description="Priority level between 1 and 5 (default: 1)"
    )


class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    priority: int
