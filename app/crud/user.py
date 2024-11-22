from typing import Annotated
from fastapi import Body, status, HTTPException
from app.db.data import users
from app.schemas.user import AccountDetails, HeaderParams, User, UserLogin, UserParams, UserUpdate

class UserCrud():
    #Signup endpoint
    @staticmethod
    def create_users(user:User, confirm_password:str):
        for Id, user_data in users.items():
            if Id == user.username:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or password already exist")
        for k, v in user_data.items():
            if user_data["email"] == user.email:
                HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or password already exist")
        if user.password != confirm_password:
            return "Passwords do not match"
        users[user.username] = user.model_dump()
        new_user = AccountDetails(**user.model_dump())
        
        return new_user
    
    #Login endpoint
    @staticmethod
    def login(user:UserLogin):
        for Id, user_data in users.items():
            if user_data["password"] == user.password and (
            user.username == user_data["username"]
            or user.username == user_data["email"]
        ):
                return {"data":"Login Successful"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username or password not found") 
    
    #Get users endpoint
    @staticmethod
    def get_users(user_params:UserParams):
        filtered_users = {}
        #match = True
        for user_id, user_profile in users.items():
            match = True
            for field in user_params.model_fields_set:
                param_value = getattr(user_params, field)
                print(param_value)
                if param_value is not None and user_profile.get(field) != param_value:
                    match = False
                    break
            if match:
                filtered_users[user_id] = user_profile
                
        if not filtered_users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No match found")
              
        return filtered_users 
    
    @staticmethod
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
<<<<<<< HEAD
                return "Update Successful"
=======
                return {"message":"Account Updated Successfully", "success":True}
>>>>>>> 40ee1b3030d940c28f6f7b92c1e102e1239c7997
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No match found")
    
    @staticmethod
    def delete_profile(user_Id:str):
        assert type(user_Id) == str , "user_id must be a string"
        for Id, user_data in users.items():
            if Id == user_Id:
                del users[Id]
                return "Account deleted"
            return "Unauthorised Access"

user_crud = UserCrud()