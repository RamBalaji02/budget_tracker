from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date as date_type

from app.models.expense import Expense
from app.core.deps import get_current_user, get_db
from app.schemas.expense import ExpenseCreate
from app.services.expense_service import create_expense, get_expenses, update_expense, delete_expense

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return create_expense(db, data, user_id=user_id)


@router.get("/")
def list_expenses(
    start_date: date_type = None,
    end_date: date_type = None,
    category: str = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    query = db.query(Expense).filter(Expense.user_id == user_id)
    if start_date:
        query = query.filter(Expense.exp_date >= start_date)
    if end_date:
        query = query.filter(Expense.exp_date <= end_date)
    if category:
        query = query.filter(Expense.category == category)
        
    expenses = query.all()
    return [
        {
            "id": e.id,
            "amount": float(e.amount),
            "category": e.category,
            "note": e.note,
            "date": str(e.exp_date)
        }
        for e in expenses
    ]


@router.put("/{id}")
def edit_expense(
    id: int,
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    expense = update_expense(db, id, data, user_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense


@router.delete("/{id}")
def remove_expense(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    success = delete_expense(db, id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return {"message": "Expense deleted successfully"}