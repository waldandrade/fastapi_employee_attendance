from datetime import datetime, timedelta
import pytest
from fastapi.exceptions import HTTPException
from app.repositories import attendance
from app.schemas import AttendanceStatus, Attendance
from app.models import Attendance as AttendanceModel

@pytest.mark.skip(reason="Teste sensível")
def test_should_create(db_session, current_user):
    new_attendance = Attendance(
        date=datetime.now(), status=AttendanceStatus.ENTERING)
    att = attendance.create(new_attendance, current_user, db_session)
    assert isinstance(att, AttendanceModel)

@pytest.mark.skip(reason="Teste sensível")
def test_user_six_hour_can_not_pause(db_session,
                                     current_user_no_pauses,
                                     mock_attendance_and_retrieve):
    tempo_adicional = timedelta(hours=1, minutes=30)
    new_attendance = Attendance(date=mock_attendance_and_retrieve.date + tempo_adicional,
                                status=AttendanceStatus.PAUSE_STARTING)
    with pytest.raises((HTTPException)):
        attendance.create(
            new_attendance, current_user_no_pauses, db_session)
