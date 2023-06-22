from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from settings.settings import Settings

from roadmap.router import router as router_roadmap
from auth.router import router as router_auth, router_admin


app = FastAPI()
settings = Settings()



@app.on_event("startup")
async def startup_db_client():
    # from pymongo import results
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client[settings.MONGO_DB_NAME]
    app.collection_roadmap = app.mongodb["roadmaps"]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()



app.include_router(router_auth, tags=["Auth"], prefix="/auth")
app.include_router(router_roadmap, tags=["Roadmap"], prefix="/roadmap")
app.include_router(router_admin, tags=["User Admin"], prefix="/admin")