from pydantic import BaseModel

class FollowRequest(BaseModel):
    followee_id: str