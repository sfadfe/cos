from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from config.db import get_db
from services.auth_service import create_user, login_user
from services.jwt_service import create_access_token
from fastapi.responses import JSONResponse, Response
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.post("/signup")
def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(user_create, db)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    response = JSONResponse(
        content={"message": "User created successfully"},
        status_code=201,
    )
    access_token = create_access_token(user.id, user.username, user.is_admin)
    response.set_cookie(
        key="access_token",
        value=access_token,
        secure=True,
    )
    return response


@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    response = JSONResponse(
        content={"message": "User logged in successfully"},
        status_code=200,
    )
    user = login_user(user_login, db)
    access_token = create_access_token(user.id, user.username, user.is_admin)
    response.set_cookie(
        key="access_token",
        value=access_token,
        secure=True,
    )
    return response


@router.get("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return response