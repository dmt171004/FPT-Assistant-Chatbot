from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest, LoginResponse, MessageResponse
from app.services.auth_service import login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    token = login_user(request.username, request.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return LoginResponse(access_token=token)


@router.post("/logout", response_model=MessageResponse)
def logout():
    # Vì dùng JWT stateless nên logout chỉ cần phía client xóa token
    return MessageResponse(message="Logout successful")