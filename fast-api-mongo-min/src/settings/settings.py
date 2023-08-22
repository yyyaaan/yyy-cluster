# YYYan
from motor.motor_asyncio import AsyncIOMotorClient
from sys import modules
try:
    from pydantic_settings import BaseSettings
except:  # noqa: E722
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    YYYan common settings to be loaded by main
    pydantic.BaseSettings can automatically load env vars
    mongo_url should be pydantic.MongoDsn, but Atlas require +srv
    `mongodb+srv://{u}:{p}@%{server}/{collection}?retryWrites=true&w=majority`
    """
    MONGO_URL: str
    MONGO_DB_NAME: str
    MONGO_USER_COLLECTION: str = "users"
    HOSTNAME_ROOTPATH: str = "localhost:9001/app"
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    JWT_SECRET: str = "6a315d39f885e190b240ab88bd6f869e7af4694de59fdf052933576216091958"  # noqa
    JWT_ALGORITHM: str = "HS256"
    JWT_VALID_MINUTES: int = 1440
    GOOGLE_CLIENT_ID: str = "not-provided"
    GOOGLE_CLIENT_SECRET: str = "not-provided"
    GITHUB_CLIENT_ID: str = "not-provided"
    GITHUB_CLIENT_SECRET: str = "not-provided"
    MICROSOFT_CLIENT_ID: str = "not-provided"
    MICROSOFT_CLIENT_SECRET: str = "not-provided"
    IS_RUNNING_TEST: bool = ("pytest" in modules)
    USE_MOCK_MONGODB: str = "yes"

    def get_user_collection_client(self):
        if self.IS_RUNNING_TEST and (self.USE_MOCK_MONGODB.lower() == "yes"):
            from mongomock_motor import AsyncMongoMockClient
            print("Using Mock Mongo DB for test only")
            return AsyncMongoMockClient()[self.MONGO_DB_NAME][self.MONGO_USER_COLLECTION]               # noqa
        return AsyncIOMotorClient(str(self.MONGO_URL))[self.MONGO_DB_NAME][self.MONGO_USER_COLLECTION]  # noqa

    class Config:
        env_prefix = "FAST001_"
