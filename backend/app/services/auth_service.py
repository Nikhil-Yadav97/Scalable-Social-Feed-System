from datetime import datetime, timezone
from bson import ObjectId

from app.db.mongodb import users
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt import create_access_token


async def register_user(user_data):

    # Check username
    existing_username = await users.find_one(
        {
            "username": user_data.username
        }
    )

    if existing_username:
        raise ValueError("Username already exists")

    # Check email
    existing_email = await users.find_one(
        {
            "email": user_data.email
        }
    )

    if existing_email:
        raise ValueError("Email already exists")

    # Create document
    document = {

        "username": user_data.username,

        "email": user_data.email,

        "password_hash": hash_password(
            user_data.password
        ),

        "bio": "",

        "followers_count": 0,

        "following_count": 0,

        "post_count": 0,

        "is_celebrity": False,

        "created_at": datetime.now(
            timezone.utc
        )

    }

    result = await users.insert_one(document)

    return str(result.inserted_id)

async def login_user(login_data):

    user = await users.find_one(
        {
            "email": login_data.email
        }
    )

    if not user:
        raise ValueError("Invalid email or password")

    valid = verify_password(
        login_data.password,
        user["password_hash"]
    )

    if not valid:
        raise ValueError("Invalid email or password")

    token = create_access_token(
        {
            "sub": str(user["_id"])
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }