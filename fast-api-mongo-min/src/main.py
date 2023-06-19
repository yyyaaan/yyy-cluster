from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from settings.settings import Settings

from roadmap.router import router as roadmap_router


app = FastAPI()
settings = Settings()

@app.on_event("startup")
async def startup_db_client():
    # for typing see 
    # from pymongo import results
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client[settings.MONGO_DB_NAME]
    app.collection_roadmap = app.mongodb["roadmaps"]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(roadmap_router, tags=["Roadmap"], prefix="/roadmap")


