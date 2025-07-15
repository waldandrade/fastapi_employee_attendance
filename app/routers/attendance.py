from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database
from app.lib import oauth2
from app.repositories import attendance

router = APIRouter(
    prefix="/attendance",
    tags=['Attendances']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowAttendance])
def get_all(db: Session = Depends(get_db), _: schemas.User = Depends(oauth2.get_current_user)):
    return attendance.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Attendance,
           db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with the email {current_user.email} is not available")
    return attendance.create(request, current_user, db)


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(item_id: int,
            db: Session = Depends(get_db),
            _: schemas.User = Depends(oauth2.get_current_user)):
    return attendance.destroy(item_id, db)


@router.put('/{item_id}', status_code=status.HTTP_202_ACCEPTED)
def update(item_id: int,
           request: schemas.Attendance,
           db: Session = Depends(get_db),
           _: schemas.User = Depends(oauth2.get_current_user)):
    return attendance.update(item_id, request, db)


@router.get('/{item_id}', status_code=200, response_model=schemas.ShowAttendance)
def show(item_id: int,
         db: Session = Depends(get_db),
         _: schemas.User = Depends(oauth2.get_current_user)):
    return attendance.show(item_id, db)
