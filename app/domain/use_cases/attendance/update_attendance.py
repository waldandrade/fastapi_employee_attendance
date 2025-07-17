from app.domain.interfaces.i_attendances_repository import IAttendanceRepository
from .interfaces.i_update_attendance import IUpdateAttendance


class UpdateAttendanceUseCase(IUpdateAttendance):
    def __init__(self, repository: IAttendanceRepository):
        self.repository = repository

    def execute(self, item_id, data):
        return self.repository.update(item_id, data)
