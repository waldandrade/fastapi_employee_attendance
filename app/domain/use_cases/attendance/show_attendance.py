from app.infra.db.repositories.interfaces.i_attendances_repository import IAttendanceRepository
from .interfaces.i_show_attendance import IShowAttendance


class ShowAttendanceUseCase(IShowAttendance):
    def __init__(self, repository: IAttendanceRepository):
        self.repository = repository

    def execute(self, item_id):
        return self.repository.show(item_id)
