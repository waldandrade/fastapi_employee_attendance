from app.infra.db.repositories.users_repository import UserRepository
from .interfaces.i_getall_users import IGetAllUsers


class GetAllUsersUseCase(IGetAllUsers):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self):
        return self.repository.get_all()
