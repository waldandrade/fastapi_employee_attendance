from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AttendanceStatus(Enum):
    ENTERING = 'entering'
    PAUSE_STARTING = 'pausing'
    PAUSE_ENDING = 'backing'
    EXITING = 'exiting'


class ScheduleMethod(Enum):
    SIX_HOURS_WITHOUT_BREAK = 'six_hours_without_break'
    EIGHT_HOURS_WITH_BREAK = 'eight_hours_with_break'


class AttendanceBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    date: datetime
    status: AttendanceStatus


class Attendance(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    name: Optional[str] = None
    email: str
    password: str
    is_superuser: Optional[bool] = False
    schedule_method: Optional[ScheduleMethod] = None


class ShowUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: str
    schedule_method: str


class ShowAttendance(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)
    date: datetime
    status: str
    employee: ShowUser


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
