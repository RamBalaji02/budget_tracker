from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date as date_type

from app.models.income import Income
from app.core.deps import get_current_user, get_db
from app.schemas.income import IncomeCreate
from app.services.income_service import create_income, get_income, update_income, delete_income

router = APIRouter(prefix="/income", tags=["Income"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_income(
    data: IncomeCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return create_income(db, data, user_id=user_id)


@router.get("/")
def list_income(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    incomes = db.query(Income).filter(Income.user_id == user_id).all()
    return [
        {
            "id": i.id,
            "amount": float(i.amount),
            "source": i.source,
            "date": str(i.date)
        }
        for i in incomes
    ]


@router.put("/{id}")
def edit_income(
    id: int,
    data: IncomeCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    income = update_income(db, id, data, user_id)
    if not income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Income not found"
        )
    return income


@router.delete("/{id}")
def remove_income(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    success = delete_income(db, id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Income not found"
        )
    return {"message": "Income deleted successfully"}