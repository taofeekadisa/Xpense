from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Sample data
users = [
    {"username": "Alee", "age": 28, "city": "Lagos", "salary": 70000},
    {"username": "Desayo", "age": 32, "city": "Abuja", "salary": 60000},
    {"username": "Chidi", "age": 29, "city": "Onitsha", "salary": 45000},
    {"username": "Tokun", "age": 26, "city": "Ibadan", "salary": 75000},
    {"username": "Daniel", "age": 30, "city": "Lagos", "salary": 62000}
]

# Pydantic model to represent query parameters
class UserQuery(BaseModel):
    age: Optional[int] = None
    city: Optional[str] = None
    salary: Optional[int] = None

@app.get("/users/", response_model=List[dict])
async def get_users(query: UserQuery = Depends()):
    # Start with the full list and filter based on query parameters
    filtered_users = users
    
    if query.age is not None:
        filtered_users = [user for user in filtered_users if user["age"] == query.age]
    if query.city is not None:
        filtered_users = [user for user in filtered_users if user["city"] == query.city]
    if query.salary is not None:
        filtered_users = [user for user in filtered_users if user["salary"] == query.salary]
    
    return filtered_users
