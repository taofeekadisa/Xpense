from pydantic import BaseModel, Field, EmailStr, validate_email
from typing import Annotated, Optional, Union
from uuid import UUID
from datetime import datetime, date, time
from app.utils.current_time import current_time



class BaseUser(BaseModel):
    first_name: str
    last_name:str
    email: str
    country: str
    city:Optional[str]
    phone_number:Optional[str]
    password: str

class Login(BaseModel):
    email:str
    password:str

class UserParams(BaseModel):
    model_config = {"extra": "forbid"}
    
    city: Optional[str] = None
    country: Optional[str] = None

    
class AccountDetails(BaseModel):
    account_name: str
    account_number: Annotated[int, Field(ge=10)]
    bank_name: str
    account_type: str
  
  
class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name:Optional[str]
    country: Optional[str]
    city:Optional[str]
    phone_number:Optional[str]
    
  

