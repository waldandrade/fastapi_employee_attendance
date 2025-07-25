from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    is_superuser: Optional[bool] = None
    exp: Optional[datetime] = None
