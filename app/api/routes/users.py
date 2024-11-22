from fastapi import APIRouter, Body, Header, Query, status, Form
from typing import Annotated, Optional, Union
from app.schemas.user import AccountDetails, HeaderParams, User, UserLogin, UserParams, UserUpdate
from app.db.data import users
from app.crud.user import user_crud

user_router =  APIRouter()


@user_router.post("/signup", response_model_exclude=["bank_name"], status_code=status.HTTP_201_CREATED)
def signup(user:User, confirm_password:Annotated[str, Body()], is_active:Annotated[bool, Body()], header_params:Annotated[HeaderParams, Header()]):
    new_user = user_crud.create_users(user, confirm_password)
    return {"message":"Account Created Successfully", "data":new_user}


@user_router.post("/Login")
async def login(user:Annotated[UserLogin, Form()]):
   response = user_crud.login(user)
   return response


<<<<<<< HEAD
@user_router.get("/users")
=======
@user_router.get("/users",  status_code=status.HTTP_200_OK)
>>>>>>> 40ee1b3030d940c28f6f7b92c1e102e1239c7997
def get_users(user_params: Annotated[UserParams, Query()]):
    users_data = user_crud.get_users(user_params)
    return users_data


<<<<<<< HEAD
@user_router.put("/users/{user_Id}")
=======
@user_router.put("/users/{user_Id}", status_code=status.HTTP_201_CREATED)
>>>>>>> 40ee1b3030d940c28f6f7b92c1e102e1239c7997
def update_profile(user_Id:str, update_profile:UserUpdate):
    updated_profile = user_crud.update_profile(user_Id, update_profile)
    
    return updated_profile
    
    
<<<<<<< HEAD
@user_router.delete("/users/{user_Id}")
=======
@user_router.delete("/users/{user_Id}", status_code=status.HTTP_204_NO_CONTENT)
>>>>>>> 40ee1b3030d940c28f6f7b92c1e102e1239c7997
def delete_profile(user_Id:str):
    profile_deleted = user_crud.delete_profile(user_Id)
    
    return profile_deleted

