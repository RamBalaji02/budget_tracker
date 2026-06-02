from sqlalchemy import Column, Integer, Float, String, Date
from app.db.database import Base

class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    source = Column(String)
    date = Column(Date)
    user_id = Column(Integer)