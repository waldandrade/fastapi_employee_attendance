from abc import ABC, abstractmethod
from typing import Any

from app.domain.entities.attendances import Attendance as AttendanceEntity


class IUpdateAttendance(ABC):

    @abstractmethod
    def execute(self, item_id: int, data: AttendanceEntity) -> Any: pass
