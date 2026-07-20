from fastapi import APIRouter, Depends

from app.schemas.post import CreatePostRequest
from app.services.post_service import create_post
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/")
async def create(
    request: CreatePostRequest,
    current_user=Depends(get_current_user)
):
    return await create_post(
        current_user,
        request
    )