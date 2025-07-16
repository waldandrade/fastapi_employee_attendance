from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.dependencies import get_db
from app.domain.use_cases.user.create_user import CreateUserUseCase
from app.domain.use_cases.user.getall_users import GetAllUsersUseCase
from app.domain.use_cases.user.profile_user import ProfileUserUseCase
from app.domain.use_cases.user.show_user import ShowUserUseCase
from app.lib import oauth2, permissions
from app.infra.db.repositories.users_repository import UserRepository
from app.domain.entities.users import ShowUser, User as UserEntity

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


def get_repository(db: Session = Depends(get_db)):
    return UserRepository(db)


@router.post('/', response_model=ShowUser)
def create_user(request: UserEntity, repo: UserRepository = Depends(get_repository)):
    use_case = CreateUserUseCase(repo)
    use_case.execute(request)


@router.get('/', response_model=List[ShowUser])
def get_all(repo: UserRepository = Depends(get_repository),
            _=Depends(permissions.get_current_active_superuser)):
    use_case = GetAllUsersUseCase(repo)
    return use_case.execute()


@router.get('/profile', response_model=ShowUser)
def get_profile(repo: UserRepository = Depends(get_repository),
                current_user: UserEntity = Depends(oauth2.get_current_user)):
    use_case = ProfileUserUseCase(repo)
    return use_case.execute(current_user.email)


@router.get('/{item_id}', response_model=ShowUser)
def get_user(item_id: int,
             repo: UserRepository = Depends(get_repository),
             _=Depends(oauth2.get_current_user)):
    use_case = ShowUserUseCase(repo)
    return use_case.execute(item_id)
