from abc import ABC, abstractmethod
from typing import Any

from app.domain.entities.attendances import Attendance as AttendanceEntity


class ICreateAttendance(ABC):

    @abstractmethod
    def execute(self, data: AttendanceEntity) -> Any: pass
