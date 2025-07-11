import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.database import Base
from app.schemas import User, ScheduleMethod, AttendanceStatus
from app.repositories import user
from datetime import datetime
from app.models import Attendance


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    yield session
    session.rollback()  # Rollback changes after each test
    session.close()


@pytest.fixture
def current_user(db_session):
    new_user = User(email="test@test.com", name="Waldney Souza de Andrade",
                    password='123456', schedule_method=ScheduleMethod.EIGHT_HOURS_WITH_BREAK)
    return user.create(new_user, db_session)


@pytest.fixture
def mock_attendances_and_get_recent(db_session, current_user):
    # Entradas dia 9/7
    db_session.add(Attendance(date=datetime(2025, 7, 9, 10, 0, 0),
                   status=AttendanceStatus.ENTERING, employee_id=current_user.id))
    db_session.add(Attendance(date=datetime(2025, 7, 9, 11, 30, 0),
                   status=AttendanceStatus.EXITING, employee_id=current_user.id))
    db_session.add(Attendance(date=datetime(2025, 7, 9, 9, 0, 0),
                   status=AttendanceStatus.ENTERING, employee_id=current_user.id))
    db_session.add(Attendance(date=datetime(2025, 7, 9, 10, 0, 0),
                   status=AttendanceStatus.EXITING, employee_id=current_user.id))

    # Entradas dia 10/7
    db_session.add(Attendance(date=datetime(2025, 7, 10, 8, 0, 0),
                   status=AttendanceStatus.ENTERING, employee_id=current_user.id))
    db_session.add(Attendance(date=datetime(2025, 7, 9, 9, 45, 0),
                   status=AttendanceStatus.EXITING, employee_id=current_user.id))
    recent_attendance = Attendance(date=datetime(2025, 7, 9, 10, 0, 0),
                                   status=AttendanceStatus.ENTERING, employee_id=current_user.id)
    db_session.add(Attendance(date=recent_attendance,
                   status=AttendanceStatus.ENTERING, employee_id=current_user.id))
    return recent_attendance


@pytest.fixture
def current_user_no_pauses(db_session):
    new_user = User(email="test@test.com", name="Waldney Souza de Andrade",
                    password='123456', schedule_method=ScheduleMethod.SIX_HOURS_WITHOUT_BREAK)
    return user.create(new_user, db_session)


@pytest.fixture
def mock_attendance_and_retrieve(db_session, current_user_no_pauses):
    # Entradas dia 9/7
    new_attendance = Attendance(date=datetime(2025, 7, 9, 10, 0, 0),
                                status=AttendanceStatus.ENTERING, employee_id=current_user_no_pauses.id)
    db_session.add(new_attendance)
    return new_attendance
