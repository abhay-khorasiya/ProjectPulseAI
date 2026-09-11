from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas import (
    ApprovalResult,
    AttentionResult,
    DecisionResult,
    TaskResult,
)


class AnalyzeAndSaveRequest(BaseModel):
    source: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    text: str = Field(
        ...,
        min_length=1
    )


class AnalyzeAndSaveResponse(BaseModel):
    conversation_id: int

    source: str

    summary: str

    tasks: list[TaskResult]

    decisions: list[DecisionResult]

    approvals: list[ApprovalResult]

    attention_needed: list[AttentionResult]

    memory_items_created: int


class MemoryItemResponse(BaseModel):
    id: int

    conversation_id: int

    item_type: str

    content: str

    responsible: str | None

    deadline: str | None

    status: str

    source: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class MemoryStatsResponse(BaseModel):
    conversations: int

    total_memory_items: int

    tasks: int

    open_tasks: int

    decisions: int

    pending_approvals: int