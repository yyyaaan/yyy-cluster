# Yan Pan, 2023
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorCollection
from passlib.context import CryptContext


from auth import schemas
from settings.settings import Settings

class JwtAuth():
    """
    Wrapped JWT authentication class, backend should be MongoDB or other noSQL supports .find()
    collection_users should from app, for example
    - request.app.collection_users

    This class does not send HTTP response, and should be handled in app or router.
    """

    crypto = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/app002/auth/token")
    # remember to check the tokenUrl, needs to include base_url
    
    def __init__(self, collection_users: AsyncIOMotorCollection) -> None:
        settings = Settings()
        self.secret_key = settings.JWT_SECRET
        self.algorithm = settings.JWT_ALGORITHM
        self.valid_minutes = settings.JWT_VALID_MINUTES
        self.registered_users = collection_users

    async def create_user(self, payload: schemas.UserWithPassword):
        """
        create new user with password, DB will encrypt it, and _id as username
        return: pymongo.results.InsertOneResult
        """
        payload = payload.dict()
        payload["hashed_password"] = self.crypto.hash(payload.pop("password"))
        payload["_id"] = payload["username"]
        result = await self.registered_users.insert_one(payload)
        return result 
    
    async def authenticate_user(self, username: str, password: str):
        user = await self.registered_users.find_one({"username": username})
        if not user:
            return False
        if not self.crypto.verify(password, user["hashed_password"]):
            return False
        return user

    def create_access_token(self, data: dict):
        """return type is string/raw token"""
        to_encode = data.copy()
        to_encode.update({
            "exp": datetime.utcnow() + timedelta(minutes=self.valid_minutes)
        })
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    async def authenticate_user_and_create_token(self, username: str, password: str):
        """
        wrapping authenticate and token creation, return wrapped JWT 
        """
        user = await self.authenticate_user(username, password)
        if not user:
            return None
        return {
            "access_token": self.create_access_token(data={"sub": user["username"]}), 
            "token_type": "bearer"
        }
    
    async def get_current_user(self, token):
        """
        get current user from a JWT token
        returns user object, or None (if token is invalid, user not existing or disabled)
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
            user = await self.registered_users.find_one({"username": username})
            if user is None or user.get("disabled") is True:
                return None
            return user
        except JWTError:
            return None
