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
token_url = "/app002/auth/token"

CRYPTO = CryptContext(schemes=["bcrypt"])
SCHEME = OAuth2PasswordBearer(tokenUrl=token_url)  # needs root

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
    payload["_id"] = payload["email"]
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
    token refresh also take this one
    """
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_VALID_MINUTES) # noqa
    })
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return {
        "access_token": encoded_jwt,
        "token_type": "Bearer"
    }


async def authenticate_user_and_create_token(username: str, password: str):
    """
    wrapping authenticate and token creation, return wrapped JWT
    """
    user = await authenticate_user(username, password)
    if not user:
        return None
    return create_access_token(data={"sub": user["username"]})


async def create_token_for_google_sign_in(userinfo):
    """
    wrapping social login and find registered user
    """
    print(userinfo)
    user = await UserCollection.find_one({"email": userinfo["email"]})

    if user:
        username = user["username"]
    else:
        username = userinfo["name"].replace(" ", "_")
        user_model = schemas.UserWithHashedPassword(
            username=username,
            email=userinfo["email"],
            full_name=userinfo["name"],
            hashed_password="OAuth2-Only-Google"
        )
        result = await UserCollection.insert_one({
            "_id": f"google@{user_model.email}", **user_model.dict()
        })
        print("New user created:", username, result.inserted_id)

    return create_access_token(data={"sub": username})


####################################
# authentication and authorization #
####################################


async def auth_user_token(token: Annotated[str, Depends(SCHEME)]):
    """
    validate JWT token and return associating user
    """
    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")

        print("JWT Decode", payload.get('exp', "???"))

        if username is None:
            raise HTTPException(401, "User not found")
        return username
    except JWTError:
        raise HTTPException(401, "Invalid token")


async def is_authenticated_user(
    username: Annotated[str, Depends(auth_user_token)]
):
    """
    validate JWT token and return associating user
    """
    return username


async def is_authenticated_admin(
        username: Annotated[str, Depends(auth_user_token)]
):
    """
    validate JWT token and confirm if is admin
    """
    user = await UserCollection.find_one({"username": username})
    if 0 not in user.get("roles", []):
        raise HTTPException(403, "Forbidden. Admin user required")
    return username
