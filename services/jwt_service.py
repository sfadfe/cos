from jose import ExpiredSignatureError, JWTError, jwt
from datetime import datetime, timedelta, timezone
from config.settings import settings
from fastapi import HTTPException, Cookie
from schemas.user import UserResponse


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(user_id: str, username: str, is_admin: bool) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "is_admin": is_admin,
        "exp": _utc_now() + timedelta(hours=settings.JWT_ACCESS_EXPIRES_IN_HOURS),
    }
    return jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def verify_access_token(token: str) -> UserResponse:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return UserResponse(
            id=payload["sub"],
            username=payload["username"],
            is_admin=payload["is_admin"],
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
def get_current_user_from_token(access_token: str = Cookie(None)) -> UserResponse:
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return verify_access_token(access_token)