from fastapi import Cookie, Depends, FastAPI, Body, Form, HTTPException, Header, Query, status
from datetime import date
from fastapi.security import OAuth2PasswordBearer
from data import users, expenses
from pydantic import BaseModel, Field
from typing import Annotated, Optional, Union


app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username:str
    email:str
    password:str
    
class UserLogin(BaseModel):
    username_email:str
    password:str
  
class UserUpdate(BaseModel):
    username:str
    email:str
  
class UserParams(BaseModel):
    model_config = {"extra": "forbid"}
    
    job: Optional[str] = None
    age: Annotated[str | float, Field(gt=0, lt=70, description="Age of users", title="Age of users")] = None
    city: Optional[str] = None
    salary: Optional[float] = None
    experience:Optional[int] = None
    department: Optional[str] = None
    gender: Optional[str] = None
            
@app.post("/v1/signup")
def signup(user:User, confirm_password:Annotated[str, Body()]):
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
    filtered_users = users
    
    if user_params.job is not None:
        filtered_users = [user for user in filtered_users if user["job"] == user_params.job ]
        
        return filtered_users
    return users
        
    
    
    # if query.age is not None:
    #     filtered_users = [user for user in filtered_users if user["age"] == query.age]


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


    
    
 
        
        
        



