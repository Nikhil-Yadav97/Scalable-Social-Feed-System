from datetime import datetime
from pydantic import BaseModel


class FeedPostResponse(BaseModel):
    id: str
    author_id: str
    content: str
    created_at: datetime
    like_count: int
    comment_count: int