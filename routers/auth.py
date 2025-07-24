from fastapi import APIRouter, Cookie, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from config.db import get_db
from services.auth_service import create_user, login_user
from services.jwt_service import create_access_token, verify_access_token
from fastapi.responses import JSONResponse, Response, RedirectResponse
from sqlalchemy.exc import IntegrityError

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/signup")
def get_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    try:
        create_user(user_create, db)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User with this email or username already exists")
    
    return RedirectResponse(url="/auth/signin", status_code=303)

@router.post("/signin")
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
        httponly=True
    )
    return response


@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token")
    return response

@router.get("/profile", summary="Get user profile page")
def get_profile_page(request: Request, access_token: str = Cookie(None)):    
    if not access_token:
        return RedirectResponse(url="/", status_code=302)
    try:
        user = verify_access_token(access_token)
        return templates.TemplateResponse("profile.html", {"request": request, "user": user})
    except HTTPException:
        return RedirectResponse(url="/", status_code=302)