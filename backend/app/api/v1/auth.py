from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, LoginResponse, MessageResponse
from app.services.auth_service import login_user, create_user, get_user_by_username
from app.db.deps import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# REGISTER
# =========================
@router.post("/register", response_model=MessageResponse)
def register(request: LoginRequest, db: Session = Depends(get_db)):

    # Kiểm tra username đã tồn tại chưa
    existing_user = get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    user = create_user(db, request.username, request.password)

    return MessageResponse(
        message=f"User created successfully (id={user.id})"
    )


# =========================
# LOGIN
# =========================
@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):

    token = login_user(db, request.username, request.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return LoginResponse(access_token=token)


# =========================
# LOGOUT
# =========================
@router.post("/logout", response_model=MessageResponse)
def logout():
    # JWT là stateless → client chỉ cần xóa token
    return MessageResponse(message="Logout successful")