from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Boolean
from app.schemas import AttendanceStatus
from app.infra.db.settings.base import Base

class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    end = Column(Boolean, default=False)
    status = Column("status", Enum(AttendanceStatus))
    employee_id = Column(Integer, ForeignKey('users.id'))
    employee = relationship("User")
