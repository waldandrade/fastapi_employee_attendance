
from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status
from app.lib.crypt import Hash
from app.schemas import ScheduleMethod


def get_schedule_method(method: str):
    if method is not None:
        return ScheduleMethod(method)
    return None


def create(request: schemas.User, db: Session):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password), is_superuser=request.is_superuser, schedule_method=get_schedule_method(request.schedule_method),)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user


def profile(email: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the email {email} is not available")
    print(user)
    return user
