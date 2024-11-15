from fastapi import APIRouter, Body, Header, Query, status, Form
from typing import Annotated, Optional, Union
from app.schemas.user import AccountDetails, HeaderParams, User, UserLogin, UserParams, UserUpdate
from app.db.data import users
from app.crud.user import user_crud

user_router =  APIRouter()




@user_router.post("/v1/signup", response_model=AccountDetails, response_model_exclude=["bank_name"], status_code=status.HTTP_201_CREATED, tags=["Users"])
def signup(user:User, confirm_password:Annotated[str, Body()], is_active:Annotated[bool, Body()], header_params:Annotated[HeaderParams, Header()]) -> any:
    new_user = user_crud.create_users(user, confirm_password)
    return {"message":"Sign Successful", "data":new_user}



# @app.post("/v1/signup")
# def signup(user:User, confirm_password:Annotated[str, Body()], is_active:Annotated[bool, Body()]):
#     for Id, user_data in users.items():
#         if Id == user.username:
#             return "Username already exit"
#         for k, v in user_data.items():
#             if user_data["email"] == user.email:
#                 return "Email already exist"
#         if user.password != confirm_password:
#             return "Passwords do not match"
#     users[user.username] = user.model_dump()
#     return "Sign Up Successful" 


@user_router.post("/v1/Login",  tags=["Users"])
async def login(user:Annotated[UserLogin, Form()]):
    for Id, user_data in users.items():
        if user_data["password"] == user.password and (
            user.username == user_data["username"]
            or user.username == user_data["email"]
        ):
            return "Login Successful"
    return "Invalid login credentials" 


@user_router.get("/v1/users",  tags=["Users"])
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


@user_router.put("/v1/users/{user_Id}",  tags=["Users"])
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
    
    
@user_router.delete("/v1/users/{user_Id}",  tags=["Users"])
def delete_profile(user_Id:str):
    for Id, user_data in users.items():
        if Id == user_Id:
            del users[Id]
            return "Account deleted"
    return "Unauthorised Access"