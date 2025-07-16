from app.infra.db.repositories.attendances_repository import AttendanceRepository
from .interfaces.i_create_attendance import ICreateAttendance


class CreateAttendanceUseCase(ICreateAttendance):
    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    def execute(self, data, user):
        return self.repository.create(data, user)
