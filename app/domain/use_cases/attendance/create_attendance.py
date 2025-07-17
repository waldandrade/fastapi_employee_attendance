from app.domain.interfaces.i_attendances_repository import IAttendanceRepository
from .interfaces.i_create_attendance import ICreateAttendance


class CreateAttendanceUseCase(ICreateAttendance):
    def __init__(self, repository: IAttendanceRepository):
        self.repository = repository

    def execute(self, data, user):
        return self.repository.create(data, user)
