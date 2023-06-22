# YYYan
from pydantic import BaseSettings, MongoDsn


class Settings(BaseSettings):
    """
    YYYan common settings to be loaded by main
    pydantic.BaseSettings can automatically load env vars
    """
    MONGO_URL: MongoDsn
    MONGO_DB_NAME: str
    MONGO_USER_COLLECTION: str = "users"
    JWT_SECRET: str = "6a315d39f885e190b240ab88bd6f869e7af4694de59fdf052933576216091958"
    JWT_ALGORITHM: str = "HS256"
    JWT_VALID_MINUTES: int = 10
    GOOGLE_CLIENT_ID: str = "not-provided"
    GOOGLE_CLIENT_SECRET: str = "not-provided"
    USE_MOCK_MONGODB: str = "no"
    
    class Config:
        env_prefix = "FAST001_"
