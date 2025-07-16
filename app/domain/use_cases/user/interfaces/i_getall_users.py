from abc import ABC, abstractmethod
from typing import Dict


class IGetAllUsers(ABC):

    @abstractmethod
    def execute(self) -> Dict: pass
