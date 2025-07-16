from app.infra.db.repositories.attendances_repository import AttendanceRepository
from .interfaces.i_update_attendance import IUpdateAttendance


class UpdateAttendanceUseCase(IUpdateAttendance):
    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    def execute(self, item_id, data):
        return self.repository.update(item_id, data)
