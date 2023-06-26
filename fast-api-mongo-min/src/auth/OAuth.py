# Yan Pan, 2023
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Annotated


from auth import schemas
from settings.settings import Settings


settings = Settings()

CRYPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")
SCHEME = OAuth2PasswordBearer(tokenUrl="/app002/auth/token") # needs include root

UserCollection = settings.get_user_collection_client()

########################
# Auth functionalities #
########################

async def get_user(username: str):
    doc = await UserCollection.find_one({"username": username})
    return doc

async def list_users():
    docs = await UserCollection.find().to_list(None)
    return docs

async def create_user(payload: schemas.UserWithPassword):
    """
    create new user with password, DB will encrypt it, and _id as username
    return: pymongo.results.InsertOneResult
    """
    payload = payload.dict()
    payload["hashed_password"] = CRYPTO.hash(payload.pop("password"))
    payload["_id"] = payload["username"]
    result = await UserCollection.insert_one(payload)
    return result 

async def delete_user(username: str):
    deletion_result = await UserCollection.delete_one({"username": username})
    return deletion_result

async def authenticate_user(username: str, password: str):
    user = await UserCollection.find_one({"username": username})
    if not user:
        return False
    if not CRYPTO.verify(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict):
    """
    create token providing {"sub": username}
    return type is string/raw token
    """
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_VALID_MINUTES)
    })
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def authenticate_user_and_create_token(username: str, password: str):
    """
    wrapping authenticate and token creation, return wrapped JWT 
    """
    user = await authenticate_user(username, password)
    if not user:
        return None
    return {
        "access_token": create_access_token(data={"sub": user["username"]}), 
        "token_type": "bearer"
    }

####################################
# authentication and authorization #
####################################

async def auth_user_token(token: Annotated[str, Depends(SCHEME)]):
    """
    validate JWT token and return associating user
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(401, "User not found")
        return username
    except JWTError:
        raise HTTPException(401, "Invalid token")

async def is_authenticated_user(username: Annotated[str, Depends(auth_user_token)]):
    """
    validate JWT token and return associating user
    """
    return username

async def is_authenticated_admin(username: Annotated[str, Depends(auth_user_token)]):
    """
    validate JWT token and confirm if is admin
    """
    user = await UserCollection.find_one({"username": username})
    if 0 not in user.get("roles", []):
        raise HTTPException(403, "Forbidden. Admin user required")
    return username
