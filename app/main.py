from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infra.controllers import attendance, user, auth
from app.infra.db.settings.connections import DBConnectionHandler
from app.initial_data import init_db

db_connection_handle = DBConnectionHandler()
engine = db_connection_handle.get_engine()


@asynccontextmanager
async def lifespan():
    with Session(engine) as db:
        init_db(db)
        yield

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
