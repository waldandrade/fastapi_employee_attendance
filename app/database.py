from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import settings
from app import models, schemas
from app.repositories import user


# SQLALCHAMY_DATABASE_URL = 'sqlite:///./attendance.db'

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(db: Session) -> None:
    superuser = db.query(models.User).filter(
        models.User.email == settings.FIRST_SUPERUSER).first()
    if not superuser:
        user_in = schemas.User(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        superuser = user.create(user_in, db)
