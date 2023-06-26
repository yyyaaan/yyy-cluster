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


@app.get("/health")
async def health_check():
    wrap = lambda x: f"{x[:3]}{'*' * (len(x) - 5)}{x[-2:]}" if not x.startswith("not") else x # noqa
    return {
        "db": settings.MONGO_URL.split("@")[-1].split("?")[0],
        "jwt": f"{settings.JWT_ALGORITHM} {wrap(settings.JWT_SECRET)}",
        "google": f"{wrap(settings.GOOGLE_CLIENT_ID)} {wrap(settings.GOOGLE_CLIENT_SECRET)}", # noqa
        "status": "ok"
    }

app.include_router(router_auth, tags=["Auth"], prefix="/auth")
app.include_router(router_admin, tags=["User Admin"], prefix="/admin")
app.include_router(router_roadmap, tags=["Roadmap"], prefix="/roadmap")
