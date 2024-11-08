from uuid import UUID
from fastapi import Cookie, Depends, FastAPI, Body, Form, HTTPException, Header, Query, status
from datetime import date
from fastapi.security import OAuth2PasswordBearer
from data import users, expenses
from pydantic import BaseModel, Field, EmailStr, validate_email
from typing import Annotated, Optional, Union
from datetime import datetime, date, time



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
    username_email:str
    password:str
  
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

def user_auth(user: UserLogin):
    for Id, user_data in users.items():
        if user_data["password"] == user.password and (
            user.username_email == user_data["username"]
        ):
            pass
    return "Unauthorised Access" 
            
@app.post("/v1/signup", response_model=AccountDetails, response_model_exclude=["bank_name"])
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


@app.post("/v1/Login")
async def login(user: UserLogin) -> UserLogin:
    for Id, user_data in users.items():
        if user_data["password"] == user.password and (
            user.username_email == user_data["username"]
            or user.username_email == user_data["email"]
        ):
            return user
    return "Invalid login credentials" 

@app.get("/v1/users")
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


@app.delete("/v1/users/{user_Id}")
def delete_profile(user_Id:str):
    for Id, user_data in users.items():
        if Id == user_Id:
            del users[Id]
            return "Account deleted"
    return "Unauthorised Access"
 
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

#Example on Response Model stops here   
    
 
        
        
        



