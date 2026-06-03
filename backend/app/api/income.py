from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.income import Income
from app.core.deps import get_current_user

router = APIRouter(prefix="/income", tags=["Income"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_income(data: dict,
               db: Session = Depends(get_db),
               user_id: int = Depends(get_current_user)):

    new_income = Income(
        amount=data["amount"],
        source=data["source"],
        date=data["inc_date"],
        user_id=user_id
    )

    db.add(new_income)
    db.commit()

    return {"message": "Income added successfully"}


@router.get("/")
def get_income(db: Session = Depends(get_db),
               user_id: int = Depends(get_current_user)):

    incomes = db.query(Income).filter(
        Income.user_id == user_id
    ).all()

    return [
        {
            "id": i.id,
            "amount": float(i.amount),
            "source": i.source,
            "date": str(i.date)
        }
        for i in incomes
    ]