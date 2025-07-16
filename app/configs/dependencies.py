from fastapi import Request
from sqlalchemy.orm import Session


def get_db(request: Request) -> Session:
    return request.app.state.db_session
