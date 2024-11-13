from uuid import UUID
from fastapi import Cookie, Depends, FastAPI, Body, File, Form, HTTPException, Header, Query, UploadFile, status
from datetime import date
from fastapi.security import OAuth2PasswordBearer
from data import users, expenses
from pydantic import BaseModel, Field, EmailStr, validate_email
from typing import Annotated, Optional, Union
from datetime import datetime, date, time
from time import time
import uuid



app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Address(BaseModel):
    AddressLine: list[str]
    City: str
    postal_code:str
class AccountDetails(BaseModel):
    account_name: str
    account_number: Annotated[int, Field(ge=10)]
    bank_name: str
    account_type: str
 
class User(AccountDetails):
    Id:UUID
    username: str
    email: str
    address: Address
    password: str
    created_at:datetime
    
    model_config = {
   "json_schema_extra": {
  "user": {
    "username": "Alee",
    "email": "ta@ta.com",
    "address": {
      "AddressLine": [
        "12, kenton, kilo"
      ],
      "City": "gika",
      "postal_code": "7yf=-fg"
    },
    "account_details": [
      {
        "account_name": "Alee ta",
        "account_number": 1234567890,
        "bank_name": "USB",
        "account_type": "htgfthj"
      }
    ],
    "password": "dfghtdf"
  },
  "confirm_password": "hdfg",
  "is_active": True
}  
}

class ResponseParams(User):
    account_name: str
    account_number: Annotated[int, Field(ge=10)]
    bank_name: str
    account_type: str

           
class UserLogin(BaseModel):
    username:str
    password:str
    
    model_config = {"extra": "forbid"}
  
class UserUpdate(BaseModel):
    username:str
    email:str
    updated_at:datetime
  
class UserParams(BaseModel):
    model_config = {"extra": "forbid"}
    
    job: Optional[str] = None
    age: Annotated[int, Field(description="Age of users", title="Age of users")] = None
    city: Optional[str] = None
    salary: Optional[float] = None
    experience:Optional[int] = None
    department: Optional[str] = None
    gender: Optional[str] = None

class HeaderParams(BaseModel):
    user_agent:Annotated[str,Field()] = None
    user_ip:Annotated[str,Field()] = None


class BioDocs(BaseModel):
    Id_card:bytes
    passport_page:bytes


def current_time():
    return datetime.now()


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
   

def user_auth(user: UserLogin):
    for Id, user_data in users.items():
        if user_data["password"] == user.password and (
            user.username_email == user_data["username"]
        ):
            pass
    return "Unauthorised Access" 

            
@app.post("/v1/signup", response_model=AccountDetails, response_model_exclude=["bank_name"], status_code=status.HTTP_201_CREATED, tags=["Users"])
def signup(user:User, confirm_password:Annotated[str, Body()], is_active:Annotated[bool, Body()], header_params:Annotated[HeaderParams, Header()]) -> any:
    for Id, user_data in users.items():
        if Id == user.username:
            return "Username already exit"
        for k, v in user_data.items():
            if user_data["email"] == user.email:
                return "Email already exist"
        if user.password != confirm_password:
            return "Passwords do not match"
    users[user.username] = user.model_dump()
    
    # user_data_dict = user.model_dump()
    # account_details = AccountDetails(**user_data_dict)
    return user


@app.post("/v1/Login",  tags=["Users"])
async def login(user:Annotated[UserLogin, Form()]):
    for Id, user_data in users.items():
        if user_data["password"] == user.password and (
            user.username == user_data["username"]
            or user.username == user_data["email"]
        ):
            return "Login Successful"
    return "Invalid login credentials" 


# @app.post("/v1/Login")
# async def login(username:Annotated[str, Form(title="Login username", description="Email or username of the app user")], password:Annotated[str, Form(title="User password", description="The password of the app")]) :
#     for Id, user_data in users.items():
#         if user_data["password"] == password and (
#             username == user_data["username"]
#             or username == user_data["email"]
#         ):
#             return "Login Successful"
#     return "Invalid login credentials"

@app.get("/v1/users",  tags=["Users"])
def get_users(user_params: Annotated[UserParams, Query()]):
    filtered_users = {}
    for user_id, user_profile in users.items():
        match = True
        for field in user_params.model_fields_set:
            param_value = getattr(user_params, field)
            if param_value is not None and user_profile.get(field) != param_value:
                match = False
                return {"message": "No match"}
                break
        if match:
            filtered_users[user_id] = user_profile

    return filtered_users



@app.put("/v1/users/{user_Id}",  tags=["Users"])
def update_profile(user_Id:str, update_profile:UserUpdate):
    for Id, user_data in users.items():
        if Id == user_Id:
            
            if Id == update_profile.username:
                return "Username already exit"
            for k, v in user_data.items():
                if user_data["email"] == update_profile.email:
                    return "Email already exist"
            users[update_profile.username] = users.pop(Id) 
            user_data["username"] = update_profile.username
            user_data["email"] = update_profile.email         
            return "Update Successful"
        return "User Not Found"

@app.delete("/v1/users/{user_Id}",  tags=["Users"])
def delete_profile(user_Id:str):
    for Id, user_data in users.items():
        if Id == user_Id:
            del users[Id]
            return "Account deleted"
    return "Unauthorised Access"


@app.post("/v1/users/{user_id}/expenses", status_code=status.HTTP_201_CREATED, tags=["Expenses"])
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


# @app.get("/v1/expenses", status_code=status.HTTP_200_OK, tags=["Expenses"])
# def get_expenses(expense_params:Annotated[ExpenseParams, Query()]):
#     for user_id, expense_dict in expenses.items():
#         filtered_expenses = {}
#         #for expense_id, expense in expense_dict.items():
#         match = True
#         for field in expense_params.model_fields_set:
#             param_value = getattr(expense_params, field)
#             if param_value is not None and expense_dict.get(field) != param_value:
#                 match = False
#                 return {"message": "No match"}
#                 break
#         if match:
#             filtered_expenses[user_id] = expense_dict

#     return filtered_expenses
# # return expenses

@app.get("/v1/expenses", status_code=status.HTTP_200_OK, tags=["Expenses"])
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

@app.get("/v1/users/{user_id}/expenses", status_code=status.HTTP_200_OK, tags=["Expenses"])
def user_expenses():
    pass

@app.get("/v1/users/{user_id}/expenses/{expense_id}", status_code=status.HTTP_200_OK, tags=["Expenses"])
def user_expense():
    pass

@app.put("/v1/users/{user_id}/expenses/{expense_id}", status_code=status.HTTP_201_CREATED, tags=["Expenses"])
def update_expense():
    pass

@app.delete("/v1/users/{user_id}/expenses/{expense_id}",status_code=status.HTTP_204_NO_CONTENT, tags=["Expenses"])
def delete_expense():
    pass





















 
#Example on Response Model No part of our Expense Application API
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def save_to_db(user:UserIn):
    hashed_password = fake_password_hasher(user.password)
    user_to_db = UserInDB(**user.model_dump(), hashed_password = hashed_password)
    user_to_db = UserInDB(username=user.username, hashed_password = hashed_password, email=user.email, full_name=user.full_name)
    return user_to_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = save_to_db(user_in)
    return user_saved

   

@app.post("/files/")
async def create_file(docs: Annotated[list[bytes], File()]):
    for doc in docs:

        return {"message": "Upload Succesful",
                "data":{"doc_size": f"{len(doc)/1000} KB"
                        }
                }
    
    
@app.post("/uploadfile/")
async def create_profile(*, first_name:Annotated[str, Form()],
                         last_name:Annotated[str, Form()], 
                         Id_card: UploadFile | None = None, passport_page:UploadFile):
    if not Id_card and  passport_page:
        return {"message":"Upload Successful",
            "data":[
                    {"passport_page":{"filename": passport_page.filename,
                    "size":f"{passport_page.size/1000} KB",
                    "type":passport_page.content_type}}]
            }
    elif Id_card and passport_page:   
        return {"message":"Upload Successful",
                "data":[{"Id_card":{"filename": Id_card.filename,
                        "size":f"{Id_card.size/1000} KB",
                        "type":Id_card.content_type}},
                        
                        {"passport_page":{"filename": passport_page.filename,
                        "size":f"{passport_page.size/1000} KB",
                        "type":passport_page.content_type}}]
                }      
        
class UploadFiles(BaseModel):
    Id_card:Annotated[UploadFile, File()]
    passport:Annotated[UploadFile, File()]
    cert:Annotated[UploadFile, File()]
    trans:Annotated[UploadFile, File()]
    
       
@app.post("/uploadfiles/")
async def create_profile(docs:Annotated[UploadFiles, File()]):
    return "Upload Successful"



