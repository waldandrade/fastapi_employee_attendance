from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.commons.enums import AttendanceStatus
from app.domain.entities.users import ShowUser


class AttendanceBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    date: datetime
    status: AttendanceStatus


class Attendance(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)


class ShowAttendance(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)
    date: datetime
    status: str
    employee: ShowUser
