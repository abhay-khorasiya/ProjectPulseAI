from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy import or_
from sqlalchemy.orm import Session

import memory_models
import models

from analyzer import analyze_conversation
from database import get_db
from memory_schemas import (
    AnalyzeAndSaveRequest,
    AnalyzeAndSaveResponse,
    MemoryItemResponse,
    MemoryStatsResponse,
)


router = APIRouter(
    prefix="/api",
    tags=["Project Memory"]
)


# ---------------------------------------------------------
# Analyze Conversation + Save Everything
# ---------------------------------------------------------

@router.post(
    "/analyze-and-save",
    response_model=AnalyzeAndSaveResponse
)
def analyze_and_save(
    request: AnalyzeAndSaveRequest,
    db: Session = Depends(get_db)
):
    """
    Complete ProjectPulse workflow:

    Conversation
        ↓
    Analyze
        ↓
    Extract Tasks / Decisions / Approvals
        ↓
    Save Conversation
        ↓
    Save Structured Project Memory
    """

    result = analyze_conversation(
        request.text
    )

    try:
        # -------------------------------------------------
        # Save original conversation
        # -------------------------------------------------

        conversation = models.Conversation(
            source=request.source.strip(),
            raw_text=request.text.strip(),
            summary=result["summary"]
        )

        db.add(conversation)

        # Get conversation ID before final commit.
        db.flush()

        memory_items = []

        # -------------------------------------------------
        # Save Tasks
        # -------------------------------------------------

        for task in result["tasks"]:
            item = memory_models.ProjectMemoryItem(
                conversation_id=conversation.id,
                item_type="task",
                content=task["task"],
                responsible=task["responsible"],
                deadline=task["deadline"],
                status=task["status"],
                source=request.source.strip()
            )

            db.add(item)
            memory_items.append(item)

        # -------------------------------------------------
        # Save Decisions
        # -------------------------------------------------

        for decision in result["decisions"]:
            item = memory_models.ProjectMemoryItem(
                conversation_id=conversation.id,
                item_type="decision",
                content=decision["decision"],
                responsible=None,
                deadline=None,
                status=decision["status"],
                source=request.source.strip()
            )

            db.add(item)
            memory_items.append(item)

        # -------------------------------------------------
        # Save Pending Approvals
        # -------------------------------------------------

        for approval in result["approvals"]:
            item = memory_models.ProjectMemoryItem(
                conversation_id=conversation.id,
                item_type="approval",
                content=approval["item"],
                responsible=None,
                deadline=None,
                status=approval["status"],
                source=request.source.strip()
            )

            db.add(item)
            memory_items.append(item)

        # Save everything together.
        db.commit()

        return {
            "conversation_id": conversation.id,
            "source": request.source,
            "summary": result["summary"],
            "tasks": result["tasks"],
            "decisions": result["decisions"],
            "approvals": result["approvals"],
            "attention_needed": result["attention_needed"],
            "memory_items_created": len(memory_items)
        }

    except Exception:
        db.rollback()
        raise


# ---------------------------------------------------------
# Get Complete Project Memory
# ---------------------------------------------------------

@router.get(
    "/memory",
    response_model=list[MemoryItemResponse]
)
def get_project_memory(
    db: Session = Depends(get_db)
):
    items = (
        db.query(
            memory_models.ProjectMemoryItem
        )
        .order_by(
            memory_models.ProjectMemoryItem.id.desc()
        )
        .all()
    )

    return items


# ---------------------------------------------------------
# Search Project Memory
# ---------------------------------------------------------

@router.get(
    "/memory/search",
    response_model=list[MemoryItemResponse]
)
def search_project_memory(
    q: str = Query(
        ...,
        min_length=1
    ),
    db: Session = Depends(get_db)
):
    """
    Search structured project memory.

    Example searches:

    marble
    Abhay
    approval
    Friday
    """

    search_term = f"%{q.strip()}%"

    items = (
        db.query(
            memory_models.ProjectMemoryItem
        )
        .filter(
            or_(
                memory_models.ProjectMemoryItem.content.ilike(
                    search_term
                ),
                memory_models.ProjectMemoryItem.responsible.ilike(
                    search_term
                ),
                memory_models.ProjectMemoryItem.deadline.ilike(
                    search_term
                ),
                memory_models.ProjectMemoryItem.status.ilike(
                    search_term
                ),
                memory_models.ProjectMemoryItem.item_type.ilike(
                    search_term
                )
            )
        )
        .order_by(
            memory_models.ProjectMemoryItem.id.desc()
        )
        .all()
    )

    return items


# ---------------------------------------------------------
# Dashboard Statistics
# ---------------------------------------------------------

@router.get(
    "/memory/stats",
    response_model=MemoryStatsResponse
)
def get_memory_stats(
    db: Session = Depends(get_db)
):
    conversation_count = (
        db.query(models.Conversation)
        .count()
    )

    total_items = (
        db.query(
            memory_models.ProjectMemoryItem
        )
        .count()
    )

    task_count = (
        db.query(
            memory_models.ProjectMemoryItem
        )
        .filter(
            memory_models.ProjectMemoryItem.item_type
            == "task"
        )
        .count()
    )

    open_task_count = (
        db.query(
            memory_models.ProjectMemoryItem
        )
        .filter(
            memory_models.ProjectMemoryItem.item_type
            == "task",
            memory_models.ProjectMemoryItem.status
            == "Open"
        )
        .count()
    )

    decision_count = (
        db.query(
            memory_models.ProjectMemoryItem
        )
        .filter(
            memory_models.ProjectMemoryItem.item_type
            == "decision"
        )
        .count()
    )

    pending_approval_count = (
        db.query(
            memory_models.ProjectMemoryItem
        )
        .filter(
            memory_models.ProjectMemoryItem.item_type
            == "approval",
            memory_models.ProjectMemoryItem.status
            == "Pending"
        )
        .count()
    )

    return {
        "conversations": conversation_count,
        "total_memory_items": total_items,
        "tasks": task_count,
        "open_tasks": open_task_count,
        "decisions": decision_count,
        "pending_approvals": pending_approval_count
    }