from pydantic import BaseModel


class MemoryStatusUpdate(BaseModel):
    status: str