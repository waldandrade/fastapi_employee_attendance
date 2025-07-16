from app.infra.db.repositories.users_repository import UserRepository
from .interfaces.i_create_user import ICreateUser


class CreateUserUseCase(ICreateUser):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, data):
        return self.repository.create(data)
