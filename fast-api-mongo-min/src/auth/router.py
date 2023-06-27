# Yan Pan, 2023
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from auth import JWT, OAuth, schemas
from templates.override import TEMPLATES_ALT


router_auth = APIRouter()
router_login = APIRouter()
router_admin = APIRouter()
typing_auth_user = Annotated[str, Depends(JWT.is_authenticated_user)]
typing_auth_admin = Annotated[str, Depends(JWT.is_authenticated_admin)]


##############
# Login flow #
##############

@router_login.get(("/"))
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


@router_login.get("/success")
async def login_success_page(request: Request):
    """
    success.html must be used to save JWT in user's browser session
    functionality mainly achieved in VueJS
    """
    token = request.session.get("jwt", "")
    return TEMPLATES_ALT.TemplateResponse(
        name="success.html",
        context={"request": request, "token": token}
    )


@router_login.get("/google")
async def login_google(request: Request):
    """
    activator for Google OAuth2.0 login
    """
    return await OAuth.oauth.google.authorize_redirect(
        request,
        "http://localhost:9001/app/auth/token"
    )


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
async def register_new_user(user: schemas.UserWithPassword):
    """
    Register a new user
    """
    res = await JWT.create_user(user)
    return {"user_id": str(res.inserted_id)}


@router_auth.get("/token")
async def token_from_google_login(request: Request):
    """
    This GET endpoint is for Google OAuth2.0 login.
    It will redirect to Google OAuth2.0 login page.
    """
    try:
        access_token = await OAuth.oauth.google.authorize_access_token(request)
        userinfo = access_token.get('userinfo')
        token_data = await JWT.create_token_for_google_sign_in(dict(userinfo))
        request.session["jwt"] = token_data["access_token"]
        return RedirectResponse(url="http://localhost:9001/app/login/success")
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f'Could not validate Google Login {str(e)}',
            headers={'WWW-Authenticate': 'Bearer'},
        )


@router_auth.post("/token", response_model=schemas.Token)
async def login_for_access_token(
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
    return JWT.create_access_token({'sub': username})


######################
# User Admin Actions #
######################


@router_admin.get("/list-users")
async def list_registered_users(username: typing_auth_admin):
    """
    List registered users from database
    """
    docs = await JWT.list_users()
    return docs


@router_admin.get("/user/me", response_model=schemas.User)
async def check_bearer_token(username: typing_auth_user):
    """
    Check the active user that sends a Bearer token
    """
    user_doc = await JWT.get_user(username)
    return user_doc


@router_admin.get("/user/{username}", response_model=schemas.User)
async def describe_user(username: str):
    """
    Get user from database WITHOUT authentication
    """
    doc = await JWT.get_user(username)
    if doc is None:
        raise HTTPException(status_code=404, detail="User not found")
    return doc


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
