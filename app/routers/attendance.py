from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app import schemas, database
from app.lib import oauth2
from sqlalchemy.orm import Session
from app.repositories import attendance

router = APIRouter(
    prefix="/attendance",
    tags=['Attendances']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowAttendance])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return attendance.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Attendance, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return attendance.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return attendance.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Attendance, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return attendance.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowAttendance)
def show(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return attendance.show(id, db)
