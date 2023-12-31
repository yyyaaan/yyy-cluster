# Yan Pan, 2023
from pydantic import BaseModel, EmailStr, Field
from typing import Union
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str
    fullname: Optional[str] = ""


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[EmailStr, None] = None
    full_name: str = ""
    roles: list[int] = [1]  # 0 is admin
    disabled: bool = False


class UserWithPassword(User):
    password: str


class UserWithHashedPassword(User):
    hashed_password: str
    created_at: float = -1


class UserWithExtra(User):
    id: Union[str, int] = Field(alias="_id")
    accepted: bool = True
    origin: dict = {}
