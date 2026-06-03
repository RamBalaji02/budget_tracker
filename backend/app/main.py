from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.expense import router as expense_router
from app.api.income import router as income_router
from app.api.summary import router as summary_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(expense_router)
app.include_router(income_router)
app.include_router(summary_router)


@app.get("/health")
def health():
    return {"status": "ok"}