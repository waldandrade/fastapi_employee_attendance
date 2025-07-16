

from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.infra.db.repositories.interfaces.i_users_repository import IUserRepository
from app.lib.crypt import Hash
from app.infra.db.models.users import User as UserModel
from app.domain.entities.users import User as UserEntity
from app.lib.utils import get_schedule_method


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[UserModel]:
        users = self.db.query(UserModel).all()
        return users

    def create(self, request: UserEntity) -> UserModel:
        new_user = UserModel(name=request.name,
                             email=request.email,
                             password=Hash.bcrypt(request.password),
                             is_superuser=request.is_superuser,
                             schedule_method=get_schedule_method(request.schedule_method))
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def show(self, item_id: int) -> UserModel:
        user = self.db.query(UserModel).filter(UserModel.id == item_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with the id {item_id} is not available")
        return user

    def profile(self, email: str) -> UserModel:
        user = self.db.query(UserModel).filter(
            UserModel.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with the email {email} is not available")
        return user
