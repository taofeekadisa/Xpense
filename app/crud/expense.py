from typing import Annotated
import uuid
from fastapi import Body, status, HTTPException

from app.db.data import expenses, users
from app.schemas.expense import ExpenseModel, ExpenseParams

from fastapi.encoders import jsonable_encoder
from app.db.data import expenses, users
from app.schemas.expense import ExpenseModel, ExpenseParams, ExpenseUpdate


class ExpenseCrud():
    #Create expense endpoint
    @staticmethod
    def create_expense(user_id:str, expense:ExpenseModel):
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
    
    #Get all users expenses    
    @staticmethod
    def get_expenses(expense_params: ExpenseParams):
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
            else:    
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No match found")
            
        # Return all filtered expenses
        return filtered_expenses
    
   
    #Get all user expenses
    @staticmethod
    def user_expenses(user_id:str, expense_params: ExpenseParams):

        # Iterate over each user and their expenses
        for Id, expense_dict in expenses.items():
            if user_id == Id:
                
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
                    else:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No match found")  
                        
            return user_filtered_expenses

    
    #Get user expense
    @staticmethod
    def user_expense(user_id:str, expense_id:str):
        if user_id in expenses:
            expense_dict = expenses[user_id]
            
            if expense_id in expense_dict:
                expense = expense_dict[expense_id]
                
                return expense
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="expense id not found")
         
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user id not found")           
            
            
    #Update user expense
    @staticmethod

    def update_expense():
        pass
    
    #Delete user expense
    @staticmethod
    def delete_expense():
        pass
    @staticmethod
    def update_expense(user_id:str, expense_id:str, expense:ExpenseUpdate):
        if user_id in expenses:
            expense_dict = expenses[user_id]
            
            if expense_id in expense_dict:
                stored_expense = expense_dict[expense_id]
                stored_expense_model = ExpenseUpdate(**stored_expense)
                update_expense = expense.model_dump(exclude_unset=True)
                updated_expense = stored_expense_model.model_copy(update=update_expense)
                expense_dict[expense_id] = jsonable_encoder( updated_expense)
                
                return updated_expense
            
            return None
        return None
    
    #Delete user expense
    @staticmethod
    def delete_expense(user_id: str, expense_id: str):
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

expense_crud = ExpenseCrud()


