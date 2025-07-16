from app.infra.db.repositories.users_repository import UserRepository
from .interfaces.i_profile_user import IProfileUser


class ProfileUserUseCase(IProfileUser):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, email):
        return self.repository.profile(email)
