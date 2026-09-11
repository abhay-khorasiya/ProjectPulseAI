from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import memory_models

from database import get_db
from memory_schemas import MemoryItemResponse
from status_schemas import MemoryStatusUpdate


router = APIRouter(
    prefix="/api/memory",
    tags=["Memory Status"]
)


ALLOWED_STATUS = {
    "task": {
        "Open",
        "Completed",
    },
    "approval": {
        "Pending",
        "Approved",
    },
    "decision": {
        "Confirmed",
    },
}


@router.patch(
    "/{item_id}/status",
    response_model=MemoryItemResponse
)
def update_memory_status(
    item_id: int,
    update: MemoryStatusUpdate,
    db: Session = Depends(get_db)
):
    item = (
        db.query(memory_models.ProjectMemoryItem)
        .filter(
            memory_models.ProjectMemoryItem.id
            == item_id
        )
        .first()
    )

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Project memory item not found"
        )

    allowed = ALLOWED_STATUS.get(
        item.item_type,
        set()
    )

    if update.status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Status '{update.status}' is not "
                f"valid for {item.item_type}"
            )
        )

    item.status = update.status

    db.commit()
    db.refresh(item)

    return item