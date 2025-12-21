from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from database.db import SessionDependency
from models.User import User
from request_model.PasswordChangeRequest import PasswordChangeRequest
from utility import hash_password, validate_password, validate_token

auth_user_dependency = Annotated[dict, Depends(validate_token)]

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.put("/change_password")
async def change_password(user_password: PasswordChangeRequest, user: auth_user_dependency, session: SessionDependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to authorize")
    
    # Read user by user id
    db_user = session.get(User, user.get("id"))

    # check if db password == user_password.current_password
    db_password = db_user.password
    isSame = validate_password(hashed_password=db_password, password=user_password.current_password)

    # if False, return 400
    if not isSame:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your current password is not correct")

    # If True, update new password
    db_user.password = hash_password(user_password.new_password)
    session.add(db_user)
    session.commit()
    return {"message": "Password Changed!!!"}
