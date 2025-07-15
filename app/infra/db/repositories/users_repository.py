
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.lib.crypt import Hash
from app.infra.db.models.users import User as UserModel
from app.domain.entities.users import User as UserEntity
from app.commons.enums import ScheduleMethod


def get_schedule_method(method: str):
    if method is not None:
        return ScheduleMethod(method)
    return None


class UserRepository:
    @classmethod
    def get_all(cls, db: Session) -> List[UserModel]:
        users = db.query(UserModel).all()
        return users

    @classmethod
    def create(cls, request: UserEntity, db: Session) -> UserModel:
        new_user = UserModel(name=request.name,
                             email=request.email,
                             password=Hash.bcrypt(request.password),
                             is_superuser=request.is_superuser,
                             schedule_method=get_schedule_method(request.schedule_method))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @classmethod
    def show(cls, item_id: int, db: Session) -> UserModel:
        user = db.query(UserModel).filter(UserModel.id == item_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with the id {item_id} is not available")
        return user

    @classmethod
    def profile(cls, email: str, db: Session) -> UserModel:
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with the email {email} is not available")
        return user
