from curses import color_content
from fastapi import Depends, FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from pydantic.generics import GenericModel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse
from app.schemes import SuccessResponse, ErrorResponse
from .models import User
from .scheme import (UserModel, UserCreate, UserLogin)
from typing import List, Generic
from app.passwords import hash_password, verify_password
from app.dependencies import get_db

router = InferringRouter()

@cbv(router)
class UserView:
    db: Session = Depends(get_db)

    @router.get('/')
    def get_users_list(self):
        users = self.db.query(User).all()
        return SuccessResponse[List[UserModel]](
            message="User data retrieved successfully",
            data=users
        )
    
    @router.post('/register')
    def create_user(self, user:UserCreate):
        existing_user = self.db.query(User).filter(User.email == user.email).first()
        if existing_user:
            return JSONResponse(status_code=400,
            content=ErrorResponse(
                error="User with this email already exists."
            ).model_dump())
        if user.password != user.confirm_password:
            raise HTTPException(status_code=400,
            detail={"error":"Both password field must match with eachother"})
        password = hash_password(user.password)
        new_user = User(
            name=user.name,
            email=user.email,
            password = password
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return SuccessResponse[UserModel](
            message="User Registered Successfully",
            data = new_user
        )
    
    @router.get('/{email}')
    def get_user_by_email(self, email:str):
        existing_user = self.db.query(User).filter(User.email == email).first()
        if not existing_user:
            return JSONResponse(status_code=404,
            content=ErrorResponse(
                error="User with this email doesnot exists."
            ).model_dump())
        return SuccessResponse[UserModel](
            message="User Retrieved Successfully",
            data = existing_user
        )
    
    @router.post('/login')
    def get_user_login(self, user:UserLogin):
        existing_user = self.db.query(User).filter(User.email == user.email).first()
        if not existing_user:
            return JSONResponse(status_code=404,
                content=ErrorResponse(
                    error="User with this email doesnot exists."
                ).model_dump())
        if not verify_password(user.password, existing_user.password):
            return JSONResponse(status_code=400,
                content=ErrorResponse(
                    error="Invalid Password Received."
                ).model_dump())
        
        return JSONResponse(status_code=200,
            content=SuccessResponse[UserModel](
                message="User Logged in successfully",
                data = existing_user
            ).model_dump())
        
