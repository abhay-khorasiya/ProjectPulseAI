from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------
# Conversation Database Schemas
# ---------------------------------------------------------

class ConversationCreate(BaseModel):
    source: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    raw_text: str = Field(
        ...,
        min_length=1
    )


class ConversationResponse(BaseModel):
    id: int
    source: str
    raw_text: str
    summary: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------------------------------------------------
# Conversation Analyzer Schemas
# ---------------------------------------------------------

class AnalyzeRequest(BaseModel):
    source: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    text: str = Field(
        ...,
        min_length=1
    )


class TaskResult(BaseModel):
    task: str
    responsible: str
    deadline: str | None = None
    status: str


class DecisionResult(BaseModel):
    decision: str
    status: str


class ApprovalResult(BaseModel):
    item: str
    status: str


class AttentionResult(BaseModel):
    type: str
    message: str
    detail: str


class AnalyzeResponse(BaseModel):
    source: str
    summary: str
    tasks: list[TaskResult]
    decisions: list[DecisionResult]
    approvals: list[ApprovalResult]
    attention_needed: list[AttentionResult]