from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.db.mongodb import (
    connect_to_mongodb,
    close_mongodb_connection
)

from app.db.redis import (
    connect_to_redis,
    close_redis_connection
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

app.include_router(auth_router)

@app.get("/")
async def home():

    return {

        "message": "Social Feed API Running"

    }


@app.get("/health")
async def health():

    from app.db.redis import redis_client

    return {

        "status": "healthy",

        "mongodb": "connected",
        "redis": "connected" if redis_client is not None else "disconnected"

    }