from abc import ABC, abstractmethod
from typing import Dict


class IGetAllAttendances(ABC):

    @abstractmethod
    def execute(self) -> Dict: pass
