from abc import ABC, abstractmethod
from typing import List
from app.infra.db.models.attendances import Attendance as AttendanceModel


class IGetAllAttendances(ABC):

    @abstractmethod
    def execute(self) -> List[AttendanceModel]: pass
