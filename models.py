from pydantic import BaseModel
from typing import Optional
from datetime import date

class Transaction(BaseModel):
    id: Optional[int] = None
    amount: float
    category: str
    description: Optional[str] = ""
    date: date
    type: str  # "income" или "expense"