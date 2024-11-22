import uuid
from fastapi import APIRouter, Body, HTTPException, Header, Query, status, Form
from typing import Annotated, Optional, Union
from app.api.routes import users, expenses
from app.schemas.expense import ExpenseModel, ExpenseParams, ExpenseUpdate
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
def user_expense(user_id:str, expense_id:str):
    expense = expense_crud.user_expense(user_id, expense_id)
    
    return expense

@expense_router.put("/users/{user_id}/expenses/{expense_id}", status_code=status.HTTP_201_CREATED)
<<<<<<< HEAD
def update_expense():
    pass

@expense_router.delete("/users/{user_id}/expenses/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_expense():
    pass
=======
def update_expense(user_id:str, expense_id:str, expense:ExpenseUpdate):
    updated_expense = expense_crud.update_expense(user_id, expense_id, expense)
    
    if not updated_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user_id and expense_id not found")
    
    return updated_expense

@expense_router.delete("/users/{user_id}/expenses/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(user_id:str, expense_id:str):
    if user_id not in expenses:
            return {"success": False, "message": f"User ID {user_id} not found."}, 404

    expense_dict = expenses[user_id]
    if expense_id not in expense_dict:
        return {
            "success": False,
            "message": f"Expense ID {expense_id} not found for User ID {user_id}.",
        }, 404

    expense_dict.pop(expense_id)
    return {"success": True, "message": "Deleted successfully."}, 200 
    

    
  
    

        
>>>>>>> 40ee1b3030d940c28f6f7b92c1e102e1239c7997
