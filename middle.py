from typing import Annotated
from fastapi import Body, FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import time

app = FastAPI()

user_db = {"Alee":{"username":"Alee", "name":"John", "email":"ta@ta.com","password":"mypass", "age":27}}

class User(BaseModel):
    username:str
    name:str
    email:EmailStr
    password:str
    age:int

#Logger Middleware    

@app.middleware("http")
async def request_logger(request:Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    response.headers["X-Process-Time"] = str(duration)
    log_info = {"Duration":duration, "Request":request.method, "Status":response.status_code}
    print(log_info)
    
    return response

origins = [
    "http://localhost:8000"
]

methods = ["POST"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/signup",status_code=status.HTTP_201_CREATED)
async def sign_up(user:Annotated[User, Body()]):
    for Id, user_profile in user_db.items():
        if Id == user.username and user_profile["email"] == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email and username already exist")
    
    user_db[user.username] = user.model_dump()
    
    return "Profile Created Succesfully"
 
   
@app.get("/user",status_code=status.HTTP_200_OK)
async def get_users():
    return user_db