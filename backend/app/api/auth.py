from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)

from app.services.auth_service import (
    register_user,
    login_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def register(user: RegisterRequest):

    try:

        user_id = await register_user(user)

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(user: LoginRequest):

    try:

        return await login_user(user)

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )