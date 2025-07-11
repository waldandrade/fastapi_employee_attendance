from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app import database, schemas
from app.repositories import user
from app.lib import oauth2, permissions

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/', response_model=List[schemas.ShowUser])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(permissions.get_current_active_superuser)):
    return user.get_all(db)


@router.get('/profile', response_model=schemas.ShowUser)
def get_profile(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.profile(current_user.email, db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.show(id, db)
