from app.domain.interfaces.i_attendances_repository import IAttendanceRepository
from .interfaces.i_getall_attendances import IGetAllAttendances


class GetAllAttendancesUseCase(IGetAllAttendances):
    def __init__(self, repository: IAttendanceRepository):
        self.repository = repository

    def execute(self):
        return self.repository.get_all()
