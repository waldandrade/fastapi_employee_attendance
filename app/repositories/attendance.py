from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status
from app.schemas import AttendanceStatus


def get_all(db: Session):
    attendances = db.query(models.Attendance).all()
    return attendances


def create(request: schemas.Attendance, current_user: schemas.User, db: Session):
    user = db.query(models.User).filter(
        models.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with the email {current_user.email} is not available")

    new_attendance = models.Attendance(
        date=request.date, status=AttendanceStatus(request.status), employee_id=user.id)
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance


def destroy(id: int, db: Session):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == id)

    if not attendance.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Attendance with id {id} not found")

    attendance.delete(synchronize_session=False)
    db.commit()
    return 'done'


def update(id: int, request: schemas.Attendance, db: Session):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == id)

    if not attendance.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Attendance with id {id} not found")

    attendance.update(request)
    db.commit()
    return 'updated'


def show(id: int, db: Session):
    attendance = db.query(models.Attendance).filter(
        models.Attendance.id == id).first()
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Attendance with the id {id} is not available")
    return attendance
