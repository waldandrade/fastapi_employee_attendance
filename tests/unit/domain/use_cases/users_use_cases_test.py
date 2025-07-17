import pytest
from app.commons.enums import ScheduleMethod
from app.domain.entities.users import User
from app.domain.use_cases.user.create_user import CreateUserUseCase
from app.domain.use_cases.user.getall_users import GetAllUsersUseCase
from app.domain.use_cases.user.profile_user import ProfileUserUseCase
from app.domain.use_cases.user.show_user import ShowUserUseCase
from app.infra.db.repositories.users_repository import UserRepository
from app.infra.db.models.users import User as UserModel


@pytest.fixture(scope='function')
def repo(db_session):
    return UserRepository(db_session)


def test_should_create_user(repo):
    new_user = User(
        email='test2@test.com',
        name='Teste user',
        password='123456',
        schedule_method=ScheduleMethod.SIX_HOURS_WITHOUT_BREAK)
    use_case = CreateUserUseCase(repo)
    att = use_case.execute(new_user)
    assert isinstance(att, UserModel)
    assert att.email == new_user.email
    assert att.is_superuser == new_user.is_superuser
    assert att.schedule_method.value == new_user.schedule_method
    assert att.name == new_user.name


def test_should_get_user_by_id(repo, current_user_no_pauses):
    use_case = ShowUserUseCase(repo)
    att = use_case.execute(current_user_no_pauses.id)
    assert isinstance(att, UserModel)
    assert att.id == current_user_no_pauses.id
    assert att.name == current_user_no_pauses.name
    assert att.email == current_user_no_pauses.email
    assert att.is_superuser == current_user_no_pauses.is_superuser
    assert att.schedule_method.value == current_user_no_pauses.schedule_method.value


def test_should_get_user_by_email(repo, current_user_no_pauses):
    use_case = ProfileUserUseCase(repo)
    att = use_case.execute(current_user_no_pauses.email)
    assert isinstance(att, UserModel)
    assert att.id == current_user_no_pauses.id
    assert att.name == current_user_no_pauses.name
    assert att.email == current_user_no_pauses.email
    assert att.is_superuser == current_user_no_pauses.is_superuser
    assert att.schedule_method.value == current_user_no_pauses.schedule_method.value


def test_should_getall_users(repo, mocked_users):
    use_case = GetAllUsersUseCase(repo)
    att_list = use_case.execute()
    assert len(att_list) == len(mocked_users)
