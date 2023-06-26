# Yan Pan, 2023
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from auth import schemas
from auth import OAuth


router = APIRouter()
router_admin = APIRouter()
typing_auth_user = Annotated[str, Depends(OAuth.is_authenticated_user)]
typing_auth_admin = Annotated[str, Depends(OAuth.is_authenticated_admin)]


@router_admin.get("/list-users")
async def list_registered_users(request: Request, username: typing_auth_admin):
    """
    List registered users from database
    """
    docs = await OAuth.list_users()
    return docs


@router_admin.get("/user/me", response_model=schemas.User)
async def check_bearer_token(request: Request, username: typing_auth_user):
    """
    Check the active user that sends a Bearer token
    """
    user_doc = await OAuth.get_user(username)
    return user_doc


@router_admin.get("/user/{username}", response_model=schemas.User)
async def describe_user(request: Request, username: str):
    """
    Get user from database WITHOUT authentication
    """
    doc = await OAuth.get_user(username)
    if doc is None:
        raise HTTPException(status_code=404, detail="User not found")
    return doc


@router_admin.delete("/user/{username}", status_code=204)
async def delete_user(
    request: Request, username: str,
    username_auth: typing_auth_admin
):
    """
    Delete user from database (use with caution), required admin
    """
    deletion_result = await OAuth.delete_user(username)
    if deletion_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="user not found")
    return {"username": username, "raw": deletion_result.raw_result}


@router.post("/register", status_code=201)
async def register_new_user(user: schemas.UserWithPassword):
    """
    Register a new user
    """
    res = await OAuth.create_user(user)
    return {"user_id": str(res.inserted_id)}


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    token_data = await OAuth.authenticate_user_and_create_token(
        form_data.username, form_data.password
    )

    if not token_data:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data


@router.post("/token/refresh", response_model=schemas.Token)
async def refresh_token(request: Request, username: typing_auth_user):
    return OAuth.create_access_token({'sub': username})
