# YYYan
from pydantic import BaseSettings, MongoDsn


class Settings(BaseSettings):
    """
    YYYan common settings to be loaded by main
    pydantic.BaseSettings can automatically load env vars
    """
    MONGO_URL: MongoDsn
    MONGO_DB_NAME: str

    class Config:
        env_prefix = "FAST001_"
