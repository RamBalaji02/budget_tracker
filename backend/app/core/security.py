from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

def create_token(data: dict):
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + timedelta(hours=2)})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)