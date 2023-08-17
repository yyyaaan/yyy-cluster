# Yan Pan, 2023
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from httpx import AsyncClient
from typing import Annotated

from auth import JWT, schemas
from settings.settings import Settings


router_auth = APIRouter()
router_login = APIRouter()
router_admin = APIRouter()
typing_registered = Annotated[str, Depends(JWT.is_registered_user)]
typing_auth_user = Annotated[str, Depends(JWT.is_authenticated_user)]
typing_auth_admin = Annotated[str, Depends(JWT.is_authenticated_admin)]


#############################
# Login flow using OAuth2.0 #
#############################


@router_login.get("/google")
async def login_google(request: Request, callback: str = JWT.token_url):
    """
    activator for Google OAuth2.0 login (server side)
    https://accounts.google.com/.well-known/openid-configuration
    """
    return RedirectResponse(
        url=(
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={Settings().GOOGLE_CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={callback}"
            f"&scope=email"
        )
    )


@router_login.get("/github")
async def login_github(request: Request, callback: str = JWT.token_url):
    """
    activator for Github OAuth2.0 login (github NOT for openid, server side)
    https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
    """
    return RedirectResponse(
        url=(
            "https://github.com/login/oauth/authorize"
            f"?client_id={Settings().GITHUB_CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={callback}"
            # f"&scope=email"  # no scope means only profile
        )
    )


@router_login.get("/microsoft")
async def login_microsoft(request: Request, callback: str = JWT.token_url):
    """
    activator for Microsoft OAuth2.0 login
    https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration
    https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow
    """
    print("Callback URL", callback)

    return RedirectResponse(
        url=(
            f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
            f"?client_id={Settings().MICROSOFT_CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={callback}"
            f"&scope=https://graph.microsoft.com/User.Read"
        )
    )

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
    __Deprecated and Currently Closed__: only super user can create a new user (auth-required)
    <br>Use 3rd party (Google or Github) is highly recommended.
    """
    res = await JWT.create_user(user)
    return {"user_id": str(res.inserted_id)}


@router_auth.get("/token")
async def login_from_third_party(
    request: Request,
    callback: str = JWT.token_url,
    code: str = "",
    prompt: str = "nothing",
    authuser: int = -1
):
    """
    This GET endpoint is for third-party login: Redeem token and Fetch User
    For Google, it send prompt and auth_user as param
    For Microsoft, code only M.C102_BAY.2.87b638bc-xxxx-xxxx-xxxx-6fd06d3ded66
    For Github, code only abcd61f1a17xxxxxxxxx
    """
    settings = Settings()

    # print("Callback URL (auth)", callback, code, request.query_params)

    # Note that microsoft use different approach in POST (query/data)
    if prompt != "nothing" and authuser > -1:
        print("Auth requested from Google token!")
        url_token = "https://oauth2.googleapis.com/token"
        url_user = "https://www.googleapis.com/oauth2/v1/userinfo"
        post_content = {
            "params": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "grant_type": 'authorization_code',
                "redirect_uri": callback,
                "code": code
            }
        }

    elif "." in code and "-" in code:
        print("Auth requested from Microsoft token!")
        url_token = "https://login.microsoftonline.com/common/oauth2/v2.0/token"  # noqa: E501
        url_user = "https://graph.microsoft.com/oidc/userinfo"
        url_user = "https://graph.microsoft.com/v1.0/me"
        post_content = {
            "data": {
                "client_id": settings.MICROSOFT_CLIENT_ID,
                "client_secret": settings.MICROSOFT_CLIENT_SECRET,
                "scope": "https://graph.microsoft.com/User.Read",
                "grant_type": 'authorization_code',
                "redirect_uri": callback,
                "code": code
            }
        }

    else:
        print("Auth requested from Github token!")
        url_token = "https://github.com/login/oauth/access_token"
        url_user = "https://api.github.com/user"
        post_content = {
            "params": {
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "scope": "email",
                "grant_type": "authorization_code",
                "redirect_uri": callback,
                "code": code,
            }
        }

    try:
        # retrieve access token
        async with AsyncClient() as client:
            res = await client.post(
                url=url_token,
                headers={'Accept': 'application/json'},
                **post_content  # Microsoft uses data, Google/Github uses params
            )
        if res.status_code > 299:
            raise Exception("failed to request token", res.text)
        access_token = res.json().get("access_token")

        # get userinfo from access token
        async with AsyncClient() as client:
            res = await client.get(
                url=url_user,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {access_token}"
                },
            )
        userinfo = res.json()

        token_data = await JWT.create_token_for_third_login(userinfo)
        return token_data

    except Exception as e:
        print("error in auth/login_from_third_party", e)
        raise HTTPException(
            status_code=401,
            detail=f'Could not validate 3rd party login {str(e)}',
            headers={'WWW-Authenticate': 'Bearer'},
        )


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
    return token_data


@router_auth.post("/token/refresh", response_model=schemas.Token)
async def refresh_token(username: typing_auth_user):
    doc = await JWT.get_user(username)
    return {
        **JWT.create_access_token({'sub': username}),
        "fullname": doc["full_name"],
    }


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
    _ = await JWT.new_user_accept(username)
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
