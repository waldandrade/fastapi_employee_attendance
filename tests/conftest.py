from datetime import datetime
from typing import List
import pytest
from sqlalchemy.orm import Session
from app.infra.db.settings.connections import DBConnectionHandler
from app.infra.db.repositories.users_repository import UserRepository
from app.infra.db.models.attendances import Attendance as AttendanceModel
from app.infra.db.models.users import User as UserModel
from app.infra.db.settings.base import Base
from app.domain.entities.users import User as UserEntity
from app.commons.enums import ScheduleMethod, AttendanceStatus


@pytest.fixture(scope='function')
def db_session():
    with DBConnectionHandler(scoped=True) as database:
        engine = database.get_engine()
        Base.metadata.create_all(engine)
        session = database.session
        session.expunge_all()
        yield session
        session.rollback()  # Rollback changes after each test


@pytest.fixture(scope='function')
def current_user(db_session):
    new_user = UserEntity(email="test3@test.com", name="Waldney Souza de Andrade",
                          password='123456', schedule_method=ScheduleMethod.EIGHT_HOURS_WITH_BREAK)
    users_repository = UserRepository(db_session)
    return users_repository.create(new_user)


@pytest.fixture(scope='function')
def mock_attendances_and_get_list(db_session: Session, current_user) -> List[AttendanceModel]:
    new_attendances = [
        AttendanceModel(date=datetime(2025, 7, 9, 10, 0, 0),
                        status=AttendanceStatus.ENTERING, employee_id=current_user.id),
        AttendanceModel(date=datetime(2025, 7, 9, 11, 30, 0),
                        status=AttendanceStatus.EXITING, employee_id=current_user.id),
        AttendanceModel(date=datetime(2025, 7, 9, 9, 0, 0),
                        status=AttendanceStatus.ENTERING, employee_id=current_user.id),
        AttendanceModel(date=datetime(2025, 7, 9, 10, 0, 0),
                        status=AttendanceStatus.EXITING, employee_id=current_user.id),
        AttendanceModel(date=datetime(2025, 7, 10, 8, 0, 0),
                        status=AttendanceStatus.ENTERING, employee_id=current_user.id),
        AttendanceModel(date=datetime(2025, 7, 9, 9, 45, 0),
                        status=AttendanceStatus.EXITING, employee_id=current_user.id),
        AttendanceModel(date=datetime(2025, 7, 9, 10, 0, 0),
                        status=AttendanceStatus.ENTERING,
                        employee_id=current_user.id)]
    db_session.add_all(new_attendances)
    db_session.commit()
    return new_attendances


@pytest.fixture(scope='function')
def current_user_no_pauses(db_session):
    new_user = UserEntity(email="test3@test.com", name="Waldney Souza de Andrade",
                          password='123456', schedule_method=ScheduleMethod.SIX_HOURS_WITHOUT_BREAK)
    users_repository = UserRepository(db_session)
    return users_repository.create(new_user)


@pytest.fixture(scope='function')
def mock_attendance_and_retrieve(db_session, current_user_no_pauses) -> AttendanceModel:
    # Entradas dia 9/7
    new_attendance = AttendanceModel(date=datetime(2025, 7, 9, 10, 0, 0),
                                     status=AttendanceStatus.ENTERING,
                                     employee_id=current_user_no_pauses.id)
    db_session.add(new_attendance)
    db_session.commit()
    return new_attendance


@pytest.fixture(scope='function')
def mocked_users(db_session):
    users = [
        UserModel(email="test1@test.com", name="Waldney Souza de Andrade 1",
                  password='123456', schedule_method=ScheduleMethod.SIX_HOURS_WITHOUT_BREAK),
        UserModel(email="test2@test.com", name="Waldney Souza de Andrade 2",
                  password='123456', schedule_method=ScheduleMethod.EIGHT_HOURS_WITH_BREAK),
        UserModel(email="test3@test.com", name="Waldney Souza de Andrade 3",
                  password='123456', schedule_method=ScheduleMethod.SIX_HOURS_WITHOUT_BREAK),
        UserModel(email="test4@test.com", name="Waldney Souza de Andrade 4",
                  password='123456', schedule_method=ScheduleMethod.EIGHT_HOURS_WITH_BREAK)
    ]
    db_session.add_all(users)
    db_session.commit()
    return users
