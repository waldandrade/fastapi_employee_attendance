from sqlalchemy import Column, Integer, String, Enum, Boolean
from app.infra.db.settings.base import Base
from app.commons.enums import ScheduleMethod


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    schedule_method = Column("method", Enum(ScheduleMethod))
    is_superuser = Column(Boolean, default=False)
