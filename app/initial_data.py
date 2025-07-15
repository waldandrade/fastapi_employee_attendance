import os
from pytest import Session
from app import models, schemas
from app.repositories import user


def init_db(db: Session) -> None:
    super_user_email = os.getenv('FIRST_SUPERUSER')
    super_user_password = os.getenv('FIRST_SUPERUSER_PASSWORD')
    if super_user_email is not None and super_user_password is not None:
        superuser = db.query(models.User).filter(
            models.User.email == super_user_email).first()
        if not superuser:
            user_in = schemas.User(
                email=super_user_email,
                password=super_user_password,
                is_superuser=True,
            )
            superuser = user.create(user_in, db)
