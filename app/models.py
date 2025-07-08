import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from app.database import Base
from sqlalchemy.orm import relationship


class AttendanceStatus(enum.Enum):
    ENTERING = 'entering'
    EXITING = 'exiting'


class ScheduleMethod(enum.Enum):
    SIX_HOURS_WITHOUT_BREAK = 'six_hours_without_break'
    EIGHT_HOURS_WITH_BREAK = 'eight_hours_with_break'


class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    end = Column(Boolean, default=False)
    status = Column(Enum(AttendanceStatus))
    employee_id = Column(Integer, ForeignKey('users.id'))
    employee = relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    schedule_method = Column(Enum(ScheduleMethod))
