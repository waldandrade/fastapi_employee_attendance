import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from app.schemas import AttendanceStatus, ScheduleMethod
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    end = Column(Boolean, default=False)
    status = Column("status", Enum(AttendanceStatus))
    employee_id = Column(Integer, ForeignKey('users.id'))
    employee = relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    schedule_method = Column("method", Enum(ScheduleMethod))
    is_superuser = Column(Boolean, default=False)
