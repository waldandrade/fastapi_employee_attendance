from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status


def get_all(db: Session):
    attendances = db.query(models.Attendance).all()
    return attendances


def create(request: schemas.Attendance, db: Session):
    new_attendance = models.Attendance(
        title=request.title, body=request.body, user_id=1)
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
