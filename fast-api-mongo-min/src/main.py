# Yan Pan, 2023
from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from auth.router import router_admin, router_auth, router_login
from roadmap.router import router as router_roadmap
from settings.settings import Settings

settings = Settings()

app = FastAPI(
    title="FastAPI with Mongo DB and JWT + Google OAuth2",
)
if settings.IS_RUNNING_TEST:
    pass
else:
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SESSION_SECRET
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup_db_client():
    # from pymongo import results
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client[settings.MONGO_DB_NAME]
    app.collection_roadmap = app.mongodb["roadmaps"]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check(request: Request):
    wrap = lambda x: f"{x[:3]}{'*' * (len(x) - 5)}{x[-2:]}" if not x.startswith("not") else x # noqa
    return {
        "db": settings.MONGO_URL.split("@")[-1].split("?")[0],
        "jwt": f"{settings.JWT_ALGORITHM} {wrap(settings.JWT_SECRET)}",
        "google": f"{wrap(settings.GOOGLE_CLIENT_ID)} {wrap(settings.GOOGLE_CLIENT_SECRET)}", # noqa
        "url": str(request.url_for("health_check")),
        "status": "ok",
    }

app.include_router(router_auth, tags=["Auth"], prefix="/auth")
app.include_router(router_login, tags=["Auth"], prefix="/login")
app.include_router(router_admin, tags=["User Admin"], prefix="/admin")
app.include_router(router_roadmap, tags=["Roadmap"], prefix="/roadmap")
