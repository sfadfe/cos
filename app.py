from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers import auth, admin
from models.user import Base
from config.db import engine
from fastapi.responses import RedirectResponse
from services.jwt_service import create_access_token
from config.db import SessionLocal
from schemas.user import UserLogin
from services.auth_service import login_user
from services.jwt_service import verify_access_token

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def home(request: Request):
    access_token = request.cookies.get("access_token")
    context = {"request": request, "user": None, "username": None}

    if access_token:
        try:
            user_data = verify_access_token(access_token)
            context["user"] = user_data
            context["username"] = user_data.username
        except Exception:
            response = RedirectResponse("/", status_code=302)
            response.delete_cookie("access_token")
            return response
            
    return templates.TemplateResponse("index.html", context)

@app.get("/about")
async def about(request: Request):
    access_token = request.cookies.get("access_token")
    context = {"request": request, "user": None, "username": None}
    if access_token:
        try:
            user_data = verify_access_token(access_token)
            context["user"] = user_data
            context["username"] = user_data.username
        except Exception:
            response = RedirectResponse("/", status_code=302)
            response.delete_cookie("access_token")
            return response
    return templates.TemplateResponse("about.html", context)

@app.get("/auth/signin")
async def signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.post("/auth/signin")
async def signin_post(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    db = SessionLocal()
    user = login_user(UserLogin(username=username, password=password), db)

    access_token = create_access_token(
        user_id=str(user.id),
        username=user.username,
        is_admin=user.is_admin
    )

    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/profile")
async def Profile(request: Request):
    access_token = request.cookies.get("access_token")
    context = {"request": request, "user": None, "username": None}

    if access_token:
        try:
            user_data = verify_access_token(access_token)
            context["user"] = user_data
            context["username"] = user_data.username
        except Exception:
            response = RedirectResponse("/", status_code=302)
            response.delete_cookie("access_token")
            return response
            
    return templates.TemplateResponse("profile.html", context)

@app.get("/admin")
async def Admin(request: Request):
    access_token = request.cookies.get("access_token")
    context = {"request": request, "user": None, "username": None}
    if access_token:
        try:
            pass
        except:
            pass
    