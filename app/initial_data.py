from pytest import Session

from app import models
from app import models, schemas
from app.repositories import user
from app.config import settings


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
