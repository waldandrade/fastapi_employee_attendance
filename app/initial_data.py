import os
from sqlalchemy.orm import Session
from app.infra.db.repositories.users_repository import UserRepository
from app.infra.db.models.users import User as UserModel
from app.domain.entities.users import User as UserEntity


def init_db(db: Session) -> None:
    super_user_email = os.getenv('FIRST_SUPERUSER')
    super_user_password = os.getenv('FIRST_SUPERUSER_PASSWORD')
    if super_user_email is not None and super_user_password is not None:
        superuser = db.query(UserModel).filter(
            UserModel.email == super_user_email).first()
        if not superuser:
            user_in = UserEntity(
                email=super_user_email,
                password=super_user_password,
                is_superuser=True,
            )
            users_repository = UserRepository(db)
            superuser = users_repository.create(user_in)
