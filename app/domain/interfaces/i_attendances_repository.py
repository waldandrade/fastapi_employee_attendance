from abc import ABC, abstractmethod
from datetime import date
from app.domain.entities.attendances import Attendance as AttendanceEntity
from app.domain.entities.users import User as UserEntity
from app.infra.db.models.attendances import Attendance as AttendanceModel
from app.infra.db.models.users import User as UserModel
from app.commons.enums import AttendanceStatus


class IAttendanceRepository(ABC):
    @abstractmethod
    def get_all(self) -> AttendanceModel: pass

    @abstractmethod
    def ensure_journey(self,
                       user: UserModel,
                       attendance_status: AttendanceStatus,
                       last_attendance_of_day: AttendanceModel): pass

    @abstractmethod
    def get_most_recent_entry_by_day(self,
                                     target_date: date,
                                     employee: UserModel) -> AttendanceModel | None: pass

    @abstractmethod
    def create(self, request: AttendanceEntity,
               current_user: UserEntity) -> AttendanceModel: pass

    @abstractmethod
    def destroy(self, item_id: int) -> str: pass

    @abstractmethod
    def update(self, item_id: int, request: AttendanceEntity) -> str: pass

    @abstractmethod
    def show(self, item_id: int) -> AttendanceModel: pass
