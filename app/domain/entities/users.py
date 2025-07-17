from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.commons.enums import ScheduleMethod


class User(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    name: Optional[str] = None
    email: str
    password: str
    is_superuser: Optional[bool] = False
    schedule_method: Optional[ScheduleMethod] = None


class ShowUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    email: str
    schedule_method: Optional[str] = None
    is_superuser: Optional[bool] = False
