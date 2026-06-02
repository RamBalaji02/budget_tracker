from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas.category import CategoryCreate
from app.services.category_service import create_category, get_categories
from app.core.deps import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return create_category(db, data, user_id=1)


@router.get("/")
def list_categories(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return get_categories(db, user_id=1)