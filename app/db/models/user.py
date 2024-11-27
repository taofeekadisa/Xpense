from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str 
    last_name: str
    email: str
    country: str
    city: str = Field(default=None)
    phone_number: str = Field(default=None)
    password:str
   
    
