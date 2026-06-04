from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_db
from app.services.summary_service import get_summary

router = APIRouter(tags=["Summary"])


@router.get("/summary")
def summary(
    month: str = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    try:
        return get_summary(db, user_id, month=month)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )