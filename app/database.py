from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


# SQLALCHAMY_DATABASE_URL = 'sqlite:///./attendance.db'

# engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

# Base = declarative_base()


def get_db():
    db = None
    try:
        yield db
    finally:
        db.close()
