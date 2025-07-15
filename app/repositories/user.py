
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import schemas
from app.lib.crypt import Hash
from app.schemas import ScheduleMethod
from app.infra.db.models.users import User as UserModel


def get_schedule_method(method: str):
    if method is not None:
        return ScheduleMethod(method)
    return None


def get_all(db: Session):
    users = db.query(UserModel).all()
    return users


def create(request: schemas.User, db: Session):
    new_user = UserModel(name=request.name,
                           email=request.email,
                           password=Hash.bcrypt(request.password),
                           is_superuser=request.is_superuser,
                           schedule_method=get_schedule_method(request.schedule_method))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(item_id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == item_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {item_id} is not available")
    return user


def profile(email: str, db: Session):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the email {email} is not available")
    return user
