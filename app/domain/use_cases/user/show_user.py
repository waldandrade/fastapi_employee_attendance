from app.infra.db.repositories.users_repository import UserRepository
from .interfaces.i_show_user import IShowUser


class ShowUserUseCase(IShowUser):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, item_id):
        return self.repository.show(item_id)
