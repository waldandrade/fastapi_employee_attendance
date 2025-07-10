import pytest
from datetime import datetime
from app.repositories import attendance
from app.schemas import ScheduleMethod, AttendanceStatus, User, Attendance
from app.models import Attendance as AttendanceModel
from datetime import datetime, timedelta


def test_should_create(db_session, current_user):
    new_attendance = Attendance(
        date=datetime.now(), status=AttendanceStatus.ENTERING)
    att = attendance.create(new_attendance, current_user, db_session)
    assert isinstance(att, AttendanceModel)


def test_user_six_hour_can_not_pause(db_session, current_user_no_pauses, mock_attendance_and_retrieve):
    tempo_adicional = timedelta(hours=1, minutes=30)
    new_attendance = Attendance(
        date=mock_attendance_and_retrieve.date + tempo_adicional, status=AttendanceStatus.PAUSE_STARTING)
    with pytest.raises((TypeError, KeyError)):
        attendance.create(
            new_attendance, current_user_no_pauses, db_session)


def test_should_create(db_session, current_user, mock_attendances_and_get_recent):
    # assert mock_attendances_and_get_recent.date.ctime() == datetime.now().ctime()
    pass
