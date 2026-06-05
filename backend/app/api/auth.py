from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.deps import get_db
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_token

router = APIRouter()

@router.post("/register")
def register(data: dict, db: Session = Depends(get_db)):

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"detail": "Missing fields"}

    user = db.query(User).filter(User.username == username).first()

    if user:
        return {"detail": "User already exists"}

    new_user = User(
        username=username,
        password=password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "registered"}


@router.post("/login")
def login(data: UserCreate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token({"user_id": user.id})

    return {"access_token": token}