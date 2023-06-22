# Yan Pan, 2023
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from auth import schemas
from auth.JwtAuth import JwtAuth


router = APIRouter()
router_protected = APIRouter()

@router_protected.get("/list-users")
async def list_registered_users(request: Request):
    """
    List registered users from database
    """
    doc = await request.app.collection_user.find().to_list(length=None)
    return doc


@router_protected.get("/user/{username}", response_model=schemas.User)
async def describe_user(request: Request, username: str):
    """
    Get user from database WITHOUT authentication
    """
    doc = await request.app.collection_user.find_one({"username": username})
    if doc is None:
        raise HTTPException(status_code=404, detail="User not found")
    return doc


@router_protected.get("/who-am-I", response_model=schemas.User)
async def check_bearer_token(request: Request, token: Annotated[str, Depends(JwtAuth.oauth2_scheme)]):
    """
    Determine the active user that sends a Bearer token
    """
    doc = await JwtAuth(request.app.collection_user).get_current_user(token)
    if doc is None:
        raise HTTPException(status_code=401, detail="Invalid token or user disabled")
    return doc


@router.post("/register", status_code=201)
async def register_new_user(request: Request, user: schemas.UserWithPassword):
    """
    Register a new user
    """
    res = await JwtAuth(request.app.collection_user).create_user(user)
    return {"user_id": str(res.inserted_id)}


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    request: Request, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    token_data = await JwtAuth(request.app.collection_user) \
        .authenticate_user_and_create_token(form_data.username, form_data.password)
    
    if not token_data:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data
    
    

# @router.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user


# @router.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]