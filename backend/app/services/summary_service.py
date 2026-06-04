from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.models.expense import Expense
from app.models.income import Income

def get_summary(db: Session, user_id: int, month: str = None):
    expense_query = db.query(Expense).filter(Expense.user_id == user_id)
    income_query = db.query(Income).filter(Income.user_id == user_id)
    
    if month:
        try:
            year, m = map(int, month.split("-"))
            expense_query = expense_query.filter(
                extract('year', Expense.exp_date) == year,
                extract('month', Expense.exp_date) == m
            )
            income_query = income_query.filter(
                extract('year', Income.date) == year,
                extract('month', Income.date) == m
            )
        except (ValueError, AttributeError):
            pass
            
    total_income = sum(float(i.amount or 0) for i in income_query.all())
    total_expense = sum(float(e.amount or 0) for e in expense_query.all())
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }