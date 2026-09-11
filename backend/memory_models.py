from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from database import Base


class ProjectMemoryItem(Base):
    """
    Stores structured information extracted
    from project conversations.

    Item types:
    - task
    - decision
    - approval
    """

    __tablename__ = "project_memory_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False,
        index=True
    )

    item_type = Column(
        String(30),
        nullable=False,
        index=True
    )

    content = Column(
        Text,
        nullable=False
    )

    responsible = Column(
        String(100),
        nullable=True
    )

    deadline = Column(
        String(100),
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False
    )

    source = Column(
        String(50),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )