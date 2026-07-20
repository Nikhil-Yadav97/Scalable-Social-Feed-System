from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.feed import router as feed_router
from app.api.follow import router as follow_router
from app.api.like import router as like_router
from app.api.post import router as post_router

from app.db.mongodb import (
    connect_to_mongodb,
    close_mongodb_connection
)

from app.db.redis import (
    connect_to_redis,
    close_redis_connection,
    redis_client
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    await connect_to_mongodb()
    await connect_to_redis()

    yield

    await close_mongodb_connection()
    await close_redis_connection()


app = FastAPI(
    title="Scalable Social Feed System",
    version="1.0.0",
    lifespan=lifespan
)


# Authentication
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

# Follow
app.include_router(
    follow_router,
    prefix="/follow",
    tags=["Follow"]
)

# Posts
app.include_router(
    post_router,
    prefix="/posts",
    tags=["Posts"]
)

# Feed
app.include_router(
    feed_router,
    prefix="/feed",
    tags=["Feed"]
)

# Likes
app.include_router(
    like_router,
    prefix="/likes",
    tags=["Likes"]
)


@app.get("/")
async def home():

    return {
        "message": "Social Feed API Running"
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "mongodb": "connected",
        "redis": "connected" if redis_client else "disconnected"
    }