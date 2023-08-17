# Yan Pan, 2023
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Annotated

from auth import schemas
from settings.settings import Settings


settings = Settings()
token_url = f"http://{settings.HOSTNAME_ROOTPATH}/auth/token"
if "localhost" not in token_url:
    token_url = token_url.replace("http://", "https://")
UserCollection = settings.get_user_collection_client()

SCHEME = OAuth2PasswordBearer(tokenUrl=token_url)
CRYPTO = CryptContext(schemes=["bcrypt"])


#############################
# User and Token Generation #
#############################


async def get_user(username: str):
    doc = await UserCollection.find_one({"username": username})
    return doc


async def new_user_accept(username: str):
    try:
        return await UserCollection.update_one(
            {"username": username},
            {"$set": {"accepted": True}}
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Unexpected authentication issue: {e}"
        )


async def list_users():
    docs = await UserCollection.find().to_list(None)
    return docs


async def create_user(payload: schemas.UserWithPassword):
    """
    create new user with password, DB will encrypt it, and _id as username
    return: pymongo.results.InsertOneResult
    """
    payload = payload.model_dump()
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
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_VALID_MINUTES)  # noqa: E501
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


async def create_token_for_third_login(userinfo):
    """
    wrapping social login and find registered user
    same email will return same user, update may occur
    """
    # determining origin
    if "gists_url" in userinfo:
        origin = "github"
    elif "microsoft" in userinfo.get("@odata.context", "x"):
        origin = "microsoft"
    else:
        origin = "google"

    user_email = userinfo.get("email", userinfo.get("mail", None))
    if user_email is None:
        raise Exception("Email is not found for OpenId")
    print("Creating Token", origin, user_email, userinfo)

    # found matched user by email
    user = await UserCollection.find_one({"email": user_email})

    # existing, may add new
    if user:
        username = user["username"]
        if origin not in user["origin"]:
            result = await UserCollection.update_one(
                {"username": username},
                {"$set": {"origin": {origin: userinfo, **user["origin"]}}}
            )
            print("New origin added for existing user:", username, origin)
    # new user
    else:
        username = f"{origin}@{user_email}"
        user_model = schemas.UserWithHashedPassword(
            username=username,
            email=user_email,
            full_name=userinfo.get("name", userinfo.get("displayName", user_email)),  # noqa: E501
            created_at=datetime.utcnow().timestamp(),
            hashed_password="OAuth2-Only"
        )
        try:
            schema_data = user_model.model_dump()
        except:  # noqa: E722 this is for backward compatibility
            schema_data = user_model.dict()
        result = await UserCollection.insert_one({
            "_id": username,
            "accepted": False,
            **schema_data,
            "origin": {origin: userinfo},
        })
        print("New user created:", username, result.inserted_id)

    return create_access_token(data={"sub": username})


####################################
# authentication and authorization #
####################################


async def auth_user_token(
    request: Request,
    token: Annotated[str, Depends(SCHEME)]
):
    """
    validate JWT token and return associating user
    Two states are injected to request:
    - username: str
    - trace: callable for possible record something to db
    """
    # print("AuthChain: validate token")
    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(401, "User not found")

        # inject state (inc. callables) to request
        def __trace(x: dict):
            print({"username": username, "usage": x})
        request.state.username = username
        request.state.trace = __trace
        return username

    except JWTError:
        raise HTTPException(401, "Invalid token")


async def is_registered_user(
    request: Request,
    username: Annotated[str, Depends(auth_user_token)]
):
    """
    is user registered, this will return OK even if user is not accepted.
    generally, stronger is_authenticated_user is necessary.
    """
    # print("AuthChain: validate user is registered")
    user = await UserCollection.find_one({"username": username})
    if user is None:
        raise HTTPException(401, "Not authenticated. User not found.")
    return username


async def is_authenticated_user(
    request: Request,
    username: Annotated[str, Depends(is_registered_user)]
):
    """
    validate JWT token and return associating user
    """
    # print("AuthChain: validate user has accepted")
    user = await UserCollection.find_one({"username": username})
    if not user.get("accepted", True):
        raise HTTPException(401, "Not authenticated. Pending acceptance.")
    return username


async def is_authenticated_admin(
    request: Request,
    username: Annotated[str, Depends(is_authenticated_user)]
):
    """
    validate JWT token and confirm if is admin
    """
    # print("AuthChain: validate user is admin")
    user = await UserCollection.find_one({"username": username})
    if 0 not in user.get("roles", []):
        raise HTTPException(403, "Forbidden. Admin user required")
    return username
