import os

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import memory_models
import models

from analyzer import analyze_conversation
from api_router import api_router
from database import engine, get_db
from schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ConversationCreate,
    ConversationResponse,
)


models.Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="ProjectPulse AI API",
    description=(
        "Intelligent project communication API "
        "for ArchScale Guild Hackathon AS-02"
    ),
    version="1.0.0"
)


cors_env = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
)

if cors_env.strip() == "*":
    allowed_origins = ["*"]
    allow_credentials = False
else:
    allowed_origins = [
        origin.strip()
        for origin in cors_env.split(",")
        if origin.strip()
    ]
    allow_credentials = True


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    api_router
)


@app.get("/")
def home():
    return {
        "message": "ProjectPulse AI Backend is running",
        "status": "success"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "project": "ProjectPulse AI",
        "challenge": "AS-02"
    }


@app.post(
    "/api/analyze",
    response_model=AnalyzeResponse
)
def analyze_project_conversation(
    request: AnalyzeRequest
):
    result = analyze_conversation(
        request.text
    )

    return {
        "source": request.source,
        "summary": result["summary"],
        "tasks": result["tasks"],
        "decisions": result["decisions"],
        "approvals": result["approvals"],
        "attention_needed": result["attention_needed"]
    }


@app.post(
    "/api/conversations",
    response_model=ConversationResponse
)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    new_conversation = models.Conversation(
        source=conversation.source.strip(),
        raw_text=conversation.raw_text.strip()
    )

    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return new_conversation


@app.get(
    "/api/conversations",
    response_model=list[ConversationResponse]
)
def get_conversations(
    db: Session = Depends(get_db)
):
    conversations = (
        db.query(models.Conversation)
        .order_by(
            models.Conversation.id.desc()
        )
        .all()
    )

    return conversations


@app.get(
    "/api/conversations/search",
    response_model=list[ConversationResponse]
)
def search_conversations(
    q: str = Query(
        ...,
        min_length=1
    ),
    db: Session = Depends(get_db)
):
    search_term = f"%{q.strip()}%"

    conversations = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.raw_text.ilike(
                search_term
            )
        )
        .order_by(
            models.Conversation.id.desc()
        )
        .all()
    )

    return conversations


@app.get(
    "/api/conversations/{conversation_id}",
    response_model=ConversationResponse
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    conversation = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id
            == conversation_id
        )
        .first()
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return conversation