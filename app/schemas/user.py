from pydantic import BaseModel, Field, EmailStr, validate_email
from typing import Annotated, Optional, Union
from uuid import UUID
from datetime import datetime, date, time
from app.utils.current_time import current_time



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
    created_at:current_time
    
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