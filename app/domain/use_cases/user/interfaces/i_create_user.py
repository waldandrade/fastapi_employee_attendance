from abc import ABC, abstractmethod
from typing import Any
from app.domain.entities.users import User as UserEntity


class ICreateUser(ABC):

    @abstractmethod
    def execute(self, data: UserEntity) -> Any: pass
