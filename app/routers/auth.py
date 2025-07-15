from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import database
from app.lib import jwt_token
from app.lib.crypt import Hash
from app.infra.db.models.users import User as UserModel

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(UserModel).filter(
        UserModel.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    if not Hash.verify(user.password, form_data.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password")

    access_token = jwt_token.create_access_token(
        data={"sub": user.email, "is_superuser": user.is_superuser})
    return {"access_token": access_token, "token_type": "bearer"}
