from fastapi import FastAPI
from .database import Base, engine
from .users.routing import router as user_router

Base.metadata.create_all(bind=engine)  # create tables

app = FastAPI()

app.include_router(user_router, prefix="/api/auth", tags=["users"])