from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class AttendanceBase(BaseModel):
    date: datetime
    status: str


class Attendance(AttendanceBase):
    class Config():
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config():
        from_attributes = True


class ShowAttendance(AttendanceBase):
    date: datetime
    status: str
    employee: ShowUser

    class Config():
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
