from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from services.jwt_service import get_current_user_from_token
from config.db import get_db
from models.user import User
from sqlalchemy.orm import Session

router = APIRouter()

def admin_required(user=Depends(get_current_user_from_token)):
    if not user or not getattr(user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("/", response_class=HTMLResponse)
def admin_dashboard(request: Request, user=Depends(admin_required)):
    return request.app.state.templates.TemplateResponse(
        "admin.html", {"request": request, "user": user}
    )

@router.get("/users", response_class=HTMLResponse)
def admin_user_list(request: Request, user=Depends(admin_required), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return request.app.state.templates.TemplateResponse(
        "admin_users.html", {"request": request, "user": user, "users": users}
    )