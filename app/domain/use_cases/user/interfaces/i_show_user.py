from abc import ABC, abstractmethod
from typing import Any


class IShowUser(ABC):

    @abstractmethod
    def execute(self, item_id: int) -> Any: pass
