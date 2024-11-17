from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date, time
from app.utils.current_time import current_time


class ExpenseModel(BaseModel):
    title:str
    category:str
    description:str
    amount:float
    created_at:current_time

class ExpenseParams(BaseModel):
    model_config = {"extra": "forbid"}
    
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float | int] = None
    created_at:Optional[str] = None