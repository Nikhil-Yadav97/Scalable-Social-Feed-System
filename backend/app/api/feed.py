from fastapi import APIRouter, Depends, Query

from app.services.feed_service import get_feed
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/feed",
    tags=["Feed"]
)


@router.get("/")
async def feed(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    current_user=Depends(get_current_user),
):
    return await get_feed(
        current_user["id"],
        page,
        limit
    )