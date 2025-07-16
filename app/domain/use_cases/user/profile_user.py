from app.infra.db.repositories.interfaces.i_users_repository import IUserRepository
from .interfaces.i_profile_user import IProfileUser


class ProfileUserUseCase(IProfileUser):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def execute(self, email):
        return self.repository.profile(email)
