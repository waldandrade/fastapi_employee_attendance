from datetime import datetime, timedelta
import pytest
from fastapi.exceptions import HTTPException
from app.domain.use_cases.attendance.create_attendance import CreateAttendanceUseCase
from app.infra.db.models.attendances import Attendance as AttendanceModel
from app.infra.db.repositories.attendances_repository import AttendanceRepository
from app.domain.entities.attendances import Attendance
from app.commons.enums import AttendanceStatus


def test_should_create(db_session, current_user):
    new_attendance = Attendance(
        date=datetime.now(), status=AttendanceStatus.ENTERING)
    repo = AttendanceRepository(db_session)
    use_case = CreateAttendanceUseCase(repo)
    att = use_case.execute(new_attendance, current_user)
    assert isinstance(att, AttendanceModel)


def test_user_six_hour_can_not_pause(db_session,
                                     current_user_no_pauses,
                                     mock_attendance_and_retrieve):
    tempo_adicional = timedelta(hours=1, minutes=30)
    new_attendance = Attendance(date=mock_attendance_and_retrieve.date + tempo_adicional,
                                status=AttendanceStatus.PAUSE_STARTING)
    with pytest.raises((HTTPException)):
        repo = AttendanceRepository(db_session)
        use_case = CreateAttendanceUseCase(repo)
        use_case.execute(new_attendance, current_user_no_pauses)
