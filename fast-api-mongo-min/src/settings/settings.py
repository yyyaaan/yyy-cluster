# YYYan
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings, MongoDsn
from sys import modules


class Settings(BaseSettings):
    """
    YYYan common settings to be loaded by main
    pydantic.BaseSettings can automatically load env vars
    """
    MONGO_URL: MongoDsn
    MONGO_DB_NAME: str
    MONGO_USER_COLLECTION: str = "users"
    JWT_SECRET: str = "6a315d39f885e190b240ab88bd6f869e7af4694de59fdf052933576216091958"  # noqa
    JWT_ALGORITHM: str = "HS256"
    JWT_VALID_MINUTES: int = 10
    GOOGLE_CLIENT_ID: str = "not-provided"
    GOOGLE_CLIENT_SECRET: str = "not-provided"
    USE_MOCK_MONGODB: str = "yes"
    IS_RUNNING_TEST: bool = ("pytest" in modules)

    class Config:
        env_prefix = "FAST001_"

    def get_user_collection_client(self):
        if self.IS_RUNNING_TEST and (self.USE_MOCK_MONGODB.lower() == "yes"):
            from mongomock_motor import AsyncMongoMockClient
            print("Using Mock Mongo DB for test only")
            return AsyncMongoMockClient()[self.MONGO_DB_NAME][self.MONGO_USER_COLLECTION]               # noqa
        return AsyncIOMotorClient(str(self.MONGO_URL))[self.MONGO_DB_NAME][self.MONGO_USER_COLLECTION]  # noqa
