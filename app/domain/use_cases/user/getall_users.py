from app.infra.db.repositories.interfaces.i_users_repository import IUserRepository
from .interfaces.i_getall_users import IGetAllUsers


class GetAllUsersUseCase(IGetAllUsers):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def execute(self):
        return self.repository.get_all()
