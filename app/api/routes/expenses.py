import uuid
from fastapi import APIRouter, Body, HTTPException, Header, Query, status, Form
from typing import Annotated, Optional, Union
from app.api.routes import users, expenses
from app.schemas.expense import ExpenseModel, ExpenseParams
from app.db.data import users, expenses


expense_router =  APIRouter()


@expense_router.post("/v1/users/{user_id}/expenses", status_code=status.HTTP_201_CREATED, tags=["Expenses"])
def create_expense(user_id:str, expense:Annotated[ExpenseModel,Body()]):
    if user_id in users:
        expense_id = str(uuid.uuid4())
        expense_dict = expense.model_dump()
        if user_id not in expenses:
            expenses[user_id] = {}
            expenses[user_id][expense_id] = expense_dict
        expenses[user_id][expense_id] = expense_dict
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Expense created succesfully", "data":expense_dict}


@expense_router.get("/v1/expenses", status_code=status.HTTP_200_OK, tags=["Expenses"])
def get_expenses(expense_params: Annotated[ExpenseParams, Query()]):
    filtered_expenses = {}

    # Iterate over each user and their expenses
    for user_id, expense_dict in expenses.items():
        user_filtered_expenses = {}

        for expense_id, expense in expense_dict.items():
            match = True

            # Check each field in the query parameters
            for field in expense_params.model_fields_set:
                param_value = getattr(expense_params, field)
                
                # Skip check if the query parameter is not set
                if param_value is not None:
                    # Check if the field in the expense does not match the query parameter
                    if expense.get(field) != param_value:
                        match = False
                        break  # Stop checking further fields if there's a mismatch

            if match:
                user_filtered_expenses[expense_id] = expense

        # Only add user to filtered_expenses if there are matching expenses
        if user_filtered_expenses:
            filtered_expenses[user_id] = user_filtered_expenses

    # Return all filtered expenses
    return filtered_expenses

@expense_router.get("/v1/users/{user_id}/expenses", status_code=status.HTTP_200_OK, tags=["Expenses"])
def user_expenses():
    pass

@expense_router.get("/v1/users/{user_id}/expenses/{expense_id}", status_code=status.HTTP_200_OK, tags=["Expenses"])
def user_expense():
    pass

@expense_router.put("/v1/users/{user_id}/expenses/{expense_id}", status_code=status.HTTP_201_CREATED, tags=["Expenses"])
def update_expense():
    pass

@expense_router.delete("/v1/users/{user_id}/expenses/{expense_id}",status_code=status.HTTP_204_NO_CONTENT, tags=["Expenses"])
def delete_expense():
    pass
