from fastapi import APIRouter

from app.event.adapter.input.api.v1.event import event_router as event_v1_router

router = APIRouter()
router.include_router(event_v1_router, prefix="/api/v1/event", tags=["Event"])

__all__ = ["router"]