from fastapi import APIRouter
from .cinema import router as cinema_router


actions_router = APIRouter()
actions_router.include_router(cinema_router)