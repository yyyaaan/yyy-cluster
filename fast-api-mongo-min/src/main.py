# Yan Pan, 2023
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from os.path import exists
from starlette.middleware.sessions import SessionMiddleware
from sys import path

from auth.JWT import is_authenticated_user
from auth.router import router_admin, router_auth, router_login
from roadmap.router import router as router_roadmap
from settings.settings import Settings
from templates.override import TEMPLATES_ALT

settings = Settings()

app = FastAPI(
    title="YAN.FI v2",
    description="MongoDB, JWT, OAuth2, Login with Google and a few frontend",
    swagger_ui_parameters={"docExpansion": "none", "tagsSorter": "alpha"}
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


@app.exception_handler(401)
async def custom_401_handler(request: Request, __):
    url = request.url.path
    cond = ("/login/success" in url or "/bot/c" in url)
    if request.method == "GET" and cond:
        if not settings.IS_RUNNING_TEST:
            request.session["landing"] = url
        return TEMPLATES_ALT.TemplateResponse(
            name="400.html",
            context={"request": request},
            status_code=401
        )

    return JSONResponse(
        content={"detail": "Not authenticated", "landing": url},
        status_code=401
    )


@app.get("/", tags=["SysHealth"])
async def index():
    return {"message": "Hello World"}


@app.get("/health", tags=["SysHealth"])
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


# Mount Sub Apps and add auth
if exists("./appbot/router.py"):
    path.append("./appbot")
    from appbot.router import router  # type: ignore
    app.include_router(
        router=router,
        prefix="/bot",
        dependencies=[Depends(is_authenticated_user)]
    )
