from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database
from app.lib import oauth2, permissions
from app.infra.db.repositories.users_repository import UserRepository
from app.domain.entities.users import ShowUser, User as UserEntity

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=ShowUser)
def create_user(request: UserEntity, db: Session = Depends(get_db)):
    users_repository = UserRepository()
    return users_repository.create(request, db)


@router.get('/', response_model=List[ShowUser])
def get_all(db: Session = Depends(get_db),
            _: UserEntity = Depends(permissions.get_current_active_superuser)):
    users_repository = UserRepository()
    return users_repository.get_all(db)


@router.get('/profile', response_model=ShowUser)
def get_profile(db: Session = Depends(get_db),
                current_user: UserEntity = Depends(oauth2.get_current_user)):
    users_repository = UserRepository()
    return users_repository.profile(current_user.email, db)


@router.get('/{item_id}', response_model=ShowUser)
def get_user(item_id: int,
             db: Session = Depends(get_db),
             _: UserEntity = Depends(oauth2.get_current_user)):
    users_repository = UserRepository()
    return users_repository.show(item_id, db)
