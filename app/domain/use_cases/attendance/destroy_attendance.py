from app.infra.db.repositories.attendances_repository import AttendanceRepository
from .interfaces.i_destroy_attendance import IDestroyAttendance


class DestroyAttendanceUseCase(IDestroyAttendance):
    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    def execute(self, item_id):
        return self.repository.destroy(item_id)
