from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# 🔐 Config JWT (sau này đưa vào config.py)
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_LATER"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------
# MOCK USER (tạm thời)
# -----------------------------
fake_users = [
    {
        "id": "1",
        "username": "tri",
        "password_hash": pwd_context.hash("123456")
    }
]


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(username: str):
    for user in fake_users:
        if user["username"] == username:
            return user
    return None


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def login_user(username: str, password: str):
    user = get_user_by_username(username)

    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    access_token = create_access_token(
        data={"sub": user["username"]}
    )

    return access_token