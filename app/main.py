from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import user, auth, attendance
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
