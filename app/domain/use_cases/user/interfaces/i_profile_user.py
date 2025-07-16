from abc import ABC, abstractmethod
from typing import Any


class IProfileUser(ABC):

    @abstractmethod
    def execute(self, email: str) -> Any: pass
