from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status
from app.schemas import AttendanceStatus, ScheduleMethod
from datetime import date, datetime, time


def get_all(db: Session):
    attendances = db.query(models.Attendance).all()
    return attendances


def ensure_journey(user: models.User, date: datetime, attendance_status: AttendanceStatus, last_attendance_of_day: models.Attendance):
    # TODO Implementar mais regras aqui
    if AttendanceStatus(last_attendance_of_day.status) == AttendanceStatus.EXITING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Day journey already endded")

    if AttendanceStatus(last_attendance_of_day.status) == AttendanceStatus.PAUSE_STARTING and attendance_status != AttendanceStatus.PAUSE_ENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Pause must to be endded")

    if ScheduleMethod(user.schedule_method) == ScheduleMethod.SIX_HOURS_WITHOUT_BREAK:
        if AttendanceStatus(last_attendance_of_day.status) == AttendanceStatus.ENTERING and attendance_status != AttendanceStatus.EXITING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Attendance can not be created")


def get_most_recent_entry_by_day(target_date: date, employee: models.User, db: Session) -> models.Attendance | None:
    start_of_day = datetime.combine(
        target_date.date(), time.min)
    end_of_day = datetime.combine(
        target_date.date(), time.max)

    entrada_mais_recente = db.query(models.Attendance) \
        .filter(models.Attendance.date >= start_of_day,
                models.Attendance.date <= end_of_day, models.Attendance.employee_id == employee.id) \
        .order_by(models.Attendance.date.desc()) \
        .first()
    return entrada_mais_recente


def create(request: schemas.Attendance, current_user: schemas.User, db: Session):
    user = db.query(models.User).filter(
        models.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with the email {current_user.email} is not available")
    recent_attendance = get_most_recent_entry_by_day(
        request.date, user, db)

    ensure_journey(user, request.date, AttendanceStatus(
        request.status), recent_attendance)

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
