from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from app.db.database import SessionLocal

security = HTTPBearer()

SECRET_KEY = "secret123"
ALGORITHM = "HS256"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token=Depends(security)):

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]

    except:
        raise HTTPException(status_code=401, detail="Not authenticated")