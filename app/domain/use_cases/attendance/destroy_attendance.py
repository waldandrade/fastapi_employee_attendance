from app.domain.interfaces.i_attendances_repository import IAttendanceRepository
from .interfaces.i_destroy_attendance import IDestroyAttendance


class DestroyAttendanceUseCase(IDestroyAttendance):
    def __init__(self, repository: IAttendanceRepository):
        self.repository = repository

    def execute(self, item_id):
        return self.repository.destroy(item_id)
