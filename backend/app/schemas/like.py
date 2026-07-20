from pydantic import BaseModel


class LikeResponse(BaseModel):
    message: str


class LikeStatusResponse(BaseModel):
    liked: bool


class PostLikesResponse(BaseModel):
    count: int
    users: list[str]