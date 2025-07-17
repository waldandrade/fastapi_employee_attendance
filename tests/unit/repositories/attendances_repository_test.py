from datetime import datetime
from typing import List
import pytest
from fastapi.exceptions import HTTPException
from app.infra.db.models.attendances import Attendance as AttendanceModel
from app.infra.db.repositories.attendances_repository import AttendanceRepository
from app.domain.entities.attendances import Attendance as AttendanceEntity
from app.commons.enums import AttendanceStatus


@pytest.fixture(scope='function')
def repo(db_session):
    return AttendanceRepository(db_session)


def test_should_get_attendance_by_id(
        repo, mock_attendance_and_retrieve: AttendanceModel):
    att = repo.show(mock_attendance_and_retrieve.id)
    assert isinstance(att, AttendanceModel)
    assert att.id == mock_attendance_and_retrieve.id
    assert att.date == mock_attendance_and_retrieve.date
    assert att.employee_id == mock_attendance_and_retrieve.employee_id


def test_should_getall_attendances(
        repo, mock_attendances_and_get_list: List[AttendanceModel]):
    att_list = repo.get_all()
    assert len(att_list) == len(mock_attendances_and_get_list)


def test_should_delete_attendance(repo, mock_attendance_and_retrieve: AttendanceModel):
    att_id = mock_attendance_and_retrieve.id
    repo.destroy(mock_attendance_and_retrieve.id)
    with pytest.raises(HTTPException, match=f'Attendance with the id {att_id} is not available'):
        repo.show(att_id)


def test_should_create_attendance(repo, current_user_no_pauses):
    new_attendance = AttendanceEntity(date=datetime(2025, 7, 9, 10, 0, 0),
                                      status=AttendanceStatus.ENTERING)
    attendance_model = repo.create(new_attendance, current_user_no_pauses)
    assert attendance_model.date == new_attendance.date
    assert attendance_model.status == AttendanceStatus(new_attendance.status)
    assert attendance_model.employee_id == current_user_no_pauses.id
