from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    MONGO_URI: str
    CELEBRITY_THRESHOLD = 10000
    DATABASE_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()