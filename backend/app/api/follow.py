from fastapi import APIRouter, Depends, HTTPException

from app.services.follow_service import (
    follow_user,
    unfollow_user
)
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/follow",
    tags=["Follow"]
)


@router.post("/{followee_id}")
async def follow(
    followee_id: str,
    current_user=Depends(get_current_user)
):
    try:
        return await follow_user(
            current_user["id"],
            followee_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/{followee_id}")
async def unfollow(
    followee_id: str,
    current_user=Depends(get_current_user)
):
    try:
        return await unfollow_user(
            current_user["id"],
            followee_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )