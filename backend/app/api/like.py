from fastapi import APIRouter, Depends, HTTPException
from app.schemas.like import (
    LikeResponse,
    LikeStatusResponse,
    PostLikesResponse,
)
from app.dependencies.auth import get_current_user
from app.services.like_service import (
    like_post,
    unlike_post,
    get_post_likes,
    has_liked
)

router = APIRouter()


@router.post("/{post_id}", response_model=LikeResponse)
async def like(
    post_id: str,
    current_user=Depends(get_current_user)
):

    try:
        return await like_post(
            current_user["id"],
            post_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/{post_id}", response_model=LikeResponse)
async def unlike(
    post_id: str,
    current_user=Depends(get_current_user)
):

    try:
        return await unlike_post(
            current_user["id"],
            post_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/{post_id}", response_model=PostLikesResponse)
async def get_likes(
    post_id: str
):

    try:
        return await get_post_likes(post_id)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/{post_id}/status", response_model=LikeStatusResponse)
async def like_status(
    post_id: str,
    current_user=Depends(get_current_user)
):

    try:
        liked = await has_liked(
            current_user["id"],
            post_id
        )

        return {
            "liked": liked
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )