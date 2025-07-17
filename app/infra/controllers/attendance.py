from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.configs.dependencies import get_db
from app.lib import oauth2
from app.domain.use_cases.attendance.create_attendance import CreateAttendanceUseCase
from app.domain.use_cases.attendance.destroy_attendance import DestroyAttendanceUseCase
from app.domain.use_cases.attendance.getall_attendances import GetAllAttendancesUseCase
from app.domain.use_cases.attendance.show_attendance import ShowAttendanceUseCase
from app.domain.use_cases.attendance.update_attendance import UpdateAttendanceUseCase
from app.infra.db.repositories.attendances_repository import AttendanceRepository
from app.domain.entities.attendances import ShowAttendance, Attendance as AttendanceEntity
from app.domain.entities.users import User as UserEntity

router = APIRouter(
    prefix="/attendance",
    tags=['Attendances']
)


def get_repository(db: Session = Depends(get_db)):
    return AttendanceRepository(db)


@router.get('/', response_model=List[ShowAttendance])
def get_all(repo: AttendanceRepository = Depends(get_repository),
            _: UserEntity = Depends(oauth2.get_current_user)):
    use_case = GetAllAttendancesUseCase(repo)
    return use_case.execute()


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create(request: AttendanceEntity,
           repo: AttendanceRepository = Depends(get_repository),
           current_user: UserEntity = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with the email {current_user.email} is not available")
    use_case = CreateAttendanceUseCase(repo)
    return use_case.execute(request, current_user)


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(item_id: int,
            repo: AttendanceRepository = Depends(get_repository),
            _=Depends(oauth2.get_current_user)):
    use_case = DestroyAttendanceUseCase(repo)
    return use_case.execute(item_id)


@router.put('/{item_id}', status_code=status.HTTP_202_ACCEPTED)
def update(item_id: int,
           request: AttendanceEntity,
           repo: AttendanceRepository = Depends(get_repository),
           _=Depends(oauth2.get_current_user)):
    use_case = UpdateAttendanceUseCase(repo)
    return use_case.execute(item_id, request)


@router.get('/{item_id}', status_code=200, response_model=ShowAttendance)
def show(item_id: int,
         repo: AttendanceRepository = Depends(get_repository),
         _=Depends(oauth2.get_current_user)):
    use_case = ShowAttendanceUseCase(repo)
    return use_case.execute(item_id)
