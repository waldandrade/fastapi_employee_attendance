from abc import ABC, abstractmethod


class IDestroyAttendance(ABC):

    @abstractmethod
    def execute(self, item_id: int): pass
