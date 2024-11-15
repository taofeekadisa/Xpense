from typing import Annotated
from fastapi import Body
from app.db.data import users
from app.schemas.user import AccountDetails, HeaderParams, User, UserLogin, UserParams, UserUpdate

class UserCrud():
    #Signup endpoint
    @staticmethod
    def create_users(user:User, confirm_password:Annotated[str, Body()]):
        for Id, user_data in users.items():
            if Id == user.username:
                return "Username already exit"
        for k, v in user_data.items():
            if user_data["email"] == user.email:
                return "Email already exist"
        if user.password != confirm_password:
            return "Passwords do not match"
        users[user.username] = user.model_dump()
        #new_user = User(**user.model_dump())
        
        return user.model_dump()
    
    #Login endpoint
    @staticmethod
    def login():
        pass
    
user_crud = UserCrud()