from fastapi import APIRouter

from app.schemas.common import MessageResponse


system_router = APIRouter(tags=["System"])


@system_router.get(
    "/ping"
)
async def ping() -> MessageResponse:
    return MessageResponse(message="pong")
