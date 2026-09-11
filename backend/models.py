from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(
        String(50),
        nullable=False
    )

    raw_text = Column(
        Text,
        nullable=False
    )

    summary = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )