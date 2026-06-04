from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.category import CategoryCreate
from app.services.category_service import create_category, get_categories
from app.core.deps import get_current_user, get_db

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/")
def add_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return create_category(db, data, user_id=user_id)


@router.get("/")
def list_categories(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return get_categories(db, user_id=user_id)