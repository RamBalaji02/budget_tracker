from fastapi import APIRouter
from app.db.database import SessionLocal
from app.models.user import User

router = APIRouter()

db = SessionLocal()

@router.post("/register")
def register(data: dict):

    try:
        existing_user = db.query(User).filter(
            User.username == data["username"]
        ).first()

        if existing_user:
            return {"error": "username already exists"}

        user = User(
            username=data["username"],
            password=data["password"]
        )

        db.add(user)
        db.commit()

        return {"message": "registered successfully"}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}


@router.post("/login")
def login(data: dict):

    try:
        user = db.query(User).filter(
            User.username == data["username"],
            User.password == data["password"]
        ).first()

        if not user:
            return {"error": "invalid credentials"}

        return {
            "message": "login success",
            "user_id": user.id
        }

    except Exception as e:
        return {"error": str(e)}