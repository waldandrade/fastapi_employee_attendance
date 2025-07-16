from app.domain.interfaces.i_users_repository import IUserRepository
from .interfaces.i_show_user import IShowUser


class ShowUserUseCase(IShowUser):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def execute(self, item_id):
        return self.repository.show(item_id)
