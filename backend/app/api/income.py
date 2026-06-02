from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.db.database import SessionLocal
from app.models.income import Income

router = APIRouter(prefix="/income", tags=["Income"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/")
def create_income(amount: float, source: str, inc_date: date, db: Session = Depends(get_db)):

    income = Income(
        amount=amount,
        source=source,
        date=inc_date
    )

    db.add(income)
    db.commit()
    db.refresh(income)

    return income


@router.get("/")
def get_income(db: Session = Depends(get_db)):
    return db.query(Income).all()