from fastapi import APIRouter, Body, Header, Query, status, Form
from typing import Annotated, Optional, Union
from app.schemas.user import AccountDetails, HeaderParams, User, UserLogin, UserParams, UserUpdate
from app.db.data import users
from app.crud.user import user_crud

user_router =  APIRouter()


@user_router.post("/v1/signup", response_model_exclude=["bank_name"], status_code=status.HTTP_201_CREATED, tags=["Users"])
def signup(user:User, confirm_password:Annotated[str, Body()], is_active:Annotated[bool, Body()], header_params:Annotated[HeaderParams, Header()]):
    new_user = user_crud.create_users(user, confirm_password)
    return {"message":"Account Created Successfully", "data":new_user}


@user_router.post("/v1/Login",  tags=["Users"])
async def login(user:Annotated[UserLogin, Form()]):
   response = user_crud.login(user)
   return response


@user_router.get("/v1/users",  tags=["Users"])
def get_users(user_params: Annotated[UserParams, Query()]):
    users_data = user_crud.get_users(user_params)
    return users_data


@user_router.put("/v1/users/{user_Id}",  tags=["Users"])
def update_profile(user_Id:str, update_profile:UserUpdate):
    updated_profile = user_crud.update_profile(user_Id, update_profile)
    
    return updated_profile
    
    
@user_router.delete("/v1/users/{user_Id}",  tags=["Users"])
def delete_profile(user_Id:str):
    profile_deleted = user_crud.delete_profile(user_Id)
    
    return profile_deleted

