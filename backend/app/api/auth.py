from fastapi import APIRouter
from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import create_token

router = APIRouter()
db = SessionLocal()

@router.post("/login")
def login(data: dict):

    user = db.query(User).filter(
        User.username == data["username"],
        User.password == data["password"]
    ).first()

    if not user:
        return {"error": "invalid credentials"}

    token = create_token({"user_id": user.id})

    return {
        "access_token": token,
        "user_id": user.id
    }