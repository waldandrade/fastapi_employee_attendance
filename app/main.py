from fastapi import Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from functools import lru_cache
from fastapi import FastAPI
from app import models
from app.database import engine, init_db, get_db
from app.routers import user, auth, attendance
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


@asynccontextmanager
async def lifespan(app=FastAPI):
    with Session(engine) as db:
        init_db(db)
        yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(attendance.router)
