# Yan Pan, 2023
from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.sessions import SessionMiddleware

from auth.router import router as router_auth, router_admin
from auth.OAuth import oauth
from roadmap.router import router as router_roadmap
from settings.settings import Settings
from templates.override import TEMPLATES_ALT

settings = Settings()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)


@app.on_event("startup")
async def startup_db_client():
    # from pymongo import results
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client[settings.MONGO_DB_NAME]
    app.collection_roadmap = app.mongodb["roadmaps"]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/login")
async def login(request: Request):
    return TEMPLATES_ALT.TemplateResponse(
        name="login.html",
        context={"request": request}
    )


@app.get("/login/google")
async def login_google(request: Request):
    redirect_uri = "http://localhost:9001/app002/auth/token"
    return await oauth.google.authorize_redirect(request, redirect_uri)


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
