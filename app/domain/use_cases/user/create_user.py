from app.infra.db.repositories.interfaces.i_users_repository import IUserRepository
from .interfaces.i_create_user import ICreateUser


class CreateUserUseCase(ICreateUser):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def execute(self, data):
        return self.repository.create(data)
