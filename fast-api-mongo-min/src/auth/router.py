# Yan Pan, 2023
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from httpx import AsyncClient

from typing import Annotated

from auth import JWT, schemas
from settings.settings import Settings
from templates.override import TEMPLATES_ALT


router_auth = APIRouter()
router_login = APIRouter()
router_admin = APIRouter()
typing_registered = Annotated[str, Depends(JWT.is_registered_user)]
typing_auth_user = Annotated[str, Depends(JWT.is_authenticated_user)]
typing_auth_admin = Annotated[str, Depends(JWT.is_authenticated_admin)]


#############################
# Login flow using OAuth2.0 #
#############################

@router_login.get("")
async def login_page(request: Request):
    """
    login.html will show whether users has logged in <br>
    functionality achieved in VueJS

    For social login:
    login request is handled by OAuth and redirect to GET /auth/token <br>
    A local JWT token is generated and parsed to login_success_page. <br>
    The page saves JWT token to browser localStorage by Javascript, <br>
    which must be removed by clear_session if logged out
    """
    return TEMPLATES_ALT.TemplateResponse(
        name="login.html",
        context={"request": request}
    )


@router_login.get("/google")
async def login_google(request: Request):
    """
    activator for Google OAuth2.0 login (server side)
    https://accounts.google.com/.well-known/openid-configuration
    """
    return RedirectResponse(
        url=(
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={Settings().GOOGLE_CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={JWT.token_url}-google"
            f"&scope=email"
        )
    )


@router_login.get("/github")
async def login_github(request: Request):
    """
    activator for Github OAuth2.0 login (github NOT for openid, server side)
    https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
    """
    return RedirectResponse(
        url=(
            "https://github.com/login/oauth/authorize"
            f"?client_id={Settings().GITHUB_CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={JWT.token_url}-github"
            # f"&scope=email"  # no scope means only profile
        )
    )


@router_auth.get("/token-google")
async def token_from_google_login(request: Request, code: str = ""):
    """
    This GET endpoint is for Google OAuth2.0 login.
    It will redirect to Google OAuth2.0 login page.
    """
    try:
        # retrieve access token
        async with AsyncClient() as client:
            res = await client.post(
                url="https://oauth2.googleapis.com/token",
                headers={'Accept': 'application/json'},
                params={
                    "client_id": Settings().GOOGLE_CLIENT_ID,
                    "client_secret": Settings().GOOGLE_CLIENT_SECRET,
                    'grant_type': 'authorization_code',
                    'redirect_uri': f"{JWT.token_url}-google",
                    'code': code
                }
            )
        access_token = res.json().get("access_token")

        # get userinfo from access token
        async with AsyncClient() as client:
            res = await client.get(
                url="https://www.googleapis.com/oauth2/v1/userinfo",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {access_token}"
                },
            )
        userinfo = res.json()

        token_data = await JWT.create_token_for_third_login(userinfo)
        if not JWT.settings.IS_RUNNING_TEST:
            request.session["jwt"] = token_data["access_token"]
        return RedirectResponse(url=request.url_for("login_success_page"))

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=401,
            detail=f'Could not validate Github Login {str(e)}',
            headers={'WWW-Authenticate': 'Bearer'},
        )


@router_auth.get("/token-github")
async def token_from_github_login(request: Request, code: str = ""):
    """
    This GET endpoint is for Github OAuth2.0 login.
    """
    try:
        # retrieve access token
        async with AsyncClient() as client:
            res = await client.post(
                url="https://github.com/login/oauth/access_token",
                headers={'Accept': 'application/json'},
                params={
                    "client_id": Settings().GITHUB_CLIENT_ID,
                    "client_secret": Settings().GITHUB_CLIENT_SECRET,
                    'redirect_uri': f"{JWT.token_url}-github",
                    'code': code
                }
            )
        access_token = res.json().get("access_token")

        # get userinfo from access token
        async with AsyncClient() as client:
            res = await client.get(
                url="https://api.github.com/user",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {access_token}"
                },
            )
        userinfo = res.json()

        token_data = await JWT.create_token_for_third_login(userinfo)
        if not JWT.settings.IS_RUNNING_TEST:
            request.session["jwt"] = token_data["access_token"]
        return RedirectResponse(url=request.url_for("login_success_page"))

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=401,
            detail=f'Could not validate Google Login {str(e)}',
            headers={'WWW-Authenticate': 'Bearer'},
        )


@router_login.get("/success")
async def login_success_page(request: Request, username: typing_registered):
    """
    success.html must be used to save JWT in user's browser session
    functionality mainly achieved in VueJS
    """
    response = TEMPLATES_ALT.TemplateResponse(
        name="success.html",
        context={"request": request}
    )
    if not JWT.settings.IS_RUNNING_TEST:
        response.set_cookie("landing", request.session.get("landing", ""))
        response.set_cookie("jwt", request.session.get("jwt", ""))
    return response


@router_login.post("/clear-session")
async def clear_session(request: Request):
    """
    part of logout action (javascript should delete jwt from session)
    """
    try:
        _ = request.session.pop("jwt", None)
    except Exception as e:
        print("clear session by removing jwt from session failed", e)
    return {"status": "logout successful"}


#################
# User and Auth #
#################


@router_auth.post("/register", status_code=201)
async def register_new_user(
    user: schemas.UserWithPassword,
    username: typing_auth_admin  # require super user to register new user
):
    """
    Register a new user.\n
    __Currently Closed__: only super user can create a new user (auth-required)
    <br>Google login is still possible.
    """
    res = await JWT.create_user(user)
    return {"user_id": str(res.inserted_id)}


@router_auth.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    This POST endpoint is for username-password auth.
    """

    token_data = await JWT.authenticate_user_and_create_token(
        form_data.username, form_data.password
    )

    if not token_data:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not JWT.settings.IS_RUNNING_TEST:
        request.session["jwt"] = token_data["access_token"]
    return token_data


@router_auth.post("/token/refresh", response_model=schemas.Token)
async def refresh_token(username: typing_auth_user):
    return JWT.create_access_token({'sub': username})


######################
# User Admin Actions #
######################


@router_admin.get("/list-users", response_model=list[schemas.UserWithExtra])
async def list_registered_users(username: typing_auth_admin):
    """
    List registered users from database
    """
    docs = await JWT.list_users()
    return docs


@router_admin.get("/user/me", response_model=schemas.UserWithExtra)
async def check_bearer_token(username: typing_registered):
    """
    Check the active user that sends a Bearer token\n
    Even user is new, this endpoint is open - for prompting acceptance
    """
    user_doc = await JWT.get_user(username)
    if user_doc:
        return user_doc
    return {"username": "Deleted", "_id": "Deleted"}


@router_admin.post("/user/me", response_model=schemas.UserWithExtra)
async def agree_to_register(request: Request, username: typing_registered):
    """
    mark registered user to accept use of this system
    """
    update_result = await JWT.new_user_accept(username)
    print(update_result.raw_result)
    user_doc = await JWT.get_user(username)
    if user_doc:
        return user_doc
    return {"username": "Deleted", "_id": "Deleted"}


@router_admin.get("/user/{username}", response_model=schemas.UserWithExtra)
async def describe_user(username: typing_auth_admin):
    """
    Get user from database
    """
    doc = await JWT.get_user(username)
    if doc is None:
        raise HTTPException(status_code=404, detail="User not found")
    return doc


@router_admin.delete("/user/me", status_code=204)
async def delete_me(username: typing_registered):
    """
    Delete myself from database (use with caution
    """
    deletion_result = await JWT.delete_user(username)
    if deletion_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="user not found")
    return {"username": username, "raw": deletion_result.raw_result}


@router_admin.delete("/user/{username}", status_code=204)
async def delete_user(
    username: str,
    username_auth: typing_auth_admin
):
    """
    Delete user from database (use with caution), required admin
    """
    deletion_result = await JWT.delete_user(username)
    if deletion_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="user not found")
    return {"username": username, "raw": deletion_result.raw_result}
