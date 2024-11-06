from fastapi import Cookie, Depends, FastAPI, Body, Form, HTTPException, Header, Query, status
from datetime import date
from fastapi.security import OAuth2PasswordBearer
from data import users, expenses
from pydantic import BaseModel, Field, EmailStr, validate_email
from typing import Annotated, Optional, Union


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
 
class User(BaseModel):
    username: str
    email: str
    address: Address
    account_details: list[AccountDetails]
    password: str

    
class UserLogin(BaseModel):
    username_email:EmailStr
    password:str
  
class UserUpdate(BaseModel):
    username:str
    email:str
  
class UserParams(BaseModel):
    model_config = {"extra": "forbid"}
    
    job: Optional[str] = None
    age: Annotated[str | float, Field(description="Age of users", title="Age of users")] = None
    city: Optional[str] = None
    salary: Optional[float] = None
    experience:Optional[int] = None
    department: Optional[str] = None
    gender: Optional[str] = None
            
@app.post("/v1/signup")
def signup(user:User, confirm_password:Annotated[str, Body()], is_active:Annotated[bool, Body()]):
    for Id, user_data in users.items():
        if Id == user.username:
            return "Username already exit"
        for k, v in user_data.items():
            if user_data["email"] == user.email:
                return "Email already exist"
        if user.password != confirm_password:
            return "Passwords do not match"
    users[user.username] = user.model_dump()
    return "Sign Up Successful"


@app.post("/v1/Login")
def login(user: UserLogin):
    for Id, user_data in users.items():
        if user_data["password"] == user.password and (
            user.username_email == user_data["username"]
            or user.username_email == user_data["email"]
        ):
            return "Login Successful"
    return "Invalid login credentials" 


@app.get("/v1/users")
def get_users(user_params:Annotated[UserParams, Query()]):
    # filtered_users = {Id:user_profile for Id, user_profile in users.items() if user_profile["job"] == user_params.job}
    # return filtered_users
    filtered_users = {}
    for Id, value in user_params.model_dump().items():
        if user_params.job is not None:
            for Id, user_profile in users.items():
                if user_profile["job"] == user_params.job:
                    filtered_users[Id] = user_profile  
                    return filtered_users

        if user_params.age is not None:
            for Id, user_profile in users.items():
                if user_profile["age"] == user_params.age:
                    filtered_users[Id] = user_profile  
                    return filtered_users
    return users
        

# @app.get("/v1/users")
# def get_users(user_params: Annotated[UserParams, Query()]):
#     filtered_users = {}

#     for Id, user_profile in users.items():
#         if user_params.job is not None and user_profile["job"] != user_params.job:
#             continue
#         if user_params.age is not None and user_profile["age"] != user_params.age:
#             continue
#         filtered_users[Id] = user_profile

#     return filtered_users if filtered_users else users 



@app.put("/v1/users/{user_Id}")
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


    
    
 
        
        
        



