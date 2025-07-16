from app.infra.db.repositories.attendances_repository import AttendanceRepository
from .interfaces.i_getall_attendances import IGetAllAttendances


class GetAllAttendancesUseCase(IGetAllAttendances):
    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    def execute(self):
        return self.repository.get_all()
