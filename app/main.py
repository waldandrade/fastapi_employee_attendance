from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infra.controllers import attendance, user, auth
from app.infra.db.settings.base import Base
from app.initial_data import init_db
from app.infra.db.settings.connections import DBConnectionHandler


@asynccontextmanager
async def lifespan(_app: FastAPI):
    with DBConnectionHandler() as database:
        engine = database.get_engine()
        Base.metadata.create_all(engine)
        db_session = database.session
        app.state.db_session = db_session
        init_db(db_session)
        yield
        db_session.close()

app = FastAPI(title='Employee Attendance', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(attendance.router)
