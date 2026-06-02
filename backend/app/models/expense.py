from sqlalchemy import Column, Integer, Float, String, Date
from app.db.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    category = Column(String)
    note = Column(String)
    exp_date = Column(Date)
    user_id = Column(Integer)