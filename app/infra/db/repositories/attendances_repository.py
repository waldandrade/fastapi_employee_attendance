from datetime import date, datetime, time
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.domain.interfaces.i_attendances_repository import IAttendanceRepository
from app.infra.db.models.users import User as UserModel
from app.infra.db.models.attendances import Attendance as AttendanceModel
from app.domain.entities.attendances import Attendance as AttendanceEntity
from app.domain.entities.users import User as UserEntity
from app.commons.enums import AttendanceStatus, ScheduleMethod


class AttendanceRepository(IAttendanceRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        attendances = self.db.query(AttendanceModel).all()
        return attendances

    def ensure_journey(self,
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

    def get_most_recent_entry_by_day(self, target_date: date,
                                     employee: UserModel) -> AttendanceModel | None:
        start_of_day = datetime.combine(
            target_date.date(), time.min)
        end_of_day = datetime.combine(
            target_date.date(), time.max)

        entrada_mais_recente = self.db.query(AttendanceModel) \
            .filter(AttendanceModel.date >= start_of_day,
                    AttendanceModel.date <= end_of_day,
                    AttendanceModel.employee_id == employee.id) \
            .order_by(AttendanceModel.date.desc()) \
            .first()
        return entrada_mais_recente

    def create(self, request: AttendanceEntity, current_user: UserEntity):
        user = self.db.query(UserModel).filter(
            UserModel.email == current_user.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User with the email {current_user.email} is not available")
        recent_attendance = self.get_most_recent_entry_by_day(
            request.date, user)

        if recent_attendance is not None:
            self.ensure_journey(user, AttendanceStatus(
                request.status), recent_attendance)

        new_attendance = AttendanceModel(
            date=request.date, status=AttendanceStatus(request.status), employee_id=user.id)
        self.db.add(new_attendance)
        self.db.commit()
        self.db.refresh(new_attendance)
        return new_attendance

    def destroy(self, item_id: int):
        attendance = self.db.query(AttendanceModel).filter(
            AttendanceModel.id == item_id)

        if not attendance.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Attendance with id {item_id} not found")

        attendance.delete(synchronize_session=False)
        self.db.commit()
        return 'done'

    def update(self, item_id: int, request: AttendanceEntity):
        attendance = self.db.query(AttendanceModel).filter(
            AttendanceModel.id == item_id)

        if not attendance.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Attendance with id {item_id} not found")

        attendance.update(request)
        self.db.commit()
        return 'updated'

    def show(self, item_id: int):
        attendance = self.db.query(AttendanceModel).filter(
            AttendanceModel.id == item_id).first()
        if not attendance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Attendance with the id {item_id} is not available")
        return attendance
