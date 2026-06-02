from pydantic import BaseModel
from datetime import date

class IncomeCreate(BaseModel):
    amount: float
    source: str
    date: date