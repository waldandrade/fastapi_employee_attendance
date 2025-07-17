from datetime import timedelta, datetime
from typing import List
import pytest
from fastapi.exceptions import HTTPException
from app.domain.use_cases.attendance.create_attendance import CreateAttendanceUseCase
from app.domain.use_cases.attendance.destroy_attendance import DestroyAttendanceUseCase
from app.domain.use_cases.attendance.getall_attendances import GetAllAttendancesUseCase
from app.domain.use_cases.attendance.show_attendance import ShowAttendanceUseCase
from app.infra.db.models.attendances import Attendance as AttendanceModel
from app.infra.db.repositories.attendances_repository import AttendanceRepository
from app.domain.entities.attendances import Attendance as AttendanceEntity
from app.commons.enums import AttendanceStatus


def test_should_get_attendance_by_id(
        db_session, mock_attendance_and_retrieve: AttendanceModel):
    repo = AttendanceRepository(db_session)
    use_case = ShowAttendanceUseCase(repo)
    att = use_case.execute(mock_attendance_and_retrieve.id)
    assert isinstance(att, AttendanceModel)
    assert att.id == mock_attendance_and_retrieve.id
    assert att.date == mock_attendance_and_retrieve.date
    assert att.employee_id == mock_attendance_and_retrieve.employee_id


def test_should_getall_attendances(
        db_session, mock_attendances_and_get_list: List[AttendanceModel]):
    repo = AttendanceRepository(db_session)
    use_case = GetAllAttendancesUseCase(repo)
    att_list = use_case.execute()
    assert len(att_list) == len(mock_attendances_and_get_list)


def test_should_delete_attendance(db_session, mock_attendance_and_retrieve: AttendanceModel):
    repo = AttendanceRepository(db_session)
    att_id = mock_attendance_and_retrieve.id
    use_case = DestroyAttendanceUseCase(repo)
    use_case.execute(mock_attendance_and_retrieve.id)
    with pytest.raises(HTTPException, match=f'Attendance with the id {att_id} is not available'):
        repo.show(att_id)


def test_should_create_attendance(db_session, current_user_no_pauses):
    repo = AttendanceRepository(db_session)
    new_attendance = AttendanceEntity(date=datetime(2025, 7, 9, 10, 0, 0),
                                      status=AttendanceStatus.ENTERING)
    use_case = CreateAttendanceUseCase(repo)
    attendance_model = use_case.execute(new_attendance, current_user_no_pauses)
    assert attendance_model.date == new_attendance.date
    assert attendance_model.status == AttendanceStatus(new_attendance.status)
    assert attendance_model.employee_id == current_user_no_pauses.id


@pytest.mark.skip(reason="Teste sensível")
def test_user_six_hour_can_not_pause(db_session,
                                     current_user_no_pauses,
                                     mock_attendance_and_retrieve):
    tempo_adicional = timedelta(hours=1, minutes=30)
    new_attendance = AttendanceEntity(date=mock_attendance_and_retrieve.date + tempo_adicional,
                                      status=AttendanceStatus.PAUSE_STARTING)
    with pytest.raises((HTTPException)):
        repo = AttendanceRepository(db_session)
        use_case = CreateAttendanceUseCase(repo)
        use_case.execute(new_attendance, current_user_no_pauses)
