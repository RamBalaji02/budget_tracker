from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret123"
ALGORITHM = "HS256"


def get_password_hash(password: str):
    return password


def verify_password(plain, hashed):
    return plain == hashed


def create_token(data: dict):
    payload = data.copy()
    payload.update({
        "exp": datetime.utcnow() + timedelta(hours=2)
    })

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )