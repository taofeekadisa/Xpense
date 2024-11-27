from fastapi import APIRouter, Body, HTTPException, Header, Query, status, Form
from typing import Annotated, Optional, Union
from app.schemas.user import AccountDetails, BaseUser, Login, UserParams, UserUpdate
#from app.crud.user import user_crud
from app.db.database import *
from app.db.models.user import *

user_router =  APIRouter()

#Public Endpoint
@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user:BaseUser, confirm_password:Annotated[str, Body()], session: SessionDep):
    statement = select(Users).where(Users.email == user.email)
    user_profile = session.exec(statement).first()
    
    if user_profile:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist")
    
    #if not user_profile: 
    new_user = Users(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        country = user.country,
        city = user.city,
        phone_number = user.phone_number,
        password = user.password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"message":"Account Created Successfully", "success":True}

@user_router.post("/Login", status_code=status.HTTP_200_OK)
async def login(form_data:Annotated[Login, Form()]):
   return {"message":"Login Successful", "success":True}


# Internal Endpoint
@user_router.get("/users",  status_code=status.HTTP_200_OK)
def get_users(user_params: Annotated[UserParams, Query()]):
    pass



@user_router.put("/users/{user_Id}", status_code=status.HTTP_201_CREATED)
def update_profile(user_Id:str, update_profile:UserUpdate):
    pass
    
    


@user_router.delete("/users/{user_Id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(user_Id:str):
    pass

