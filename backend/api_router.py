from fastapi import APIRouter

from memory_routes import router as memory_router
from status_routes import router as status_router


api_router = APIRouter()

api_router.include_router(
    memory_router
)

api_router.include_router(
    status_router
)