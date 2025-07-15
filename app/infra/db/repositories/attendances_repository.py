from datetime import date, datetime, time
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import schemas
from app.schemas import AttendanceStatus, ScheduleMethod
from app.infra.db.models.users import User as UserModel
from app.infra.db.models.attendances import Attendance as AttendanceModel


class AttendanceRepository:
    @classmethod
    def get_all(cls, db: Session):
        attendances = db.query(AttendanceModel).all()
        return attendances

    @classmethod
    def ensure_journey(cls,
                       user: UserModel,
                       attendance_status: AttendanceStatus,
                       last_attendance_of_day: AttendanceModel):
        if AttendanceStatus(last_attendance_of_day.status) == AttendanceStatus.EXITING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Day journey already endded")

        if (AttendanceStatus(last_attendance_of_day.status) == AttendanceStatus.PAUSE_STARTING and
            attendance_status != AttendanceStatus.PAUSE_ENDING):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Pause must to be endded")

        if ScheduleMethod(user.schedule_method) == ScheduleMethod.SIX_HOURS_WITHOUT_BREAK:
            if (AttendanceStatus(last_attendance_of_day.status) == AttendanceStatus.ENTERING and
                attendance_status != AttendanceStatus.EXITING):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Attendance can not be created")

    @classmethod
    def get_most_recent_entry_by_day(cls, target_date: date,
                                    employee: UserModel,
                                    db: Session) -> AttendanceModel | None:
        start_of_day = datetime.combine(
            target_date.date(), time.min)
        end_of_day = datetime.combine(
            target_date.date(), time.max)

        entrada_mais_recente = db.query(AttendanceModel) \
            .filter(AttendanceModel.date >= start_of_day,
                    AttendanceModel.date <= end_of_day,
                    AttendanceModel.employee_id == employee.id) \
            .order_by(AttendanceModel.date.desc()) \
            .first()
        return entrada_mais_recente


    @classmethod
    def create(cls, request: schemas.Attendance, current_user: schemas.User, db: Session):
        user = db.query(UserModel).filter(
            UserModel.email == current_user.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User with the email {current_user.email} is not available")
        recent_attendance = cls.get_most_recent_entry_by_day(
            request.date, user, db)

        if recent_attendance is not None:
            cls.ensure_journey(user, AttendanceStatus(
                request.status), recent_attendance)

        new_attendance = AttendanceModel(
            date=request.date, status=AttendanceStatus(request.status), employee_id=user.id)
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        return new_attendance

    @classmethod
    def destroy(cls, item_id: int, db: Session):
        attendance = db.query(AttendanceModel).filter(AttendanceModel.id == item_id)

        if not attendance.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Attendance with id {item_id} not found")

        attendance.delete(synchronize_session=False)
        db.commit()
        return 'done'

    @classmethod
    def update(cls, item_id: int, request: schemas.Attendance, db: Session):
        attendance = db.query(AttendanceModel).filter(AttendanceModel.id == item_id)

        if not attendance.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Attendance with id {item_id} not found")

        attendance.update(request)
        db.commit()
        return 'updated'

    @classmethod
    def show(cls, item_id: int, db: Session):
        attendance = db.query(AttendanceModel).filter(
            AttendanceModel.id == item_id).first()
        if not attendance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Attendance with the id {item_id} is not available")
        return attendance
