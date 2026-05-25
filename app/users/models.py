import uuid
from sqlalchemy import Column, Integer, String, Boolean, true
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)


    