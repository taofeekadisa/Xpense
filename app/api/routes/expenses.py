import uuid
from fastapi import APIRouter, Body, HTTPException, Header, Query, status, Form
from typing import Annotated, Optional, Union
from app.api.routes import users, expenses
from app.schemas.expense import ExpenseModel, ExpenseParams
from app.db.data import users, expenses
from app.crud.expense import expense_crud


expense_router =  APIRouter()


@expense_router.post("/users/{user_id}/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(user_id:str, expense:Annotated[ExpenseModel,Body()]):
    new_expense = expense_crud.create_expense(user_id, expense)
    
    return new_expense

@expense_router.get("/expenses", status_code=status.HTTP_200_OK)
def get_expenses(expense_params: Annotated[ExpenseParams, Query()]):
    filtered_expenses = expense_crud.get_expenses(expense_params)
    
    return filtered_expenses
    

@expense_router.get("/users/{user_id}/expenses", status_code=status.HTTP_200_OK)
def user_expenses(user_id:str, expense_params: Annotated[ExpenseParams, Query()]):
    user_expenses = expense_crud.user_expenses(user_id, expense_params)
    
    return user_expenses

@expense_router.get("/users/{user_id}/expenses/{expense_id}", status_code=status.HTTP_200_OK)
def user_expense():
    pass

@expense_router.put("/users/{user_id}/expenses/{expense_id}", status_code=status.HTTP_201_CREATED)
def update_expense():
    pass

@expense_router.delete("/users/{user_id}/expenses/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_expense():
    pass
