from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from database.db import SessionDependency
from models.User import User
from request_model.UserRequest import UserRequest
from response_model.UserResponse import UserResponse
from sqlmodel import select
from fastapi.security import OAuth2PasswordRequestForm
from utility import check_user_credentials, hash_password, create_jwt_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signup/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(userReq: UserRequest, session: SessionDependency):
    user = User.model_validate(userReq)

    existing_user = session.exec(select(User).where(User.email == userReq.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registerd.")
    
    user.password = hash_password(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# https://fastapi.tiangolo.com/tutorial/security/first-steps/#how-it-looks
@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDependency):
    email = form_data.username
    password = form_data.password

    # Validate credentials email and password
    authorized_user = await check_user_credentials(email, password, session)

    if not authorized_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Credentials")
    
    # JWT Token generate
    data = {
        'sub': authorized_user.email,
        'id': authorized_user.id,
        'name': authorized_user.name
    }
    token_dict = await create_jwt_token(data, timedelta(minutes=15))

    return token_dict
    

