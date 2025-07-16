from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from app.infra.db.models.users import User as UserModel
from app.domain.entities.users import User as UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def get_all(self, db: Session) -> List[UserModel]: pass

    @abstractmethod
    def create(self, request: UserEntity, db: Session) -> UserModel: pass

    @abstractmethod
    def show(self, item_id: int, db: Session) -> UserModel: pass

    @abstractmethod
    def profile(self, email: str, db: Session) -> UserModel: pass
