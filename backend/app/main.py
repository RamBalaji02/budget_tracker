from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.expense import router as expense_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(expense_router)